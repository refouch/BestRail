import requests
import zipfile
import io
import os
import shutil


# requeter l'api SNCF pour avoir les datasets en GTFS

SOURCES = {
    "SNCF_NATIONAL": "https://eu.ftp.opendatasoft.com/sncf/plandata/Export_OpenData_SNCF_GTFS_NewTripId.zip",
    "TRANSILIEN": "https://eu.ftp.opendatasoft.com/sncf/gtfs/transilien-gtfs.zip"
}

dir = "donnees_gtfs"

def download_and_extract_gtfs(name, url):
    '''Télécharge et extrait les données GTFS '''
    path = os.path.join(dir, name)

    try:
        response = requests.get(url)
        response.raise_for_status() 

        # Suppression des anciennes données
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(path)
            
    except Exception as e:
        print(f"Erreur lors du traitement de {name} : {e}\n")


if __name__ == "__main__":
    # Création du dossier racine si inexistant
    if not os.path.exists(dir):
        os.makedirs(dir)

    for name, url in SOURCES.items():
        download_and_extract_gtfs(name, url)


# Mettre à jour les informations de correspondance IDH
URL_IDH = "https://eu.ftp.opendatasoft.com/sncf/prr/temps_correspondance/INFOTRAINS_Export_IDH.zip"
dir_idh = "donnees_idh"

def update_idh_data():
    '''Met à jour les données IDH'''
    try:
        response = requests.get(URL_IDH, timeout=60)
        response.raise_for_status()

        if os.path.exists(dir_idh):
            shutil.rmtree(dir_idh)
        os.makedirs(dir_idh)


        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dir_idh)
            
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    update_idh_data()