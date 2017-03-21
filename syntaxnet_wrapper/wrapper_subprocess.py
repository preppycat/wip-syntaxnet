# coding:utf8
"""
Wrapper permettant l'utilisation de SyntaxNet en python
Lance trois processus nécessaire à l'analyse de dépendance syntaxique en Français pour chaque analyse
Si plusieurs phrases sont à analyser, elles sont toutes envoyées d'un coup aux processes et le résultat est une liste d'arbre
"""

import time, subprocess

from syntaxnet_wrapper.abstract_wrapper import AbstractSyntaxNetWrapper
from syntaxnet_wrapper import *


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
    stdout, stderr = process.communicate(input)
    return stdout


class SyntaxNetWrapperSubprocess(AbstractSyntaxNetWrapper):
    """
    Wrapper allow SyntaxNet use with subprocess calling. Similar to the "demo.sh" call
    Launch tree processes needed to the parsing for each analyse
    If you have several sentences to process, you might prefer to parse them all in one call with convinient function instead 
    of several heavy calls
    """

    def _start_processes(self, process_to_start=['morpho', 'pos', 'dependency']):
        morpho_analyzer = None
        pos_tagger = None
        dependency_parser = None

        if 'morpho' in process_to_start:
            # Open the morphological analyzer
            morpho_analyzer = open_parser_eval([
                "--input=stdin",
                "--output=stdout-conll",
                "--hidden_layer_sizes=64",
                "--arg_prefix=brain_morpher",
                "--graph_builder=structured",
                "--task_context=%s" %context_path,
                "--resource_dir=%s" %self._model_file,
                "--model_path=%s/morpher-params" %self._model_file,
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
                "--resource_dir=%s" %self._model_file,
                "--model_path=%s/tagger-params" %self._model_file,
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
                "--resource_dir=%s" %self._model_file,
                "--model_path=%s/parser-params" %self._model_file,
                "--slim_model",
                "--batch_size=1024",
                "--alsologtostderr"
            ])

        return morpho_analyzer, pos_tagger, dependency_parser


    def morpho_sentence(self, sentence):
        morpho_analyzer, _, _ = self._start_processes(process_to_start=['morpho'])
        # do morpgological analyze
        return send_input(morpho_analyzer, self._format_sentence(sentence) + "\n").decode('utf-8')

    def morpho_sentences(self, sentences):
        morpho_analyzer, _, _ = self._start_processes(process_to_start=['morpho'])

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morpgological analyze
        return send_input(morpho_analyzer, joined_sentences + "\n").decode('utf-8')


    def tag_sentence(self, sentence):
        morpho_analyzer, pos_tagger, _  = self._start_processes(process_to_start=['morpho', 'pos'])

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, self._format_sentence(sentence) + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form).decode('utf-8')

    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, _ = self._start_processes(process_to_start=['morpho', 'pos'])

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form).decode('utf-8')


    def parse_sentence(self, sentence):
        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes()

        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, self._format_sentence(sentence) + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # do syntax parsing
        return send_input(dependency_parser, pos_tags).decode('utf-8')

    def parse_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes()

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morpgological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # do syntax parsing
        return send_input(dependency_parser, pos_tags).decode('utf-8')
