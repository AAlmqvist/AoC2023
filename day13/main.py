import sys
sys.path.append('../')

import numpy as np

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [1 if x == "#" else 0 for x in s if x != '']

# def compare_slices(s1: np.array, s2: np.array):
#     if len(s1) != len(s2):
#         print("FAULTY LENGTH")
#         return False
#     for i in range(len(s1)):
#         if s1[i] != s2[i]:
#             return False
#     return True    

# def part1(cards):
#     reflection_lines = []
#     for k, card in enumerate(cards):
#         reflection_start = 0
#         r,c = card.shape
#         for i in range(r-1):
#             same = False
#             if compare_slices(card[i,:], card[i+1,:]):
#                 # Potential reflection point, make sure this pattern keeps until edge is hit
#                 d = 1
#                 same = True
#                 while i-d >= 0 and i+d+1 < r:
#                     if not compare_slices(card[i-d,:], card[i+d+1, :]):
#                         same = False
#                         break
#                     d += 1
#             if same:
#                 reflection_start = i
#                 break
#         if same:
#             reflection_lines.append((reflection_start+1, True))
#             continue
#         same = False
#         for i in range(c-1):
#             if compare_slices(card[:,i], card[:,i+1]):
#                 # Potential reflection point, make sure this pattern keeps until
#                 d = 1
#                 same = True
#                 while i-d >= 0 and i+d+1 < c:
#                     if not compare_slices(card[:,i-d], card[:, i+d+1]):
#                         same = False
#                         break
#                     d += 1
#             if same:
#                 reflection_start = i
#                 break
#         if same:
#             reflection_lines.append((reflection_start+1, False))
#     return reflection_lines

def get_diff(s1: np.array, s2: np.array) -> int:
    if len(s1) != len(s2):
        return 1000
    diff = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            diff += 1
    return diff

def find_reflection_lines(cards, match_diff=1):
    reflection_lines = []
    for k, card in enumerate(cards):
        reflection_start = -1
        r,c = card.shape
        for i in range(r-1):
            tot_diff = 0
            d = 0
            while i-d >= 0 and i+d+1 < r and tot_diff <= match_diff:
                tot_diff += get_diff(card[i-d,:], card[i+d+1, :])
                d += 1
            if tot_diff == match_diff:
                reflection_start = i
                break
        if reflection_start >= 0:
            reflection_lines.append((reflection_start+1, True))
            continue
        # Check vertical next
        for i in range(c-1):
            tot_diff = 0
            d = 0
            while i-d >= 0 and i+d+1 < c and tot_diff <= match_diff:
                tot_diff += get_diff(card[:,i-d], card[:, i+d+1])
                d += 1
            if tot_diff == match_diff:
                reflection_start = i
                break
        reflection_lines.append((reflection_start+1, False))
    return reflection_lines

def run():
    data = read_with_delimeter("input.txt", split_by="\n\n")
    cards = [np.array([parse_data(y) for y in x.split('\n') if y!='']) for x in data]
    reflection_lines = find_reflection_lines(cards, match_diff=0)
    # Calculate total
    reflection_total = sum([x[0]*100 if x[1] else x[0] for x in reflection_lines])
    print(reflection_total)
    new_reflection_lines = find_reflection_lines(cards)
    # Calculate total
    reflection_total2 = sum([x[0]*100 if x[1] else x[0] for x in new_reflection_lines])
    print(reflection_total2)

if __name__ == "__main__":
    run()