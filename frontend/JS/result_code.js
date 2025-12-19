// ======================================
// Initialisation de la carte Leaflet
// ======================================

const map = L.map('map_result').setView([46.603354, 1.888334], 5.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map); // Ajout du fond de carte depuis OpenStreetMap

// Stockage des couches de la carte
let currentMapLayers = [];

// fonction pour nettoyer les layers de la carte
function clearMapLayers() {
    currentMapLayers.forEach(layer => {
        map.removeLayer(layer);
    });
    currentMapLayers = [];
}

// Fonction pour créer un arc courbe entre deux points
function createCurvedLine(latlng1, latlng2, color = '#2563eb') {
    const offsetX = latlng2[1] - latlng1[1];
    const offsetY = latlng2[0] - latlng1[0];
    
    // Calcul du point de contrôle pour la courbe (point milieu décalé perpendiculairement)
    const midX = (latlng1[1] + latlng2[1]) / 2;
    const midY = (latlng1[0] + latlng2[0]) / 2;
    
    // Calcul de la distance pour ajuster la courbure
    const distance = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
    const curvature = distance * 0.2; // 20% de la distance pour la courbure
    
    // Point de contrôle perpendiculaire à la ligne
    const controlX = midX - offsetY * curvature / distance;
    const controlY = midY + offsetX * curvature / distance;
    
    // Création de points le long de la courbe de Bézier quadratique
    const points = [];
    const numPoints = 50; // Nombre de points pour lisser la courbe
    
    for (let i = 0; i <= numPoints; i++) {
        const t = i / numPoints;
        const t1 = 1 - t;
        
        // Formule de courbe de Bézier quadratique
        const lat = t1 * t1 * latlng1[0] + 2 * t1 * t * controlY + t * t * latlng2[0];
        const lng = t1 * t1 * latlng1[1] + 2 * t1 * t * controlX + t * t * latlng2[1];
        
        points.push([lat, lng]);
    }
    
    // Création de la polyligne avec animation
    const polyline = L.polyline(points, {
        color: color,
        weight: 3,
        opacity: 0.8,
        smoothFactor: 1
    });
    
    return polyline;
}

