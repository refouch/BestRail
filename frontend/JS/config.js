/** 
 * config.js
 * Fichier de configuration centralisé pour l'application
 * Contient toutes les constants et paramètres de configuratio
 */

// Configuration de l'API
export const API_CONFIG = {
    BASE_URL: "http://localhost:8000",
    ENDPOINTS: {
        SEARCH: "/search",
        STATIONS: "/stations"
    }
};


// Configuration de la carte Leaflet
export const MAP_CONFIG = {
    // Initialisation de la carte
    CENTER: [46.603354, 1.888334],
    ZOOM: 5.5,

    // Tuiles OpenStreetMap
    TILE_LAYER: {
        URL: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        ATTRIBUTION: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
        MAX_ZOOM: 19
    },

    // Configuration des courbes entre les points
    CURVE: {
        NUM_POINTS: 50,
        CURVATURE: 0.2
    },

    // Styles des lignes et marqueurs
    STYLES: {
        LINE_DEFAULT: {
            color: '#2563eb',
            weight: 3,
            opacity: 0.8
        },
        LINE_HIGHLIGHT: {
            color: '#1d4ed8',
            weight: 3.5,
            opacity: 0.8
        },
        MARKER_START: {
            radius: 8,
            fillColor: '#10b981',
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        },
        MARKER_CONNECTION: {
            radius: 6,
            fillColor: '#f59e0b',
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        },
        MARKER_END: {
            radius: 8,
            fillColor: '#dc2626',
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }
    },

    // Padding pour l'ajustement de la vue
    BOUNDS_PADDING: [50,50]
};

// Clés pour le sessionStorage
export const STORAGE_KEYS = {
    SEARCH_PARAMS: "searchParams",
    SEARCH_RESULTS: "searchResults",
    STATIONS_LIST: "stationsList"
};

// Messages utilisateur
export const MESSAGES= {
    SEARCH_IN_PROGRESS: "Recherche en cours...",
    SEARCH_ERROR: "Une erreur s'est produite lors de la recherche. Veuillez réessayer.",
    NO_RESULTS: "Aucun trajet trouvé pour cette recherche.",
    FILL_ALL_FIELDS: "Veuillez remplir tous les champs.",
    STATIONS_LOAD_ERROR: "Impossible de charger la liste des gares."
};
