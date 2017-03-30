# coding: utf-8

from unittest2 import TestCase

from syntaxnet_wrapper.abstract_wrapper import *


class TestAbstractWrapper(TestCase):

    def test_morpho_transform(self):
        input_morpho = u'1\tCette\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\t_\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'
        result = {1: OrderedDict([('index', 1), ('token', u'Cette'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: OrderedDict([('index', 2), ('token', u'phrase'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: OrderedDict([('index', 3), ('token', u'est'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: OrderedDict([('index', 4), ('token', u'un'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: OrderedDict([('index', 5), ('token', u'test'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, AbstractSyntaxNetWrapper(language='French').transform_morpho(input_morpho))


    def test_transform_tag(self):
        input_tag = u'1\tCette\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'

        result = {1: OrderedDict([('index', 1), ('token', u'Cette'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: OrderedDict([('index', 2), ('token', u'phrase'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: OrderedDict([('index', 3), ('token', u'est'), ('label', u'VERB'), ('pos', u'_'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: OrderedDict([('index', 4), ('token', u'un'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: OrderedDict([('index', 5), ('token', u'test'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, AbstractSyntaxNetWrapper(language='French').transform_tag(input_tag))


    def test_transform_dependency(self):
        input_sentence = "Cette phrase est un test"
        input_dependency = u'1\tCette\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t2\tdet\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t5\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t5\tcop\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t5\tdet\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n\n'

        result = OrderedDict([
            ('sentence', 'Cette phrase est un test'),
            ('tree', OrderedDict([
                (u'ROOT', [
                    OrderedDict([
                        ('index', 5), 
                        ('token', u'test'), 
                        ('label', u'NOUN'), 
                        ('pos', u'_'), 
                        ('tree', OrderedDict([
                            (u'nsubj', [
                                OrderedDict([
                                    ('index', 2),
                                    ('token', u'phrase'),
                                    ('label', u'NOUN'),
                                    ('pos', u'_'),
                                    ('tree', OrderedDict([
                                        (u'det', [
                                            OrderedDict([
                                                ('index', 1), 
                                                ('token', u'Cette'),
                                                ('label', u'DET'), 
                                                ('pos', u'_')
                                            ])
                                        ])
                                    ]))
                                ])
                            ]),
                            (u'cop', [
                                OrderedDict([
                                    ('index', 3),
                                    ('token', u'est'),
                                    ('label', u'VERB'),
                                    ('pos', u'_')])
                            ]),
                            (u'det', [
                                OrderedDict([
                                    ('index', 4),
                                    ('token', u'un'),
                                    ('label', u'DET'),
                                    ('pos', u'_')]
                                )]
                            )]
                        ))])])]))])
        self.assertEqual(result, AbstractSyntaxNetWrapper(language='French').transform_dependency(input_dependency, input_sentence))
