# Mock server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste des gares disponibles
GARES = [
    "Paris Gare de Lyon",
    "Lyon Part-Dieu",
    "Marseille Saint-Charles",
    "Dijon",
    "Macon",
    "Roanne",
    "Bordeaux Saint-Jean",
    "Toulouse Matabiau",
    "Lille Europe",
    "Strasbourg",
    "Nantes",
    "Rennes",
    "Montpellier Saint-Roch",
    "Nice Ville",
    "Grenoble",
    "Avignon TGV",
    "Le Mans",
    "Tours",
    "Angers Saint-Laud",
    "Reims"
]



@app.get("/")
def home():
    return {"message": "Serveur actif !"}

@app.get("/stations")
def get_stations():
    return {
        "status": "success",
        "stations": sorted(GARES)
    }

@app.post("/search")
def recherche(data: dict):
    print(f"Données reçues : {data}")

    return {
        "status" :"success",
        "message": "Données bien reçues et traitées !",
        "trajets" : [
                        {"departure_stop": "Paris Gare de Lyon",
                        "arrival_stop": "Lyon Part-Dieu",
                        "segments": [
                                {"from": "Paris Gare de Lyon",
                                "to": "Dijon",
                                "dep_coor": [48.8447, 2.3737],
                                "arr_coor": [47.3230, 5.0272],
                                "board_time": 10,
                                "arrival_time": 12,
                                "trip": "R2_T1",
                                "route": "R2"},
                                {"from": "Dijon",
                                "to": "Lyon Part-Dieu",
                                "dep_coor": [47.3230, 5.0272],
                                "arr_coor": [45.7605, 4.8601],
                                "board_time": 14,
                                "arrival_time": 24,
                                "trip": "R3_T1",
                                "route": "R3"}
                                    ]
                        },
                        {"departure_stop": "Paris Gare de Lyon",
                        "arrival_stop": "Lyon Part-Dieu",
                        "segments": [
                                {"from": "Paris Gare de Lyon",
                                "to": "Lyon Part-Dieu",
                                "dep_coor": [48.8447, 2.3737],
                                "arr_coor": [45.7605, 4.8601],
                                "board_time": 10,
                                "arrival_time": 40,
                                "trip": "R1_T1",
                                "route": "R1"}
                                    ]
                        },
                        {"departure_stop": "Paris Gare de Lyon",
                         "arrival_stop": "Lyon Part-Dieu",
                         "segments": [
                                {"from": "Paris Gare de Lyon",
                                "to": "Macon",
                                "dep_coor": [48.8447, 2.3737],
                                "arr_coor": [46.3027, 4.8250],
                                "board_time": 10,
                                "arrival_time": 40,
                                "trip": "R2_T1",
                                "route": "R2"},                              
                                {"from": "Macon",
                                "to": "Roanne",
                                "dep_coor": [46.3027, 4.8250],
                                "arr_coor": [46.0393, 4.0629],
                                "board_time": 110,
                                "arrival_time": 250,
                                "trip": "R4_T2",
                                "route": "R4"},
                                {"from": "Roanne",
                                "to": "Lyon Part-Dieu",
                                "dep_coor": [46.0393, 4.0629],
                                "arr_coor": [45.7605, 4.8601],
                                "board_time": 320,
                                "arrival_time": 415,
                                "trip": "R5_T7",
                                "route": "R5"}
                             
                         ]
                        }
                    ]   
            }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)