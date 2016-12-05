from unittest2 import TestCase
from wrapper import *
from collections import OrderedDict

class TestWrapper(TestCase):

    def setUp(self):
        # Open processes for test purpose
        # Open the morphological analyzer
        self.test_morpho_analyzer = open_parser_eval([
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
        test_pos_tagger = open_parser_eval([
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
        test_dependency_parser = open_parser_eval([
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

    def test_send_input(self):
        result = """1\tCet\t_\t_\t_\tfPOS=PROPN++\t0\t_\t_\t_
2\tinput\t_\t_\t_\tfPOS=PROPN++\t0\t_\t_\t_
3\test\t_\t_\t_\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|fPOS=VERB++\t0\t_\t_\t_
4\tun\t_\t_\t_\tDefinite=Ind|Gender=Masc|Number=Sing|PronType=Dem|fPOS=DET++\t0\t_\t_\t_
5\ttest\t_\t_\t_\tGender=Masc|Number=Sing|fPOS=NOUN++\t0\t_\t_\t_\n\n"""

        self.assertEqual(result, send_input(self.test_morpho_analyzer, "Cet input est un test"))

    def test_split_tokens(self):
        input_tokens = '1\ttoken1\tunknown11\tlabel1\tpos1\tunknown21\t1\trelation1\tunknown31\tunknown41\n2\ttoken2\tunknown12\tlabel2\tpos2\tunknown22\t2\trelation2\tunknown32\tunknown42\t'

        result = [
            OrderedDict([('index', 1), ('token', 'token1'), ('label', 'label1'), ('pos', 'pos1'), ('parent', 1), ('relation', 'relation1')]),
            OrderedDict([('index', 2), ('token', 'token2'), ('label', 'label2'), ('pos', 'pos2'), ('parent', 2), ('relation', 'relation2')])
        ]
        self.assertEqual(result, split_tokens(input_tokens))

    def test_parse_sentence(self):
        input_sentence = "Cet phrase est un test"
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
        self.assertEqual(result, parse_sentence(input_sentence))

    
