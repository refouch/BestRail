/**
 * index.js
 * Script principal de la page d'accueil
 * Gère le formulaire de recherche et la soumission vers le serveur
 */

import { SearchAPI } from "../api/searchAPI.js";
import { StorageManager } from "../utils/storageUtils.js";
import { MESSAGES } from "../config.js";

/**
 * Charge la liste des gares et remplit le datalist
 */
async function loadStations() {
    // Vérifier si les gares sont déjà en cache
    let stations = StorageManager.getStations();

    if (stations && stations.length > 0) {
        console.log("Gares chargées depuis le cache");
        populateDatalist(stations);
        setupInputFiltering(); // Filtrage autocomplétion selon taille de l'input
        return;
    }

    // Sinon, récupérer depuis le serveur
    try {
        stations = await SearchAPI.getStations();

        // Sauvegarde dans le sessionStorage pour les prochaines utilisations
        StorageManager.saveStations(stations);

        // Remplir le datalist
        populateDatalist(stations);

        // Configurer le filtrage
        setupInputFiltering();

        console.log(`${stations.length} gares chargées avec succès !`);
    } catch (error) {
        console.error("Erreur lors du chargement des gares:", error);
    }
}

/**
 * Remplit le datalist avec la liste des gares
 * @param {Array<string>} stations - Liste des nomes de gares
 */
function populateDatalist(stations) {
    const datalist = document.getElementById("stations-list");

    if (!datalist) {
        console.error("Datalist #stations-list non trouvé");
        return;
    }

    // Vider le datalist existant
    datalist.innerHTML = "";

    // Ajouter chaque gare comme option
    stations.forEach(station => {
        const option = document.createElement("option");
        option.value = station;
        datalist.appendChild(option);
    });

    console.log(`Datalist rempli avec ${stations.length} gares.`);
}

/**
 * Configure le filtrage : le datalist n'apparaît qu'à partir de 2 caractères
 */
function setupInputFiltering() {
    const departInput = document.getElementById("depart");
    const arriveeInput = document.getElementById("arrivee");

    if (!departInput || !arriveeInput) {
        console.error("Inputs non trouvés");
        return;
    }

    // Fonction pour gérer l'affichage du datalist
    const handleInputChange = (input) => {
        const value = input.value;

        if (value.length < 2) {
            // Retirer la connexion au datalist
            input.removeAttribute("list");
        } else {
            // Connecter au datalist
            input.setAttribute("list", "stations-list");
        }
    };

    // Attacher les événements aux deux inputs
    departInput.addEventListener("input", (e) => {
        handleInputChange(e.target);
    });

    arriveeInput.addEventListener("input", (e) => {
        handleInputChange(e.target);
    });

    // Retirer l'attribut list au chargement
    departInput.removeAttribute("list");
    arriveeInput.removeAttribute("list");

    console.log("Filtrage configuré : datalist visible à partir de 2 caractères")
}

/**
 * Initialise le formulaire de recherdhe
 */
function initSearchForm() {
    const formulaire = document.getElementById("search-form");

    if (!formulaire) {
        console.error("Formulaire de recherche non trouvé.");
        return;
    }

    formulaire.addEventListener("submit",handleFormSubmit);
    console.log("Formulaire de recherche initialisé");
}

/**
 * Gère la soumission du formulaire de recherche
 * @param {Event} event - Événement de soumission du formulaire
 */

async function handleFormSubmit(event) {
    event.preventDefault(); // Empêcher le rechargement automatique de la page

    // Récupération du formulaire
    const formulaire = event.target;

    // Récupération des données du formulaire
    const depart = document.getElementById("depart").value;
    const arrivee = document.getElementById("arrivee").value;
    const datetime = document.getElementById("datetime").value;

    console.log("Données du formulaire :", {depart, arrivee, date: datetime});

    // Validation des champs
    if (!depart || !arrivee || !datetime) {
        alert(MESSAGES.FILL_ALL_FIELDS);
        return;
    }

    // Préparation du payload pour le serveur
    const payload = {
        depart: depart,
        arrivee: arrivee,
        date: datetime
    };

    console.log("Payload:", payload)

    // Gestion du bouton de recherche (indicateur de chargement)
    const boutonRecherche = formulaire.querySelector("button[type='submit']");
    const textOriginal = boutonRecherche.textContent;
    boutonRecherche.textContent = MESSAGES.SEARCH_IN_PROGRESS;
    boutonRecherche.disabled = true;

    try {
        // Envoi de la requête au serveur
        const data = await SearchAPI.searchTrains(payload);

        // Sauvegarde des données dans le sessionStorage
        StorageManager.saveSearch(payload,data);

        // Redicrection vers la page de résultats
        window.location.href = "result.html";

    } catch (error) {
        // Gestion des erreurs
        console.error("Erreur losr de la recherche:", error);

        // Restauration du bouton de recherche
        boutonRecherche.textContent = textOriginal;
        boutonRecherche.disabled = false;

        // Message d'erreur à l'utilisateur
        alert(MESSAGES.SEARCH_ERROR);
    }
}

/**
 * Initialise la page d'accueil
 */
async function initIndexPage() {

    // Charger les gares
    await loadStations();

    // Puis initialiser le formulaire
    initSearchForm();
    console.log("Page d'accueil initialisée");
}

// Initialisation au chargement du DOM
document.addEventListener("DOMContentLoaded", initIndexPage);
