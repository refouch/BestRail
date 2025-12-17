
// Initialiser la carte centrée sur la France
const map = L.map('map_result').setView([46.603354, 1.888334], 5.5);

// Ajouter le fond de carte (tiles) depuis OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map);


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

// Affichage des résultats reçus du serveur

if (searchResults && searchResults.trajets) {
    
    const trajetList = document.querySelector(".trajet_list");

    trajetList.innerHTML = ""; 

    if (searchResults.trajets.length === 0) {
        trajetList.innerHTML = "<p>Aucun trajet trouvé pour cette recherche.</p>";
    } else {
        searchResults.trajets.forEach((trajet,index) => {
            const article = document.createElement("article");
            article.className = "trip_card";

            article.innerHTML = `
                <div class="trip_route">
                    <span class="departure_station">${trajet.depart}</span>
                    <span class="arrow">→</span>
                    <span class="arrival_station">${trajet.arrivee}</span>
                </div>
                <div class="trip_header">
                    <span class="departure_time">${trajet.heure_depart}</span>
                    <span class="duration">${trajet.duree}</span>
                    <span class="arrival_time">${trajet.heure_arrivee}</span>
                </div>
                <div class="trip_details">
                    <p class="train_type">${trajet.train_type}</p>
                    <p class="connections">${trajet.correspondances}</p>
                </div>
                <div class="trip_footer">
                    <span class="price">${trajet.prix}€</span>
                    <button class="select_trip_btn" data-trajet-index= ${index}>Sélectionner</button>
                </div>`;

            trajetList.appendChild(article);
        });

    console.log(`${searchResults.trajets.length} trajet(s) affiché(s)`);

    }
} else {
    console.warn("Aucune donnée trouvée dans sessionStorage");
    document.querySelector(".trajet_list").innerHTML =
        "<p>Aucun résultat. Veuillez effectuer une nouvelle recherche.</p>";   
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