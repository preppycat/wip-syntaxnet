# coding:utf8
"""
Wrapper permettant l'utilisation de SyntaxNet en python
Lance trois processus nécessaire à l'analyse de dépendance syntaxique en Français pour chaque analyse
Si plusieurs phrases sont à analyser, elles sont toutes envoyées d'un coup aux processes et le résultat est une liste d'arbre
"""

import time, subprocess
import os.path as path
from collections import OrderedDict
import requests
import zipfile
import random, string

from syntaxnet_wrapper.parser_eval import SyntaxNetConfig, SyntaxNetProcess, configure_stdout
from syntaxnet_wrapper import *

class SyntaxNetWrapper:

    def __init__(self, language='English'):
        self._language = language
        self._model_file = path.join(root_dir, model_path, self._language)

        # Download language model if not in folder
        if not path.exists(self._model_file):
            self._model_file = self._load_model()

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
    
    def _load_model(self):
        print "Load model %s" %self._language
        response = requests.get('http://download.tensorflow.org/models/parsey_universal/%s.zip' %self._language)
        if not response.ok:
            raise Exception('Error during load of model : %s' %response.status_code)
        
        model_file = path.join(root_dir, model_path, self._language)
        with open(model_file + '.zip', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        zip_ref = zipfile.ZipFile(model_file + '.zip', 'r')
        zip_ref.extractall(path.join(root_dir, model_path))
        zip_ref.close()
        
        return model_file

    def _split_tokens(self, parse, fields_to_del=['lemma', 'feats', 'enhanced_dependency', 'misc']):
        
        # Format the result following ConLL convention http://universaldependencies.org/format.html
        def format_token(line):
            x = OrderedDict(zip(
                ['index', 'token', 'lemma', 'label', 'pos', 'feats', 'parent', 'relation', 'enhanced_dependency', 'misc'],
                line.split('\t')
            ))
            if x['index']:
                x['index'] = int(x['index'])
            if x['parent']:
                x['parent'] = int(x['parent'])

            for field in fields_to_del:
                del x[field]
            return x

        return [format_token(line) for line in parse.strip().split('\n') if line]

    def _format_sentence(self, sentence):
	try:
	    return sentence.encode('utf-8')
	except UnicodeError:
	    raise ValueError("Input sentence should be utf8 compliant, problem with : %s" %sentence)

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

    def transform_morpho(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'label', 'pos', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def tag_sentence(self, sentence):

        # do morpgological analyze
        morpho_form = self.morpho_sentence(self._format_sentence(sentence))
        
        # do pos tagging
       	pos_tags = self._tagger_process.parse(morpho_form)
	return pos_tags.decode('utf-8')

    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        joined_sentences = '\n'.join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morpgological analyze
        morpho_form = self._morpher_process.parse(joined_sentences + "\n")
        
        # do pos tagging
       	pos_tags = self._tagger_process.parse(morpho_form)
        return pos_tags.decode('utf-8')

    def transform_tag(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def parse_sentence(self, sentence):
        # do morpgological analyze
        morpho_form = self.morpho_sentence(self._format_sentence(sentence))
        
        # do pos tagging
       	pos_tags = self._tagger_process.parse(morpho_form)

        # Do syntaxe parsing
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
        
        # Do syntaxe parsing
        syntax_form = self._parser_process.parse(pos_tags)
        return syntax_form.decode('utf-8')

    def transform_dependency(self, to_parse, sentence):
        # Make a tree from dependency parsing
        to_parse = self._split_tokens(to_parse)
        tokens = {token['index']: token for token in to_parse}
        tokens[0] = OrderedDict([("sentence", sentence)])
        
        for token in to_parse:
            tokens[token['parent']].setdefault('tree', OrderedDict()).setdefault(token['relation'], []).append(token)
            del token['parent']
            del token['relation']

        return tokens[0]

if __name__ == '__main__':
    # Exemple d'utilisation avec l'entré standard
    import sys, pprint
    pprint.pprint(SyntaxNetWrapper(language='French').parse_sentence(sys.stdin.read().strip())['tree'])


