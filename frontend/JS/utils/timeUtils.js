/**
 * timeUtils.js
 * Utilitaires pour le formatage et la conversion du temps
 * Fonctions réutilisables dans toute l'application
 */

/**
 * Convertit un nombre de minutes total en format HH:MM
 * @param {number} totalMinutes - Nombre total de minutes
 * @returns {string} Heure au format HH:MM (ex: "14:30")
 * 
 * @example
 * convertHHMM(630) // retourne "10:30"
 * convertHHMM(65)  // retourne "01:05"
 */
export function convertHHMM(totalMinutes) {
    const hours = Math.floor(totalMinutes/60);
    const minutes = totalMinutes %60;

    const hh = String(hours).padStart(2,'0');
    const mm = String(minutes).padStart(2,'0');

    return `${hh}:${mm}`;
}

/**
 * Convertir une durée en minutes en un format lisible (ex: "6h30" ou "45min")
 * @param {number} duration - Durée en minutes
 * @returns {string} Durée formatée
 * 
 * @example
 * convertDuration(150) // retourne "2h30"
 * convertDuration(45)  // retourne "45min"
 * convertDuration(120) // retourne "2h00"
 */
export function convertDuration(duration) {
    const hours = Math.floor(duration/60);
    const minutes = duration %60;

    if (hours === 0) {
        return `${minutes} min`;
    }
    return `${hours}h${String(minutes).padStart(2,'0')}`;
}