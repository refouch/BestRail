# Projet Infrastructure et Systèmes Logiciels

### Fonctionnement du repo :

Pour tester le code avec le mock serveur

* Lancer le mock serveur frontend/server.py via le terminal

* Accéder aux pages HTML - Activation d'un protocole HTTP. Dans un terminal, se mettre dans le dossier frontend puis taper la commande suivante : "python -m http.server 8080" (ou un autre port que 8080 si voulu). Ensuite, dans un navigateur, taper "http://localhost:8080/" (remplacer le nom du port si besoin).


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