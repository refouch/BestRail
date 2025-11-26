# Simulation de la table "Gares"
# ID, Nom, Ville (données statiques)
GARES_DB = [
    {"id": 1, "nom": "Paris Gare de Lyon", "ville": "Paris"},
    {"id": 2, "nom": "Lyon Part-Dieu", "ville": "Lyon"},
    {"id": 3, "nom": "Marseille Saint-Charles", "ville": "Marseille"}
]

def get_all_gares():
    """Simule une requête SELECT * FROM gares"""
    return GARES_DB

def get_gare_by_id(gare_id: int):
    """Simule une requête SELECT WHERE id = ..."""
    # On cherche simplement dans la liste
    for gare in GARES_DB:
        if gare["id"] == gare_id:
            return gare
    return None