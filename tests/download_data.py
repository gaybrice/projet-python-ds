import requests
import zipfile
import io
# import pandas as pd
import os

def download_unzip(url, dossier_temp="cache", fichier_cible="ValeursFoncieres-2024.txt"):
    """
    Télécharge un fichier ZIP depuis une URL, extrait le CSV et le charge avec pandas.
    
    :param url: URL du fichier ZIP
    :param dossier_temp: Dossier temporaire pour l’extraction
    :return: DataFrame pandas
    """

    os.makedirs(dossier_temp, exist_ok=True)
    print("Téléchargement du fichier ZIP...")

    # Vérifier si un fichier CSV/TXT est déjà présent dans le cache
    fichiers_caches = [f for f in os.listdir(dossier_temp) if f.lower().endswith(('.txt', '.csv', '.zip'))]
    
    if not fichier_cible in fichiers_caches:
        print(f"{fichier_cible} non trouvé, téléchargement depuis {url}")
        # Téléchargement en flux pour éviter de surcharger la mémoire
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            # On lit directement le contenu dans un buffer mémoire
            file_like_object = io.BytesIO(r.content)
        
        print("Extraction du ZIP...")
        with zipfile.ZipFile(file_like_object) as zip_ref:
            zip_ref.extractall(dossier_temp)
        print("Extraction terminée")
    else:
        print("Utilisation du cache")

    return os.path.join(dossier_temp, fichier_cible)

def afficher_premieres_lignes_txt(chemin_fichier, nb_lignes=10):
    """
    Affiche les premières lignes d’un fichier texte sans le charger entièrement.
    """
    print(f"\n--- Premières {nb_lignes} lignes du fichier texte ---")
    with open(chemin_fichier, "r", encoding="utf-8", errors="ignore") as f:
        for i in range(nb_lignes):
            ligne = f.readline()
            if not ligne:
                break
            print(ligne.strip())
    print("--- Fin de l’aperçu ---\n")



if __name__ == "__main__":
    url_zip = "https://www.data.gouv.fr/api/1/datasets/r/af812b0e-a898-4226-8cc8-5a570b257326" 
    file_path = download_unzip(url_zip)

    url_zip = "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip" 
    file_path = download_unzip(url_zip, fichier_cible="lol")

    # afficher_premieres_lignes_txt(file_path, nb_lignes=20, fichier_cible="lol")

