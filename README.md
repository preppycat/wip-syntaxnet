# Wrapper SyntaxNet

Wrapper qui permet l'utilisation de SyntaxNet en python pour avoir l'arbre syntaxique de dépendence d'une phrase. Le wrapper gère le Français.
Très fortement inspiré de https://github.com/JoshData/parsey-mcparseface-server

## Installation du wrapper syntaxnet
```bash
(virtualenv)$ git clone https://github.com/short-edition/syntaxnet-wrapper.git
(virtualenv)$ cd syntaxnet-wrapper
(virtualenv)/syntaxnet-wrapper$ pip install -r requirements.txt
(virtualenv)/syntaxnet-wrapper$ vim config.yml
syntaxnet:
  ROOT_DIR: /home/user/workspace/syntactic_parser/tensorflow_models/syntaxnet
  PARSER_EVAL: bazel-bin/syntaxnet/parser_eval
  CONTEXT: syntaxnet/models/parsey_universal/context.pbtxt
  MODEL: syntaxnet/models/parsey_universal/French

(virtualenv)/syntaxnet-wrapper$ python -m unittest discover syntaxnet_wrapper
....
----------------------------------------------------------------------
Ran 4 tests in 56.793s

OK

(virtualenv) /syntaxnet-wrapper$ echo "La fille descend dans la rue" | python syntaxnet_wrapper/wrapper.py
OrderedDict([(u'ROOT', [OrderedDict([('index', 3), ('token', u'descend'), ('label', u'VERB'), ('pos', u'_'), ('tree', OrderedDict([(u'nsubj', [OrderedDict([('index', 2), ('token', u'fille'), ('label', u'NOUN'), ('pos', u'_'), ('tree', OrderedDict([(u'det', [OrderedDict([('index', 1), ('token', u'La'), ('label', u'DET'), ('pos', u'_')])])]))])]), (u'nmod', [OrderedDict([('index', 6), ('token', u'rue'), ('label', u'NOUN'), ('pos', u'_'), ('tree', OrderedDict([(u'case', [OrderedDict([('index', 4), ('token', u'dans'), ('label', u'ADP'), ('pos', u'_')])]), (u'det', [OrderedDict([('index', 5), ('token', u'la'), ('label', u'DET'), ('pos', u'_')])])]))])])]))])])])
```

## Utilisation du wrapper

**Exemple d'utilisation**

`echo "Une fille descend la rue dans sa voiture" | python wrapper.py`

**API**

La package met à disposition deux fonctions principales, étant `parse_sentence` et `parse_sentences`. Si plusieurs sentences sont à parser d'un coup, il est important d'utiliser `parse_sentences`. En effet, le processus SyntaxNet s'arrête à chaque analyse, que ce soit 1 ou 10 phrases. Il faut donc l'utiliser au mieux. Le lancement des process nécessaires est long et couteux en ressources.


## Installation de SyntaxNet

### Pré-requis

Guide d'installation officiel :
https://github.com/tensorflow/models/tree/master/syntaxnet#installation

Pré-requis
  - Version java 8
```bash
$ java -version
java version "1.8.0_101"
Java(TM) SE Runtime Environment (build 1.8.0_101-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.101-b13, mixed mode)
```
  - python 2.7
```bash
$ python
Python 2.7.9 (default, Jun 24 2016, 11:14:55)
[GCC 4.8.4] on linux2
Type "help", "copyright", "credits" or "license" for more information.
```
  - gcc 4.8 (5 non fonctionnel pour sûr)
```bash
$ gcc -v
gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3)
```
  - pip
```bash
$ pip -V
pip 1.5.4 from /usr/lib/python2.7/dist-packages (python 2.7)
```
  - bazel 3.0.0 ou 3.0.1
```bash
$ bazel version
Build label: 0.3.1
Build target: bazel-out/local-fastbuild/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Fri Jul 29 09:09:52 2016 (1469783392)
Build timestamp: 1469783392
Build timestamp as int: 1469783392
```
  - swig
```bash
$ swig -version

SWIG Version 2.0.11

Compiled with g++ [x86_64-unknown-linux-gnu]

Configured options: +pcre

Please see http://www.swig.org for reporting bugs and further information
```
  - protocol buffer
