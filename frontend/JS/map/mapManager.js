/**
 * mapManager.js
 * Gestion complète de la carte Leaflet
 * Gère l'affichage des trajets, marqueurs, lignes courbes et animations
 * Dépendances : Leaflet.js
 */

import { MAP_CONFIG } from "../config.js";
import { convertHHMM } from "../utils/timeUtils.js";

/**
 * Gestionnaire de carte pour l'affichage des trajets
 */
export class MapManager {

    /**
     * Crée une nouvelle instance du gestionnaire de carte
     * @param {string} mapElementId - ID de l'élément HTML qui contiendra la carte
     */
    constructor(mapElementId) {
        // Initialisation de la carte Leaflet
        this.map = L.map(mapElementId).setView(
            MAP_CONFIG.CENTER,
            MAP_CONFIG.ZOOM
        );

        // Ajout de la couche OpenStreetMap
        L.tileLayer(MAP_CONFIG.TILE_LAYER.URL, {
            attribution: MAP_CONFIG.TILE_LAYER.ATTRIBUTION,
            maxZoom: MAP_CONFIG.TILE_LAYER.MAX_ZOOM
        }).addTo(this.map);

        // Stockage des couches actuellement affichées
        this.currentLayers = [];

        console.log("Carte Leaflet initialisée");
    }

    /**
     * Nettoie toutes les couches de la carte
     */
    clearLayers() {
        this.currentLayers.forEach(layer => {
            this.map.removeLayer(layer);
        });
        this.currentLayers = [];
    }

    /**
     * Crée une ligne courbe entre deux points
     * @param {Array} latlng1 - Coordonnées du point de départ [lat, lng]
     * @param {Array} latlng2 - Coordonnées du point d'arrivée [lat, lng]
     * @param {string} color - Couleur de la ligne (hex)
     * @returns {L.Polyline} Polyline Leaflet représentant la courbe
     * @private
     */
    _createCurvedLine(latlng1, latlng2, color) {
        const offsetX = latlng2[1] - latlng1[1];
        const offsetY = latlng2[0] - latlng1[0];

        // Calcul du point de contrôle de la courbe
        const midX = (latlng1[1] + latlng2[1]) / 2;
        const midY = (latlng1[0] + latlng2[0]) / 2;

        // Calcul de la distance
        const distance = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
        const curvature = distance * MAP_CONFIG.CURVE.CURVATURE;

        // Point de contrôle perpendiculaire à la ligne
        const controlX = midX - offsetY * curvature / distance;
        const controlY = midY + offsetX * curvature / distance;

        // Création de points le long de la courbe
        const points = [];
        const numPoints = MAP_CONFIG.CURVE.NUM_POINTS;

        for (let i=0; i <= numPoints; i++) {
            const t = i / numPoints;
            const t1 = 1-t;

            // Formule de la courbe
            const lat = t1 * t1 * latlng1[0] + 2 * t1 * t * controlY + t * t * latlng2[0];
            const lng = t1 * t1 * latlng1[1] + 2 * t1 * t * controlX + t * t * latlng2[1];

            points.push([lat,lng]);
        }

        // Création de la polyline
        return L.polyline(points, {
            color: color,
            weight: 3,
            opacity: 0.8,
            smoothFactor: 1
        });
    }

    /**
     * Crée un marqueur circulaire sur la carte
     * @param {Array} latlng - Coordonnées [lat, lng]
     * @param {Object} style - Style du marqueur
     * @param {string} popupText - Texte du popup (HTML)
     * @returns {L.CircleMarker} Marqueur circulaire
     * @private
     */
    _createMarker(latlng, style, popupText) {
        const marker = L.circleMarker(latlng, style);

        if (popupText) {
            marker.bindPopup(popupText);
        }

        return marker;
    }

    /**
     * Affichage un trajet complet sur la carte avec tous les segments
     * @param {Object} trajet - Objet trajet contenant les segments
     * @param {boolean} highlight - Si true, affiche en rouge (sinon bleu)
     * 
     * @example 
     * mapManager.displayTrip(trajet, false); // Affichage classique (bleu)
     * mapManager.displayTrip(trajet, true);  // Affichage mis en avant (rouge)
     */
    displayTrip(trajet, highlight = false) {
        // Nettoyage des couches précédentes
        this.clearLayers();

        // Choix de la couleur selon le mode highlight
        const lineColor = highlight
            ? MAP_CONFIG.STYLES.LINE_HIGHLIGHT.color
            : MAP_CONFIG.STYLES.LINE_DEFAULT.color;
        
        const allCoordinates = [];

        // Pour chaque segment du trajet
        trajet.segments.forEach((segment, index) => {
            const depCoord = segment.dep_coor;
            const arrCoord = segment.arr_coor;

            allCoordinates.push(depCoord, arrCoord);

            // Création de l'arc courbe entre départ et arrivée
            const curvedLine = this._createCurvedLine(depCoord, arrCoord, lineColor);
            curvedLine.addTo(this.map);
            this.currentLayers.push(curvedLine);

            // Marqueur pour la gare de départ (départ originel)
            if (index === 0) {
                const startMarker = this._createMarker(
                    depCoord,
                    MAP_CONFIG.STYLES.MARKER_START,
                    `<b>Départ</b><br>${segment.from}<br>${convertHHMM(segment.board_time)}`
                );

                startMarker.addTo(this.map);
                this.currentLayers.push(startMarker);
            }

            // Marqueur pour la gare d'arrivée
            const isLastSegment = index === trajet.segments.length -1;
            const markerStyle = isLastSegment
                ? MAP_CONFIG.STYLES.MARKER_END
                : MAP_CONFIG.STYLES.MARKER_CONNECTION;
            
            const markerLabel = isLastSegment ? "Arrivée" : "Correspondance";

            const endMarker = this._createMarker(
                arrCoord,
                markerStyle,
                `<b>${markerLabel}</b><br>${segment.to}<br>${convertHHMM(segment.arrival_time)}`
            );

            endMarker.addTo(this.map);
            this.currentLayers.push(endMarker);
        });
    }

    /**
     * Recentre la carte sur sa position initiale
     */
    resetView() {
        this.map.setView(MAP_CONFIG.CENTER, MAP_CONFIG.ZOOM);
    }

    /**
     * Détruit la carte et libère les ressources
     * Utile pour le nettouage lors du changement de page
     */
    destroy() {
        this.clearLayers();
        this.map.remove();
        console.log('Carte Leaflet détruite');
    }
}