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

@app.post("/search")
def recherche(data:dict):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)