import sys
sys.path.append('../')
import numpy as np

from tools.parsing import read_by_line, read_with_delimeter

DEBUG = False
DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def walk_to_next_branchoff(trails, start, dir):
    x, y = start[0] + DIRS[dir][0], start[1] + DIRS[dir][1]
    steps = 0
    upphill = False
    visited = set([(start[0], start[1])])
    while True:
        visited.add((x,y))
        steps += 1
        match trails[x][y]:
            case 'v':
                if dir != 1:
                    upphill = True
            case '^':
                if dir != 3:
                    upphill = True
            case '>':
                if dir != 0:
                    upphill = True
            case '<':
                if dir != 2:
                    upphill = True
        neighbs = []
        for n_dir, (dx, dy) in enumerate(DIRS):
            nx, ny = x+dx, y+dy
            if (nx, ny) in visited:
                continue
            if trails[nx][ny] == '#':
                continue
            # Found entrance/exit
            if nx == 0 or nx == len(trails)-1:
                return (nx, ny), steps, upphill
            neighbs.append((nx, ny, n_dir))
        if len(neighbs) > 1:
            break
        x, y, dir = neighbs[0]
    return (x, y), steps, upphill

def find_all_branchoffs(trails):
    branch_offs = dict()
    for i in range(1,len(trails)-1):
        for j in range(1,len(trails[i])-1):
            nbs = []
            if trails[i][j] == '.':
                for d in range(len(DIRS)):
                    di, dj = DIRS[d]
                    if trails[i+di][j+dj] != '#':
                        nbs.append(d)
            if len(nbs) > 2:
                branch_offs[(i, j)] = []

    to_add = []
    # Add the neighboring branchoffs to the dict
    for x,y in branch_offs.keys():
        for dir in range(len(DIRS)):
            if trails[x+DIRS[dir][0]][y+DIRS[dir][1]] != '#':
                point, steps, upphill = walk_to_next_branchoff(trails, (x, y), dir)
                branch_offs[(x,y)].append((point, steps, upphill))
                if point[0] == 0 or point[0] == len(trails)-1:
                    to_add.append((point, [((x,y), steps, False)]))
    for point, node in to_add:
        branch_offs[point] = node
    return branch_offs

def hike(branchoffs, start, end, visited, steps, slippery=False):
    # Shouldn't end up with start == end, but nice catch all
    if start == end:
        return
    visited.add(start)
    nodes = branchoffs[start]
    # Fast iteration through neihbors to see if we are next to the end
    # as this is a DFS search
    for i in range(len(nodes)):
        if nodes[i][0] == end:
            return steps+nodes[i][1]
    possible_steps = []
    for pos, new_steps, upphill in nodes:
        if pos in visited:
            continue
        if slippery and upphill:
            continue
        possible_steps.append(hike(branchoffs, pos, end, visited.copy(), steps+new_steps, slippery))
    if possible_steps:
        return max(possible_steps)
    return -1

def run():
    trails = read_by_line('input.txt')
    start = (0, trails[0].find('.'))
    end = (len(trails)-1, trails[-1].find('.'))
    branch_offs = find_all_branchoffs(trails)
    # Add 2 as I seem to have missed two steps (probably one each step at start and stop)
    print(hike(branch_offs, start, end, set(), 0, slippery=True)+2)
    print(hike(branch_offs, start, end, set(), 0)+2)

if __name__ == "__main__":
    run()