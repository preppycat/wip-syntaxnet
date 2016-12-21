# coding:utf8
"""
Wrapper permettant l'utilisation de SyntaxNet en python
Lance trois processus nécessaire à l'analyse de dépendance syntaxique en Français pour chaque analyse
Si plusieurs phrases sont à analyser, elles sont toutes envoyées d'un coup aux processes et le résultat est une liste d'arbre
"""

import yaml, time, subprocess
import os.path as path
from collections import OrderedDict

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

def start_processes():
    # Open the morphological analyzer
    morpho_analyzer = open_parser_eval([
        "--input=stdin",
        "--output=stdout-conll",
        "--hidden_layer_sizes=64",
        "--arg_prefix=brain_morpher",
        "--graph_builder=structured",
        "--task_context=%s" %context_path,
        "--resource_dir=%s" %model_path,
        "--model_path=%s/morpher-params" %model_path,
        "--slim_model",
        "--batch_size=1024",
        "--alsologtostderr"
    ])

    # Open the part of speech tagger
    pos_tagger = open_parser_eval([
        "--input=stdin-conll",
        "--output=stdout-conll",
        "--hidden_layer=64",
        "--arg_prefix=brain_tagger",
        "--graph_builder=structured",
        "--task_context=%s" %context_path,
        "--resource_dir=%s" %model_path,
        "--model_path=%s/tagger-params" %model_path,
        "--slim_model",
        "--batch_size=1024",
        "--alsologtostderr"

    ])

    # Open the syntactic dependency parser.
    dependency_parser = open_parser_eval([
        "--input=stdin-conll",
        "--output=stdout-conll",
        "--hidden_layer_sizes=512,512",
        "--arg_prefix=brain_parser",
        "--graph_builder=structured",
        "--task_context=%s" %context_path,
        "--resource_dir=%s" %model_path,
        "--model_path=%s/parser-params" %model_path,
        "--slim_model",
        "--batch_size=1024",
        "--alsologtostderr"
    ])
    return morpho_analyzer, pos_tagger, dependency_parser

def send_input(process, input):
    # communicate attend la fin du processus, une fois cette fonction appelé le processus est donc terminé.
    stdout, stderr = process.communicate(input.encode('utf8'))
    return stdout.decode("utf8")


def split_tokens(parse, fields_to_del=['lemma', 'feats', 'enhanced_dependency', 'misc']):
    
    # Format the result following ConLL convention http://universaldependencies.org/format.html
    def format_token(line):
        x = OrderedDict(zip(
            ['index', 'token', 'lemma', 'label', 'pos', 'feats', 'parent', 'relation', 'enhanced_dependency', 'misc'],
            line.split('\t')
        ))
        x['index'] = int(x['index'])
        x['parent'] = int(x['parent'])
        for field in fields_to_del:
            del x[field]
        return x

    return [format_token(line) for line in parse.strip().split('\n')]

def parse_sentence(sentence):
    morpho_analyzer, pos_tagger, dependency_parser = start_processes()

    # do morpgological analyze
    morpho_form = send_input(morpho_analyzer, sentence + "\n")
    
    # do pos tagging
    pos_tags = send_input(pos_tagger, morpho_form)
    
    # Do syntaxe parsing
    dependency_parse = send_input(dependency_parser, pos_tags)
    
    dependency_tree = transform_dependency_tree(dependency_parse, sentence)
    return dependency_tree

def tag_sentence(sentence):
    morpho_analyzer, pos_tagger, dependency_parser = start_processes()

    # do morpgological analyze
    morpho_form = send_input(morpho_analyzer, sentence + "\n")
    
    # do pos tagging
    pos_tags = send_input(pos_tagger, morpho_form)
    
    pos_tree = transform_tag(pos_tags, sentence)
    return pos_tree
    

def parse_sentences(sentences):
    if type(sentences) is not list:
        raise ValueError("sentences must be given as a list object")

    morpho_analyzer, pos_tagger, dependency_parser = start_processes()

    joined_sentences = "\n".join(sentences)
    
    # do morpgological analyze
    morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
    
    # do pos tagging
    pos_tags = send_input(pos_tagger, morpho_form)
    
    # Do syntaxe parsing
    dependency_parses = send_input(dependency_parser, pos_tags)
 
    for idx_sentence, dependency_parse in enumerate(dependency_parses.split('\n\n')[:-1]):
        yield transform_dependency_tree(dependency_parse, sentences[idx_sentence])

def tag_sentences(sentences):
    if type(sentences) is not list:
        raise ValueError("sentences must be given as a list object")

    morpho_analyzer, pos_tagger, dependency_parser = start_processes()

    joined_sentences = "\n".join(sentences)
    
    # do morpgological analyze
    morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
    
    # do pos tagging
    pos_tags = send_input(pos_tagger, morpho_form)
    
    for idx_sentence, pos_tag in enumerate(pos_tags.split('\n\n')[:-1]):
        yield transform_tag(pos_tag, sentences[idx_sentence])

def transform_dependency_tree(to_parse, sentence):
    # Make a tree from dependency parsing
    to_parse = split_tokens(to_parse)
    tokens = {token['index']: token for token in to_parse}
    tokens[0] = OrderedDict([("sentence", sentence)])
    
    for token in to_parse:
        tokens[token['parent']].setdefault('tree', OrderedDict()).setdefault(token['relation'], []).append(token)
        del token['parent']
        del token['relation']

    return tokens[0]

def transform_tag(to_parse, sentence):
    # Make a tree from pos tagging
    to_parse = split_tokens(to_parse, fields_to_del=['lemma', 'enhanced_dependency', 'misc', 'relation', 'parent'])
    tokens = {token['index']: token for token in to_parse}
    tokens[0] = OrderedDict([("sentence", sentence)])
    return tokens

if __name__ == '__main__':
    # Exemple d'utilisation avec l'entré standard
    import sys, pprint
    pprint.pprint(parse_sentence(sys.stdin.read().strip())['tree'])


