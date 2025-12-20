import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
import pickle
import os
import re
import json
from datetime import datetime

# --- UTILITAIRES DE PARSING ---

def extract_uic7(stop_id):
    """Extrait les 7 chiffres UIC. Gère les formats avec espaces et tirets."""
    digits = re.findall(r'\d+', str(stop_id))
    if digits:
        full = "".join(digits)
        return full[:7]
    return None

def get_train_num(trip_id):
    """Extrait le numéro de train (2 à 6 chiffres)."""
    match = re.search(r'(\d{2,6})', str(trip_id))
    return match.group(1) if match else "0000"

def time_to_seconds(time_str):
    if pd.isna(time_str): return 0
    try:
        parts = time_str.split(':')
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except: return 0

class RaptorEngine:
    def __init__(self, gtfs_path, force_rebuild=False):
        self.path = gtfs_path
        self.cache_file = "raptor_expert_final_multimodal.pkl"
        
        if os.path.exists(self.cache_file) and not force_rebuild:
            print(">>> Chargement de l'index expert (SNCF Voyageurs + TER) depuis le cache...")
            self.load_cache()
        else:
            self.build_index()

    def build_index(self):
        print(f"--- Indexation Experte (Dossier: {self.path}) ---")
        
        # 1. Chargement GTFS
        print("1/5 Chargement des fichiers GTFS...")
        stops = pd.read_csv(os.path.join(self.path, "stops.txt"), dtype={'stop_id': str, 'parent_station': str})
        trips = pd.read_csv(os.path.join(self.path, "trips.txt"), dtype={'trip_id': str, 'route_id': str, 'service_id': str})
        stop_times = pd.read_csv(os.path.join(self.path, "stop_times.txt"), dtype={'stop_id': str, 'trip_id': str})
        routes = pd.read_csv(os.path.join(self.path, "routes.txt"), dtype={'route_id': str})
        
        self.route_names = dict(zip(routes.route_id, routes.route_long_name))
        
        # --- AJOUT : Extraction des coordonnées GPS ---
        self.stop_coords = {row.stop_id: [row.stop_lat, row.stop_lon] for row in stops.itertuples()}

        # 2. Calendrier & Exceptions
        self.service_calendar = {}
        if os.path.exists(os.path.join(self.path, "calendar.txt")):
            cal_df = pd.read_csv(os.path.join(self.path, "calendar.txt"), dtype={'service_id': str, 'start_date': str, 'end_date': str})
            self.service_calendar = cal_df.set_index('service_id').to_dict('index')
        
        self.service_exceptions = defaultdict(dict)
        if os.path.exists(os.path.join(self.path, "calendar_dates.txt")):
            dates_df = pd.read_csv(os.path.join(self.path, "calendar_dates.txt"), dtype={'service_id': str, 'date': str})
            for _, row in dates_df.iterrows():
                self.service_exceptions[row['service_id']][row['date']] = int(row['exception_type'])

        # 3. UNIFICATION DES MODES ET TRANSFERTS OFFICIELS
        print("3/5 Unification des StopPoints (TGV/OUIGO/TER) et lecture des délais...")
        self.transfers = defaultdict(list)
        self.intra_station_min_delay = {}
        self.train_to_train_rules = {}

        # A. Unification des enfants d'une même StopArea
        area_to_stops = defaultdict(list)
        self.stop_to_parent = {}
        for _, row in stops.iterrows():
            if pd.notna(row['parent_station']):
                area_to_stops[row['parent_station']].append(row['stop_id'])
                self.stop_to_parent[row['stop_id']] = row['parent_station']
        
        for children in area_to_stops.values():
            for s1 in children:
                for s2 in children:
                    if s1 != s2:
                        self.transfers[s1].append((s2, 0))

        # B. Export_CONNECTION_TIMES.csv
        conn_path = os.path.join(self.path, 'Export_CONNECTION_TIMES.csv')
        uic7_to_gtfs = defaultdict(list)
        for sid in stops['stop_id'].unique():
            uic = extract_uic7(sid)
            if uic: uic7_to_gtfs[uic].append(sid)

        if os.path.exists(conn_path):
            conn_df = pd.read_csv(conn_path, sep=';')
            for _, row in conn_df.iterrows():
                if row['MIN_DELAY'] == -1: continue
                u_arr, u_dep = str(int(row['ARRIVAL_STATION_UIC']))[:7], str(int(row['DEPARTURE_STATION_UIC']))[:7]
                delay = int(row['MIN_DELAY']) * 60
                
                if row['TYPE'] == 'INTRA_STATION':
                    self.intra_station_min_delay[u_arr] = delay
                else:
                    for s_arr in uic7_to_gtfs.get(u_arr, []):
                        for s_dep in uic7_to_gtfs.get(u_dep, []):
                            self.transfers[s_arr].append((s_dep, delay))

        # C. Export_TRAIN_CONNECTION_TIMES.csv
        t_conn_path = os.path.join(self.path, 'Export_TRAIN_CONNECTION_TIMES.csv')
        if os.path.exists(t_conn_path):
            t_df = pd.read_csv(t_conn_path, sep=';')
            for _, row in t_df.iterrows():
                uic = str(int(row['ARRIVAL_STATION_UIC']))[:7]
                self.train_to_train_rules[(uic, str(row['ARRIVAL_TRAIN']).strip(), str(row['DEPARTURE_TRAIN']).strip())] = int(row['MIN_DELAY']) * 60

        # 4. ROUTES RAPTOR
        print("4/5 Indexation des routes...")
        stop_times['arr_sec'] = stop_times['arrival_time'].map(time_to_seconds)
        stop_times['dep_sec'] = stop_times['departure_time'].map(time_to_seconds)
        merged = stop_times.merge(trips[['trip_id', 'service_id', 'route_id']], on='trip_id')
        
        self.routes, self.route_trips, self.stop_to_routes = {}, defaultdict(list), defaultdict(set)
        stop_seq_to_route_id, route_counter = {}, 0

        for trip_id, group in tqdm(merged.sort_values(['trip_id', 'stop_sequence']).groupby('trip_id'), desc="Groupement"):
            seq = tuple(group['stop_id'].tolist())
            if seq not in stop_seq_to_route_id:
                stop_seq_to_route_id[seq] = route_counter
                self.routes[route_counter] = list(seq)
                route_counter += 1
            rid = stop_seq_to_route_id[seq]
            self.route_trips[rid].append({
                'id': trip_id, 'train_no': get_train_num(trip_id), 'route_id': group['route_id'].iloc[0],
                'service_id': group['service_id'].iloc[0], 'departures': group['dep_sec'].values, 'arrivals': group['arr_sec'].values
            })
            for sid in seq: self.stop_to_routes[sid].add(rid)

        for rid in self.route_trips: self.route_trips[rid].sort(key=lambda x: x['departures'][0])
        self.stop_names = dict(zip(stops.stop_id, stops.stop_name))
        self.save_cache()

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump((self.routes, self.route_trips, self.stop_to_routes, self.stop_names, 
                         self.service_calendar, self.service_exceptions, self.transfers,
                         self.intra_station_min_delay, self.train_to_train_rules, self.route_names, self.stop_to_parent, self.stop_coords), f)

    def load_cache(self):
        with open(self.cache_file, 'rb') as f:
            (self.routes, self.route_trips, self.stop_to_routes, self.stop_names, 
             self.service_calendar, self.service_exceptions, self.transfers,
             self.intra_station_min_delay, self.train_to_train_rules, self.route_names, self.stop_to_parent, self.stop_coords) = pickle.load(f)

    def is_service_active(self, service_id, date_str):
        if service_id in self.service_exceptions:
            if date_str in self.service_exceptions[service_id]: return self.service_exceptions[service_id][date_str] == 1
        if service_id in self.service_calendar:
            cal = self.service_calendar[service_id]
            if not (int(cal['start_date']) <= int(date_str) <= int(cal['end_date'])): return False
            day_name = datetime.strptime(date_str, "%Y%m%d").strftime('%A').lower()
            return cal.get(day_name, 0) == 1
        return False

    def solve(self, source_id, date_str, start_time_str, max_k=4):
        start_time = time_to_seconds(start_time_str)
        tau = {k: defaultdict(lambda: (float('inf'), None)) for k in range(max_k + 1)}
        tau[0][source_id] = (start_time, None)
        
        for target, dur in self.transfers[source_id]:
            tau[0][target] = (start_time + dur, ('walk', source_id))
            
        marked_stops = {source_id} | {t for t, d in self.transfers[source_id]}
        journey_ptr = {}

        for k in range(1, max_k + 1):
            print(f"Calcul Round {k}...")
            tau[k] = tau[k-1].copy()
            routes_to_scan = defaultdict(lambda: float('inf'))
            for stop in marked_stops:
                for rid in self.stop_to_routes[stop]:
                    routes_to_scan[rid] = min(routes_to_scan[rid], self.routes[rid].index(stop))
            
            marked_stops = set()
            for rid, start_idx in routes_to_scan.items():
                current_trip, board_stop = None, None
                route_stops = self.routes[rid]
                for i in range(start_idx, len(route_stops)):
                    stop_id = route_stops[i]
                    if current_trip is not None:
                        arr = current_trip['arrivals'][i]
                        if arr < tau[k][stop_id][0]:
                            tau[k][stop_id] = (arr, current_trip)
                            b_idx = list(route_stops).index(board_stop)
                            journey_ptr[(k, stop_id)] = ('trip', current_trip['id'], board_stop, current_trip['departures'][b_idx], current_trip['route_id'])
                            marked_stops.add(stop_id)
                    
                    p_time, p_trip = tau[k-1][stop_id]
                    if p_time < float('inf'):
                        uic = extract_uic7(stop_id)
                        delay = self.intra_station_min_delay.get(uic, 300)
                        for trip in self.route_trips[rid]:
                            final_delay = delay
                            if p_trip and not isinstance(p_trip, tuple) and not isinstance(p_trip, str):
                                rule = self.train_to_train_rules.get((uic, p_trip['train_no'], trip['train_no']))
                                if rule: final_delay = rule
                            if final_delay == -1: continue
                            if trip['departures'][i] >= p_time + final_delay:
                                if self.is_service_active(trip['service_id'], date_str):
                                    if current_trip is None or trip['arrivals'][-1] < current_trip['arrivals'][-1]:
                                        current_trip, board_stop = trip, stop_id
                                    break
            
            new_marked = set()
            for stop in list(marked_stops):
                for target, dur in self.transfers[stop]:
                    if tau[k][stop][0] + dur < tau[k][target][0]:
                        tau[k][target] = (tau[k][stop][0] + dur, ('walk', stop))
                        journey_ptr[(k, target)] = ('walk', stop, dur, tau[k][target][0])
                        new_marked.add(target)
            marked_stops |= new_marked
            if not marked_stops: break
        return tau, journey_ptr

    # --- AJOUT : FONCTION POUR FORMAT JSON ---
    def get_json_results(self, tau, ptr, target_id, max_k):
        parent = self.stop_to_parent.get(target_id)
        valid_targets = [sid for sid, p in self.stop_to_parent.items() if p == parent] if parent else [target_id]
        
        results = []
        for k in range(1, max_k + 1):
            best_sid, best_time = None, float('inf')
            for sid in valid_targets:
                if tau[k][sid][0] < best_time:
                    best_time, best_sid = tau[k][sid][0], sid
            
            if best_sid and best_time < float('inf'):
                journey = {
                    "departure_stop": "", # Rempli après backtracking
                    "arrival_stop": self.stop_names.get(best_sid, best_sid),
                    "segments": []
                }
                
                curr = best_sid
                for r in range(k, 0, -1):
                    if (r, curr) not in ptr: break
                    info = ptr[(r, curr)]
                    
                    if info[0] == 'walk':
                        segment = {
                            "from": self.stop_names.get(info[1], info[1]),
                            "to": self.stop_names.get(curr, curr),
                            "dep_coor": self.stop_coords.get(info[1], [0, 0]),
                            "arr_coor": self.stop_coords.get(curr, [0, 0]),
                            "board_time": int(tau[r][info[1]][0]) if info[1] in tau[r] else 0,
                            "arrival_time": int(info[3]),
                            "trip": "WALK",
                            "route": "TRANSFER"
                        }
                        journey["segments"].append(segment)
                        curr = info[1]
                        
                        # Check si un train arrive à cet arrêt dans le même round
                        if (r, curr) in ptr and ptr[(r, curr)][0] == 'trip':
                            _, tid, b_stop, b_time, rid = ptr[(r, curr)]
                            segment_train = {
                                "from": self.stop_names.get(b_stop, b_stop),
                                "to": self.stop_names.get(curr, curr),
                                "dep_coor": self.stop_coords.get(b_stop, [0, 0]),
                                "arr_coor": self.stop_coords.get(curr, [0, 0]),
                                "board_time": int(b_time),
                                "arrival_time": int(tau[r][curr][0]),
                                "trip": tid,
                                "route": self.route_names.get(rid, "SNCF")
                            }
                            journey["segments"].append(segment_train)
                            curr = b_stop
                    else:
                        _, tid, b_stop, b_time, rid = info
                        segment = {
                            "from": self.stop_names.get(b_stop, b_stop),
                            "to": self.stop_names.get(curr, curr),
                            "dep_coor": self.stop_coords.get(b_stop, [0, 0]),
                            "arr_coor": self.stop_coords.get(curr, [0, 0]),
                            "board_time": int(b_time),
                            "arrival_time": int(tau[r][curr][0]),
                            "trip": tid,
                            "route": self.route_names.get(rid, "SNCF")
                        }
                        journey["segments"].append(segment)
                        curr = b_stop
                
                journey["segments"].reverse()
                if journey["segments"]:
                    journey["departure_stop"] = journey["segments"][0]["from"]
                results.append(journey)
                
        return results

    def print_all_options(self, tau, ptr, target_id, max_k):
        # On garde cette fonction pour le debug console
        parent = self.stop_to_parent.get(target_id)
        valid_targets = [sid for sid, p in self.stop_to_parent.items() if p == parent] if parent else [target_id]
        
        print(f"\n=== SOLUTIONS TROUVÉES POUR LA ZONE : {self.stop_names.get(target_id, target_id)} ===")
        for k in range(1, max_k + 1):
            best_sid, best_time = None, float('inf')
            for sid in valid_targets:
                if tau[k][sid][0] < best_time:
                    best_time, best_sid = tau[k][sid][0], sid
            
            if best_sid and best_time < float('inf'):
                print(f"\n[Option {k} - {k} étapes] Arrivée à {self.format_sec(best_time)}")
                curr, path = best_sid, []
                for r in range(k, 0, -1):
                    if (r, curr) not in ptr: break
                    info = ptr[(r, curr)]
                    if info[0] == 'walk':
                        path.append(f"  [Ville] Transfert/Unification : {self.stop_names[info[1]]} -> {self.stop_names[curr]} ({info[2]//60} min)")
                        curr = info[1]
                        if (r, curr) in ptr and ptr[(r, curr)][0] == 'trip':
                            _, tid, b_stop, b_time, rid = ptr[(r, curr)]
                            path.append(f"  [Train] {self.route_names.get(rid, 'SNCF'):18} | {self.stop_names[b_stop]} ({self.format_sec(b_time)}) -> {self.stop_names[curr]} ({self.format_sec(tau[r][curr][0])})")
                            curr = b_stop
                    else:
                        _, tid, b_stop, b_time, rid = info
                        path.append(f"  [Train] {self.route_names.get(rid, 'SNCF'):18} | {self.stop_names[b_stop]} ({self.format_sec(b_time)}) -> {self.stop_names[curr]} ({self.format_sec(tau[r][curr][0])})")
                        curr = b_stop
                for step in reversed(path): print(step)

    def format_sec(self, seconds):
        return f"{int(seconds//3600):02d}:{int((seconds%3600)//60):02d}"

if __name__ == "__main__":
    engine = RaptorEngine("gtfs_sncf", force_rebuild=True)
    DEPART = "StopPoint:OCETGV INOUI-87723197" 
    ARRIVEE = "StopPoint:OCETGV INOUI-87575001"
    DATE = "20251225"
    
    tau, ptr = engine.solve(DEPART, DATE, "08:00:00")
    
    # Génération et affichage du JSON
    json_results = engine.get_json_results(tau, ptr, ARRIVEE, 4)
    print("\n--- OUTPUT JSON ---")
    print(json.dumps(json_results, indent=2, ensure_ascii=False))