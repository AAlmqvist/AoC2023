import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

DEBUG = False

# EAST, SOUTH, WEST, NORTH
DIRS = [(0, 1), (1,0), (0,-1), (-1, 0)]
OK_DIR = [['-', '7', 'No','J'], ['L','|','J','No'], ['No', 'F', '-','L'], ['F','No','7','|']]

def match_num(c):
    if c == -1:
        return '#'
    if c == -2:
        return 'O'
    return '.'

def print_pipes(pipes, loop):
    for r, row in enumerate(loop):
        print(''.join([pipes[r][c] if row[c]==1 else match_num(row[c]) for c in range(len(row))]))

def followPipeLoop(pipes: list[str], start: tuple[int,int]):
    loop_marked = []
    for r in pipes:
        row = []
        for c in r:
            row.append(0)
        loop_marked.append(row)
    nodes = []
    r_s, c_s = start
    loop_marked[r_s][c_s] = 1
    # Find a direction to start in
    dir = 0
    for i_dir, (dr, dc) in enumerate(DIRS):
        # Out of bounds
        if r_s+dr < 0 or r_s+dr >= len(pipes) or c_s+dc < 0 or c_s+dc >= len(pipes[0]):
            continue
        if pipes[r_s+dr][c_s+dc] in OK_DIR[i_dir]:
            dir = i_dir
            break
    r, c = start[0], start[1]
    nbrSteps = 0
    while True:
        # Fill loop and its borders
        loop_marked[r][c] = 1
        right_side, left_side = (dir+1) % 4, (dir+3) % 4
        dr_r, dc_r = DIRS[right_side]
        if r+dr_r >= 0 and r+dr_r < len(pipes) and c+dc_r >= 0 and c+dc_r < len(pipes[r]) and loop_marked[r+dr_r][c+dc_r] != 1:
            loop_marked[r+dr_r][c+dc_r] = -1
        dr, dc = DIRS[left_side]
        if r+dr >= 0 and r+dr < len(pipes) and c+dc >= 0 and c+dc < len(pipes[r]) and loop_marked[r+dr][c+dc] != 1:
            loop_marked[r+dr][c+dc] = -2
        # get positions going forward
        dr, dc = DIRS[dir]
        if pipes[r+dr][c+dc] == 'S':
            nbrSteps += 1
            break
        next_dir =  OK_DIR[dir].index(pipes[r+dr][c+dc])
        # Fill any corner missed
        if dir != next_dir:
            opp_dir = (next_dir + 2) % 4
            n_dr, n_dc = DIRS[opp_dir]
            # Assume it is left side and check if it matches right
            to_put = -2
            if n_dr == dr_r and n_dc == dc_r:
                to_put = -1
                if loop_marked[r+dr+n_dr][c+dc+n_dc] != 1:
                    loop_marked[r+dr+n_dr][c+dc+n_dc] = to_put
        r, c, dir = r+dr, c+dc, next_dir
        nbrSteps+=1

    return nbrSteps, loop_marked

def fill(loop: list[list[int]], start: tuple[int,int]):
    to_fill = []
    nodes = [start]
    fill_with = 0
    while nodes:
        new_nodes = []
        r, c = nodes[0]
        nodes = nodes[1:]
        to_fill.append((r, c))
        for dr, dc in DIRS:
            # Out of bounds
            if r+dr < 0 or r+dr >= len(loop) or c+dc < 0 or c+dc >= len(loop[r]):
                continue
            if loop[r+dr][c+dc] == 1:
                continue
            if loop[r+dr][c+dc] < 0:
                fill_with = loop[r+dr][c+dc]
                continue
            if (r+dr,c+dc) in to_fill:
                continue
            new_nodes.append((r+dr, c+dc))
        nodes = new_nodes
    if start[0] == 0 and start[1] == 0:
        fill_with
    for r, c in to_fill:
        loop[r][c] = fill_with
    return loop

def fill_space(loop):
    for r in range(len(loop)):
        for c in range(len(loop[r])):
            if loop[r][c] == 0:
                loop = fill(loop, (r, c))
    return loop

def run():
    pipes = read_by_line("input.txt")
    for i, row in enumerate(pipes):
        found = False
        for j in range(len(row)):
            if row[j] == 'S':
                start = (i, j)
                found = True
                break
        if found:
            break
    farthest_dist, loop = followPipeLoop(pipes, start)
    print(farthest_dist//2)
    loop = fill_space(loop)
    if DEBUG:
        print_pipes(pipes, loop)
        print("#", sum([sum([1 if c==-1 else 0 for c in x]) for x in loop]))
        print("O", sum([sum([1 if c==-2 else 0 for c in x]) for x in loop]))
    # Assume outer area is larger then enclosed are,
    print(min(sum([sum([1 if c==-1 else 0 for c in x]) for x in loop]), sum([sum([1 if c==-2 else 0 for c in x]) for x in loop])))
    
if __name__ == "__main__":
    run()