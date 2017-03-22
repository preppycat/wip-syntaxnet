# SyntaxNet Wrapper

*A lightweight SyntaxNet wrapper*

The wrapper allows generic use of SyntaxNet in python. It provides interfaces for morphological analyse, pos tagging and dependency resolution along with optional formatting tool.

The wrapper does not intend to make any assumptions on the use of SyntaxNet, that's why it provides a simple interface and the raw output as default.

Disclaimer : Has been inspired from other [wrapper](https://github.com/JoshData/parsey-mcparseface-server) but we did not want a server based wrapper.

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
....
----------------------------------------------------------------------
Ran 4 tests in 56.793s

OK
(virtualenv)/syntaxnet-wrapper$ pip install -e .
```
You should be able to use the wrapper from now

## How to use this wrapper

**Two mode**

You can use the wrapper in two modes, embodied in two different classes with the same interface
* `SyntaxNetWrapperSubprocess`, a python implementation of `demo.sh`shell script provided in SyntaxNet. Starts new subprocesses at each call.
* `SyntaxNetWrapper`, using wrapper's syntaxnet python implementation. Have the advantage to be faster and more memory efficient than the version with subprocesses. However, we are experience some trouble with it. See [Well-known issues]()

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
>>>from syntaxnet_wrapper import SyntaxNetWrapper, SyntaxNetWrapperSubprocess
>>>sn_wrapper = SyntaxNetWrapper()
>>>dependency_output = sn_wrapper.parse_sentence(u"This is a test sentence")
>>>print dependency_output
 u'g1\tCet\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t2\tdet\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t5\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t5\tcop\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t5\tdet\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n\n'
```

## Well-known issues

The wrapper seems to lead on `stack smashing` error with some SyntaxNet installation, we do not know the reason. In this case, you can use the `SyntaxNetSubprocess` which is working fine

We are aware of the dirty logging with non-subprocess version. We are currently investigating.

## Use of different language

The wrapper use by default english model but you can use every ["Parsey Universal"](https://github.com/tensorflow/models/blob/master/syntaxnet/g3doc/universal.md) released by Google. You just need to pass the name of the model as a constructor's argument. The wrapper will then automatically download the model and use it.

`>>> sn_wrapper = SyntaxNetWrapper(language='French')`
