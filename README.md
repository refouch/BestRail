# BestRail - Calculateur d'itinéraires de train 
### *Projet Infrastructures et Systèmes Logiciels - ENSAE 3A*

## 1. Présentation du groupe
* **Thomas** : Responsable données et API
* **Rémi** : Responsable backend et algorithmes de pathfinding
* **Félix** : Gestion du serveur FastAPI 
* **Léo** : Responsable frontend et interface utilisateur
* **Camille** : Coordination générale et dockerisation

---

## 2. Présentation du projet

Nous avons décidé de construire une application web permettant de calculer efficacement des trajets en train entre deux gares données. C'est un type de projet qui nous a permis de mettre en oeuvre la plupart des notions abordées en cours (logique algorithmique, contenairisation, mise en place d'un serveur...). 

L'application ainsi développée permet de calculer à travers une interface utilisateur les différents trajets les plus courts sur une plage de temps donnée, en utilisant les horaires de train prévisionels fournis par l'API de la SNCF. 

## 3. Architecture du Système

Le projet est construit sur la base de plusieurs modules complémentaires

* **Backend -** Un premier module écrit en Python qui permet séquentiellement :
    - Le téléchargement des horaires théoriques de tous les trains d'une journée au format GTFS
    - La conversion de ces mêmes données en plusieurs objets adaptés pour le calcul d'itinéraires
    - Le calcul des itinéraires en lui même par une implémentation from scratch de l'algorithme RAPTOR, très utilisé pour ce genre de cas d'usage (référence [ici](https://www.microsoft.com/en-us/research/wp-content/uploads/2012/01/raptor_alenex.pdf))

Nous avons essayé d'implémenter ce module de la façon la plus optimisée possible, tout en essayant au maximum de ne pas utiliser de librairies externes.

* **Frontend -** Un module écrit en HTML/CSS/JS pour construire une interface utilisateur fonctionnelle :
    - Une page d'accueil qui permet d'effectuer une recherche d'itinéraire et qui présente le projet
    - Une page de résultats qui affiche les trajets disponibles et qui permet de relancer une recherche
    - Communication avec le serveur backend pour envoyer les recherches de l'utilisateur et afficher les résultats de l'algorithme de pathfinding

* **Serveur -** Le module qui permet de faire la liaison entre le backend et le frontend :
    - Noyau opérationnel du backend, développé avec le framework FastAPI
    - Automatisation du cycle de vie des données GTFS : téléchargement, extraction et mise à jour via un planificateur de tâche en arrière-plan
    - Différents endpoints : recherche d'itinéraire basée sur l'agorithme RAPTOR, référencement des stations disponibles, traitement des requêtes de navigation

* **Contenairisation :** Trois  fichiers permettant de créer une image Docker. Le container instancié expose le port 8000 et est mappé sur le port 8080 de la machine de l'hôte.

## 4. Présentation des fonctionnalités de l'application

L'application permet d'effectuer une recherche d'itinéraires en train à partir d'une gare de départ et jusqu'à une gare d'arrivée : 

* La recherche couvre toutes les gares françaises ainsi que certaines gares de pays frontaliers (Allemagne, Espagne, ...)

* Un système d'autocomplétion suggère en temps réel les gares disponibles lorsque l'utilisateur remplit les champs correspondants

* L'algorithme renvoie une liste de trajets possibles, avec les informations majeures relatives au trajet (horaires, durée, nombres de correspondances)

* Au survol, le trajet s'affiche sur une carte pour visualiser les différentes gares du trajet (départ, arrivée et correspondances)

* Un panneau déroulant permet d'en savoir plus sur les détails de chaque trajet 

* La page des résultats permet de modifier et de relancer la recherche d'itinéraires

* Nous avons négligé les liaisons non ferroviaires lors de l'implémentation, l'algorithme renvoie donc des trajets non optimaux lorsqu'une correspondance non ferroviaire entre deux gares serait optimale (par exemple prendre le métro entre deux gares parisiennes).

---


### Installation et containerisation

- Installer et lancer Docker Desktop
- Cloner le projet en local :
```bash
git clone https://github.com/refouch/BestRail.git
```
- Se placer à la racine du projet : "Projet-infra-sncf"
- Construire l'image : 
```bash
docker build -t sncf-app .
```

- Lancer le docker : 
```bash
docker run -p 8080:8000 --name sncf-app sncf-app
```
Le docker est mappé sur le port local http://localhost:8080/

- Stoper le container :
```bash
docker stop sncf-app
```

- Supprimer le container :
```bash
docker rm sncf-app
```

