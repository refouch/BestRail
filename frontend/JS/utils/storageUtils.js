/**
 * storageUtils.js
 * Utilitaires pour la gestion du sessionStorage
 * Centralise tous les accès au stockage de session
 */

import { STORAGE_KEYS } from "../config.js";

/**
 * Gestionnaire de stockage pour les données de recherche
 */
export const StorageManager = {

    /**
     * Sauvegarder les paramètres de recherche et les résultats dans le sessionStorage
     * @param {Object} searchParams - Paramètres de la recherche (depart, arrivee, date)
     * @param {Object} searchResults - Résultats retournés par le serveur
     * 
     * @example
     * StorageManager.saveSearch(
     * { depart: "Paris", arrivee: "Lyon", date: "2024-01-15T10:00" },
     * { status: "success", trajets: [...] });
     */
    saveSearch(searchParams, searchResults) {
        try {
            sessionStorage.setItem(
                STORAGE_KEYS.SEARCH_PARAMS,
                JSON.stringify(searchParams)
            );
            sessionStorage.setItem(
                STORAGE_KEYS.SEARCH_RESULTS,
                JSON.stringify(searchResults)
            );
            console.log("Recherche sauvegardée dans sessionStorage");
        } catch (error) {
            console.error("Erreur lors de la sauvegarde dans sessionStorage:", error);
        }
    },

    /**
     * Récupère les paramètres de recherche depuis le sessionStorage
     * @returns {Object|null} Les paramètres de recherche ou null si non trouvés
     * 
     * @exeample
     * const params = StorageManager.getSearchParams();
     * if (params) {
     *      console.log(params.depart, params.arrivee);
     * }
     */
    getSearchParams() {
        try {
            const data = sessionStorage.getItem(STORAGE_KEYS.SEARCH_PARAMS);
            return data ? JSON.parse(data) : null;
        } catch(error) {
            console.error("Erreur lors de la lecture des paramètres:", error);
            return null;
        }
    },

    /**
     * Récupères les résultats de recherche depuis le sessionStorage
     * @returns {Object|null} Les résultats de recherche ou null si non trouvés
     * 
     * @example 
     * const results = StorageManager.getSearchResults();
     * if (results && results.trajets) {
     *      console.log(`${results.trajets.length} trajets trouvés`);
     * }
     */
    getSearchResults() {
        try {
            const data = sessionStorage.getItem(STORAGE_KEYS.SEARCH_RESULTS);
            return data ? JSON.parse(data) : null;
        } catch(error) {
            console.error("Erreur lors de la lecture des résultats:", error);
            return null;
        }
    },

    /**
     * Efface toutes les données de recherche du sessionStorage
     * Utile pour le bouton "Nouvelle recherche" ou la déconnexion
     * 
     * @example
     * StorageManager.clearSearch();
     */
    clearSearch() {
        try {
            sessionStorage.removeItem(STORAGE_KEYS.SEARCH_PARAMS);
            sessionStorage.removeItem(STORAGE_KEYS.SEARCH_RESULTS);
            console.log("Données de recherche effacées");
        } catch(error) {
            console.error("Erreur lors de l'effacement:", error);
        }

    },

    /**
     * Vérifie si des données de recherche existent dans le sessionStorage
     * @returns {boolean} true si des données existent
     * 
     * @example
     * if (!Storage.Manager.hasSearchData()) {
     *      window.location.href = 'index.html';
     * }
     */
    hasSearchData() {
        return sessionStorage.getItem(STORAGE_KEYS.SEARCH_PARAMS) !== null &&
               sessionStorage.getItem(STORAGE_KEYS.SEARCH_RESULTS) !== null;
    }
};