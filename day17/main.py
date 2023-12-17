import sys
sys.path.append('../')
import numpy as np
import heapq

from tools.parsing import read_by_line, read_with_delimeter

DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def parse_data(s: str):
    return [int(x) for x in s if x != '']

def dijkstras(start: int, end: int, edge_dict: dict, min_steps=4, max_steps=10):
    h = [(0, d, 0, start, [start]) for d in range(len(DIRS))]
    visited = [[[0 for _ in range(10)] for _ in DIRS] for x in edge_dict.keys()]
    while len(h) > 0:
        dist, dir, dir_count, curr, path = heapq.heappop(h)
        if curr == end:
            return dist, path
        if visited[curr][dir][dir_count-1] != 0:
            continue
        visited[curr][dir][dir_count-1] = 1
        for new_dir, (node, dist_to_neigh) in enumerate(edge_dict[curr]):
            # OOB
            if dist_to_neigh > 10:
                continue
            # Need to walk a minimum 4 steps in any direction
            if new_dir != dir and dir_count < min_steps:
                continue
            # Don't walk in the same path
            if node in path:
                continue
            new_dir_count = 1
            if new_dir == dir:
                if dir_count + 1 > max_steps:
                    continue
                new_dir_count = dir_count + 1
            new_path = path.copy()
            if visited[node][new_dir][new_dir_count-1] == 0:
                new_path.append(node)
                heapq.heappush(h, (dist+dist_to_neigh, new_dir, new_dir_count, node, new_path))
    return -1, []


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
    dist, _ = dijkstras(0, end, heat_mapping, min_steps=1, max_steps=3)
    print(dist)
    dist2, _ = dijkstras(0, end, heat_mapping)
    print(dist2)

if __name__ == "__main__":
    run()