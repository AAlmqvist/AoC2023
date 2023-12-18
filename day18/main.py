import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    info = s.split()
    return (info[0], int(info[1]), info[2][2:-1])


# Find vertical digs
def digOut(inst: list[int,int]) -> tuple[list[int,int,int],list[int,int,int]]:
    x, y = 0, 0
    vert = []
    horiz = []
    for dir, num in inst:
        match dir:
            case 'U':
                vert.append((x, y-num, y, 1))
                y -= num
            case 'D':
                vert.append((x, y, y+num, 0))
                y += num
            case 'R':
                horiz.append((y, x, x+num))
                x += num
            case 'L':
                horiz.append((y, x-num, x))
                x -= num
    return vert, horiz

def fill(vert: list[int,int,int], horiz: list[int,int,int]):
    filled = 0

    # List of y-values with horizontal edges for smarter solution
    break_points = list(set([x[0] for x in horiz]))
    break_points.sort()

    # Only calculate specific rows where we have new values
    for row in range(len(break_points)):
        y1 = break_points[row]
        xs = [v for v in vert if y1 >= v[1] and y1 <= v[2]]
        xs.sort()
        h = [(hx[1], hx[2]) for hx in horiz if hx[0] == y1]
        area_row = fill_row(xs, h)
        filled += area_row
        # If we have any rows without horizontal edges between
        # Find that area and multiply by number of rows
        if row+1 < len(break_points) and break_points[row+1] > y1+1:
            y2 = break_points[row] + 1
            xs = [v for v in vert if y2 > v[1] and y2 < v[2]]
            xs.sort()
            h = [(hx[1], hx[2]) for hx in horiz if hx[0] == y2]
            area_row = fill_row(xs, h)
            n_rows = break_points[row+1]-y1-1
            filled += area_row*n_rows

    return filled

def fill_row(xs, h):
    filled = 0
    i = 0
    # Start outside the area
    inside = False
    for i in range(len(xs)-1):
        filled += 1
        x1, x2 = xs[i], xs[i+1]
        between = x2[0]-x1[0]-1
        # On horizontal line, add 
        if (x1[0], x2[0]) in h:
            filled += between
            # Flip to flip back on next turn
            if x2[3] != x1[3]:
                inside = not inside
            continue
        # On an edge
        inside = not inside
        if inside:
            filled += between
    filled += 1
    return filled

def decode_hex(col: str) -> tuple[str, int]:
    dist = int(col[:-1], 16)
    match int(col[-1]):
        case 0:
            dir = 'R'
        case 1:
            dir = 'D'
        case 2:
            dir = 'L'
        case 3:
            dir = 'U'
    return dir, dist

def run():
    inst = read_by_line("input.txt", parse_func=parse_data)
    vert, horiz = digOut([(x,y) for x, y, _ in inst])
    p1 = fill(vert, horiz)
    print(p1)
    vert, horiz = digOut([decode_hex(col) for _, _, col in inst])
    p2 = fill(vert, horiz)
    print(p2)

if __name__ == "__main__":
    run()