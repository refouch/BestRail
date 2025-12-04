


// Initialiser la carte centrée sur la France
const map = L.map('map_result').setView([46.603354, 1.888334], 5.5);

// Ajouter le fond de carte (tiles) depuis OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
}).addTo(map);