import sys
sys.path.append('../')
import numpy as np

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    d = []
    for x in s:
        if x == '':
            continue
        if x == 'O':
            d.append(1)
            continue
        if x == '#':
            d.append(-1)
            continue
        d.append(0)
    return d

def print_dish(dish: np.ndarray):
    r, c = dish.shape
    for i in range(r):
        to_print = ''
        for j in range(c):
            if dish[i,j] == 0:
                to_print += '.'
            elif dish[i,j] == 1:
                to_print += 'O'
            else:
                to_print += '#'
        print(to_print)

def tilt_up(dish: np.ndarray):
    r, c = dish.shape
    i, j = 0, 0
    while i < r:
        while j < c:
            if dish[i, j] == 1:
                di = i
                # Current position is [di, j]
                while di > 0 and dish[di-1, j] == 0:
                    # Move rock up, leaving empty space behind
                    dish[di-1, j] = 1
                    dish[di, j] = 0
                    di -= 1
            j += 1
        j = 0
        i += 1
    return dish

def calculate_support_total(dish: np.ndarray) -> int:
    total = 0
    r, c = dish.shape
    for i in range(r):
        for j in range(c):
            if dish[i,j] == 1:
                total += r-i
    return total

def find_cycle(hist: list[int]) -> list[int]:
    wind = 4
    cmp_wind = hist[-4:]
    # Start one window length before
    i = len(hist)-wind-1
    while i > wind:
        n_wind = hist[i:i+wind]
        same = True
        for j in range(wind):
            if cmp_wind[j] != n_wind[j]:
                same = False
                break
        if same:
            cycle_len = len(hist) - wind - i 
            return hist[-cycle_len:]
        i -= 1
    print("NO CYCLE :(")
    return []

def run():
    dish = np.array(read_by_line("input.txt", parse_func=parse_data))
    max_cycles = 1000000000
    load_hist = []
    curr = 0
    for i in range(max_cycles):
        for j in range(4):
            dish = tilt_up(dish)
            # Print part 1
            if i == 0 and j == 0:
                print(calculate_support_total(dish))
            # Rotate the matrix
            dish = np.rot90(dish, -1)
        load = calculate_support_total(dish)
        load_hist.append(load)
        # Assumed I would find a stable cycle within this range
        if i == 150:
            curr = i
            break
    # Find cycle
    cycle = find_cycle(load_hist)
    cycle_len = len(cycle)
    nbr_iters_left = max_cycles - curr - 1
    ends_on = nbr_iters_left % cycle_len
    print(cycle[ends_on-1])

if __name__ == "__main__":
    run()