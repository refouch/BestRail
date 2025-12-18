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

@app.get("/")
def home():
    return {"message": "Serveur actif !"}

@app.post("/search_old")
def recherche_old(data:dict):
    print(f"Données reçues : {data}")

    return {
        "status": "success",
        "message": "Données bien reçues !",
        "trajets": [
            {"depart": "Paris Gare de Lyon",
                "arrivee": "Lyon Part-Dieu",
                "heure_depart": "08:30",
                "heure_arrivee": "10:25",
                "duree": "1h55",
                "prix": 45,
                "train_type": "TGV INOUI 6601",
                "correspondances": "Direct"},
            {"depart": "Paris Gare de Lyon",
                "arrivee": "Lyon Part-Dieu",
                "heure_depart": "10:47",
                "heure_arrivee": "12:45",
                "duree": "1h58",
                "prix": 52,
                "train_type": "TGV INOUI 6605",
                "correspondances": "Direct"},
            {"depart": "Paris Gare de Lyon",
                "arrivee": "Lyon Part-Dieu",
                "heure_depart": "12:15",
                "heure_arrivee": "14:45",
                "duree": "2h30",
                "prix": 38,
                "train_type": "TGV 6607 + TER 18234",
                "correspondances": "1 correspondance (Dijon)"},
            {"depart": "Paris Gare de Lyon",
                "arrivee": "Lyon Part-Dieu",
                "heure_depart": "14:30",
                "heure_arrivee": "18:05",
                "duree": "3h35",
                "prix": 29,
                "train_type": "Intercités 4823 + TER 19056",
                "correspondances": "2 correspondances (Dijon, Mâcon)"}
        ]
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
                                "dep_coor": [42.0 ,42.0],
                                "arr_coor": [43.0, 43.0],
                                "board_time": 10,
                                "arrival_time": 12,
                                "trip": "R2_T1",
                                "route": "R2"},
                                {"from": "Dijon",
                                "to": "Lyon Part-Dieu",
                                "dep_coor": [43.0, 43.0],
                                "arr_coor": [44.0, 44.0],
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
                                "dep_coor": [42.0, 42.0],
                                "arr_coor": [44.0, 44.0],
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
                                "dep_coor": [42.0,42.0],
                                "arr_coor": [42.5,42.5],
                                "board_time": 10,
                                "arrival_time": 40,
                                "trip": "R2_T1",
                                "route": "R2"},                              
                                {"from": "Macon",
                                "to": "Roanne",
                                "dep_coor": [42.5,42.5],
                                "arr_coor": [43.5,43.5],
                                "board_time": 110,
                                "arrival_time": 250,
                                "trip": "R4_T2",
                                "route": "R4"},
                                {"from": "Roanne",
                                "to": "Lyon Part-Dieu",
                                "dep_coor": [43.5,43.5],
                                "arr_coor": [44.0,44.0],
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