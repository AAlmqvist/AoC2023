import sys
sys.path.append('../')
import numpy as np
import heapq

from tools.parsing import read_by_line, read_with_delimeter

DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def parse_data(s: str):
    return [int(x) for x in s if x != '']

def dijkstras(start: int, end: int, edge_dict: dict, min_steps=4, max_steps=10):
    h = [(0, start, 0), (0, start, 1)]
    visited = [[0 for _ in DIRS] for x in edge_dict.keys()]
    while len(h) > 0:
        dist, curr, dir = heapq.heappop(h)
        if curr == end:
            return dist
        if visited[curr][dir] != 0:
            continue
        visited[curr][dir] = 1
        for new_dir in [(dir+1)%4, (dir+3)%4]:
            node = curr
            notValid = False
            extra_dist = 0
            for _ in range(min_steps):
                node, dist_to_neigh = edge_dict[node][new_dir]
                if dist_to_neigh > 10:
                    notValid = True
                    break
                extra_dist += dist_to_neigh
            if notValid:
                continue
            heapq.heappush(h, (dist+extra_dist, node, new_dir))
            for _ in range(min_steps, max_steps):
                node, dist_to_neigh = edge_dict[node][new_dir]
                if dist_to_neigh > 10:
                    break
                extra_dist += dist_to_neigh
                heapq.heappush(h, (dist+extra_dist, node, new_dir))
    return -1

def map_neighbors(x: np.ndarray):
    r, c = x.shape
    n_map = dict()
    for i in range(r):
        for j in range(c):
            neighbs = []
            for dr, dc in DIRS:
                if i+dr < 0 or i+dr >= r or j+dc < 0 or j+dc >= c:
                    neighbs.append((0, 100))
                    continue
                neighbs.append(((i+dr)*c+j+dc, x[i+dr, j+dc]))
            n_map[i*c+j] = neighbs
    return n_map

def run():
    data = np.array(read_by_line("input.txt", parse_func=parse_data))
    heat_mapping = map_neighbors(data)
    end = len(heat_mapping.keys())-1
    dist = dijkstras(0, end, heat_mapping, min_steps=1, max_steps=3)
    print(dist)
    dist2 = dijkstras(0, end, heat_mapping)
    print(dist2)

if __name__ == "__main__":
    run()