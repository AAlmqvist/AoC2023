import sys
sys.path.append('../')
import time

from tools.parsing import read_by_line, read_with_delimeter

def parse_mappings(raw_mappings):
    mappings = dict()
    for d in raw_mappings:
        s = d.split(" = ")
        k, vals = s[0], s[1].split(", ")
        l, r = vals[0][1:], vals[1][:-1]
        mappings[k] = (l, r)
    return mappings

def navigate(mappings, move_order, start='AAA', end='ZZZ'):
    curr = start
    steps = 0
    while True:
        if curr == end:
            return steps
        lr = move_order[steps%len(move_order)]
        steps += 1
        curr = mappings[curr][lr]

def navigate_as_ghost(mappings, move_order, start):
    curr = start
    steps = 0
    while curr[-1] != 'Z':
        lr = move_order[steps%len(move_order)]
        curr = mappings[curr][lr]
        steps += 1
    return steps

def run():
    data = read_with_delimeter("input.txt", split_by="\n\n")
    move_order, raw_mappings = [1 if x == 'R' else 0 for x in data[0]], [x for x in data[1].split("\n") if x != '']
    mappings = parse_mappings(raw_mappings)
    print(navigate(mappings, move_order))
    starts = []
    for key in mappings.keys():
        if key[-1] == 'A':
            starts.append(key)
    periods = []
    for start in starts:
        period = navigate_as_ghost(mappings, move_order, start)
        periods.append(period)
    lcm_common = []
    # Find LCM (by dividing numbers by shared common denominators)
    max_check = max(periods) // 2
    for div in range(2, max_check):
        inds = [i for i in range(len(periods)) if periods[i] % div == 0]
        while len(inds) > 2:
            lcm_common.append(div)
            for j in inds:
                periods[j] = periods[j] // div
            inds = [i for i in range(len(periods)) if periods[i] % div == 0]
    LCM = 1
    for per in periods:
        LCM *= per
    for per in lcm_common:
        LCM *= per
    print(LCM)

if __name__ == "__main__":
    run()