# Mock server

import os 
from datetime import datetime
from typing import Dict, TypedDict, List, Tuple, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse

from algo_backend.raptor import paths_in_time_range
from algo_backend.postprocessing import rank_by_time, jsonify_paths
from algo_backend.preprocessing import load_gtfs_data

#------Define API instance------#
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#------Get the data------#

# path to GTFS data files
gtfs_dir = 'gtfs_sncf'
stop_list, route_list, stop_dict = load_gtfs_data(gtfs_dir)

# dict with {"stop name in French" : stop index in total stop list}
stop_name_to_index_dict = {stop.name: stop.index_in_list for stop in stop_list}

stop_names = list(stop_name_to_index_dict.keys()) # list of the stop names


@app.get("/result.html")
async def redirect_result() -> FileResponse:
    """
    Serves the result HTML page directly to handle client-side navigation.

    This explicit route ensures consistent access to the results page, 
    particularly when running behind a reverse proxy (like Onyxia).

    Returns:
        FileResponse: The 'result.html' file object.
    """
    return FileResponse(os.path.join(frontend_path, "result.html"))

@app.get("/stations")
def get_stations() -> Dict[str, Any]:
    """
    Retrieves the list of all available train stations from the loaded GTFS data.

    Returns:
        dict: A JSON response containing:
            - status (str): The success status of the request.
            - stations (List[str]): An alphabetically sorted list of all station names.
    """
    return {
        "status": "success",
        "stations": sorted(stop_names)
    }

#------ Research ------#

Segment = TypedDict("Segment", {
    "from": str,
    "to": str,
    "dep_coor": Tuple[float, float], # (lat, lon)
    "arr_coor": Tuple[float, float],
    "board_time": float,
    "arrival_time": float,
    "trip": str,
    "route": str
})

class Trajet(TypedDict):
    departure_stop: str
    arrival_stop: str
    segments: List[Segment]

class ApiResponse(TypedDict):
    status: str
    message: str
    trajets: List[Trajet]

@app.post("/search")
def recherche(data: dict) -> ApiResponse:
    
    print(f"Données reçues : {data} \n")
    
    source = data['depart']
    target = data['arrivee']
    date = data['date']
    date = datetime.fromisoformat(date) # transform to datetime format
    departure_time = float(date.hour * 60 + date.minute + date.second / 60) # convert into minutes from 0:00
    

    source_index_in_list = stop_name_to_index_dict[source]
    target_index_in_list = stop_name_to_index_dict[target]

    source_stop = stop_list[source_index_in_list]
    target_stop = stop_list[target_index_in_list]
    print(source_stop.name)
    print(target_stop.name)
    
    max_round = 5

    # tau, tau_star, parent = RAPTOR(source_stop, target_stop, departure_time, stop_list, route_list, max_round)

    # paths = get_all_paths(parent, tau, target_index_in_list, max_round)

    paths = paths_in_time_range(departure_time,source_stop,target_stop,stop_list,route_list)
    print("############------------------PATHS : \n", paths)
    print('\n')
    paths = rank_by_time(paths)
    print("############------------------RANKED PATHS : \n", paths)
    print('\n')
    print("############__________________jsonify_paths(paths, stop_list) : ", jsonify_paths(paths, stop_list))
    results = {"status": "success",
               "message": "Données bien reçues et traitées !",
               'trajets': jsonify_paths(paths, stop_list)}

    print(f"Données envoyées : {results}")
    return results


# On définit le chemin vers le dossier frontend qui est au même niveau 
# que le dossier server-fastapi
# ".." signifie "remonter d'un dossier"
current_dir = os.path.dirname(__file__)
frontend_path = os.path.join(current_dir, "..", "frontend")

# On monte le dossier frontend à la racine
# L'option html=True servira l'index.html automatiquement
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server-fastapi.final_server:app", host="0.0.0.0", port=8000, reload=True)
