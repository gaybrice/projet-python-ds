# Correlations entre prix du logement et offre de transport en Île-de-France
Analyse exploratoire et reproductible liant prix de l'immobilier et accessibilité transport en Île‑de‑France.

## Accès aux rapports
Tous les résultats sont accessibles depuis le [site du projet](https://gaybrice.github.io/projet-python-ds/notebooks/main.html).

## Structure du dépôt
- `notebooks/` : notebooks Jupyter non executés; la version exécutée est disponible sur le site.
- `scripts/` : modules Python réutilisables (prétraitement, accès API, visualisations, utilitaires).
- `cache/` : copies locales des données et fichiers intermédiaires.
- branche `gh-pages` : HTML générés pour le site statique.

# Reproduction des résultats

## Prérequis
- Python 3.12+ 
- Quarto 1.8.26+
- Outils système : curl, unzip
- Gestionnaire de dépendances : `uv`

## Installation
Depuis la racine du projet :
```bash
# synchroniser les dépendances
cd /chemin/vers/projet-python-ds
uv sync
```
(ou documenter alternative si `uv` n'est pas disponible, ex. pip/conda/poetry).

## Reproduction des données IDFM (facultatif)

> ℹ️ Cette étape est **complètement facultative**. Si vous ne l'effectuez pas, les données des 30 prochains jours seront récupérées dynamiquement lors de l'exécution.

L'API IDFM fournit des prévisions pour 30 jours. Pour assurer la reproductibilité, un fichier ZIP contenant ces données est disponible [ici](https://drive.google.com/uc?export=download&id=1yoWm96LvktgkUhv6kgPcixghCDm050Vf).

Téléchargez et décompressez son contenu dans `cache/idfm/`. Après extraction, vous devriez obtenir :

```file
cache/
    idfm/
        calendar.csv
        routes.csv
        stop_times.csv
        stops.csv
        trips.csv
```

## Reproduction du site
```bash
cd /chemin/vers/projet-python-ds
uv run quarto render --execute
```

Les notebooks sont tous executés, et les fichiers HTML du site sont créés dans `site/`.