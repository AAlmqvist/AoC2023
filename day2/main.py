import sys
sys.path.append('../')

from tools.parsing import read_by_line

def run():
    data = read_by_line("input.txt")

if __name__ == "__main__":
    run()