# PythonOC

## Projet 2 Books scrapping

Voici un script pour le projet 2 Books Scrapping

Ce script récupère l'information des livres du site web Books.toscrape et créé des fichiers CSV avec cette information.

Afin de réussir, ce script suit les étapes suivantes :
- Récupérer les urls des catégories.
- Récupérer les urls des livres de chaque catégorie parcourue.
- Récupérer l'information de chaque livre parcouru.
- Créér un fichier CSV par catégorie avec l'information de chaque livre.
- Télécharger les images de chaque livre.

## Installation

Python version : 3.9
<création du venv>

Les dépendances sont listées dans le fichier `requirements.txt`.
Lancer :

```
pip install -r requirements.txt
```

## Setup

il faut avoir créé les repertoires `data/images/` et `data/fichiers-csv/`.

## Usage
Lancer le script :

```
python projet2.py
```

Les fichiers seront écrits dans le dossier `data/fichiers-csv/`.
Les images seront enregistrées dans le dossier `data/images/`.


## Voir Aussi
http://books.toscrape.com/catalogue/category/books_1/index.html


