from fastapi import FastAPI 
from mock_bdd import get_all_gares
from mock_algo import calculer_itineraire
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

class Gare(BaseModel) : 
    id : int
    nom : str 
    ville : str

class Etape(BaseModel) : 
    gare : str
    heure : str

class Itineraire(BaseModel) :
    depart_id : int 
    arrivee_id : int 
    prix_total : float
    duree_minutes : int 
    etapes : List[Etape]
    
app = FastAPI()

# Cela autorise ton navigateur à faire des requêtes vers le serveur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" signifie "tout le monde". En prod, on mettrait l'URL précise du site.
    allow_credentials=True,
    allow_methods=["*"],  # Autorise GET, POST, etc.
    allow_headers=["*"],
)


@app.get("/")
def home_page() : 
    return {"message": "Bienvenue sur l'API du comparateur SNCF !"}

@app.get("/search", response_model=Itineraire) # Note le changement ici (plus de List)
def search(id_depart: int, id_arrivee: int):
    # On récupère le dictionnaire brut
    data = calculer_itineraire(id_depart, id_arrivee)
    
    # On le transforme en objet en une seule ligne grâce au déballage
    # Pydantic s'occupe de valider et de convertir les sous-objets (etapes) !
    res = Itineraire(**data)
    
    return res

@app.get("/gares", response_model = List[Gare])
def get_gares():
    return get_all_gares()

    
