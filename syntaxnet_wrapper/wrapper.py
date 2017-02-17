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

from syntaxnet_wrapper.parser_eval import SyntaxNetConfig, SyntaxNetProcess
from syntaxnet_wrapper import *

class SyntaxNetWrapper:

    def __init__(self, language='English'):
        print "enter init"
        self.language = language
        self.model_file = path.join(root_dir, model_path, self.language)

        # Download language model if not in folder
        if not path.exists(self.model_file):
            self.model_file = self._load_model()
        print "HAAA"
        # Initiate Morpher
        morpher_config = SyntaxNetConfig(
            task_context=context_path,
            resource_dir=self.model_file,
            model_path=path.join(model_file, 'morpher_params'),
            arg_prefix='brain_morpher',
            input_='custom_file_morpher',
            hidden_layer_sizes=64,
            batch_size=1024,
            slim_model=True,
            custom_file=path.join(custom_file_dir, 'morpher.tmp'),
            variable_scope='morpher',
            graph_builder = 'structured'
        )
        print "before process"
        self.morpher_process = SyntaxNetProcess(morpher_config)
        print "after process"
        # Initiate Tagger
        # Initiate Parser

    
    def _load_model(self):
        print "Load model %s" %self.language
        response = requests.get('http://download.tensorflow.org/models/parsey_universal/%s.zip' %self.language)
        if not response.ok:
            raise Exception('Error during load of model : %s' %response.status_code)
        
        model_file = path.join(root_dir, model_path, self.language)
        with open(model_file + '.zip', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        zip_ref = zipfile.ZipFile(model_file + '.zip', 'r')
        zip_ref.extractall(path.join(root_dir, model_path))
        zip_ref.close()
        
        return model_file

    def _start_processes(self, process_to_start=['morpho', 'pos', 'dependency']):
        # Open the morphological analyzer
        morpho_analyzer = None
        pos_tagger = None
        dependency_parser = None

        if 'morpho' in process_to_start:
	        morpho_analyzer = open_parser_eval([
		    "--input=stdin",
		    "--output=stdout-conll",
		    "--hidden_layer_sizes=64",
		    "--arg_prefix=brain_morpher",
                    "--graph_builder=structured",
                    "--task_context=%s" %context_path,
                    "--resource_dir=%s" %self.model_file,
                    "--model_path=%s/morpher-params" %self.model_file,
                    "--slim_model",
                    "--batch_size=1024",
                    "--alsologtostderr"
                ])

        if 'pos' in process_to_start:
                # Open the part of speech tagger
                pos_tagger = open_parser_eval([
                    "--input=stdin-conll",
                    "--output=stdout-conll",
                    "--hidden_layer=64",
                    "--arg_prefix=brain_tagger",
                    "--graph_builder=structured",
                    "--task_context=%s" %context_path,
                    "--resource_dir=%s" %self.model_file,
                    "--model_path=%s/tagger-params" %self.model_file,
                    "--slim_model",
                    "--batch_size=1024",
                    "--alsologtostderr"

                ])
        if 'dependency' in process_to_start:
                # Open the syntactic dependency parser.
                dependency_parser = open_parser_eval([
                    "--input=stdin-conll",
                    "--output=stdout-conll",
                    "--hidden_layer_sizes=512,512",
                    "--arg_prefix=brain_parser",
                    "--graph_builder=structured",
                    "--task_context=%s" %context_path,
                    "--resource_dir=%s" %self.model_file,
                    "--model_path=%s/parser-params" %self.model_file,
                    "--slim_model",
                    "--batch_size=1024",
                    "--alsologtostderr"
                ])

        return morpho_analyzer, pos_tagger, dependency_parser


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

    def morpho_sentence(self, sentence):
        return morpher_process.parse(sentence + "\n")

    def morpho_sentences(self, sentences):
        morpho_analyzer, _, _ = self._start_processes(process_to_start=['morpho'])

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        return send_input(morpho_analyzer, joined_sentences + "\n")

    def transform_morpho(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'label', 'pos', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def tag_sentence(self, sentence):
        morpho_analyzer, pos_tagger, _  = self._start_processes(process_to_start=['morpho', 'pos'])

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, sentence + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form)

    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, _ = self._start_processes(process_to_start=['morpho', 'pos'])

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form)

    def transform_tag(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def parse_sentence(self, sentence):
        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes()

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, sentence + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # Do syntaxe parsing
        return send_input(dependency_parser, pos_tags)

    def parse_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes()

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # Do syntaxe parsing
        return send_input(dependency_parser, pos_tags)

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


