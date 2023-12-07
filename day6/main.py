import sys
sys.path.append('../')
import numpy as np

from tools.parsing import read_by_line

def parse_data(s):
    return [int(x) for x in s.split(": ")[1].split(" ") if x != '']

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    time, dist = data[0], data[1]
    # This problem is just solving the formula: x^2-t*x >= d (find x)
    # Part 1
    race_mult = 1
    for i in range(len(time)):
        t, d = time[i], dist[i]
        lower_bound = int(np.ceil(t/2 - np.sqrt(t**2/4-d)))
        upper_bound = int(np.floor(t/2 + np.sqrt(t**2/4-d)))
        race_mult *= (upper_bound-lower_bound+1)
    print(race_mult)
    # Part 2
    t1 = int(''.join([str(x) for x in time]))
    d1 = int(''.join([str(x) for x in dist]))
    lower_bound = int(np.ceil(t1/2 - np.sqrt(t1**2/4-d1)))
    upper_bound = int(np.floor(t1/2 + np.sqrt(t1**2/4-d1)))
    print(upper_bound-lower_bound+1)

if __name__ == "__main__":
    run()