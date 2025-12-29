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
            <article class="trip-card" data-trip-index="${index}">
                <div class="trip-main-info">
                    <div class="trip-time-station">
                        <div class="trip-line">
                            <span class="card-time">${convertHHMM(departureTime)}</span>
                            <span class="card-station">${trajet.departure_stop}</span>
                        </div>
                        <div class="trip-line">
                            <span class="card-time">${convertHHMM(arrivalTime)}</span>
                            <span class="card-station">${trajet.arrival_stop}</span>
                        </div>
                    </div>
                    <div class="trip-duration">
                        ${convertDuration(duration)}
                    </div>
                </div>

                <div class="trip-footer">
                    <span class="trip-type">${tripType}</span>
                    <button class="details-btn" onclick="toggleDetails(this)">
                        Voir les détails
                    </button>
                </div>

                <div class="trip-details-panel">
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
     * Génère le panneau de détails d'un trajet
     * @param {Object} trajet - Objet trajet avec segments
     * @returns {string} HTML du panneau de détails
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
     * Génère les détails pour un trajet direct
     * @param {Object} segment - Segment unique du trajet
     * @returns {string} HTML des détails du trajet direct
     * @private
     */
    _generateDirectTripDetails(segment) {
        return `<div class="timeline">${this._generateSegmentHTML(segment,0,1)}</div>`;
    },

    /**
     * Génère les détails pour un trajet avec correspondances
     * @param {Array} segments - Tableau des segments du trajet
     * @returns {string} HTML des segments et correspondances
     * @private
     */
    _generateMultiSegmentDetails(segments) {
        let html = "<div class='timeline'>";

        segments.forEach((segment,index) => {
            // Affichage du segment
            html += this._generateSegmentHTML(segment, index, segments.length);

            // Affichage de la correspondance
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
     * @param {number} index - Index du segment dans la liste
     * @param {number} totalSegments - Nombre total de segments
     * @returns {string} HTML du segment
     * @private
     */
    _generateSegmentHTML(segment, index, totalSegments) {
        const isFirst = (index === 0);
        const isLast = (index === totalSegments -1);
        const segmentDuration = segment.arrival_time - segment.board_time;

        // CLasse du premier point
        const startPointClass = isFirst ? "timeline-point start" : "timeline-point";
        // Classe du dernier point
        const endPointClass = isLast ? "timeline-point end" : "timeline-point";

        return `
            <div class="timeline-segment">
                <div class="timeline-column">
                    <div class="segment-vertical-line"></div>
                    <div class="${startPointClass}"></div>
                    <div style="flex: 1;"></div>
                    <div class="${endPointClass}"></div>
                </div>
                <div class="timeline-content">
                    <div class="segment-card">
                        <div class="segment-info">
                            <span class="segment-time">${convertHHMM(segment.board_time)}</span>
                            <span class="segment-station">${segment.from}</span>
                        </div>
                    </div>
                
                    <div class="segment-trip">
                        <div class="segment-meta">
                            <strong>${segment.trip}</strong> · ${convertDuration(segmentDuration)}
                        </div>
                    </div>
                
                    <div class="segment-card">
                        <div class="segment-info">
                            <span class="segment-time">${convertHHMM(segment.arrival_time)}</span>
                            <span class="segment-station">${segment.to}</span>
                        </div>
                    </div>
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
        const waitingTime = nextSegment.board_time - currentSegment.arrival_time;

        return `
            <div class="timeline-connection">
                <div class="connection-column">
                    <div class="connection-line"></div>
                </div>
                <div class="connection-content-wrapper">
                    <div class="connection-content">
                        Correspondance à ${currentSegment.to} - <strong>${convertDuration(waitingTime)}</strong>
                    </div>
                </div>
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

