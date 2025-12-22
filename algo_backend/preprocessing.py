##########################################################################
### Module to tranform GTFS data into usable custom objects for RAPTOR ###
##########################################################################

import csv 
from .data_structure import Stop, Route, Trip, map_index
from typing import List, Dict
import os.path
from collections import defaultdict

def group_stop_times_by_trip(file_path):
    # Dictionnaire pour stocker temporairement les données par trajet
    # structure : { trip_id: [ {données_arrêt_1}, {données_arrêt_2} ] }
    trips_builder = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_id = row['trip_id']
            trips_builder[trip_id].append({
                'stop_id': row['stop_id'],
                'sequence': int(row['stop_sequence']),
                'arr': row['arrival_time'],
                'dep': row['departure_time'],
                'pickup': int(row.get('pickup_type', 0)),
                'dropoff': int(row.get('drop_off_type', 0))
            })
        
    for trip_id in trips_builder:
        trips_builder[trip_id].sort(key=lambda x: x['sequence'])
    
    return trips_builder

def hms_to_minutes(hms_str: str) -> float:
    """
    Converts GTFS HH:MM:SS to minutes from midnight.
    Example: "08:30:00" -> 510.0
    """
    h, m, s = hms_str.split(':')
    return int(h) * 60 + int(m) + int(s) / 60


def load_gtfs_data(gtfs_dir):
    """Function to tranform GTFS data into lists of custom objects"""

    # Building stop list and mapping 
    stop_dict = {}
    parent_dict = {}

    with open(f'{gtfs_dir}/stops.txt', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:

            if row['location_type'] == '1': # If it is a station, create a stop point
                name = row['stop_name']
                lat = row['stop_lat']
                lon = row['stop_lon']
                id = row['stop_id']

                stop_dict[id] = Stop(name,id,lat,lon)

            else : # If it is just a platform, map it to its parent station
                parent_dict[row['stop_id']] = row['parent_station']

    stop_list = [stop for stop in stop_dict.values()]
    map_index(stop_list)

    # Build all trips and routes
    trips_builder = group_stop_times_by_trip(f'{gtfs_dir}/stop_times.txt')
    route_dict = {}

    with open(f'{gtfs_dir}/trips.txt', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:

            route_id = row['route_id']
            trip_id = row['trip_id']

            stop_id_list = []
            stop_index_list = []
            dep_times = []
            arr_times = []

            for seq in trips_builder[trip_id]:

                stop_id = seq['stop_id']

                if stop_id in parent_dict:
                    stop_id = parent_dict[stop_id]

                stop_id_list.append(stop_id)

                if seq['pickup'] == 0:
                    time = hms_to_minutes(seq['dep'])
                    dep_times.append(time)
                else:
                    dep_times.append(0)

                if seq['dropoff'] == 1:
                    arr_times.append(float('inf'))
                else:
                    time = hms_to_minutes(seq['arr'])
                    arr_times.append(time)
            
            for stop_id in stop_id_list:

                stop_index = stop_dict[stop_id].index_in_list
                stop_index_list.append(stop_index)
            
            route_signature = tuple(stop_id_list) # A route is ultimately defined by a specific sequence of stops
            trip = Trip(trip_id,arr_times,dep_times)

            if route_signature not in route_dict:
                route = Route(route_id, stop_id_list,stop_index_list)
                route.add_trip(trip)
                route_dict[route_signature] = route

            else:
                route = route_dict[route_signature]
                route.add_trip(trip)

    route_list = []
    # Sort trips in a route by chronological order
    for route in route_dict.values():
        route.trips.sort(key=lambda x: x.departure_times[0])
        route_list.append(route)
    
    map_index(route_list)
            
    return stop_list, route_list
            

if __name__ == "__main__":
    gtfs_dir = os.path.dirname(__file__) + "/../gtfs_sncf"
    stop_list, route_list = load_gtfs_data(gtfs_dir)

    print(stop_list[0])
    print(route_list[0])