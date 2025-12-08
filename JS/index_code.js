// CODE JAVASCRIPT PAGE INDEX


// ===================================
// Formulaire de recherche
// ===================================

const formulaire = document.getElementById("search-form");

formulaire.addEventListener("submit", function(event) {
    event.preventDefault(); // pour empêcher le rechargement automatique de la page

    // Récupération des données du formulaire
    const depart_js = document.getElementById("depart").value;
    const arrivee_js = document.getElementById("arrivee").value;
    const datetime_js = document.getElementById("datetime").value;

    console.log("Données du formulaire :", {
        depart: depart_js,
        arrivee: arrivee_js,
        date: datetime_js
    });

    // Préparation de l'envoi vers le serveur
    const payload = { // Modifier à gauche pour fit avec les noms du serveur
        depart: depart_js,
        arrivee: arrivee_js,
        date: datetime_js
    };

    // Affichage d'un indicateur de chargement
    const boutonRecherche = formulaire.querySelector('button[type="submit"]');
    const textOriginal = boutonRecherche.textContent;
    boutonRecherche.textContent = "Recherche en cours...";
    boutonRecherche.disabled = true;

    // Envoi de la requête au serveur
    /*
    fetch("http://localhost:8000/api/recherche", {
        // Modifier l'URL pour tomber sur le bon endpoint
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })

    .then(response => response.json()) //conversion JSON de la réponse
    .then(data => {
        console.log("Réponse du serveur: ", data);
        // on rajouteras ici la suite des instructions à faire
    })
    .catch(error => {
        console.error("Erreur lors de la requête:", error);
    });
    */
   console.log("✅ Si vous voyez ce message, votre code fonctionne !");
});


// 

