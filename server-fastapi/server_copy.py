# Mock server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import os 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from algo_backend.raptor import RAPTOR, paths_in_time_range
from algo_backend.postprocessing import rank_by_time, jsonify_paths
from algo_backend.preprocessing import load_gtfs_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise tout le monde (pratique pour le dev sur Onyxia)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# # On monte le dossier frontend pour qu'il soit accessible via l'URL /frontend
# app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# # On crée une route pour afficher l'index
# @app.get("/")
# async def read_index():
#     return FileResponse('frontend/index.html')


# @app.get("/")
# def home():
#     return {"message": "Serveur actif !"}


gtfs_dir = 'gtfs_sncf'

stop_list, route_list, stop_dict = load_gtfs_data(gtfs_dir)
stop_name_to_index_dict = {stop.name: stop.index_in_list for stop in stop_list}
stop_names = list(stop_name_to_index_dict.keys())


from fastapi.responses import RedirectResponse

@app.get("/result.html")
async def redirect_result():
    # Si on détecte qu'on est sur Onyxia, on redirige vers le proxy
    # Sinon (localhost), on laisse faire le static mount
    return FileResponse(os.path.join(frontend_path, "result.html"))



@app.get("/stations")
def get_stations():
    return {
        "status": "success",
        "stations": sorted(stop_names)
    }


@app.post("/search")
def recherche(data: dict):
    print(f"Données reçues : {data}")
    print("stop_list : ", stop_list[:10])
    for i, (cle, valeur) in enumerate(stop_dict.items()):
        if i < 10:
            print(f"{cle} : {valeur}")
        else:
            break # On arrête la boucle après 10 éléments
    source = data['depart']
    target = data['arrivee']
    date = data['date']
    date = datetime.fromisoformat(date)
    departure_time = float(date.hour * 60 + date.minute + date.second / 60)
    print("departure_time :", departure_time)

    source_index_in_list = stop_name_to_index_dict[source]
    target_index_in_list = stop_name_to_index_dict[target]
    print("source_index_in_list : ", source_index_in_list)
    print("target_index_in_list : ", target_index_in_list)

    source_stop = stop_list[source_index_in_list]
    target_stop = stop_list[target_index_in_list]
    print(source_stop.name)
    print(target_stop.name)
    print(stop_list[2932].name)
    print(stop_list[2822].name)
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
    uvicorn.run("server-fastapi.server_copy:app", host="0.0.0.0", port=8000, reload=True)
