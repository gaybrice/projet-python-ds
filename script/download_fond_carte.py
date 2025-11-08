import geopandas as gpd
from cartiflette import carti_download
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import os


REGION_CODE = "11"          # code INSEE de l'Île-de-France
YEAR = 2022                 # année de la source COG/IGN souhaitée
SOURCE = "EXPRESS-COG-CARTO-TERRITOIRE"
VECTOR_FORMAT = "geojson"   # topojson | geojson | shapefile etc.
OUTDIR = Path("cache/cartiflette")

def fetch_cartiflette(values, borders, filter_by, crs): # partiellement rédigé par IA
    """
    Appelle carti_download et renvoie un GeoDataFrame.
    carti_download peut renvoyer directement un GeoDataFrame ou
    un chemin vers un fichier (string). On gère les deux cas.
    """
    print(f"Téléchargement : borders={borders}, filter_by={filter_by}, values={values} ...")
    result = carti_download(
        values = values,
        crs = crs,
        borders = borders,
        vectorfile_format = VECTOR_FORMAT,
        filter_by = filter_by,
        source = SOURCE,
        year = YEAR
    )

    # Si carti_download renvoie un GeoDataFrame (ou GeoSeries), on le retourne directement.
    if isinstance(result, (gpd.GeoDataFrame, gpd.GeoSeries)):
        gdf = gpd.GeoDataFrame(result)
    else:
        # Sinon, on suppose que c'est un chemin sur disque (string / Path) :
        path = Path(result)
        if not path.exists():
            # Si cartiflette retourne du binaire / bytes ou une structure différente,
            # cela nécessiterait une adaptation — ici on essaye d'être tolérant.
            raise FileNotFoundError(f"Résultat cartiflette introuvable : {result}")
        gdf = gpd.read_file(path)

    # S'assurer du CRS
    if gdf.crs is None:
        gdf.set_crs(epsg=crs, inplace=True)
    else:
        gdf = gdf.to_crs(epsg=crs)

    return gdf


'''
Téléchargement des listes utiles pour la suite
Cett
'''
def load_fonds_carte(crs, force_download=False, ): 
    communes_out = OUTDIR / "communes_idf.geojson"
    deps_out = OUTDIR / "departements_idf.geojson"

    if not os.path.exists(OUTDIR) or force_download :
        OUTDIR.mkdir(exist_ok=True, parents=True)

        print("Téléchargement des bordures de communes / départements")

        # Departements
        departements_idf = fetch_cartiflette(values=[REGION_CODE], borders="DEPARTEMENT", filter_by="REGION", crs=crs)
        departements_idf.to_file(deps_out, driver="GeoJSON")
        print(f"Départements récupérés : {len(departements_idf)} entités, sauvegardé dans : {deps_out}")

        # Communes / arrondissements
        communes = fetch_cartiflette(values=[REGION_CODE], borders="COMMUNE_ARRONDISSEMENT", filter_by="REGION", crs=crs)
        communes.to_file(communes_out, driver="GeoJSON")
        print(f"Communes récupérées : {len(communes)} entités sauvegardé dans : {communes_out}")
    else:
        print("Téléchargement des bordures de communes / départements mis en cache")

    return [gpd.read_file(communes_out), gpd.read_file(deps_out)]

if __name__ == "__main__":
    print(load_fonds_carte(crs=4326, force_download=True))