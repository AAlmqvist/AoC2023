import sys
sys.path.append('../')
import time

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    info = s.split()
    row, expected = info[0], info[1]
    return (row, expected)

def fits(s: str, l: int) -> (bool, str):
    if l > len(s):
        return False, ""
    if sum([1 if s[i] == '.' else 0 for i in range(l)]) > 0 :
        return False, ""
    # Fit exactly on last line
    if len(s) == l:
        return True, ""
    # Make sure the next char does not continue the chunk
    if s[l] == "#":
        return False, ""
    return True, s[l+1:]

def find_layouts(s: str, s_ind: int, e_ind: int, expected: list[int], mem: list[list[tuple[int,str]]]):    
    # No chunks left to fit, check if rest can be just funcitoning space
    if not expected:
        if sum([1 if s[i] == '#' else 0 for i in range(len(s))]) > 0 :
            return 0, mem
        return 1, mem

    # cannot fit
    if expected[0] > len(s):
        return 0, mem
    
    # If we have already visited this branch
    if e_ind < len(mem) and s_ind < len(mem[e_ind]) and mem[e_ind][s_ind][0] >= 0:
        return mem[e_ind][s_ind][0], mem

    # Find next ? or #
    i = 0
    while i < len(s) and s[i] == '.':
        i += 1

    # Couldn't find any more space to fill
    if i == len(s):
        return 0, mem

    new_s = s[i:]
    nbr_combs = 0
    # Check if we fit on current index
    does_fit, inner_s = fits(new_s, expected[0])
    if does_fit:
        # Only one left and it fit perfectly
        if len(new_s) == expected[0]:
            # If there were more numbers left, we did not fit
            if len(expected) > 1:
                return 0, mem
            return 1, mem
        # Check all combinations of numbers left
        if sum([0 if x=='.' else 1 for x in inner_s]) >= sum(expected[1:]):
            new_combs, mem = find_layouts(inner_s, s_ind+len(s)-len(inner_s), e_ind+1, expected[1:], mem)
            nbr_combs += new_combs
    # Check any subsequent version if we have the option to
    if new_s[0] == '?' and sum([0 if x=='.' else 1 for x in new_s[1:]]) >= sum(expected):
        new_combs, mem = find_layouts(new_s[1:], s_ind+len(s)-len(new_s[1:]), e_ind, expected, mem)
        nbr_combs += new_combs

    # Add to memory
    if e_ind < len(mem) and s_ind < len(mem[e_ind]):
        mem[e_ind][s_ind] = (nbr_combs, s)

    return nbr_combs, mem

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    total = 0
    for row, expected_raw in data:
        expected = [int(x) for x in expected_raw.split(",") if x != '']
        mem = [[(-1, "") for _ in range(len(row))] for _ in range(len(expected))]
        nbr, _ = find_layouts(row, 0, 0, expected, mem)
        total += nbr
    print(total)

    done = 0
    total2 = 0
    for i, (row, expected_raw) in enumerate(data):
        new_row = '?'.join([row for _ in range(5)])
        expected = [int(x) for x in ','.join([expected_raw for _ in range(5)]).split(",") if x != '']
        mem = [[(-1, "") for _ in range(len(new_row))] for _ in range(len(expected))]
        nbr, mem = find_layouts(new_row, 0, 0, expected, mem)
        total2 += nbr
    print(total2)

if __name__ == "__main__":
    run()