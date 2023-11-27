import numpy as np
from algorithms import dijkstras

GRAPH = '''0 7 9 0 0 14
7 0 10 15 0 0
9 10 0 11 0 2
0 15 11 0 6 0
0 0 0 6 0 9
14 0 2 0 9 0'''

def test_dijkstras():
    graph = np.array([[int(y) for y in x.split()] for x in GRAPH.split("\n")])
    res = dijkstras(0, 4, graph)
    if res != 20:
        raise ValueError(f"djikstra's failed ({res}!={20})")

if __name__ == "__main__":
    test_dijkstras()