```
(virtualenv)$ pip freeze | grep protobuf
protobuf==3.0.0b2
```
  - package python
```bash
(virtualenv)$ pip freeze | grep asciitree
(virtualenv)$ pip freeze | grep numpy
(virtualenv)$ pip freeze | grep mock
```

### installation des pré-requis si besoin

  - pip
```bash
$ sudo apt-get install python-pip
```
  - bazel
```bash
# On s'assure que bazel est n'est pas présente sur le système
$ sudo apt-get purge bazel
$ sudo apt-get autoremove

# Installation de bazel depuis les sources (les repos installent une version trop récente)
$ wget https://github.com/bazelbuild/bazel/releases/download/0.3.1/bazel_0.3.1-linux-x86_64.deb
$ dpkg -i bazel_0.3.1-linux-x86_64.deb
$ bazel version
Extracting Bazel installation...
Build label: 0.3.1
Build target: bazel-out/local-fastbuild/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Fri Jul 29 09:09:52 2016 (1469783392)
Build timestamp: 1469783392
Build timestamp as int: 1469783392
```
  - swig
```bash
$ sudo apt-get install swig
```
  - protocol buffers
```bash
(virtualenv)$ pip install -U protobuf==3.0.0b2
```
  - package python
```
(virtualenv)$ pip install asciitree
(virtualenv)$ pip install numpy
(virtualenv)$ pip install mock
```

### Installation et compilation de syntaxnet
```bash
(virtualenv)$ git clone --recursive https://github.com/tensorflow/models.git tensorflow_models
(virtualenv)$ cd tensorflow_models/syntaxnet/tensorflow
(virtualenv)./tensorflow_models/syntaxnet/tensorflow$ ./configure
~/tensorflow_models/syntaxnet/tensorflow ~/tensorflow_models/syntaxnet/tensorflow
Please specify the location of python. [Default is /home/lerni/venv_preddy/bin/python]:
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N]
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N]
No Hadoop File System support will be enabled for TensorFlow
Found possible Python library paths:
  /home/lerni/venv_preddy/lib/python2.7/site-packages
Please input the desired Python library path to use. Default is [/home/lerni/venv_preddy/lib/python2.7/site-packages]

/home/lerni/venv_preddy/lib/python2.7/site-packages
Do you wish to build TensorFlow with GPU support? [y/N]
No GPU support will be enabled for TensorFlow
Configuration finished
Extracting Bazel installation...

....Cloning...cleaning.... and stuff ....

INFO: All external dependencies fetched successfully.

(virtualenv)./tensorflow_models/syntaxnet/tensorflow$ cd ../
(virtualenv)./tensorflow_models/syntaxnet$ bazel test syntaxnet/... util/utf8/... --verbose_failures --local_resources 2048,2.0,1.0 -j 1

... Loading .... cleaning ... and compiling.... prone to warning which are normal .... might take a while ... (25 minutes on my i3 ubuntu 16)
```

### Mise en place du modèle FR
https://github.com/tensorflow/models/blob/master/syntaxnet/universal.md
```bash
(virtualenv)/tensorflow_models/syntaxnet/syntaxnet/models/parsey_universal$ wet http://download.tensorflow.org/models/parsey_universal/French.zip
(virtualenv)/tensorflow_models/syntaxnet/syntaxnet/models/parsey_universal$ unzip French.zip
```
```bash
(virtualenv)/tensorflow_models/syntaxnet/syntaxnet/models/parsey_universal$ echo "Une fille descend la rue" | syntaxnet/models/parsey_universal/parse.sh syntaxnet/models/parsey_universal/French

.... Some start logs and ....
INFO:tensorflow:Processed 1 documents
1 Une _ DET _ Definite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++ 2 det _ _
2 fille _ NOUN _ Gender=Fem|Number=Sing|fPOS=NOUN++ 3 nsubj _ _
3 descend _ VERB _ Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++ 0 ROOT _ _
4 la _ DET _ Definite=Def|Gender=Fem|Number=Sing|fPOS=DET++ 5 det _ _
5 rue _ NOUN _ Gender=Fem|Number=Sing|fPOS=NOUN++ 3 dobj _ _
```
