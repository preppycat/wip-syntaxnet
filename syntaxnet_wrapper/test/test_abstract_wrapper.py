# coding: utf-8

from unittest2 import TestCase

from syntaxnet_wrapper.abstract_wrapper import *


class TestAbstractWrapper(TestCase):

    def test_morpho_transform(self):
        input_morpho = u'1\tCette\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\t_\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'
        result = {1: dict([('index', 1), ('token', u'Cette'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: dict([('index', 2), ('token', u'phrase'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: dict([('index', 3), ('token', u'est'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: dict([('index', 4), ('token', u'un'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: dict([('index', 5), ('token', u'test'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, AbstractSyntaxNetWrapper(language='French').transform_morpho(input_morpho))


    def test_transform_tag(self):
        input_tag = u'1\tCette\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'

        result = {1: dict([('index', 1), ('token', u'Cette'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: dict([('index', 2), ('token', u'phrase'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: dict([('index', 3), ('token', u'est'), ('label', u'VERB'), ('pos', u'_'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: dict([('index', 4), ('token', u'un'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: dict([('index', 5), ('token', u'test'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, AbstractSyntaxNetWrapper(language='French').transform_tag(input_tag))


    def test_transform_dependency(self):
        input_dependency = u'1\tCette\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t2\tdet\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t5\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t5\tcop\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t5\tdet\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n\n'
        
        result = [{'edges': [{'vertice_b': 2, 'index': '5_2', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'nsubj'}}, {'vertice_b': 3, 'index': '5_3', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'cop'}}, {'vertice_b': 4, 'index': '5_4', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'det'}}], 'vertice': {'index': 5, 'attributes': dict([('token', u'test'), ('label', u'NOUN'), ('pos', u'_'), ('parent', 0), ('relation', u'ROOT')])}}, {'edges': [{'vertice_b': 1, 'index': '2_1', 'vertice_a': 2, 'is_directed': True, 'attributes': {'relation': u'det'}}], 'vertice': {'index': 1, 'attributes': dict([('token', u'Cette'), ('label', u'DET'), ('pos', u'_'), ('parent', 2), ('relation', u'det')])}}, {'edges': [{'vertice_b': 1, 'index': '2_1', 'vertice_a': 2, 'is_directed': True, 'attributes': {'relation': u'det'}}, {'vertice_b': 2, 'index': '5_2', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'nsubj'}}], 'vertice': {'index': 2, 'attributes': dict([('token', u'phrase'), ('label', u'NOUN'), ('pos', u'_'), ('parent', 5), ('relation', u'nsubj')])}}, {'edges': [{'vertice_b': 3, 'index': '5_3', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'cop'}}], 'vertice': {'index': 3, 'attributes': dict([('token', u'est'), ('label', u'VERB'), ('pos', u'_'), ('parent', 5), ('relation', u'cop')])}}, {'edges': [{'vertice_b': 4, 'index': '5_4', 'vertice_a': 5, 'is_directed': True, 'attributes': {'relation': u'det'}}], 'vertice': {'index': 4, 'attributes': dict([('token', u'un'), ('label', u'DET'), ('pos', u'_'), ('parent', 5), ('relation', u'det')])}}]
        self.assertEqual(result, list(AbstractSyntaxNetWrapper(language='French').transform_dependency(input_dependency).serialize()))

	input_dependency = None
	self.assertEqual(None, AbstractSyntaxNetWrapper(language='French').transform_dependency(input_dependency))
