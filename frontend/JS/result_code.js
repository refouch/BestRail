// ======================================
// Initialisation de la carte Leaflet
// ======================================

const map = L.map('map_result').setView([46.603354, 1.888334], 5.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map); // Ajout du fond de carte depuis OpenStreetMap


// ======================================
// Affichage des résultats du serveur
// ======================================

// Récupération des données
const searchParams = JSON.parse(sessionStorage.getItem("searchParams"));
const searchResults = JSON.parse(sessionStorage.getItem("searchResults"));

console.log("Recap de la recherche (session storage):", searchParams);
console.log("Résultats du serveur (session storage):", searchResults);

// Récapitulatif de la recherche
if (searchParams) {

    document.querySelector(".ville_depart").textContent = searchParams.depart;
    document.querySelector(".ville_arrivee").textContent = searchParams.arrivee;

    const dateObj = new Date(searchParams.date); // Formatage de la date pour l'afficher correctement
    const dateFormatee = dateObj.toLocaleDateString('fr-FR', { 
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
    });
    document.querySelector(".travel_date").textContent = dateFormatee;
}

// Affichage de la liste des trajets 
if (searchResults && searchResults.trajets) {
    
    const trajetList = document.querySelector(".trajet_list");

    trajetList.innerHTML = "";

    if (searchResults.trajets.length === 0) { 
        // En cas d'absence de trajets
        trajetList.innerHTML = "<p>Aucun trajet trouvé pour cette recherche.</p>";
    } else { 
        // S'il existe au moins un trajet 
        searchResults.trajets.forEach((trajet,index) => {
            
            // Données liées au trajet
            const firstSegment = trajet.segments[0];
            const lastSegment = trajet.segments[trajet.segments.length-1];
            const departureTime = firstSegment.board_time;
            const arrivalTime = lastSegment.arrival_time;
            const duration = arrivalTime - departureTime;
            const nbCorrespondances = trajet.segments.length -1;

            // Type de trajet
            let tripType = "";
            if (nbCorrespondances===0) {
                tripType = "Direct";
            } else if (nbCorrespondances===1) {
                tripType = "1 correspondance";
            } else {
                tripType = `${nbCorrespondances} correspondances`;
            }

            // Création de la card
            const article = document.createElement("article");
            article.className = "trip_card";

            article.innerHTML = `
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
                    ${generateDetailsPanel(trajet)}
                </div>
            `;

            trajetList.appendChild(article);
        });
        console.log(`${searchResults.trajets.length} trajet(s) affiché(s)`);
    }
} else {
    console.warn("Aucune donnée trouvée dans sessionStorage");
    document.querySelector(".trajet_list").innerHTML =
        "<p>Aucun résultat. Veuillez effectuer une nouvelle recherche.</p>"; 
}


// Fonction pour générer le panneau de détails d'une card
function generateDetailsPanel(trajet) {

    // Trajet direct
    if (trajet.segments.length===1) {
        const segment = trajet.segments[0];
        const duration = segment.arrival_time - segment.board_time;

        return `
            <div class="direct_info">
                <p><strong>Train :</strong> ${segment.trip}</p>
                <p><strong>Durée :</strong> ${convertDuration(duration)}</p>
            </div>
        `;
    }

    // Trajet avec au moins 1 correspondance
    let html = "<div class='segments_container'>";

    trajet.segments.forEach((segment,index) => {
        const segmentDuration = segment.arrival_time - segment.board_time;

        // Affichage du segment
        html += `
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

        // Affichage de la correspondance (entre deux segments)
        if (index < trajet.segments.length -1) {
            const nextSegment = trajet.segments[index +1];
            const waitingTime = nextSegment.board_time - segment.arrival_time;

            html += `
                <div class="connection_info">
                    <span class="connection_icon">⏱️</span>
                    <p>Correspondance à ${segment.to} - Temps d'attente : ${convertDuration(waitingTime)}</p>
                </div>
            `;
        }
    });

    html += '</div>';
    return html;
}


// ======================================
// Modification de la recherche 
// ======================================

const modifyBtn = document.getElementById('modifyBtn');
let isEditing = false;

modifyBtn.addEventListener('click', function() {

    if (!isEditing) {
        // Mode édition
        const recapItems = document.querySelectorAll('.recap_item span');

        recapItems.forEach(span => {
            const currentValue = span.textContent;
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentValue;
            input.className = 'recap_input';

            span.replaceWith(input);
        });

        modifyBtn.textContent = 'Valider';
        modifyBtn.classList.add('validate_mode');
        isEditing = true;

    } else {
        // Mode validation
        const inputs = document.querySelectorAll('.recap_input');
        
        inputs.forEach(input => {
            const newValue = input.value;
            const span = document.createElement('span');
            span.textContent = newValue;

            input.replaceWith(span);
        });

        modifyBtn.textContent = 'Modifier la recherche';
        modifyBtn.classList.remove('validate_mode');
        isEditing = false;

        // Relance de la recherche
        

    }
});


// ======================================
// Gestion des panneaux déroulants
// ======================================

function toggleDetails(button) {
    const card = button.closest('.trip_card');
    const panel = card.querySelector('.trip_details_panel');

    const isOpen = panel.classList.contains('open');

    if (isOpen) {
        panel.classList.remove('open');
        button.classList.remove('active');
        button.textContent = 'Voir les détails';
    } else {
        panel.classList.add('open');
        button.classList.add('active');
        button.textContent = 'Masquer les détails';
    }
}


// ======================================
// Conversion du format de l'heure
// ======================================

function convertHHMM(totalMinutes) {
    const hours = Math.floor(totalMinutes/60);
    const minutes = totalMinutes % 60

    const hh = String(hours).padStart(2,'0');
    const mm = String(minutes).padStart(2,'0');

    return `${hh}:${mm}`;
}

function convertDuration(duration) {
    const hours = Math.floor(duration/60);
    const minutes = duration % 60;

    if (hours === 0) {
        return `${minutes} min`;
    }
    return `${hours}h${String(minutes).padStart(2,'0')}`;
}