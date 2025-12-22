import requests
import zipfile
import io
import os
import shutil

URL_LIST = [
        "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326",
        "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip"
    ]


def get_valeur_fonciere_path(force_download=False):
    url = "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326"
    return download_unzip([url], "cache/valeur_fonciere", force_download)[0]

def get_IDFM_data_path(force_download=False):
    url = "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip"
    list_files = download_unzip([url], "cache/idfm", force_download)

    # renome les txt en csv (plus simple pour ouvrir dans d'autres outils)
    for idx, f in enumerate(list_files):
        root, ext = os.path.splitext(f)
        if ext.lower() == ".txt":
            new_f = root + ".csv"
            try:
                os.replace(f, new_f)
            except OSError:
                shutil.copyfile(f, new_f)
                os.remove(f)
            list_files[idx] = new_f
        
    return {os.path.splitext(os.path.basename(f))[0]: f for f in list_files}

def get_valeur_fonciere(force_download=False):
    url = "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326"
    return download_unzip([url], "cache/valeur_fonciere", force_download)

# Télécharge des fichiers ZIP depuis les URL url_list et les extrait  
def download_unzip(url_list=URL_LIST, dossier_temp="cache", force_download=False):
    if os.path.isdir(dossier_temp) and not force_download:
        print("Utilisation des données en cache dans", dossier_temp)
    else:
        os.makedirs(dossier_temp, exist_ok=True)
        for url in url_list:
            print(f"Téléchargement depuis {url}")
            # Téléchargement en flux pour éviter de surcharger la mémoire
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                # On lit directement le contenu dans un buffer mémoire
                file_like_object = io.BytesIO(r.content)
        print("Extraction des ZIP")
        with zipfile.ZipFile(file_like_object) as zip_ref:
            zip_ref.extractall(dossier_temp)
        print("Extraction terminée")

    return [os.path.join(dossier_temp, f) 
            for f in os.listdir(dossier_temp)
            if f.lower().endswith(('.txt', '.csv'))]

if __name__ == "__main__":
    get_valeur_fonciere_path()
    get_IDFM_data_path()