# Creation d'un fond de carte avec les limites des departements et communes d'IDF
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from script.download_fond_carte import load_fonds_carte
from shapely.geometry import Polygon
import numpy as np
from branca.colormap import LinearColormap

class FondCarteLeaflet:
    def __init__(self, afficher_grande_couronne=False, crs=4326, force_download=False, location=(48.84, 2.35), zoom_start=11, tiles="cartodb positron"):
        # paramètres de la carte
        self.location = location
        self.zoom_start = zoom_start
        self.tiles = tiles

        coms, deps = load_fonds_carte(crs=crs, force_download=force_download)

        # Listes filtrées idf
        if not afficher_grande_couronne:
            IDF = [75, 92, 93, 94]
        else:
            IDF = [75, 77, 78, 91, 92, 93, 94, 95]
        self.coms_pc = coms[coms["INSEE_DEP"].astype(int).isin(IDF)].copy()
        self.deps_pc = deps[deps["INSEE_DEP"].astype(int).isin(IDF)].copy()


    def get_map(self):
        m = folium.Map(location=self.location, zoom_start=self.zoom_start, tiles=self.tiles)

        for _, row in self.deps_pc.iterrows():
            folium.GeoJson(
                row['geometry'],
                name=f"Departement {row['INSEE_DEP']}",
                style_function=lambda x: {
                    'fillColor': 'none',
                    'color': 'black',
                    'weight': 2,
                    'dashArray': '5, 5'
                }
            ).add_to(m)
        for _, row in self.coms_pc.iterrows():
            folium.GeoJson(
                row['geometry'],
                name=f"Commune {row['INSEE_COM']}",
                style_function=lambda x: {
                    'fillColor': 'none',
                    'color': 'gray',
                    'weight': 1,
                    'dashArray': '2, 2'
                }
            ).add_to(m)
        return m


def creer_grid(gdf, cell_size):
    x_cells = (gdf.geometry.x // cell_size * cell_size).astype(int)
    y_cells = (gdf.geometry.y // cell_size * cell_size).astype(int)
 
    grid_cells = [
        Polygon([
            (x, y),
            (x + cell_size, y),
            (x + cell_size, y + cell_size),
            (x, y + cell_size)
        ])
        for x, y in zip(x_cells, y_cells)
    ]

    grid = (
        gpd.GeoDataFrame({"geometry": grid_cells}, crs=gdf.crs)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return grid

def creation_heatmap(gdf, cell_size, target_value_col="Valeur foncière au mètre carré", min_points_per_cell=5):

    gdf = gdf.copy().to_crs(epsg=2154)

    # --- Grille carrée ---

    grid = creer_grid(gdf, cell_size)
    # --- Jointure spatiale ---
    gdf_joined = gpd.sjoin(
        gdf,
        grid,
        how="left",
        predicate="within"
    )

    # --- Statistiques par cellule ---
    grid_stats = (
        gdf_joined
        .groupby("index_right")
        .agg(
            nb_points=(target_value_col, "count"),
            moyenne=(target_value_col, "mean"),
            variance=(target_value_col, "var")
        )
        .reset_index()
    )

    grid_stats["moyenne"] = grid_stats.apply(
        lambda row: row["moyenne"]
        if row["nb_points"] >= min_points_per_cell
        else np.nan,
        axis=1
    )

    # --- Grille finale ---
    grid_final = (
        grid
        .merge(grid_stats, left_index=True, right_on="index_right", how="left")
        .to_crs(epsg=4326)
    )

    return grid_final

def display_heatmap(grid, target_value_col="moyenne", legend=["Prix moyen €/m² :", "Nb transactions :"], cmap=None, default_cmap_caption="Prix moyen au m² (€)", use_log_scale=False, log_base=10, display_cmap=True):
    vals = grid[target_value_col].dropna().astype(float)
    if use_log_scale:
        positive = vals[vals > 0]
        if positive.empty:
            use_log_scale = False  # fallback to linear if no positive values
        else:
            vmin = np.log(positive.min()) / np.log(log_base)
            vmax = np.log(positive.max()) / np.log(log_base)
            caption = f"{default_cmap_caption} (log{log_base})"
    if not use_log_scale:
        if vals.empty:
            vmin = 0.0
            vmax = 1.0
        else:
            vmin = vals.min()
            vmax = vals.max()
        caption = default_cmap_caption

    if type(cmap) == str:
        if  "bicolor" in cmap:
            colors = ["blue", "white", "red"]
        elif "default" in cmap:
            colors = ["#d9d9d9", "yellow", "orange", "red"]
        elif "no_grey" in cmap:
            colors = ["yellow", "orange", "red"]
        else:
            colors = plt.get_cmap(cmap).colors
        if "reverse" in cmap:
            colors = colors[::-1]

        cmap = LinearColormap(
            colors=colors,
            vmin=vmin,
            vmax=vmax,
            caption=caption
        )

    def style_function(feature):
        prix = feature["properties"].get(target_value_col)
        try:
            prix = float(prix)
            if use_log_scale:
                if prix <= 0 or np.isnan(prix):
                    fill = "#f0f0f0"
                else:
                    val = np.log(prix) / np.log(log_base)
                    fill = cmap(val)
            else:
                fill = cmap(prix) if not np.isnan(prix) else "#f0f0f0"
        except (TypeError, ValueError):
            fill = "#f0f0f0"

        return {
            "fillColor": fill,
            "color": None,
            "fillOpacity": 0.7
        }

    # --- Carte ---
    m = FondCarteLeaflet(afficher_grande_couronne=True).get_map()

    fields = [target_value_col, "nb_points"]
    if legend[1] == "":
        fields = [target_value_col]
        legend = [legend[0]]

    folium.GeoJson(
        grid,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=fields,
            aliases=legend,
            localize=True
        ),
        name="Grille transactions"
    ).add_to(m)

    # --- Légende ---
    if display_cmap:
        cmap.add_to(m)  

    return m