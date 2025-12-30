# Mock server

import os 
from datetime import datetime
from typing import Dict, TypedDict, List, Tuple, Any
from pprint import pprint

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler

from algo_backend.raptor import paths_in_time_range
from algo_backend.postprocessing import rank_by_time, jsonify_paths
from algo_backend.preprocessing import load_gtfs_data
from algo_backend.sncf_data import download_and_extract_gtfs

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
url = "https://eu.ftp.opendatasoft.com/sncf/plandata/Export_OpenData_SNCF_GTFS_NewTripId.zip"

# Initialization of data variables
stop_list = []
route_list = []
stop_dict = {}
stop_name_to_index_dict = {}
stop_names = []

# update the data 
def update_and_load_data():
    """
    Download and reload GTFS data
    """
    global stop_list, route_list, stop_dict, stop_name_to_index_dict, stop_names
    
    print(f"[{datetime.now()}] Démarrage de la mise à jour des données...")
    
    try:
        download_and_extract_gtfs(url)
        new_s_list, new_r_list, new_s_dict = load_gtfs_data(gtfs_dir)
        
        stop_list = new_s_list
        route_list = new_r_list
        stop_dict = new_s_dict
        stop_name_to_index_dict = {stop.name: stop.index_in_list for stop in stop_list}
        stop_names = list(stop_name_to_index_dict.keys())
        
        print(f"[{datetime.now()}] mise à jour terminée")
        
    except Exception as e:
        print(f"erreur : {e}")

# --- chargement au démarrage de l'app ---
@app.on_event("startup")
def startup_event():
    update_and_load_data()
    
    # mise à jour planifiée
    scheduler = BackgroundScheduler()
    # mise à jour tous les jours à 4h
    scheduler.add_job(update_and_load_data, 'cron', hour=4, minute=0)
    scheduler.start()
    print("planificateur démarré")


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

# Define Object Types to be able to check them 
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
    """Apply the RAPTOR algorithm to find the best paths between
    the departure point and the arrival point selected by the user
    on the webpage.

    Args:
        data (dict): payload from the index.html page,
                    eg. {'depart': Paris Gare de Lyon, 
                         'arrivee': 'Lyon Part Dieu', 
                         'date': '2025:27:12'}.

    Returns:
        ApiResponse: Object from the ApiResponse class defined above.
    """
    print(f"Données reçues : {data} \n")
    
    source = data['depart']
    target = data['arrivee']
    date = data['date']
    date = datetime.fromisoformat(date) # transform to datetime format
    departure_time = float(date.hour * 60 + date.minute + date.second / 60) # convert into minutes from 0:00
    
    # Associate station name with its index in the list of stations
    source_index_in_list = stop_name_to_index_dict[source]
    target_index_in_list = stop_name_to_index_dict[target]
    # Get the Stop objects
    source_stop = stop_list[source_index_in_list]
    target_stop = stop_list[target_index_in_list]
    print(f"SOURCE STOP NAME : {source_stop.name}")
    print(f"TARGET STOP NAME : {target_stop.name}\n")
    
    # Run the RAPTOR algorithm
    paths = paths_in_time_range(departure_time,source_stop,target_stop,stop_list,route_list)
    # logs
    print("############------------------PATHS : \n")
    pprint(paths)
    print('\n')
    
    paths = rank_by_time(paths)
    # logs
    print("############------------------RANKED PATHS : \n")
    pprint(paths)
    print('\n')
    
    # format the results
    jsonified_paths = jsonify_paths(paths, stop_list)
    results = {"status": "success",
               "message": "Données bien reçues et traitées !",
               'trajets': jsonified_paths}
    # logs
    print("############__________________JSONIFIED PATHS : \n")
    pprint(jsonified_paths)
    print('\n')
    print(f"Données envoyées : \n")
    pprint(results)
    
    return results


# We define the path to the frontend folder, which is at the same level
# as the server-fastapi folder
# “..” means “go up one directory”
current_dir = os.path.dirname(__file__)
frontend_path = os.path.join(current_dir, "..", "frontend")

# We mount the frontend folder at the root
# The html=True option will automatically serve index.html
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server-fastapi.final_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False)
