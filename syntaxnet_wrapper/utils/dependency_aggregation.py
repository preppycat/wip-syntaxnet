# coding=utf-8

def dependency_aggregate(graphs):
    """
    function making easier to aggregate syntaxic dependencies together
    input should come as an array of transform_dependency, graph objects.
    This allow to aggregate more than one sentence
    """
    data_deps = count_deps(graphs)

    return data_deps


def count_deps(matches):

    possible_deps = ['acl', 'advcl', 'advmod', 'amod', 'appos', 'aux', 'case', 'cc', 'ccomp',
        'clf', 'compound', 'conj', 'cop', 'csubj', 'dep', 'det', 'discourse', 'dislocated', 'expl', 'fixed',
        'flat', 'goeswith', 'iobj', 'list', 'mark', 'nmod', 'nsubj', 'nummod', 'obj', 'obl', 'orphan', 'parataxis', 'punct', 'reparadum', 'root', 'vocative', 'xcomp']

    # init dict
    aggr_dep = {dep: 0 for dep in possible_deps}

    for graph in matches:
            if graph:
                for edge in graph._edges:
                    attributes = edge.attributes
                    if attributes is not None and attributes.get('relation', None) is not None:
                        relation = attributes['relation']
                        if relation in possible_deps:
                            aggr_dep[relation] += 1

    return aggr_dep