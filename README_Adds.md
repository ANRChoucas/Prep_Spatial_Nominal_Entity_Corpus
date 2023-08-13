# Spatial Nominal Entity Recognition




Liste des fichiers
- [x] [utils_functions.py](scripts/utils_functions.py)
- [x] [run_perdido.ipynb](scripts/run_perdido.ipynb)
- [x] [create_lexicon_from_ene.ipynb](scripts/create_lexicon_from_ene.ipynb)
- [x] [generate_input_positive_class.ipynb](scripts/generate_input_positive_class.ipynb)
- [x] [generate_input_negative_class.ipynb](scripts/generate_input_negative_class.ipynb)
- [x] [ngram_json_to_tsv.ipynb](scripts/ngram_json_to_tsv.ipynb)


## Configurer un environnement conda

### Cloner ce dépôt git

```bash

git clone https://github.com/ludovicmoncla/spatial-nominal-entity-recognition.git
```

### Configurer l'environnement avec toutes les dépendances nécessaires

* Créer un nouvel environnement nommé `sner-py39`

```bash
conda create -n sner-py39 python=3.9
```

* Activer l'environnement

```bash
conda activate sner-py39
```

* Installer le paquet `fiona` avec conda (évite une erreur lors de l'installation de cette dépendence de Perdido avec `pip`)

```bash
conda install fiona==1.8.21
```

* Installer les dépendances avec `pip`

```bash
pip install -r requirements.txt
```

- Dans le fichier requirements.txt il faut ajouter ipykernel

- Ou alors si absent ajouter en ligne de commande:

  ```
  conda install ipykernel
  ```

- Dans tous les cas 

```
ipython kernel install --name sner-py39 --user
```

## GIT LFS

This repository uses Git LFS to store the file: `data/EDdA_dataset_articles_superdomainBERT_230327.tsv` 
 * [Git LFS install](https://docs.github.com/fr/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)
 * [Git LFS configuration](https://docs.github.com/fr/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)
