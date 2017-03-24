# SyntaxNet Wrapper

*A lightweight SyntaxNet wrapper*

The wrapper allows generic use of SyntaxNet in python. It provides interfaces for morphological analyse, pos tagging and dependency resolution along with optional formatting tool.

The wrapper does not intend to make any assumptions on the use of SyntaxNet, that's why it provides a simple interface and the raw output as default.

Disclaimer : Has been inspired from another [wrapper](https://github.com/JoshData/parsey-mcparseface-server) but we did not want a server based wrapper.

## Installation

We assume here that you have SyntaxNet installed and working properly on your workstation. If not, please refer to [SyntaxNet official page](https://github.com/tensorflow/models/tree/master/syntaxnet)

The wrapper has been tester on Ubuntu 14.04 Trusty and 16.04 Xenial.

```bash
(virtualenv)$ git clone https://github.com/short-edition/syntaxnet-wrapper.git
(virtualenv)$ cd syntaxnet-wrapper
(virtualenv)/syntaxnet-wrapper$ pip install -r requirements.txt
(virtualenv)/syntaxnet-wrapper$ vim config.yml
syntaxnet:
  ROOT_DIR: /home/user/workspace/syntactic_parser/tensorflow_models/syntaxnet
  PARSER_EVAL: bazel-bin/syntaxnet/parser_eval
  CONTEXT: syntaxnet/models/parsey_universal/context.pbtxt
  MODEL: syntaxnet/models/parsey_universal

(virtualenv)/syntaxnet-wrapper$ python -m unittest discover syntaxnet_wrapper
(virtualenv)/syntaxnet-wrapper$ pip install .
```
You should be able to use the wrapper from now

## How to use this wrapper

**Two mode**

You can use the wrapper in two modes, embodied in two different classes with the same interface
* `SyntaxNetWrapperSubprocess`, a python implementation of `demo.sh` shell script provided in SyntaxNet. It starts new subprocesses at each call.
* `SyntaxNetWrapper`, using wrapper's syntaxnet python implementation. Have the advantage to be faster and more memory efficient than the version with subprocesses. However, we are experience some trouble with it. See [Well-known issues](https://github.com/short-edition/syntaxnet-wrapper/tree/develop#well-known-issues)

**The interface**

The wrapper is expecting unicode text compatible with utf-8 format.
The interface is the same for both classes :
* `morpho_sentence`, make morphological analyse for a single sentence
* `morpho_sentences`, make morphological analyse for a sentences list
* `tag_sentence`, make pos tagging for a single sentence
* `tag_sentences`, make pos tagging for a sentences list
* `parse_sentence`, make dependency parsing for a single sentence
* `parse_sentences`, make dependency parsing for a sentences list

* `transform_morpho`, `transform_tag` and `transform_dependency` format the outputs in a more readable form. Deleting unfilled field.


**Example**

```python
>>> from syntaxnet_wrapper import SyntaxNetWrapper, SyntaxNetWrapperSubprocess
>>> sn_wrapper = SyntaxNetWrapper()
>>> dependency_output = sn_wrapper.parse_sentence(u"Bob brought a pizza to Alice")
>>> print dependency_output
u'1\tBob\t_\tPROPN\tNNP\tNumber=Sing|fPOS=PROPN++NNP\t2\tnsubj\t_\t_\n2\tbrought\t_\tVERB\tVBD\tMood=Ind|Tense=Past|VerbForm=Fin|fPOS=VERB++VBD\t0\tROOT\t_\t_\n3\ta\t_\tDET\tDT\tDefinite=Ind|PronType=Art|fPOS=DET++DT\t4\tdet\t_\t_\n4\tpizza\t_\tNOUN\tNN\tNumber=Sing|fPOS=NOUN++NN\t2\tdobj\t_\t_\n5\tto\t_\tADP\tIN\tfPOS=ADP++IN\t6\tcase\t_\t_\n6\tAlice\t_\tPROPN\tNNP\tNumber=Sing|fPOS=PROPN++NNP\t4\tnmod\t_\t_\n\n'
```

## Well-known issues

The wrapper seems to lead on `stack smashing` error with some SyntaxNet installation, we do not know the reason. In this case, you can use the `SyntaxNetSubprocess` which is working fine

We are aware of the dirty logging with non-subprocess version. We are currently investigating.

## Use of different language

The wrapper use by default english model but you can use every ["Parsey Universal"](https://github.com/tensorflow/models/blob/master/syntaxnet/g3doc/universal.md) released by Google. You just need to pass the name of the model as a constructor's argument. The wrapper will then automatically download the model and use it.

`>>> sn_wrapper = SyntaxNetWrapper(language='French')`
