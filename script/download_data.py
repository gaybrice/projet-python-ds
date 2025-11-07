import requests
import zipfile
import io
import os

URL_LIST = [
        "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326",
        "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip"
    ]


# Télécharge des fichiers ZIP depuis les URL url_list et les extrait  
def download_unzip(url_list=URL_LIST, dossier_temp="cache", force_download=False):
    if os.path.isdir(dossier_temp) and not force_download:
        print(print("Dossier cache trouvé, pas de téléchargement."))
    else:
        os.makedirs(dossier_temp, exist_ok=True)
        for url in url_list:
            print(f"Téléchargement depuis {url}")
            # Téléchargement en flux pour éviter de surcharger la mémoire
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                # On lit directement le contenu dans un buffer mémoire
                file_like_object = io.BytesIO(r.content)
            print("Terminé")
        print("Extraction des ZIP")
        with zipfile.ZipFile(file_like_object) as zip_ref:
            zip_ref.extractall(dossier_temp)
        print("Extraction terminée")

    return [os.path.join(dossier_temp, f) 
            for f in os.listdir(dossier_temp)
            if f.lower().endswith(('.txt', '.csv'))]

if __name__ == "__main__":
    file_list = download_unzip(URL_LIST, dossier_temp="cache", force_download=False)