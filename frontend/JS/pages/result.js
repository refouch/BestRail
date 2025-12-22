/**
 * result.js
 * Script principal de la page des résultats
 * Gère l'affichage des trajets, de la carte interactive et la modification de la recherche
 */

import { MapManager } from "../map/mapManager.js";
import { TripCardGenerator } from "../components/tripCard.js";
import { StorageManager } from "../utils/storageUtils.js";
import { SearchAPI } from "../api/searchAPI.js";
import { MESSAGES } from "../config.js";

// Variables globales de la page
let mapManager = null;
let searchParams = null;
let searchResults = null;
let isEditing = false;

/**
 * Initialise la carte Leaflet
 */
function initMap() {
    try {
        mapManager = new MapManager("map-result");
        console.log("Carte initialisée avec succès");
    } catch (error) {
        console.error("Erreur lors de l'initialisation de la carte:", error);
    }
}

/**
 * Charge les données depuis le sessionStorage
 */
function loadSearchData() {
    const data = StorageManager.getSearchData();

    if (!data.params || !data.results) {
        console.warn("Aucune donnée trouvée dans sessionStorage");
        window.location.href = "index.html";
        return false;
    }

    searchParams = data.params;
    searchResults = data.results;

    console.log("Récap de la recherche (session storage):", searchParams);
    console.log("Résultats du serveur (session storage):", searchResults);

    return true;
}

/**
 * Affiche le récapitulatif de la recherche en haut de la page
 */