// Fonction pour afficher un trajet sur la carte
function displayTripOnMap(trajet, highlight = false) {

    // Nettoyage des couches précédentes
    clearMapLayers();

    const color = highlight ? '#dc2626' : '#2563eb';
    const allCoordinates = [];

    // Pour chaque segment du trajet
    trajet.segments.forEach((segment,index) => {
        const depCoord = segment.dep_coor;
        const arrCoord = segment.arr_coor;

        allCoordinates.push(depCoord,arrCoord);

        // Création de l'arc courbe entre départ et arrivée
        const curvedLine = createCurvedLine(depCoord,arrCoord, color);
        curvedLine.addTo(map);
        currentMapLayers.push(curvedLine);

        // Marqueur pour la gare de départ
        if (index === 0) {
            const startMarker = L.circleMarker(depCoord, {
                radius: 8,
                fillColor: '#10b981',
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.9
            }).bindPopup(`<b>Départ</b><br>${segment.from}<br>${convertHHMM(segment.board_time)}`);
            
            startMarker.addTo(map);
            currentMapLayers.push(startMarker);
        }

        // Marqueur pour la gare d'arrivée
        const isLastSegment = index === trajet.segments.length - 1;
        const markerColor = isLastSegment ? '#dc2626' : '#f59e0b';

        const endMarker = L.circleMarker(arrCoord, {
            radius: isLastSegment ? 8 : 6,
            fillColor: markerColor,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }).bindPopup(`<b>${isLastSegment ? 'Arrivée' : 'Correspondance'}</b><br>${segment.to}<br>${convertHHMM(segment.arrival_time)}`);
        
        endMarker.addTo(map);
        currentMapLayers.push(endMarker);
    });

    // Ajustement de la vue pour afficher tout le trajet
    if (allCoordinates.length > 0) {
        const bounds = L.latLngBounds(allCoordinates);
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}


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

            // Evenement de survol : affichage sur la carte
            article.addEventListener('mouseenter',function() {
                displayTripOnMap(trajet, false);
            });
            article.addEventListener('mouseleave', function() {
                const detailsBtn = article.querySelector('.details_btn');
                if (!detailsBtn.classList.contains('active')) {
                    clearMapLayers();
                }
            });
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
        // ========== Mode Édition ==========

        // Récupération des informations à modifier
        const villeDepart = document.querySelector('.ville_depart');
        const villeArrivee = document.querySelector('.ville_arrivee');
        const travelDate = document.querySelector('.travel_date');
        
        // Conversion de la date au format datetime-local (format pour la recherche)
        const dateObj = new Date(searchParams.date);
        const datetimeValue = dateObj.toISOString().slice(0,16);

        // Remplacement des inputs
        villeDepart.innerHTML = `<input type="text" class="recap_input" id="edit_depart" value="${searchParams.depart}" required>`;
        villeArrivee.innerHTML = `<input type="text" class="recap_input" id="edit_arrivee" value="${searchParams.arrivee}" required>`;
        travelDate.innerHTML = `<input type="datetime-local" class="recap_input" id="edit_datetime" value="${datetimeValue}" required>`;

        modifyBtn.textContent = 'Valider';
        modifyBtn.classList.add('validate_mode');
        isEditing = true;

    } else {
        // ========== Mode Validation ==========

        // Récupération des nouvelles valeurs
        const newDepart = document.getElementById('edit_depart').value.trim();
        const newArrivee = document.getElementById('edit_arrivee').value.trim();
        const newDatetime = document.getElementById('edit_datetime').value;

        // Validation des champs
        if (!newDepart || !newArrivee || !newDatetime) {
            alert('Veuillez remplir tous les champs.');
            return;
        }

        // Préparation du payload pour le serveur
        const payload = {
            depart: newDepart,
            arrivee: newArrivee,
            date: newDatetime
        };

        console.log("Nouvelle recherche avec :", payload);

        // Indicateur de chargement
        modifyBtn.textContent = 'Recherche en cours...';
        modifyBtn.disabled = true;

        // Envoi de la requête au serveur
        fetch("http://localhost:8000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })

        // Gestion de la réponse
        .then(response => {
            console.log("Statut de la réponse:", response.status);
            console.log("Réponse OK?", response.ok);
            return response.json();
        })

        // Traitement des résultats
        .then(data => {
            console.log("Réponse du serveur:", data);

            // Mise à jour du sessionStorage
            sessionStorage.setItem("searchParams", JSON.stringify(payload));
            sessionStorage.setItem("searchResults", JSON.stringify(data));
            
            // Rechargement de la page avec les nouveaux résultats
            window.location.reload();
        })

        // Gestion des erreurs
        .catch(error => {
            console.error("Erreur lors de la requête:", error);
            console.error("Message d'erreur:", error.message);

            // Restauration du bouton de recherche
            modifyBtn.textContent = 'Valider';
            modifyBtn.disabled = false;

            // Message d'erreur à l'utilisateur
            alert("Une erreur s'est produite lors de la recherche. Veuillez réessayer.");
        });
    }
});


// ======================================
// Gestion des panneaux déroulants
// ======================================

function toggleDetails(button) {
    const card = button.closest('.trip_card');
    const panel = card.querySelector('.trip_details_panel');
    const isOpen = panel.classList.contains('open');

    // Récupération de l'index du trajet
    const allCards = document.querySelectorAll('trip_card');
    const cardIndex = Array.from(allCards).indexOf(card);

    if (isOpen) {
        // Fermeture du panneau
        panel.classList.remove('open');
        button.classList.remove('active');
        button.textContent = 'Voir les détails';

        // Nettoyage de la carte
        clearMapLayers();
    } else {
        // Fermeture de tous les autres panneaux
        document.querySelectorAll('.trip_details_panel.open').forEach(p => {
            p.classList.remove('open');
        });
        document.querySelectorAll('.details_btn.active').forEach(b => {
            b.classList.remove('active');
            b.textContent = 'Voir les détails';
        });

        // Ouverture du panneau actuel
        panel.classList.add('open');
        button.classList.add('active');
        button.textContent = 'Masquer les détails';

        // Affichage du trajet sur la carte
        if (searchResults && searchResults.trajets && searchResults.trajets[cardIndex]) {
            displayTripOnMap(searchResults.trajets[cardIndex], true);
        }
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