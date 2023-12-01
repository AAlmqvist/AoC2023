import sys
sys.path.append('../')

from tools.parsing import read_by_line

def parseData(s, part1=False):
    digits = []
    for k in range(len(s)):
        try:
            n = int(s[k])
            digits.append(n)
        except:
            if part1:
                continue
            if k+3 > len(s):
                continue
            if s[k:k+3] == "one":
                digits.append(1)
            if s[k:k+3] == "two":
                digits.append(2)
            if s[k:k+3] == "six":
                digits.append(6)
            if k+4 > len(s):
                continue
            if s[k:k+4] == "four":
                digits.append(4)
            if s[k:k+4] == "five":
                digits.append(5)
            if s[k:k+4] == "nine":
                digits.append(9)
            if k+5 > len(s):
                continue
            if s[k:k+5] == "three":
                digits.append(3)
            if s[k:k+5] == "seven":
                digits.append(7)
            if s[k:k+5] == "eight":
                digits.append(8)
    return 10*digits[0] + digits[-1]

def run():
    data = read_by_line("input.txt")
    print("part1", sum([parseData(s, part1=True) for s in data]))
    print("part2", sum([parseData(s) for s in data]))

if __name__ == "__main__":
    run()