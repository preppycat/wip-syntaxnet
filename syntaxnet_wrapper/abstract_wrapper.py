# coding: utf-8

# import common libs
import os.path as path
import requests
from collections import OrderedDict

import zipfile

from syntaxnet_wrapper import *


class AbstractSyntaxNetWrapper(object):
    """
    Abstract Wrapper class, define common function
    Should not be instanciated by user
    """

    def __init__(self, language='English'):
        self._language = language
        self._model_file = path.join(root_dir, model_path, self._language)

        # download language model if not in folder
        if not path.exists(self._model_file):
            self._model_file = self._load_model()


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
        # format the result following ConLL convention http://universaldependencies.org/format.html
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
            raise ValueError("Input sentence should be utf-8 compliant, problem with : %s" % sentence)


    def morpho_sentence(self, sentence):
        raise NotImplementedError("This method is not implemented")


    def morpho_sentences(self, sentences):
        raise NotImplementedError("This method is not implemented")


    def transform_morpho(self, to_parse):
        # make a tree from morpho form
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'label', 'pos', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        return {token['index']: token for token in to_parse}


    def tag_sentence(self, sentence):
        raise NotImplementedError("This method is not implemented")


    def tag_sentences(self, sentences):
        raise NotImplementedError("This method is not implemented")


    def transform_tag(self, to_parse):
        # make a tree from pos tagging
        to_parse = self._split_tokens(to_parse, fields_to_del=['lemma', 'enhanced_dependency', 'misc', 'relation', 'parent'])
        return {token['index']: token for token in to_parse}


    def parse_sentence(self, sentence):
        raise NotImplementedError("This method is not implemented")


    def parse_sentences(self, sentences):
        raise NotImplementedError("This method is not implemented")


    def transform_dependency(self, to_parse, sentence):
        # make a tree from dependency parsing
        to_parse = self._split_tokens(to_parse)
        tokens = {token['index']: token for token in to_parse}
        tokens[0] = OrderedDict([("sentence", sentence)])

        for token in to_parse:
            tokens[token['parent']].setdefault('tree', OrderedDict()).setdefault(token['relation'], []).append(token)
            del token['parent']
            del token['relation']

        return tokens[0]
