import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [int(x) for x in s.split(": ")[1].split(" ") if x != '']

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    time, dist = data[0], data[1]
    race_mult = 1
    for i in range(len(time)):
        t, d = time[i], dist[i]
        ds = [x*(t-x) for x in range(t)]
        count = 0
        for dx in ds:
            if dx > d:
                count += 1
        race_mult *= count
    print(race_mult)
    t1 = int(''.join([str(x) for x in time]))
    d1 = int(''.join([str(x) for x in dist]))
    ds = [x*(t1-x) for x in range(t1)]
    i, j = 0, len(ds)-1
    while ds[i] <= d1:
        i+=1
    while ds[j] <= d1:
        j-=1
    print(j-i+1)

if __name__ == "__main__":
    run()