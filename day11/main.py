import sys
sys.path.append('../')

# Using numpy merely for the nice properties with taking a slice in both directions
import numpy as np

from tools.parsing import read_by_line

FAR_EXPAND = 10**6

def parse_data(s):
    return [1 if x=='#' else 0 for x in s]

def expand(data):
    starts = []
    expand_rows = []
    expand_cols = []
    i, j = data.shape
    for r in range(i):
        if np.sum(data[r, :]) == 0:
            expand_rows.append(r)
        for c in range(j):
            if np.sum(data[:, c]) == 0 and c not in expand_cols:
                expand_cols.append(c)
            if data[r,c] == 1:
                starts.append((r,c))
    return starts ,expand_rows, expand_cols

def run():
    data = np.array(read_by_line("input.txt", parse_func=parse_data))
    starts, d_rows, d_cols = expand(data)
    total = 0
    total_far = 0
    for i in range(len(starts)):
        x1, y1 = starts[i]
        for x2, y2 in starts[i+1:]:
            dx, dy = abs(x2-x1), abs(y2-y1)
            nx, ny = 0, 0
            for x_n in d_rows:
                if x_n > min(x1, x2) and x_n < max(x1, x2):
                    nx += 1
            for y_n in d_cols:
                if y_n > min(y1, y2) and y_n < max(y1, y2):
                    ny += 1
            # Expanded L1-norm (manhattan distance)
            total += dx + nx + dy + ny
            total_far += dx + dy + nx*(FAR_EXPAND-1) + ny*(FAR_EXPAND-1)
    print(total)
    print(total_far)

if __name__ == "__main__":
    run()