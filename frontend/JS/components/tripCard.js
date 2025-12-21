/**
 * tripCard.js
 * Génération des cartes des cartes de trajets (trip cards)
 * Gère l'affichage des informations de trajet et des panneaux de détails
 */

import { convertHHMM, convertDuration } from "../utils/timeUtils.js";
import { MESSAGES } from "../config.js";

/**
 * Générateur de cartes HTML pour les trajets
 */

export const TripCardGenerator = {

    /**
     * Génère le HTML complet d'une carte de trajet
     * @param {Object} trajet - Objet trajet avec segments, horaires, etc...
     * @param {number} index - Index du trajet dans la liste (pour identification)
     * @returns {string} HTML de la carte complète
     * 
     * @example
     * const html = TripCardGenerator.generateCard(trajet, 0);
     * container.innerHTML += html;
     */
    generateCard(trajet, index) {
        // Données liées au trajet
        const firstSegment = trajet.segments[0];
        const lastSegment = trajet.segments[trajet.segments.length -1];
        const departureTime = firstSegment.board_time;
        const arrivalTime = lastSegment.arrival_time;
        const duration = arrivalTime - departureTime;
        const nbCorrespondances = trajet.segments.length -1;

        // Type de trajet (Direct, 1 correspondance, X correspondances)
        const tripType = this._getTripType(nbCorrespondances);

        return `
            <article class="trip_card" data-trip-index="${index}">
                <div class="trip_main_info">
                    <div class="trip_time_station">
                        <div class="trip_line">
                            <span class="card_time">${convertHHMM(departureTime)}</span>
                            <span class="card_station">${trajet.departure_stop}</span>
                        </div>
                        <div class="trip_line">
                            <span class="card_time">${convertHHMM(arrivalTime)}</span>
                            <span class="card_station">${trajet.arrival_stop}</span>
                        </div>
                    </div>
                    <div class="trip_duration">
                        ${convertDuration(duration)}
                    </div>
                </div>

                <div class="trip_footer">
                    <span class="trip_type">${tripType}</span>
                    <button class="details_btn" onclick="toggleDetails(this)">
                        Voir les détails
                    </button>
                </div>

                <div class="trip_details_panel">
                    ${this.generateDetailsPanel(trajet)}
                </div>
            </article>
        `;
    },

    /**
     * Détermine le texte du type de trajet selon le nombre de correspondances
     * @param {number} nbCorrespondances - Nombre de correspondances
     * @returns {string} Texte descriptif (ex: "Direct", "1 correspondance")
     * @private
     */
    _getTripType(nbCorrespondances) {
        if (nbCorrespondances === 0) {
            return "Direct";
        } else if (nbCorrespondances === 1) {
            return "1 correspondance";
        } else {
            return `${nbCorrespondances} correspondances`;
        }
    },

    /**
     * Génère le panneau de détails d'un trajet (segments + correspondances)
     * @param {Object} trajet - Objet trajet avec segments
     * @returns {string} HTML du panneau de détails
     * 
     * @example
     * const detailsHTML = TripCardGenerator.generateDetailsPanel(trajet);
     */
    generateDetailsPanel(trajet) {
        // Trajet direct (1 segment)
        if (trajet.segments.length === 1) {
            return this._generateDirectTripDetails(trajet.segments[0]);
        }

        // Trajet avec au moins 1 correspondance
        return this._generateMultiSegmentDetails(trajet.segments);
    },

    /**
     * Génère les détails pour un trajet direct (sans correspondances)
     * @param {Object} segment - Segment unique du trajet
     * @returns {string} HTML des détails du trajet direct
     * @private 
     */
    _generateDirectTripDetails(segment) {
        const duration = segment.arrival_time - segment.board_time;

        return `
            <div class="direct_info">
                <p><strong>Train :</strong> ${segment.trip}</p>
                <p><strong>Durée :</strong> ${convertDuration(duration)}</p>
            </div>
        `;
    },

    /**
     * Génère les détails pour un trajet avec correspondances
     * @param {Array} segments - Tableau des segments du trajet
     * @returns {string} HTML des segments et correspondances
     * @private
     */
    _generateMultiSegmentDetails(segments) {
        let html = "<div class='segments_container'>";

        segments.forEach((segment,index) =>{
            // Affichage du segment
            html += this._generateSegmentHTML(segment);

            // Affichage de la correspondance entre deux segments
            if (index < segments.length -1) {
                const nextSegment = segments[index +1];
                html += this._generateConnectionHTML(segment, nextSegment);
            }
        });

        html += "</div>";
        return html;
    },

    /**
     * Génère le HTML d'un segment individuel
     * @param {Object} segment - Segment avec infos sur le train, les horaires, les gares
     * @returns {string} HTML du segment
     * @private
     */
    _generateSegmentHTML(segment) {
        const segmentDuration = segment.arrival_time - segment.board_time;
        
        return `
            <div class="segment_item">
                <div class="segment_header">🚄 Train ${segment.trip}</div>
                <div class="segment_info">
                    <div class="segment_route">
                        <span>${segment.from}</span>
                        <span class="arrow_small">→</span>
                        <span>${segment.to}</span>
                    </div>
                    <p><strong>Départ :</strong> ${convertHHMM(segment.board_time)}</p>
                    <p><strong>Arrivée :</strong> ${convertHHMM(segment.arrival_time)}</p>
                    <p><strong>Durée :</strong> ${convertDuration(segmentDuration)}</p>
                </div>
            </div>
        `; 
    },

    /**
     * Génère le HTML d'une correspondance entre deux segments
     * @param {Object} currentSegment - Segment actuel
     * @param {Object} nextSegment - Segment suivant
     * @returns {string} HTML de la correspondance
     * @private
     */
    _generateConnectionHTML(currentSegment, nextSegment) {
        const waitingTime = nextSegment.board_time - currentSegment.arrivalTime;

        return `
            <div class="connection_info">
                <span class="connection_icon">⏱️</span>
                <p>Correspondance à ${currentSegment.to} - Temps d'attente : ${convertDuration(waitingTime)}</p>
            </div>
        `;
    },

    /**
     * Génère toutes les cartes pour une liste de trajets
     * @param {Array} trajets - Tableau d'objets trajet
     * @returns {string} HTML de toutes les cartes concaténées
     * 
     * @example
     * const allCardsHTML = TripCardGenerator.generateAllCards(results.trajets);
     * container.innerHTML = allCardsHTML;
     */
    generateAllCards(trajets) {
        if (!trajets || trajets.length === 0) {
            return `<p>${MESSAGES.NO_RESULTS}</p>`
        }

        return trajets.map((trajet,index) =>
            this.generateCard(trajet, index)
        ).join('');
    }
};

