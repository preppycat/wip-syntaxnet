from unittest2 import TestCase

from syntaxnet_wrapper.graph.graph import Graph
from syntaxnet_wrapper.graph.vertice import Vertice
from syntaxnet_wrapper.graph.edge import Edge

class TestGraph(TestCase):

    def test_create_graph(self):
        g1 = Graph()
        self.assertEqual([], g1._vertices)
        self.assertEqual([], g1._edges)

    def test_get_vertice(self):
        root = Vertice('root')
        g1 = Graph()
        g1._vertices.append(root)
        self.assertEqual(None, g1.get_vertice('vertice_unknown'))
        self.assertEqual(root, g1.get_vertice('root'))

    def test_add_vertice(self):
        g1 = Graph()
        v1 = Vertice('v1')
        g1.add_vertice(v1)
        self.assertIn(v1, g1._vertices)

    def test_get_edge(self):
        g1 = Graph()
        v1 = Vertice('v1')
        v2 = Vertice('v2')
        g1.add_vertice(v1)
        g1.add_vertice(v2)
        edge = Edge('e1', v1, v2)
        g1.add_edge(edge)
        self.assertEqual(edge, g1.get_edge('e1'))

    def test_add_edge(self):
        g1 = Graph()
        v1 = Vertice('v1')
        v2 = Vertice('v2')
        g1.add_vertice(v1)
        g1.add_vertice(v2)

        e1 = Edge('e1', v1, v2)
        g1.add_edge(e1)
        self.assertIn(e1, g1._edges)

        with self.assertRaises(ValueError):
            v3 = Vertice('v3')
            e2 = Edge('e2', v1, v3) # v2 is instanciated but not inserted in graph
            g1.add_edge(e2)

    def test_get_relate_edges(self):
        g1 = Graph()
        v1 = Vertice('v1')
        v2 = Vertice('v2')
        g1.add_vertice(v1)
        g1.add_vertice(v2)

        e1 = Edge('e1', v1, v2)
        g1.add_edge(e1)

        self.assertEqual([e1], list(g1.get_related_edges(v1.index)))

        v3 = Vertice('v3')
        g1.add_vertice(v3)
        e2 = Edge('e2', v1, v3)
        g1.add_edge(e2)
        self.assertEqual([e1, e2], list(g1.get_related_edges(v1.index)))

    def test_serialize(self):
        g1 = Graph()
        v1 = Vertice('v1')
        v2 = Vertice('v2')
        g1.add_vertice(v1)
        g1.add_vertice(v2)

        e1 = Edge('e1', v1, v2)
        g1.add_edge(e1)

        result = [{'edges': [{'vertice_b': 'v2', 'index': 'e1', 'vertice_a': 'v1', 'is_directed': True, 'attributes': None}], 'vertice': {'index': 'v1', 'attributes': None}}, {'edges': [{'vertice_b': 'v2', 'index': 'e1', 'vertice_a': 'v1', 'is_directed': True, 'attributes': None}], 'vertice': {'index': 'v2', 'attributes': None}}]

        self.assertEqual(result, list(g1.serialize()))


