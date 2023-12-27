import sys
sys.path.append('../')
import numpy as np
from scipy.linalg import solve

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [np.array([int(y) for y in x.split(', ')]) for x in s.split(' @ ')]

def find_colisions_2d(hail, min_range, max_range):
    particles = []
    for h in hail:
        particles.append((h[0][:2], h[1][:2]))
    collisions = 0
    for i in range(len(particles)):
        pos1, vel1 = particles[i]
        for j in range(i+1, len(particles)):
            pos2, vel2 = particles[j]
            a = np.array([vel1, -vel2]).T
            b = pos2-pos1
            try:
                x = solve(a, b)
            except:
                # Matrix was singular, parallel lines/no intersection
                continue
            if x[0] < 0 or x[1] < 0:
                # intersection already happened
                continue
            x_col = pos1[0]+vel1[0]*x[0]
            y_col = pos1[1]+vel1[1]*x[0]
            # Check if colision was in the past
            if x_col < min_range or x_col > max_range:
                continue
            if y_col < min_range or y_col > max_range:
                continue
            collisions += 1
    return collisions

def find_closest_points(line1, line2):
    b = line2[0]-line1[0]
    A = np.array([line1[1], -line2[1]]).T
    return np.linalg.pinv(A) @ b

# For each line we can set x+dx*t = a+da*t for (x,y)+(dx,dy)*t and (a,b)+(da,db)*t
# Then we can get t = t  <=>  (a-x)(dy-db) = (b-y)(dx-da)
# This will lead to a non.linear equation as we will have terms x*dy and y*dx in them.
# But doing this equation for two lines we can achieve a linear equation to solve to x, y, dx and dy
#
# After this we only need 4 pairs of different lines to solve the linear equation
def get_row(line1, line2):
    x, dx = line1
    y, dy = line2
    return np.array([dy[1]-dx[1], x[1]-y[1], dx[0]-dy[0], y[0]-x[0]]), y[0]*dy[1]-y[1]*dy[0]+x[1]*dx[0]-x[0]*dx[1]

def run():
    filename = 'input.txt'
    hail = read_by_line(filename, parse_func=parse_data)
    min_r, max_r = 200000000000000, 400000000000000
    if filename == 'test.txt':
        min_r, max_r = 7, 27
    p1 = find_colisions_2d(hail, min_r, max_r)
    print(p1)
    A = []
    b = []
    for i in range(4):
        row_x, b_x = get_row(hail[0], hail[i+1])
        A.append(row_x)
        b.append(b_x)
    A = np.array(A)
    b = np.array(b)
    # Solve equation to find (x,y) + (dx, dy)*t
    x = solve(A, b)
    # Using the information from x,y-plane we can fetch the time we intersect two other lines
    line1, line2 = hail[0], hail[1]
    t1 = (line1[0][0]-x[0]) / (x[1]-line1[1][0])
    t2 = (line2[0][0]-x[0]) / (x[1]-line2[1][0])
    # Solve for z and dz using the time of intersection with two lines
    A2 = np.array([[1, t1], [1, t2]])
    b2 = np.array([line1[0][2] + line1[1][2]*t1, line2[0][2] + line2[1][2]*t2])
    z = solve(A2, b2)
    print(int(round(x[0])+round(x[2])+round(z[0])))

if __name__ == "__main__":
    run()