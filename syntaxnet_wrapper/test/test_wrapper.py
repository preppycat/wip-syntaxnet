# -*- coding: utf-8 -*-

from unittest2 import TestCase
from collections import OrderedDict

from syntaxnet_wrapper.wrapper import *

class TestWrapper(TestCase):

    def test_morpho_sentence(self):
        input_sentence = u"Cet phrase est un test"
        result = u'1\tCet\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\t_\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper(language='French').morpho_sentence(input_sentence))

    def test_morpho_sentences(self):
        input_sentences = [u"Une première phrase de test", u"Une expression est secondaire"]
        results = u'1\tUne\t_\t_\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n2\tpremi\xe8re\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t0\t_\t_\t_\n3\tphrase\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n4\tde\t_\t_\t_\tfPOS=ADP++\t0\t_\t_\t_\n5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n1\tUne\t_\t_\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n2\texpression\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tsecondaire\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t0\t_\t_\t_\n\n'
        self.assertEqual(results, SyntaxNetWrapper(language='French').morpho_sentences(input_sentences))

    def test_morpho_transform(self):
        input_morpho = u'1\tCet\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\t_\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\t_\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'
        result = {1: OrderedDict([('index', 1), ('token', u'Cet'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: OrderedDict([('index', 2), ('token', u'phrase'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: OrderedDict([('index', 3), ('token', u'est'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: OrderedDict([('index', 4), ('token', u'un'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: OrderedDict([('index', 5), ('token', u'test'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, SyntaxNetWrapper(language='French').transform_morpho(input_morpho))

    def test_tag_sentence(self):
        input_sentence = u"Cet phrase est un test"
        result = u'1\tCet\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper(language='French').tag_sentence(input_sentence))

    def test_tag_sentences(self):
        input_sentences = [u"Une première phrase de test", u"Une expression est secondaire"]
        result = u'1\tUne\t_\tDET\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n2\tpremi\xe8re\t_\tADJ\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t0\t_\t_\t_\n3\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n4\tde\t_\tADP\t_\tfPOS=ADP++\t0\t_\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n1\tUne\t_\tDET\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n2\texpression\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tsecondaire\t_\tADJ\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t0\t_\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper(language='French').tag_sentences(input_sentences))

    def test_transform_tag(self):
        input_tag = u'1\tCet\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t0\t_\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n'

        result = {1: OrderedDict([('index', 1), ('token', u'Cet'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=DET++')]), 2: OrderedDict([('index', 2), ('token', u'phrase'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Fem|Number=Sing|fPOS=NOUN++')]), 3: OrderedDict([('index', 3), ('token', u'est'), ('label', u'VERB'), ('pos', u'_'), ('feats', u'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++')]), 4: OrderedDict([('index', 4), ('token', u'un'), ('label', u'DET'), ('pos', u'_'), ('feats', u'Definite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++')]), 5: OrderedDict([('index', 5), ('token', u'test'), ('label', u'NOUN'), ('pos', u'_'), ('feats', u'Gender=Masc|Number=Sing|fPOS=NOUN++')])}
        self.assertEqual(result, SyntaxNetWrapper(language='French').transform_tag(input_tag))
    
    def test_parse_sentence(self):
        input_sentence = u"Cet phrase est un test"
        result = u'1\tCet\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t2\tdet\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t5\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t5\tcop\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t5\tdet\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper(language='French').parse_sentence(input_sentence))
    
    def test_parse_sentences(self):
        input_sentences = [u"Une première phrase de test", u"Une expression est secondaire"]
        result = u'1\tUne\t_\tDET\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t3\tdet\t_\t_\n2\tpremi\xe8re\t_\tADJ\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t3\tamod\t_\t_\n3\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n4\tde\t_\tADP\t_\tfPOS=ADP++\t5\tcase\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t3\tnmod\t_\t_\n\n1\tUne\t_\tDET\t_\tDefinite=Ind|Gender=Fem|Number=Sing|PronType=Dem|fPOS=DET++\t2\tdet\t_\t_\n2\texpression\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t4\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t4\tcop\t_\t_\n4\tsecondaire\t_\tADJ\t_\tGender=Fem|Number=Sing|fPOS=ADJ++\t0\tROOT\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper(language='French').parse_sentences(input_sentences))
    
    def test_parse_sentence_en(self):
        input_sentence = u"This is a test sentence"
        result =  u'1\tThis\t_\tPRON\tDT\tNumber=Sing|PronType=Dem|fPOS=PRON++DT\t5\tnsubj\t_\t_\n2\tis\t_\tVERB\tVBZ\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++VBZ\t5\tcop\t_\t_\n3\ta\t_\tDET\tDT\tDefinite=Ind|PronType=Art|fPOS=DET++DT\t5\tdet\t_\t_\n4\ttest\t_\tADJ\tJJS\tDegree=Pos|fPOS=ADJ++JJ\t5\tcompound\t_\t_\n5\tsentence\t_\tNOUN\tNN\tNumber=Sing|fPOS=NOUN++NN\t0\tROOT\t_\t_\n\n'
        self.assertEqual(result, SyntaxNetWrapper().parse_sentence(input_sentence))

    def test_transform_dependency(self):
        input_sentence = "Cet phrase est un test"
        input_dependency = u'1\tCet\t_\tDET\t_\tGender=Fem|Number=Sing|fPOS=DET++\t2\tdet\t_\t_\n2\tphrase\t_\tNOUN\t_\tGender=Fem|Number=Sing|fPOS=NOUN++\t5\tnsubj\t_\t_\n3\test\t_\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t5\tcop\t_\t_\n4\tun\t_\tDET\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t5\tdet\t_\t_\n5\ttest\t_\tNOUN\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\tROOT\t_\t_\n\n'

        result = OrderedDict([
            ('sentence', 'Cet phrase est un test'),
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
                                                ('token', u'Cet'), 
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
        self.assertEqual(result, SyntaxNetWrapper(language='French').transform_dependency(input_dependency, input_sentence))
