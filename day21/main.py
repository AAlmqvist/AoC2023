import sys
sys.path.append('../')
import numpy as np

from tools.parsing import read_by_line, read_with_delimeter

DEBUG = False
DIRS = [(0,1), (1, 0), (0,-1), (-1,0)]
STEPS_PART1 = 64
STEPS_PART2 = 26501365

def print_garden(garden):
    rm, cm = garden.shape
    for i in range(rm):
        to_print = ''
        for j in range(cm):
            num = str(garden[i,j])
            to_print += ' '*(4-len(num)) + num
        print(to_print)

def parse_data(s):
    r = []
    for sx in s:
        match sx:
            case '.':
                r.append(0)
            case '#':
                r.append(-1)
            case 'S':
                r.append(2)
    return r

def walk(garden: np.ndarray, start: tuple[int,int]) -> np.ndarray:
    rm, cm = garden.shape
    seen = set()
    # seen.add(start)
    curr = set([start])
    steps = 0
    # for i in range(steps):
    while curr:
        next_iter = set()
        # Find new points
        for r, c in curr:
            for dr, dc in DIRS:
                x, y = r+dr, c+dc
                if x < 0 or x >= rm or y < 0 or y >= cm:
                    continue
                if garden[x, y] == 0 and (x, y) not in seen:
                    garden[x, y] = steps+1
                    next_iter.add((x,y))
                    seen.add((x,y))
        # seen = curr
        if len(next_iter) < 1:
            return garden
        curr = next_iter
        steps += 1
    return garden

def walk_set_steps(garden, start, steps):
    rm, cm = garden.shape
    seen = set()
    seen.add(start)
    curr = seen.copy()
    tot = 1
    odd = 0
    even = 0
    sum_outer_diags = 0
    sum_inner_diags = 0
    sum_points = 0
    num_full = steps // cm
    for i in range(steps):
        next_iter = set()
        # Find new points
        for r, c in curr:
            for dr, dc in DIRS:
                x, y = r+dr, c+dc
                if garden[x%rm, y%cm] == 0 and (x, y) not in seen:
                    if i%2 != steps%2:
                        dx, dy = x//rm, y//cm
                        if x >= 0 and x < rm and y >=0 and y < cm:
                            odd += 1
                        elif x >= rm and x < 2*rm and y >= 0 and y < cm:
                            even += 1
                        if abs(dx) + abs(dy) == num_full+1:
                            sum_outer_diags += 1
                        if abs(dx) + abs(dy) == num_full:
                            if dx == 0 or dy == 0:
                                sum_points += 1
                            else:
                                sum_inner_diags += 1
                    next_iter.add((x,y))
                    seen.add((x,y))
        if i%2 != steps%2:
            tot += len(next_iter)
        curr = next_iter
    return tot, odd, even, sum_points, sum_inner_diags // (num_full-1), sum_outer_diags // num_full

def quad(y, n):
    # Use the quadratic formula to find the output at the large steps based on the first three data points
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c

def run():
    filename = 'input.txt'
    garden = np.array(read_by_line(filename, parse_func=parse_data))
    sx, sy = -1, -1
    rm, cm = garden.shape
    for i in range(rm):
        for j in range(cm):
            if garden[i,j] == 2:
                sx, sy = i, j
                garden[i,j] = 0
                break

    steps1 = STEPS_PART1
    if filename == 'test.txt':
        steps1 = 6
    garden_middle = walk(garden.copy(), (sx,sy))

    nbr_walked_1 = 0
    for i in range(rm):
        nbr_walked_1 += sum([1 if x > 0 and x%2 == steps1%2 and x <= steps1 else 0 for x in garden_middle[i,:]])
    print(nbr_walked_1)

    steps2 = STEPS_PART2
    # Test case is harder since it is not as sparse as real input

    # Walk a smaller maze with same properties for sub-squares
    steps2 = 4*cm+65
    num_full = steps2 // cm

    _, odd, even, points, inner_diags, outer_diags = walk_set_steps(garden, (sx, sy), steps2)
    
    # Calcuate large maze with parts from smaller maze
    num_full = STEPS_PART2 // cm
    inner = odd
    for i in range(1, num_full):
        if i%2 == 0:
            inner += 4 * i * odd
            continue
        inner += 4 * i * even
    edges = points + inner_diags * (num_full-1) + outer_diags * num_full

    print(inner + edges)


if __name__ == "__main__":
    run()