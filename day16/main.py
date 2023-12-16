import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

# right, down, left, up
DIRS = [(0,1), (1,0), (0,-1), (-1,0)]
REFL = {
    '/': (3, 2, 1, 0),
    '\\': (1, 0, 3 , 2),
}

def run_light(mirrors: list[list[str]], start: tuple[int,int,int]):
    beams = [start]
    visited = [[[0 for _ in range(4)] for _ in range(len(row))] for row in mirrors]
    step = 0
    while beams:
        step += 1
        to_add = []
        for r,c,d in beams:
            nr, nc = r+DIRS[d][0], c+DIRS[d][1]
            # OUT OF BOUNDS
            if nr < 0 or nr >= len(mirrors) or nc < 0 or nc >= len(mirrors[0]):
                continue
            r, c = nr, nc
            m = mirrors[r][c]
            match m:
                case '.':
                    to_add.append((r, c, d))
                case '/' | '\\':
                    to_add.append((r, c, REFL[m][d]))
                case '|':
                    # coming from left/right will split the beam
                    if d % 2 == 0:
                        to_add.append((r,c,1))
                        to_add.append((r,c,3))
                        continue
                    # else pass through as normal
                    to_add.append((r, c, d))
                case '-':
                    # coming from left/right will split the beam
                    if d % 2 == 1:
                        to_add.append((r,c,0))
                        to_add.append((r,c,2))
                        continue
                    # else pass through as normal
                    to_add.append((r, c, d))
                case _ :
                    print("NO MATCH FOR", m)
        beams = []
        for nr, nc, nd in to_add:
            if visited[nr][nc][nd] > 0:
                # Now the cycle repeats
                continue
            visited[nr][nc][nd] = step
            beams.append((nr, nc, nd))
    return sum([sum(1 if sum(col) > 0 else 0 for col in row)for row in visited])

def run():
    mirrors = read_by_line("input.txt")
    max_energized = 0
    # Check all starting points left/right
    for i in range(len(mirrors)):
        nbr_energized = run_light(mirrors, (i, -1, 0))
        if i == 0:
            print(nbr_energized)
        if nbr_energized > max_energized:
            max_energized = nbr_energized
        nbr_energized = run_light(mirrors, (i, len(mirrors[0]), 2))
        if nbr_energized > max_energized:
            max_energized = nbr_energized
    # Check all starting points up/down
    for j in range(len(mirrors[0])):
        nbr_energized = run_light(mirrors, (-1, j, 1))
        if nbr_energized > max_energized:
            max_energized = nbr_energized
        nbr_energized = run_light(mirrors, (len(mirrors), j, 3))
        if nbr_energized > max_energized:
            max_energized = nbr_energized
    print(max_energized)

if __name__ == "__main__":
    run()