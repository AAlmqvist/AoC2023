import sys
sys.path.append('../')
import heapq

from tools.parsing import read_by_line, read_with_delimeter

def create_graph(data):
    graph = dict()
    for s in data:
        info = s.split(": ")
        node = info[0]
        if node not in graph:
            graph[node] = []
        for other in info[1].split():
            graph[node].append(other)
            if other not in graph:
                graph[other] = []
            graph[other].append(node)
    return graph

# Dijkstras with some edges already visited to start.
def find_shortest_path(graph, start, end, visited):
    h = [(1, [start, other]) for other in graph[start] if other not in visited]
    while len(h) > 0:
        dist, path = heapq.heappop(h)
        n1, n2 = path[-2], path[-1]
        if (n1, n2) in visited or (n2, n1) in visited:
            continue
        if path[-1] == end:
            return path
        visited.add((n1, n2))
        for other in graph[n2]:
            p = path.copy()
            p.append(other)
            heapq.heappush(h, (dist+1, p))
    return []

# Find all paths possible between start and end given that we remove the
# edges in the previous paths. This should allow us to find what three edges
# that are shared for all nodes that should be disconnected after the cut.
def find_independent_paths(graph, start, end):
    paths = []
    visited = set()
    path = find_shortest_path(graph, start, end, visited.copy())
    while path != []:
        for i in range(len(path)-1):
            visited.add((path[i], path[i+1]))
        paths.append(path)
        path = find_shortest_path(graph, start, end, visited.copy())
    return paths

# Find pairs of neighboring nodes that should appear in all independent paths between
# two nodes that will be part of the different sub-graphs after the cut.
def find_common_edges(set_of_paths):
    edges = dict()
    for paths in set_of_paths:
        for path in paths:
            for e1, e2 in path:
                if (e2, e1) in edges:
                    edges[(e2, e1)] += 1
                    continue
                if (e1, e2) not in edges:
                    edges[(e1, e2)] = 0
                edges[(e1, e2)] += 1
    removed = []
    to_hit = max([count for _, count in edges.items()])
    for edge, count in edges.items():
        if count == to_hit:
            removed.append(edge)
    return removed

def BFS(graph, start, removed_edges):
    visited = set()
    curr = [start]
    visited.add(start)
    while curr:
        next_iter = []
        for node in curr:
            for other in graph[node]:
                if other in visited:
                    continue
                if (node, other) in removed_edges or (other, node) in removed_edges:
                    continue
                next_iter.append(other)
                visited.add(other)
            curr = next_iter
    return visited

def run():
    data = read_by_line('input.txt')
    graph = create_graph(data)
    nodes = list(graph.keys())
    N = len(nodes)
    independent_paths = []
    for i in range(N):
        for j in range(i+1, N):
            # Find all independent paths between two pairs of nodes
            # Should be exactly 3 of them for nodes that will end up in
            # different sub-graphs.
            paths = find_independent_paths(graph, nodes[i], nodes[j])
            if sum([1 if len(p) < 3 else 0 for p in paths]) > 0:
                continue
            if len(paths) == 3:
                independent_paths.append([[(p[i], p[i+1]) for i in range(len(p)-1)] for p in paths])
                break
        if len(independent_paths) > 3:
            cut = find_common_edges(independent_paths)
            if len(cut) == 3:
                break
    # Found the 3 edges to remove, now do BFS from one of the nodes connected to
    # an edge we removed to find the size of the partial graph
    part_off_graph = BFS(graph, cut[0][0], cut)
    print((N-len(part_off_graph))*len(part_off_graph))

if __name__ == "__main__":
    run()