function displaySearchRecap() {
    if (!searchParams) return;

    document.querySelector(".ville-depart").textContent = searchParams.depart;
    document.querySelector(".ville-arrivee").textContent = searchParams.arrivee;

    // Formatage de la date pour l'affichage
    const dateObj = new Date(searchParams.date);
    const dateFormatee = dateObj.toLocaleDateString('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.querySelector(".travel-date").textContent = dateFormatee;
}

/**
 * Affiche la liste des trajets trouvés
 */
function displayTripsList() {
    const trajetList = document.querySelector(".trajet-list");

    if (!trajetList) {
        console.error("Conteneur .trajet-list non trouvé");
        return;
    }

    // Génération du HTML pour tous les trajets
    trajetList.innerHTML = TripCardGenerator.generateAllCards(searchResults.trajets);

    if (searchResults.trajets && searchResults.trajets.length > 0) {
        // Ajout des événements de survol et de clic
        attachTripCardEvents();
        console.log(`${searchResults.trajets.length} trajet(s) affiché(s)`);
    }
}

/**
 * Attache les événements de survol et de clic aux cartes de trajets
 */
function attachTripCardEvents() {
    const tripCards = document.querySelectorAll(".trip-card");

    tripCards.forEach((card, index) => {
        const trajet = searchResults.trajets[index];

        if (!trajet) return;

        //Événement de survol : affichage sur la carte
        card.addEventListener("mouseenter", () => {
            if (mapManager) {
                mapManager.displayTrip(trajet, false);
            }
        });

        // Événement de sortie : nettoyer la carte si détails fermés
        card.addEventListener("mouseleave", () => {
            if (mapManager) {
                const detailsBtn = card.querySelector(".details-btn");
                if (!detailsBtn.classList.contains("active")) {
                    mapManager.clearLayers();
                }
            }
        });
    });
}

/**
 * Initialise le bouton de modification de recherche
 */
function initModifySearchButton() {
    const modifyBtn = document.getElementById("modifyBtn");

    if (!modifyBtn) {
        console.error("Bouton modifer non trouvé");
        return;
    }

    modifyBtn.addEventListener("click", handleModifySearch);
}

/**
 * Gère le clic sur le bouton "Modifier la recherche"
 */
async function handleModifySearch() {
    const modifyBtn = document.getElementById("modifyBtn");

    if (!isEditing) {
        // Mode édition
        enableEditMode();
    } else {
        // Mode validation
        await submitModifiedSearch(modifyBtn);
    }
}

/**
 * Active le mode édition du récapitulatif de recherche
 */
function enableEditMode() {
    const villeDepart = document.querySelector(".ville-depart");
    const villeArrivee = document.querySelector(".ville-arrivee");
    const travelDate = document.querySelector(".travel-date");
    const modifyBtn = document.getElementById("modifyBtn");

    // Conversion de la date au format datetime-local
    const dateObj = new Date(searchParams.date);
    const datetimeValue = dateObj.toISOString().slice(0,16);

    // Remplacement par des inputs
    villeDepart.innerHTML = `<input type="text" class="recap-input" id="edit-depart" value="${searchParams.depart}" required>`;
    villeArrivee.innerHTML = `<input type="text" class="recap-input" id="edit-arrivee" value="${searchParams.arrivee}" required>`;
    travelDate.innerHTML = `<input type="datetime-local" class="recap-input" id="edit-datetime" value="${datetimeValue}" required>`;

    modifyBtn.textContent = "Valider";
    modifyBtn.classList.add("validate-mode");
    isEditing = true;
}

/**
 * Soumet la recherche modifiée
 * @param {HTMLElement} modifyBtn - Bouton de validation
 */
async function submitModifiedSearch(modifyBtn) {
    // Récupération des nouvelles valeurs
    const newDepart = document.getElementById("edit-depart").value.trim();
    const newArrivee = document.getElementById("edit-arrivee").value.trim();
    const newDatetime = document.getElementById("edit-datetime").value;

    // Validation des champs 
    if (!newDepart || !newArrivee || !newDatetime) {
        alert(MESSAGES.FILL_ALL_FIELDS);
        return;
    }

    // Préparation du payload
    const payload = {
        depart: newDepart,
        arrivee: newArrivee,
        date: newDatetime
    };

    console.log("Nouvelle recherche avec :", payload);

    // Indicateur de chargement
    modifyBtn.textContent = MESSAGES.SEARCH_IN_PROGRESS;
    modifyBtn.disabled = true;

    try {
        // Envoi de la requête
        const data = await SearchAPI.searchTrains(payload);

        // Mise à jour du sessionStorage
        StorageManager.saveSearch(payload, data);

        // Rechargement de la page avec les nouveaux résultats
        window.location.reload();

    } catch (error) {
        console.error("Erreur lors de la requête:", error);

        // Restauration du bouton
        modifyBtn.textContent = "Valider";
        modifyBtn.disabled = false;

        // Message d'erreur
        alert(MESSAGES.SEARCH_ERROR);
    }
}

/**
 * Fonction globale pour gérer l'ouverture/fermeture des panneaux de détails
 * Appelée par onclick dans le HTML généré
 * @param {HTMLElement} button - Bouton "Voir les détails"
 */
window.toggleDetails = function(button) {
    const card = button.closest(".trip-card");
    const panel = card.querySelector(".trip-details-panel");
    const isOpen = panel.classList.contains("open");

    // Récupération de l'index du trajet
    const cardIndex = parseInt(card.dataset.tripIndex);

    if (isOpen) {
        // Fermeture du panneau
        panel.classList.remove("open");
        button.classList.remove("active");
        button.textContent = "Voir les détails";

        // Nettoyage de la carte et réinitialisation position et zoom
        if (mapManager) {
            mapManager.clearLayers();
            mapManager.resetView();
        }
    } else {
        // Fermeture de tous les autres panneaux
        document.querySelectorAll(".trip-details-panel.open").forEach(p => {
            p.classList.remove("open");
        });
        document.querySelectorAll(".details-btn.active").forEach(b => {
            b.classList.remove("active");
            b.textContent = "Voir les détails";
        });

        // Ouverture du panneau actuel
        panel.classList.add("open");
        button.classList.add("active");
        button.textContent = "Masquer les détails";

        // Affichage du trajet sur la carte (en rouge)
        if (mapManager && searchResults.trajets[cardIndex]) {
            mapManager.resetView(); // Réinitialisation avant l'affichage
            mapManager.displayTrip(searchResults.trajets[cardIndex], true);
        }
    }
};

/**
 * Initialise la page de résultats
 */
function initResultsPage() {
    // Chargement des données
    if (!loadSearchData()) {
        return; // Redirection vers l'accueil
    }

    // Initialisation des composants
    initMap();
    displaySearchRecap();
    displayTripsList();
    initModifySearchButton();

    console.log("Page de résultats initialisée")
}

// Initialisation au chargement du DOM
document.addEventListener("DOMContentLoaded", initResultsPage);
