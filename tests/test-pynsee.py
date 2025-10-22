#%%
import pynsee
import pandas as pd
pd.set_option('display.max_columns', None)

# %%
# export en csv des donnees accessibles avec pynsee
def export_local_metadata():
    local_meta = pynsee.get_local_metadata()
    local_meta.head()
    edited = local_meta[["VARIABLES_label_fr","VARIABLES", "UNIT_label_fr"]].drop_duplicates()
    edited = edited.sort_values("VARIABLES_label_fr")
    edited.to_csv("local_metadata_filtered.csv", sep="\t", index=False)
    local_meta.to_csv("local_metadata_full.csv", sep="\t", index=False)

export_local_metadata()
# %%
# Test :
# Recuperation de NA5-CS1_6-SEXE (Activité économique agrégée en 5 postes (NA, 2008) - Catégorie socioprofessionnelle regroupée (6 postes) - Sexe)	Nombre d'emplois (lieu de travail)

'''    
Documentation de  get_local_metadata (https://github.com/InseeFrLab/pynsee/blob/master/pynsee/localdata/get_local_data.py)
Args:
        variables (str): one or several variables separated by an hyphen (see get_local_metadata)
        dataset_version (str): code of a dataset version (see get_local_metadata), if dates are replaced by 'latest' the function triggers a loop to find the latest data available (examples: 'GEOlatestRPlatest', 'GEOlatestFLORESlatest').
        nivgeo (str): code of kind of French administrative area (see get_nivgeo_list), by default it is 'FE' ie all France
        geocodes (list): code one specific area (see get_geoREG_list), by default it is ['1'] ie all France
        update (bool): data is saved locally, set update=True to trigger an update
        silent (bool, optional): Set to True to disable messages printed in log info
        backwardperiod (int, optional): this arg is used only whenever the latest data is searched, it specifies the number of past years the loop should run through.
'''
data = pynsee.get_local_data("NA5-CS1_6-SEXE",
    "GEOlatestRPlatest", 
    "FE" # france entiere pour avoir moins de ligne, remplacer par COM pour les communes
)

data.to_csv("na5_cs1_6_sexe_france.csv")
data[(data["CS1_6"] == "1") & (data["NA5"] == "AZ")] # filtrage des agriculteurs travaillant dans le secteur de l'agriculture


'''
Codes NA / CS :

Colonnes NA5 : types d'activité
AZ : Agriculture, sylviculture et pêche
BE : Industrie manufacturière, industries extractives et autres
FZ : Construction
GU : Commerce, transports et services divers
OQ : Administration publique, enseignement, santé humaine et action
sociale
ZZ : Sans objet

CS1_6 :
- 1 Agriculteurs
- 2 artisans, commerçants et chefs d’entreprises
- 3 Cadres
- 4 Techniciens, agents de maîtrise et autres professions intermédiaires-
- 5 ou 6 Employés ou ouvriers
'''
