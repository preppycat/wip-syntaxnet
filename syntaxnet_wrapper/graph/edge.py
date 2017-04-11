
class Edge(object):

    def __init__(self, index, vertice_a, vertice_b, attributes=None, is_directed=True):
        self.index = index
        self.vertice_a = vertice_a
        self.vertice_b = vertice_b
        self.attributes = attributes
        self.is_directed = is_directed

    def serialize(self):
        return {'index': self.index,
                'vertice_a': self.vertice_a.index,
                'vertice_b': self.vertice_b.index,
                'attributes': self.attributes,
                'is_directed': self.is_directed}


