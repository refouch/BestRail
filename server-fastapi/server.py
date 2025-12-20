# Mock server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_raptor import RaptorEngine
import json

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

engine = RaptorEngine("gtfs_sncf", force_rebuild=False)

@app.post("/search")
def recherche(data: dict):
    print(f"Données reçues : {data}")

    depart = data['depart']
    arrivee = data['arrivee']
    date = data['date']
    
    # DEPART = "StopPoint:OCETGV INOUI-87723197" 
    # ARRIVEE = "StopPoint:OCETGV INOUI-87575001"
    # DATE = "20251225"
    
    tau, ptr = engine.solve(depart, date, "08:00:00")
    
    # Génération et affichage du JSON
    json_results = engine.get_json_results(tau, ptr, arrivee, 4)
    
    #return json.dumps(json_results, indent=2, ensure_ascii=False)
    return json_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)