import heapq
import numpy as np

def dijkstras(start: int, end: int, edge_dict: dict):
    '''
    Performs dijkstra's algorithm on the provided graph to find distance of the
    shortest path between start and end. If there is no path between start and
    end then -1 is returned.

    Parameters
    start: The starting node index
    end: The ending node index
    edge_dict: A dict with a list of connected node indices and edge weights for each node index
    '''
    h = [(0, start)]
    visited = [0 for x in edge_dict.keys()]
    while len(h) > 0:
        dist, curr = heapq.heappop(h)
        if curr == end:
            return dist
        if visited[curr] != 0:
            continue
        visited[curr] = 1
        for (node, dist_to_neigh) in edge_dict[curr]:
            if visited[node] == 0:
                heapq.heappush(h, (dist+dist_to_neigh, node))
    return -1
