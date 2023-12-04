import sys
sys.path.append('../')

from tools.parsing import read_by_line

# example format: Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
def parse_data(s):
    # only care about numbers since cards are already sorted
    num_ind = s.find(":")+2
    # Split card number vs winning numbers and make them into ints
    numbers = s[num_ind:].split(" | ")
    win_nbrs = [int(x) for x in numbers[0].split(" ") if x != ""]
    my_nbrs = [int(x) for x in numbers[1].split(" ") if x != ""]
    return (my_nbrs, win_nbrs)

def count_matches(a: list, b: list):
    count_matches = 0
    for nbr in a:
        for nbr2 in b:
            if nbr == nbr2:
                count_matches += 1
                break
    return count_matches

def run():
    cards = read_by_line("input.txt", parse_func=parse_data)

    # Keep track of total points and number of copies of each card we have
    total_points = 0
    card_copies = [1 for x in cards]

    for i, (my_nbrs, win_nbrs) in enumerate(cards):
        # Find the number of matches we have between
        card_matches = count_matches(my_nbrs, win_nbrs)
        if card_matches > 0:
            # Add the cards score to the total
            total_points += 2 ** (card_matches-1)
            # Add one copy of each next card into the list of cards
            start, end = i+1, min(i+1+card_matches, len(card_copies))
            for j in range(start, end):
                card_copies[j] += 1 * card_copies[i]
    print(total_points)
    print(sum(card_copies))

if __name__ == "__main__":
    run()