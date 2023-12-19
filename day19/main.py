import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

XMAS_POS = {'x': 0, 'm': 1, 'a': 2, 's': 3}

def parse_starts(starts: list[str]):
    i = []
    for s in starts:
        if s == '':
            continue
        g = []
        for l in s.split(','):
            g.append(int(l.split('=')[1].replace('}', '')))
        i.append(g)
    return i

def parse_rules(rules: list[str]):
    rs = dict()
    for r in rules:
        if r == '':
            continue
        info = r.split('{')
        name, rest = info[0], info[1].replace('}','').split(',')
        rx = []
        for s in rest:
            sx = s.split(':')
            if len(sx) < 2:
                rx.append((-1, -1, -1, s))
                continue
            to = sx[1]
            m, d, val = sx[0][0], sx[0][1], sx[0][2:]
            dx = 1
            if d == '<':
                dx = 0
            rx.append((XMAS_POS[m], int(val), dx, to))
        rs[name] = rx
    return rs


def is_accepted(workflow, part):
    curr = 'in'
    while curr != 'R' and curr != 'A':
        for px, val, d, to in workflow[curr]:
            if px < 0:
                curr = to
                break
            if d > 0:
                if part[px] > val:
                    curr = to
                    break
            elif part[px] < val:
                curr = to
                break
    if curr == 'A':
        return sum(part)
    return 0

def find_accepted_ranges(start, workflow, part_ranges):
    if start == 'A':
        return [part_ranges]
    if start == 'R':
        return []
    curr = start
    accepted_ranges = []
    while curr != 'R' and curr != 'A':
        for px, val, d, to in workflow[curr]:
            if px < 0:
                curr = to
                break
            x1, x2 = part_ranges[px]
            # Should match upwards
            if d > 0:
                if x1 <= val and val < x2:
                    new_ranges = part_ranges.copy()
                    new_ranges[px] = (val+1, x2)
                    acc_ranges = find_accepted_ranges(to, workflow, new_ranges)
                    for nr in acc_ranges:
                        accepted_ranges.append(nr)
                    part_ranges[px] = (x1, val)
            elif x1 < val and val <= x2:
                new_ranges = part_ranges.copy()
                new_ranges[px] = (x1, val-1)
                acc_ranges = find_accepted_ranges(to, workflow, new_ranges)
                for nr in acc_ranges:
                    accepted_ranges.append(nr)
                part_ranges[px] = (val, x2)
                curr = to
    if curr == 'A':
        accepted_ranges.append(part_ranges)
    return accepted_ranges

def run():
    data = read_with_delimeter("input.txt", split_by='\n\n')
    workflow, parts = parse_rules(data[0].split('\n')), parse_starts(data[1].split('\n'))
    p1 = 0
    for part in parts:
        p1 += is_accepted(workflow, part)
    print(p1)
    accepted_ranges = find_accepted_ranges('in', workflow, [(1,4000) for _ in XMAS_POS])
    i = 0
    combs = 0
    for ar in accepted_ranges:
        c = 1
        for x1, x2 in ar:
            c *= x2-x1+1
        combs += c
        i+= 1
    print(combs)

if __name__ == "__main__":
    run()