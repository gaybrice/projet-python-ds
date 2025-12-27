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
uv sync
```
(ou documenter alternative si `uv` n'est pas disponible, ex. pip/conda/poetry).

## Reproduction des données IDFM (facultatif)
L'API IDFM fournit des prévisions pour 30 jours. Pour garantir la reproductibilité, un fichier zippé du cache utilisé est disponible ici (TODO AJOUT DU LIEN !!!).

Commandes pour télécharger et décompresser dans `cache/` :
```bash
cd /chemin/vers/projet-python-ds
mkdir -p cache
cd cache
curl -L -o idfm_cache.zip 'LIEN'
unzip idfm_cache.zip
rm idfm_cache.zip
```
Si vous n'effectuez pas cette étape, les données des 30 prochains jours seront récupérées dynamiquement lors de l'exécution.

## Reproduction du site
Depuis la racine du projet :
```bash
uv run quarto render --execute
```

Les fichiers HTML sont créés dans `site/`.

## Exécuter un notebook individuel
Pour exécuter un notebook/quarto spécifique :
```bash
uv run quarto render notebooks/mon_notebook.ipynb --execute
```
