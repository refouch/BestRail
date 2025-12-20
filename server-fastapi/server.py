# Mock server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_raptor import RaptorEngine
import json
from datetime import datetime

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
    date = datetime.fromisoformat(date)
    # Heure au format HH:MM:SS
    heure = date.strftime('%H:%M:%S')
    # Date au format YYYYMMDD
    date = date.strftime('%Y%m%d')
    # DEPART = "StopPoint:OCETGV INOUI-87723197" 
    # ARRIVEE = "StopPoint:OCETGV INOUI-87575001"
    # DATE = "20251225"
    
    tau, ptr = engine.solve(depart, date, heure)
    
    # Génération et affichage du JSON
    json_results = engine.get_json_results(tau, ptr, arrivee, 4)
    
    # # After getting the itineraries from the RAPTOR algorithm, filter them:
    # valid_itineraries = [
    #     itin for itin in json_results 
    #     if itin.get('departure_stop') and itin.get('segments') and len(itin['segments']) > 0
    # ]
    # print(f"Données envoyées : {valid_itineraries}")
    # return valid_itineraries
    
    # Filter valid itineraries
    valid_itineraries = [
        itin for itin in json_results 
        if itin.get('departure_stop') and itin.get('segments') and len(itin['segments']) > 0
    ]
    
    # Transform to frontend format
    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    
    def calculate_duration(segments):
        start = segments[0]['board_time']
        end = segments[-1]['arrival_time']
        duration_minutes = (end - start) // 60
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        return f"{hours}h{minutes:02d}"
    
    transformed_results = {
        "trajets": [
            {
                "depart": itin['departure_stop'],
                "arrivee": itin['arrival_stop'],
                "heure_depart": format_time(itin['segments'][0]['board_time']),
                "heure_arrivee": format_time(itin['segments'][-1]['arrival_time']),
                "duree": calculate_duration(itin['segments']),
                "train_type": itin['segments'][0]['route'],
                "correspondances": f"{len([s for s in itin['segments'] if s['trip'] == 'WALK'])} correspondance(s)",
                "prix": "N/A",
                "segments": itin['segments']  # Keep for map display
            }
            for itin in valid_itineraries
        ]
    }
    
    print(f"Données envoyées : {transformed_results}")
    return transformed_results
    
    
    #return json.dumps(json_results, indent=2, ensure_ascii=False)
    # return json_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)