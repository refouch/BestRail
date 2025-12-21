
// ===================================
// Formulaire de recherche
// ===================================

const formulaire = document.getElementById("search-form");

formulaire.addEventListener("submit", function(event) {
    // pour empêcher le rechargement automatique de la page
    event.preventDefault(); 

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

    console.log("Payload:", payload)
    console.log("Payload en JSON;", JSON.stringify(payload))

    // Affichage d'un indicateur de chargement
    const boutonRecherche = formulaire.querySelector('button[type="submit"]');
    const textOriginal = boutonRecherche.textContent;
    boutonRecherche.textContent = "Recherche en cours...";
    boutonRecherche.disabled = true;

    // Envoi de la requête au serveur
    console.log("Envoi de la requête vers le serveur...")

    fetch("/search", {
        // Modifier l'URL pour tomber sur le bon endpoint
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
        console.log("Réponse du serveur: ", data);

        sessionStorage.setItem("searchParams", JSON.stringify(payload));
        sessionStorage.setItem("searchResults", JSON.stringify(data));

        window.location.href = "/result";

        // voir les autres instruction à rajouter quand on obtient les résultats
    })

    // Gestion des erreurs
    .catch(error => {
        console.error("Erreur lors de la requête:", error);
        console.error("Message d'erreur:", error.message);

        // Restauration du bouton de recherche
        boutonRecherche.textContent = textOriginal;
        boutonRecherche.disabled = false;

        // Message d'erreur à l'utilisateur
        alert("Une erreur s'est produite lors de la recherche. Veuillez réessayer.");
    });

});


// 




console.log("Script index_code.js chargé !");