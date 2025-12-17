from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Servir les fichiers statiques (JS, CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates Jinja2
templates = Jinja2Templates(directory="templates")

# Route principale (index.html)
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Page de recherche (search.html)
@app.get("/result", response_class=HTMLResponse)
def search_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

# Endpoint API pour la recherche
@app.post("/search")
def recherche(data: dict):
    print(f"Données reçues : {data}")
    return {
        "status": "success",
        "message": "Données bien reçues !",
        "trajets": [
            {
                "depart": "Paris Gare de Lyon",
                "arrivee": "Lyon Part-Dieu",
                "heure_depart": "08:30",
                "heure_arrivee": "10:25",
                "duree": "1h55",
                "prix": 45,
                "train_type": "TGV INOUI 6601",
                "correspondances": "Direct"
            },
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
