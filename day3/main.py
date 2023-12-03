import sys
sys.path.append('../')

from tools.parsing import read_by_line

def find_nbrs_and_syms(data):
    numbers = []
    symbols = []
    for i in range(len(data)):
        nbr = 0
        start_ind = 0
        for j in range(len(data[i])):
            next = data[i][j]
            # number
            if next >= '0' and next <= '9':
                if nbr == 0:
                    start_ind = j
                nbr = 10*nbr + int(next)
                continue
            # not a number, close any previous number parsing
            if nbr > 0:
                numbers.append((nbr, i, start_ind, j-1))
                # reset vals
                nbr = 0
                start_ind = 0
            # not interesting, skip
            if next == ".":
                continue
            # all other symbols should go into the symbols
            symbols.append((i, j, next))
        if nbr > 0:
            numbers.append((nbr, i, start_ind, j))
    return numbers, symbols

def find_motorparts(nums, syms):
    part_sum = 0
    gear_sum = 0
    for sym_row, sym_col, sym in syms:
        adj = 0
        gear_ratio = 1
        for part, row, s_col, e_col in nums:
            # Same row neighbors
            if sym_row == row and sym_col in [s_col-1, e_col+1]:
                part_sum += part
                adj += 1
                gear_ratio *= part
                continue
            # Check other rows
            for i in [row-1, row+1]:
                for j in range(s_col-1, e_col+2):
                    if sym_row == i and sym_col == j:
                        part_sum += part
                        adj += 1
                        gear_ratio *= part
                        continue
        if sym == "*" and adj == 2:
            gear_sum += gear_ratio
    return part_sum, gear_sum

def run():
    data = read_by_line("input.txt")
    nbrs, syms = find_nbrs_and_syms(data)
    part_sum, gear_sum = find_motorparts(nbrs, syms)
    print(part_sum)
    print(gear_sum)

if __name__ == "__main__":
    run()