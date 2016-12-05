# Wrapper SyntaxNet

Wrapper qui permet l'utilisation de SyntaxNet en python pour avoir l'arbre syntaxique de dépendence d'une phrase. Le wrapper gère le Français.
Très fortement inspiré de https://github.com/JoshData/parsey-mcparseface-server

## Installation de SyntaxNet

Pour installer SyntaxNet, il faut suivre le tutorial : https://github.com/tensorflow/models/tree/master/syntaxnet#installation

Il faut cependant faire attention aux choses suivantes, sans quoi l'installation ne marche pas :
* installer la version 3.0 ou 3.2 de bazel et pas la plus récente des repos 
* il faut que la version de gcc utilisé par bazel soit 4.8.x. En tout cas la version 5 fait planter la compilation (Ubuntu 16.4). Si la version de gcc par défaut est 5 quelque chose, il faut changer la version.
* la compilation de SyntaxNet est gourmande en ressource, il faut limiter le nombre de job pour éviter que l'ordi plante. Ca ralentit beaucoup la compilation par contre. 
Au lieu de ` bazel test --linkopt=-headerpad_max_install_names syntaxnet/... util/utf8/...` 
On utilise ` bazel test --linkopt=-headerpad_max_install_names syntaxnet/... util/utf8/... --verbose_failures --local_resources 2048,2.0,1.0 -j 1`

* les warnings de compilation sont normals, il faut juste que les tests passent à la fin

## Mise en place du modèle pour le français

Une fois SyntaxNet fonctionnel en anglais, l'utilisation de la version anglaise est assez simple.
Suivre le tuto : https://github.com/tensorflow/models/blob/master/syntaxnet/universal.md

## Installation du wrapper

* Cloner le repo : `git clone https://github.com/short-edition/syntaxnet-wrapper.git`
* Créer le fichier de configuration `config.yml` en s'inspirant de `config.yml.dist`. Notez que les chemins `PARSER_EVAL`, `CONTEXT` et `MODEL` sont des chemins relatifs par rapport à `ROOT_DIR` qui est le `CWD` des processus lancés.
* Les tests unitaires `./syntaxnet-wrapper python -m unittest discover .` doivent fonctionner

## Utilisation du wrapper

**Exemple d'utilisation**

`echo "Une fille descend la rue dans sa voiture" | python wrapper.py`

**API**

La package met à disposition deux fonctions principales, étant `parse_sentence` et `parse_sentences`. Si plusieurs sentences sont à parser d'un coup, il est important d'utiliser `parse_sentences`. En effet, le processus SyntaxNet s'arrête à chaque analyse, que ce soit 1 ou 10 phrases. Il faut donc l'utiliser au mieux. Le lancement des process nécessaires est long et couteux en ressources.
