/**
 * searchAPI.js
 * Gestion des appels API vers le serveur
 * Centralise toute la logique de communication avec le backend
 */

import { API_CONFIG, MESSAGES } from "../config.js";

/**
 * Gestionnaire des appels API pour la recherche de trajets
 */
export const SearchAPI = {

    /**
     * Récupère la liste des gares disponibles depuis le serveur
     * @returns {Promise<Array<string>>} Liste des noms de gares
     * @throws {Error} si la requête échoue
     * 
     * @example
     * try {
     *  const stations = await SearchAPI.getStations();
     *  console.log(stations); //["Paris Gare de Lyon", "Lyon Part-Dieu", ...]
     *  } catch (error) {
     *  console.error(error);
     * }
     */
    async getStations() {
        console.log("Récupération de la liste des gares...");

        try {
            const response = await fetch(
                `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.STATIONS}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );

            console.log("Statut de la réponse (stations):", response.status);

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const data = await response.json();
            console.log("Liste des gares reçue:", data);

            return data.stations || [];
            
        } catch (error) {

        }
    },


    /**
     * Effectue une recherche de trajets auprès du serveur
     * @param {Object} searchData - Données de recherche
     * @param {string} searchData.depart - Gare de départ
     * @param {string} searchData.arrivee - Gare d'arrivée
     * @param {string} searchData.date - Date et heure au format ISO (YYYY-MM-DDTHH:mm)
     * @returns {Promise<Object>} Résultats de la recherche
     * @throws {Error} Si la requête échoue
     * 
     * @example
     * try {
     *  const results = await SearchAPI.searchTrains({
     *      depart: "Paris Gare de Lyon",
     *      arrivee: "Lyon Part-Dieu",
     *      date: "2025-12-31T17:00"
     * });
     * } catch (error) {
     *  console.error(error)
     * }
     */
    async searchTrains(searchData) {
        console.log("Envoie de la requête vers le serveur...", searchData);

        try {
            const response = await fetch(
                `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SEARCH}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': "application/json"
                    },
                    body: JSON.stringify(searchData)
                }                
            );
            
            console.log("Statut de la réponse:", response.status);
            console.log("Réponse OK?", response.ok);

            // Vérification du statut HTTP
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const data = await response.json();
            console.log("Réponse du serveur:", data);

            return data;

        } catch(error) {
            console.error("Erreur lors de la requête:", error);
            console.error("Message d'erreur:", error.message);
            throw error;
        }
    },

    /**
     * Effectue une recherche avec gestion automatique des erreurs utilisateur
     * Affiche un message d'erreur si la requête échoue
     * @param {Object} searchData - Données de recherche
     * @param {Function} onSuccess - Callback appelé en cas de succès (reçoit les données)
     * @param {Function} onError - Callback appelé en cas d'erreur (optionnel)
     * @returns {Promise<void>}
     * 
     * @example 
     * await SearchAPI.searchTrainsWithUI(
     *  { depart: "Paris", arrivee: "Lyon", date: "2024-01-15T10:00" },
     *   (data) => {
     *     // Succès : afficher les résultats
     *     console.log(data.trajets);
     *   },
     *   (error) => {
     *     // Erreur personnalisée (optionnel)
     *     console.error('Erreur custom:', error);
     *   }
     * );
     */
    async searchTrainsWithUI(searchData, onSuccess, onError = null) {
        try {
            const data = await this.searchTrains(searchData);

            if (onSuccess) {
                onSuccess(data);
            }
        } catch (error) {
            if (onError) {
                onError(error);
            } else {
                alert(MESSAGES.SEARCH_ERROR);
            }
        }
    },

    /**
     * Vérifie si le serveur est accessible 
     * @returns {Promise<boolean>} true si le serveur répond
     * 
     * @example
     * const isOnline = await SearchAPI.checkServerHealth();
     * if (!isOnline) {
     *      alert("Le serveur est indisponible.");
     * }
     */
    async checkServerHealth() {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/`);
            return response.ok;
        } catch (error) {
            console.error("Serveur inaccessible:", error);
            return false;
        }
    }
};