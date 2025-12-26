# Mock server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

from .raptor import RAPTOR, get_all_paths
from .postprocessing import rank_by_time, jsonify_paths
from .preprocessing import load_gtfs_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Serveur actif !"}


gtfs_dir = 'gtfs_sncf'

stop_list, route_list, stop_dict = load_gtfs_data(gtfs_dir)
stop_name_to_index_dict = { stop.name : stop.index_in_list for stop in stop_dict.values()}
stop_names = list(stop_name_to_index_dict.keys())

@app.get("/stations")
def get_stations():
    return {
        "status": "success",
        "stations": sorted(stop_names)
    }


@app.post("/search")
def recherche(data: dict, stop_list: list, route_list: list, stop_dict: dict, stop_name_to_index_dict: dict):
    print(f"Données reçues : {data}")

    source = data['depart']
    arrivee = data['arrivee']
    date = data['date']
    date = datetime.fromisoformat(date)
    heure = date.strftime('%H:%M:%S')
    date = date.strftime('%Y%m%d')
    source_index_in_list = stop_name_to_index_dict[source]
    target_index_in_list = stop_name_to_index_dict[target]
    source_stop = stop_list[source_index_in_list]
    target_stop = stop_list[target_index_in_list]

    tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

    paths = get_all_paths(parent,tau,2822,5)
    paths = rank_by_time(paths)

    results = {'trajets' : jsonify_paths(paths,stop_list)}
    
    # transformed_results = {
    #     "trajets": [
    #         {
    #             "departure_stop": itin['departure_stop'],
    #             "arrival_stop": itin['arrival_stop'],
    #             "segments": [
    #                 {
    #                     "from": seg['from'],
    #                     "to": seg['to'],
    #                     "dep_coor": seg['dep_coor'],
    #                     "arr_coor": seg['arr_coor'],
    #                     "board_time": seg['board_time'] // 60,  # Convert to minutes
    #                     "arrival_time": seg['arrival_time'] // 60,  # Convert to minutes
    #                     "trip": seg['trip'],
    #                     "route": seg['route']
    #                 }
    #                 for seg in itin['segments']
    #                 if seg['trip'] != 'WALK'  # Filter out WALK segments
    #             ]
    #         }
    #         for itin in valid_itineraries
    #     ]
    # }
    
    print(f"Données envoyées : {results}")
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
