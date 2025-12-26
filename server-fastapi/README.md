# Projet Infrastructure et Systèmes Logiciels

### Fonctionnement du repo :
frontend : code de Léo. Run le fichier server.py puis ouvrir index.html avec un navigateur pour l'aperçu.

docker : Code pour dockerisé le frontend. Le code de Léo a été légèrement modifié (server.py notamment)

### Modifications lors du passage vers le vrai serveur
* Modification de l'url et des endpoints dans le fichier JS/config.js 

        export const API_CONFIG = {
            BASE_URL: "http://localhost:8000",
            ENDPOINTS: {
                SEARCH: "/search",
                STATIONS: "/stations"
            }
        };

* Format voulu pour la réponse lors de la requête de la liste des gares

        {
        "status": "success",
        "stations": ["Paris Gare de Lyon",
                     "Lyon Part-Dieu",
                     ...]
        }
* Format voulu pour la réponse lors d'une requête de recherche

        {
        "status": "success",
        "trajets": *Objet liste des trajets*
        }