import requests
import zipfile
import io
import os
import shutil


# requeter l'api SNCF pour avoir les datasets en GTFS


url = "https://eu.ftp.opendatasoft.com/sncf/plandata/Export_OpenData_SNCF_GTFS_NewTripId.zip"
dir = "gtfs_sncf"

def download_and_extract_gtfs(url):
    '''Télécharge et extrait les données GTFS '''
    
    try:
        response = requests.get(url)
        response.raise_for_status() 

        # Suppression des anciennes données
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dir)
            
    except Exception as e:
        print(f"Erreur : {e}\n")


if __name__ == "__main__":
    # Création du dossier racine si inexistant
    if not os.path.exists(dir):
        os.makedirs(dir)

    download_and_extract_gtfs(url)


# Mettre à jour les informations de correspondance IDH
URL_IDH = "https://eu.ftp.opendatasoft.com/sncf/prr/temps_correspondance/INFOTRAINS_Export_IDH.zip"

def update_idh_data():
    '''Met à jour les données IDH'''
    try:
        response = requests.get(URL_IDH, timeout=60)
        response.raise_for_status()

        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)


        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(dir)
            
    except Exception as e:
        print(f"Erreur : {e}")

#if __name__ == "__main__":
#    update_idh_data()