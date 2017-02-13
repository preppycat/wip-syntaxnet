# coding:utf8
"""
Wrapper permettant l'utilisation de SyntaxNet en python
Lance trois processus nécessaire à l'analyse de dépendance syntaxique en Français pour chaque analyse
Si plusieurs phrases sont à analyser, elles sont toutes envoyées d'un coup aux processes et le résultat est une liste d'arbre
"""

import yaml, time, subprocess
import os.path as path
from collections import OrderedDict
import requests
import zipfile

config_file = yaml.load(open(path.join(path.dirname(__file__), "../config.yml")))
config_syntaxnet = config_file['syntaxnet']
root_dir = config_syntaxnet['ROOT_DIR']
parser_eval_path = config_syntaxnet['PARSER_EVAL']
context_path = config_syntaxnet['CONTEXT']
model_path = config_syntaxnet['MODEL']

def open_parser_eval(args):
    # Lance le processus parser eval de syntaxnet avec les arguments voulus
    return subprocess.Popen(
        [parser_eval_path] + args,
        cwd = root_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE # Only to avoid getting it in stdin
    )

def send_input(process, input):
    # communicate attend la fin du processus, une fois cette fonction appelé le processus est donc terminé.
    stdout, stderr = process.communicate(input.encode('utf8'))
    return stdout.decode("utf8")

class SyntaxNetWrapper:

    def __init__(self, language='English'):
        self.language = language
        self.model_file = path.join(root_dir, model_path, self.language)
        if not path.exists(self.model_file):
            self.model_file = self._load_model()
    
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

    def start_processes(self, process_to_start=['morpho', 'pos', 'dependency']):
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


    def split_tokens(self, parse, fields_to_del=['lemma', 'feats', 'enhanced_dependency', 'misc']):
        
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

        return [format_token(line) for line in parse.strip().split('\n')]

    def morpho_sentence(self, sentence):
        morpho_analyzer, _, _ = self.start_processes(process_to_start=['morpho'])
        # do morpgological analyze
        return send_input(morpho_analyzer, sentence + "\n")

    def morpho_sentences(self, sentences):
        morpho_analyzer, _, _ = self.start_processes(process_to_start=['morpho'])

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        return send_input(morpho_analyzer, joined_sentences + "\n")

    def transform_morpho(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self.split_tokens(to_parse, fields_to_del=['lemma', 'label', 'pos', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def tag_sentence(self, sentence):
        morpho_analyzer, pos_tagger, _  = self.start_processes(process_to_start=['morpho', 'pos'])

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, sentence + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form)

    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, _ = self.start_processes(process_to_start=['morpho', 'pos'])

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form)

    def transform_tag(self, to_parse):
        # Make a tree from pos tagging
        to_parse = self.split_tokens(to_parse, fields_to_del=['lemma', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        tokens = {token['index']: token for token in to_parse}
        return tokens

    def parse_sentence(self, sentence):
        morpho_analyzer, pos_tagger, dependency_parser = self.start_processes()

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, sentence + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # Do syntaxe parsing
        return send_input(dependency_parser, pos_tags)

    def parse_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, dependency_parser = self.start_processes()

        joined_sentences = "\n".join(sentences)
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # Do syntaxe parsing
        return send_input(dependency_parser, pos_tags)

    def transform_dependency(self, to_parse, sentence):
        # Make a tree from dependency parsing
        to_parse = self.split_tokens(to_parse)
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
    pprint.pprint(parse_sentence(sys.stdin.read().strip())['tree'])


