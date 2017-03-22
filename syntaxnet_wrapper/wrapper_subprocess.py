# coding:utf8

import subprocess

from syntaxnet_wrapper.abstract_wrapper import AbstractSyntaxNetWrapper
from syntaxnet_wrapper import *


def open_parser_eval(args):
    # Lance le processus parser eval de syntaxnet avec les arguments voulus
    return subprocess.Popen(
        [parser_eval_path] + args,
        cwd=root_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,  # Only to avoid getting it in stdin
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

    def _start_processes(self, morpho=False, pos=False, dependency=False):
        processes = []

        if morpho:
            # Open the morphological analyzer
            processes.append(open_parser_eval([
                "--input=stdin",
                "--output=stdout-conll",
                "--hidden_layer_sizes=64",
                "--arg_prefix=brain_morpher",
                "--graph_builder=structured",
                "--task_context=%s" % context_path,
                "--resource_dir=%s" % self._model_file,
                "--model_path=%s/morpher-params" % self._model_file,
                "--slim_model",
                "--batch_size=1024",
                "--alsologtostderr"
            ]))

        if pos:
            # Open the part of speech tagger
            processes.append(open_parser_eval([
                "--input=stdin-conll",
                "--output=stdout-conll",
                "--hidden_layer=64",
                "--arg_prefix=brain_tagger",
                "--graph_builder=structured",
                "--task_context=%s" % context_path,
                "--resource_dir=%s" % self._model_file,
                "--model_path=%s/tagger-params" % self._model_file,
                "--slim_model",
                "--batch_size=1024",
                "--alsologtostderr"

            ]))
        if dependency:
            # Open the syntactic dependency parser.
            processes.append(open_parser_eval([
                "--input=stdin-conll",
                "--output=stdout-conll",
                "--hidden_layer_sizes=512,512",
                "--arg_prefix=brain_parser",
                "--graph_builder=structured",
                "--task_context=%s" % context_path,
                "--resource_dir=%s" % self._model_file,
                "--model_path=%s/parser-params" % self._model_file,
                "--slim_model",
                "--batch_size=1024",
                "--alsologtostderr"
            ]))

        return processes


    def morpho_sentence(self, sentence):
        morpho_analyzer = self._start_processes(morpho=True)[0]
        # do morphological analyze
        return send_input(morpho_analyzer, self._format_sentence(sentence) + '\n').decode('utf-8')

    def morpho_sentences(self, sentences):
        morpho_analyzer = self._start_processes(morpho=True)[0]

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morphological analyze
        return send_input(morpho_analyzer, joined_sentences + "\n").decode('utf-8')


    def tag_sentence(self, sentence):
        morpho_analyzer, pos_tagger = self._start_processes(morpho=True, pos=True)

        # do morphological analyze
        morpho_form = send_input(morpho_analyzer, self._format_sentence(sentence) + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form).decode('utf-8')

    def tag_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger = self._start_processes(morpho=True, pos=True)

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morphological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        return send_input(pos_tagger, morpho_form).decode('utf-8')


    def parse_sentence(self, sentence):
        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes(morpho=True, pos=True, dependency=True)

        # do morphological analyze
        morpho_form = send_input(morpho_analyzer, self._format_sentence(sentence) + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # do syntax parsing
        return send_input(dependency_parser, pos_tags).decode('utf-8')

    def parse_sentences(self, sentences):
        if type(sentences) is not list:
            raise ValueError("sentences must be given as a list object")

        morpho_analyzer, pos_tagger, dependency_parser = self._start_processes(morpho=True, pos=True, dependency=True)

        joined_sentences = "\n".join([self._format_sentence(sentence) for sentence in sentences])
        
        # do morphological analyze
        morpho_form = send_input(morpho_analyzer, joined_sentences + "\n")
        
        # do pos tagging
        pos_tags = send_input(pos_tagger, morpho_form)
        
        # do syntax parsing
        return send_input(dependency_parser, pos_tags).decode('utf-8')
