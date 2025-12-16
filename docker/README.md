Dossier pour la dockerisation. Docker Desktop est nécessaire. 

# Construire l'image Docker
docker build -t test_app .

# Lancer le container
docker run --rm test_app
