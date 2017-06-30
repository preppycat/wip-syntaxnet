from syntaxnet_wrapper.graph.vertice import Vertice
from syntaxnet_wrapper.graph.edge import Edge

class Graph(object):

    def __init__(self):
        self._vertices = []
        self._edges = []

    def get_vertice(self, vertice_index):
        for vertice in self._vertices:
            if vertice.index == vertice_index:
                return vertice

    def add_vertice(self, vertice):
        if self.get_vertice(vertice.index) is not None:
            raise ValueError('The vertice %s already exist in graph' %vertice.index)

        self._vertices.append(vertice)

    def get_edge(self, edge_index):
        for edge in self._edges:
            if edge.index == edge_index:
                return edge

    def add_edge(self, edge):
        if self.get_vertice(edge.vertice_a.index) is None or self.get_vertice(edge.vertice_b.index) is None:
            raise ValueError('A vertice is missing in the graph, please ensure you inserted them all')

        if self.get_edge(edge.index) is not None:
            raise ValueError('This edge already exist in graph')

        self._edges.append(edge)

    def get_related_edges(self, vertice_index):
        for edge in self._edges:
            if edge.vertice_a.index == vertice_index or edge.vertice_b.index == vertice_index:
                yield edge

    def serialize(self):
        """
        Return all vertices with all edge linked to each vertice
        Edges will be returned several times
        """
        for vertice in self._vertices:
            yield {'vertice': vertice.__dict__, 
                   'edges': [edge.serialize() for edge in self.get_related_edges(vertice.index)]
                  }
