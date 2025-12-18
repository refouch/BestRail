// ======================================
// Initialisation de la carte Leaflet
// ======================================

const map = L.map('map_result').setView([46.603354, 1.888334], 5.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map); // Ajout du fond de carte depuis OpenStreetMap



// ======================================
// Recherche
// ======================================


// Récupération des données
const searchParams = JSON.parse(sessionStorage.getItem("searchParams"));
const searchResults = JSON.parse(sessionStorage.getItem("searchResults"));

console.log("Recap de la recherche (session storage):", searchParams);
console.log("Résultats du serveur (session storage):", searchResults);


// Modification du récapitulatif de recherche
if (searchParams) {

    document.querySelector(".ville_depart").textContent = searchParams.depart;
    document.querySelector(".ville_arrivee").textContent = searchParams.arrivee;

    // Formatage de la date pour l'afficher correctement
    const dateObj = new Date(searchParams.date);
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

// Nouvelle fonction pour l'affichage des résultats du serveur
if (searchResults && searchResults.trajets) {
    
    const trajetList = document.querySelector(".trajet_list");

    trajetList.innerHTML = "";

    if (searchResults.trajets.length === 0) {
        trajetList.innerHTML = "<p>Aucun trajet trouvé pour cette recherche.</p>";
    } else {
        
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
                <div class="trip_route">
                    <span class="departure_station">${trajet.departure_stop}</span>
                    <span class="arrow">→</span>
                    <span class="arrival_station">${trajet.arrival_stop}</span>
                </div>

                <div class="trip_header">
                    <span class="departure_time">${departureTime}</span>
                    <span class="duration">${duration} unités</span>
                    <span class="arrival_time">${arrivalTime}</span>
                </div>

                <div class="trip_type">
                    <p>${tripType}</p>
                </div>

                <button class="details_btn" onclick="toggleDetails(this)">Voir les détails</button>

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
                <p><strong>Durée :</strong> ${duration} unités</p>
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
                    <p><strong>Départ :</strong> ${segment.board_time}</p>
                    <p><strong>Arrivée :</strong> ${segment.arrival_time}</p>
                    <p><strong>Durée :</strong> ${segmentDuration} unités</p>
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
                    <p>Correspondance à ${segment.to} - Temps d'attente : ${waitingTime} unités</p>
                </div>
            `;
        }
    });

    html += '</div>';
    return html;
}




// Bouton pour modifier la recherche

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

        // Ajouter la relance de la recherche

    }
});


// ======================================
// Gestion des panneaux déroulants
// ======================================

function toggleDetails(button) {
    const panel = button.nextElementSibling;
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