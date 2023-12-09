import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [int(x) for x in s.split() if x != '']

def make_diffs(hist):
    diffs = [hist]
    i = 0
    finals_diffs = [hist[-1]]
    early_diffs = [hist[0]]
    while sum([abs(x) for x in diffs[i]]) != 0:
        new_diff = [diffs[i][j+1]-diffs[i][j] for j in range(len(diffs[i])-1)]
        diffs.append(new_diff)
        finals_diffs.append(new_diff[-1])
        early_diffs.append(new_diff[0])
        i+=1
    return early_diffs, finals_diffs

def extrapolate(diffs: list[int]):
    start = 0
    for diff in reversed(diffs):
        start += diff
    return start

def extrapolate_backwards(diffs: list[int]):
    start = 0
    for diff in reversed(diffs):
        start = diff - start
    return start

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    total = 0
    total2 = 0
    for hist in data:
        early_diffs, last_diffs = make_diffs(hist)
        total += extrapolate(last_diffs)
        total2 += extrapolate_backwards(early_diffs)
    print(total)
    print(total2)

if __name__ == "__main__":
    run()