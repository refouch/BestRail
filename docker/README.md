Dossier pour la dockerisation. Docker Desktop est nécessaire. 

# Construire l'image Docker
docker build -t test_app .

# Lancer le container
docker run -p 8080:8000 --name test_app test_app
docker run -p 8080:8000 --name sncf-app sncf-app

# Stoper le container
docker stop test_app

# Arrêter le container
docker rm test_app
