# BestRail - Calculateur d'itinéraires de train 
### *Projet Infrastructure et Systèmes Logiciels - ENSAE 3A*

## 1. Présentation du groupe
* **Thomas** : Responsable données et API
* **Rémi** : Responsable backend et algirthmes de pathfinding
* **Félix** : Gestion du serveur Flask 
* **Léo** : Responsable frontend et interface graphique
* **Camille** : Coordination générale et dockerisation

---

## 2. Présentation du projet

Nous avons décidé de construire une application web permettant de calculer efficacement des trajets en train entre deux gares données. C'est un type de projet qui nous a permis de mettre en oeuvre la plupart des notions abordées en cours (logique algorithmique, contenairisation, mise en place d'un serveur...). 

L'application ainsi devellopée permet pour l'instant de calculer à travers une interface graphique les différents trajets les plus courts sur une plage de temps donnée, en utilisant les horaires de train prévisionels fournies par l'API de la SNCF. 

## 3. Architecture du Système

Le projet est construit sur la base de plusieurs modules complémentaires

* **Backend :** Un premier module écrit en Python qui permet séquentiellement:
    - Le téléchargement des horaires théoriques de tous les trains d'une journée au format GTFS
    - La conversion de ces mêmes données en plusieurs objets adaptés pour le calcul d'itinéraires
    - Le calcul des itinéraires en lui même par une implémentation de zéro de l'algorithme RAPTOR, très utilisé pour ce genre de cas d'usage

Nous avons essayé d'implémenter ce module de la façon la plus optimisée possible, tout en essayant au maximum de ne pas utiliser de librairies externes.

* **Frontend :** Un module écrit en HTML/CSS/JS pour construire un GUI facilement utilisable (Léo à toi de décrire ?)

* **Serveur :** Le troisième module qui permet de faire la liaison entre le backend et le frontend (Felix)

* **Contenairisation :** Camille

### Prérequis et installation

Décrire ici comment installer et lancer le projet (notamment docker!)
```bash
git pull etc..
```