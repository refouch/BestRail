/**
 * index.js
 * Script principal de la page d'accueil
 * Gère le formulaire de recherche et la soumission vers le serveur
 */

import { SearchAPI } from "../api/searchAPI.js";
import { StorageManager } from "../utils/storageUtils.js";
import { MESSAGES } from "../config.js";

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
function initIndexPage() {
    initSearchForm();
    console.log("Page d'accueil initialisée");
}

// Initialisation au chargement du DOM
document.addEventListener("DOMContentLoaded", initIndexPage);
