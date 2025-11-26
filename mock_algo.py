def calculer_itineraire(id_depart: int, id_arrivee: int):
    """
    Renvoie toujours le même trajet factice, peu importe la demande.
    C'est suffisant pour tester que ton Backend transmet bien la réponse.
    """
    return {
        "depart_id": id_depart,
        "arrivee_id": id_arrivee,
        "prix_total": 45.50,
        "duree_minutes": 120,
        "etapes": [
            {"gare": "Paris Gare de Lyon", "heure": "10:00"},
            {"gare": "Lyon Part-Dieu", "heure": "12:00"}
        ]
    }