# coding:utf8

import os.path as path
import random, string

from syntaxnet_wrapper.abstract_wrapper import AbstractSyntaxNetWrapper
from syntaxnet_wrapper.parser_eval import SyntaxNetConfig, SyntaxNetProcess, configure_stdout
from syntaxnet_wrapper import *

class SyntaxNetWrapper(AbstractSyntaxNetWrapper):
    """
    Wrapper allow use of SyntaxNet in python without subpocess calling
    The pure python call improve efficiency, mainly when the user needs to make several distinct calls to the wrapper
    """

    def __init__(self, language='English'):

        super(SyntaxNetWrapper, self).__init__(language)

        # init stdout file
        configure_stdout('/tmp/stdout.tmp')

        # Initiate Morpher
        morpher_config = SyntaxNetConfig(
            task_context=path.join(root_dir, context_path),
            resource_dir=self._model_file,
            model_path=path.join(self._model_file, 'morpher-params'),
            arg_prefix='brain_morpher',
            input_='custom_file_morpher',
            hidden_layer_sizes=[64],
            batch_size=1024,
            slim_model=True,
            custom_file='/tmp/morpher.tmp', # Need to be hardcoded, dependant with custom context.pbtxt
            # add random string to variable scope to have unique one. Allow instanciate several SyntaxNetWrapper
            variable_scope='morpher' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
            graph_builder_ = 'structured'
        )
        self._morpher_process = SyntaxNetProcess(morpher_config)

        # Initiate Tagger
        tagger_config = SyntaxNetConfig(
            task_context=path.join(root_dir, context_path),
            resource_dir=self._model_file,
            model_path=path.join(self._model_file, 'tagger-params'),
            arg_prefix='brain_tagger',
            input_='custom_file_tagger',
            hidden_layer_sizes=[64],
            batch_size=1024,
            slim_model=True,
            custom_file='/tmp/tagger.tmp', # Need to be hardcoded, dependant with custom context.pbtxt
            # add random string to variable scope to have unique one. Allow instanciate several SyntaxNetWrapper
            variable_scope='tagger' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
            graph_builder_ = 'structured'
        )
        self._tagger_process = SyntaxNetProcess(tagger_config)

        # Initiate Parser
        parser_config = SyntaxNetConfig(
            task_context=path.join(root_dir, context_path),
            resource_dir=self._model_file,
            model_path=path.join(self._model_file, 'parser-params'),
            arg_prefix='brain_parser',
            input_='custom_file_parser',
            hidden_layer_sizes=[512, 512],
            batch_size=1024,
            slim_model=True,
            custom_file='/tmp/parser.tmp', # Need to be hardcoded, dependant with custom context.pbtxt
            # add random string to variable scope to have unique one. Allow instanciate several SyntaxNetWrapper
            variable_scope='parser' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
            graph_builder_ = 'structured'
        )

        self._parser_process = SyntaxNetProcess(parser_config)


    def morpho_sentence(self, sentence):
        result = self._morpher_process.parse(self._format_sentence(sentence) + "\n")
        return result.decode('utf-8')


    def morpho_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        joined_sentences = '\n'.join([self._format_sentence(sentence) for sentence in sentences])

        # do morpgological analyze
        result = self._morpher_process.parse(joined_sentences + "\n")
        return result.decode('utf-8')


    def tag_sentence(self, sentence):

        # do morpgological analyze
        morpho_form = self._morpher_process.parse(sentence)

        # do pos tagging
        pos_tags = self._tagger_process.parse(morpho_form)
        return pos_tags.decode('utf-8')


    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        joined_sentences = '\n'.join([self._format_sentence(sentence) for sentence in sentences])

        # do morpgological analyze
        morpho_form = self._morpher_process.parse(joined_sentences + '\n')

        # do pos tagging
        pos_tags = self._tagger_process.parse(morpho_form)
        return pos_tags.decode('utf-8')


    def parse_sentence(self, sentence):
        # do morpgological analyze
        morpho_form = self._morpher_process.parse(sentence)

        # do pos tagging
        pos_tags = self._tagger_process.parse(morpho_form)

        # do syntax parsing
        syntax_form = self._parser_process.parse(pos_tags)
        return syntax_form.decode('utf-8')


    def parse_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        joined_sentences = '\n'.join([self._format_sentence(sentence) for sentence in sentences])

        # do morpgological analyze
        morpho_form = self._morpher_process.parse(joined_sentences + "\n")

        # do pos tagging
        pos_tags = self._tagger_process.parse(morpho_form)

        # do syntax parsing
        syntax_form = self._parser_process.parse(pos_tags)
        return syntax_form.decode('utf-8')
