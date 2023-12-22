import sys
sys.path.append('../')
import numpy as np

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [[int(x) for x in y.split(',') if x != ''] for y in s.split('~') if y != '']

def map_bricks(data):
    bricks = []
    for e1, e2 in data:
        brick = []
        if e1[0] != e2[0]:
            for x in range(e1[0], e2[0]+1):
                brick.append((x, e1[1], e1[2]))
        elif e1[1] != e2[1]:
            for y in range(e1[1], e2[1]+1):
                brick.append((e1[0], y, e1[2]))
        else:
            for z in range(e1[2], e2[2]+1):
                brick.append((e1[0], e1[1], z))
        bricks.append(brick)
    return bricks

def let_bricks_fall(bricks):
    # sort bricks by falling heights
    bricks.sort(key=lambda x: x[0][2])
    support_map = [[] for _ in bricks]
    settled = dict()
    for i in range(len(bricks)):
        b = bricks[i]
        # if the brick is vertical, only compare the bottom part when falling
        if len(b) < 2 or b[0][2] != b[1][2]:
            x, y, z = b[0]
            j = 0
            supp = -1
            while z-j > 1:
                if (x,y,z-j-1) in settled:
                    supp = settled[(x,y,z-j-1)]
                    break
                j += 1
            support_map[i] = [supp]
            for x, y, z in b:
                settled[(x,y,z-j)] = i
            continue
        # brick lays in x or y direction
        supported_by = []
        z_s = b[0][2]
        while z_s > 1:
            for x, y, _ in b:
                if (x, y, z_s-1) in settled:
                    if settled[x,y,z_s-1] not in supported_by:
                        supported_by.append(settled[x,y,z_s-1])
            if supported_by:
                break
            z_s -= 1
        support_map[i] = supported_by
        for x, y, _ in b:
            settled[(x, y, z_s)] = i
    return support_map

def remove(support_map:list[list[int]], i: int):
    tot = 0
    to_remove = []
    for (j, sm) in enumerate(support_map):
        if i in sm:
            sm.remove(i)
            if not sm:
                tot += 1
                to_remove.append(j)
    for j in to_remove:
        tot += remove(support_map, j)
    return tot

def run():
    data = read_by_line('input.txt', parse_func=parse_data)
    support_map = let_bricks_fall(map_bricks(data))
    nbr_safe_remove = 0
    for i in range(len(support_map)):
        is_safe = True
        for sm in support_map:
            if i in sm and len(sm) == 1:
                is_safe = False
                break
        if is_safe:
            nbr_safe_remove += 1
    print(nbr_safe_remove)
    tot_falls = 0
    for i in range(len(support_map)):
        support_map_copy = [sm.copy() for sm in support_map]
        tot_falls += remove(support_map_copy, i)
    print(tot_falls)

if __name__ == "__main__":
    run()