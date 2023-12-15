import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

DEBUG = False

def cust_hash(word):
    curr = 0
    for c in word:
        curr += ord(c)
        curr *= 17
        curr = curr % 256
    return curr

def getLatestBox(boxes) -> int:
    curr = [0]
    visited = []
    while curr:
        next_i = curr[0]
        curr = curr[1:]

def print_boxes(boxes):
    for i, b in enumerate(boxes):
        if len(b) > 0:
            print(f"Box {i}: [{', '.join([f'{key}={val}' for key, val in b])}]")

def run():
    data = read_with_delimeter("input.txt", split_by=',')
    tot = 0
    boxes = [[] for _ in range(256)]
    for word in data:
        if DEBUG:
            print("------------------------", word, "--------------------")
        word = word.replace('\n', '')
        tot += cust_hash(word)
        if '=' in word:
            info = word.split('=')
            label, focal_len = info[0], int(info[1])
            box_nbr = cust_hash(label)
            is_new = True
            for i in range(len(boxes[box_nbr])):
                if boxes[box_nbr][i][0] == label:
                    boxes[box_nbr][i] = (label, focal_len)
                    is_new = False
                    break
            if is_new:
                boxes[box_nbr].append((label, focal_len))
        if '-' in word:
            label = word[:-1]
            box_nbr = cust_hash(label)
            for i in range(len(boxes[box_nbr])):
                if boxes[box_nbr][i][0] == label:
                    boxes[box_nbr].pop(i)
                    break
        if DEBUG:
            print_boxes(boxes)
    print(tot)
    tot2 = 0
    for i, b in enumerate(boxes):
        for j, (label, focal_len) in enumerate(b):
            label_val = (i+1) * (j+1)*focal_len
            if DEBUG:
                print(label, "=>", label_val)
            tot2 += label_val
    print(tot2)

if __name__ == "__main__":
    run()