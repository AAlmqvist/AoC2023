import sys
sys.path.append('../')

from tools.parsing import read_by_line

def run():
    input = read_by_line("input.txt", format_func=int)

if __name__ == "__main__":
    run()