import heapq
import numpy as np

def dijkstras(start, end, adj_mat):
    '''
    Performs dijkstra's algorithm on the provided graph to find distance of the
    shortest path between start and end. If there is no path between start and
    end then -1 is returned.

    Parameters
    start: The starting node index
    end: The ending node index
    adj_mat: The adjecancy matrix for the graph (NxN np.ndarray)
    '''
    if adj_mat.shape[0] != adj_mat.shape[1]:
        raise ValueError(f"Adjacency matrix is not squared ({adj_mat.shape}")
    N = adj_mat.shape[0]
    h = [(0, start)]
    visited = np.zeros((N))
    while len(h) > 0:
        dist, curr = heapq.heappop(h)
        if curr == end:
            return dist
        if visited[curr] != 0:
            continue
        visited[curr] = 1
        for i in range(N):
            if visited[i] == 0 and adj_mat[curr, i] != 0:
                heapq.heappush(h, (dist+adj_mat[curr, i], i))
    return -1
