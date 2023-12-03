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
            for i in range(sym_row-1, sym_row+2):
                found = False
                for j in range(sym_col-1, sym_col+2):
                    if i == row and s_col <= j and e_col >= j:
                        part_sum += part
                        adj += 1
                        gear_ratio *= part
                        found = True
                        break
                if found:
                    break
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