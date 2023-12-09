class AdjacencyGraph():
    """Represent a graph as an adjacency list"""

    def __init__(self, edges, vertices):
        for i, v in enumerate(vertices):
            vertices[i] = v
            for e in v:

