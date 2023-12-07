import sys
sys.path.append('../')

from tools.parsing import read_by_line, read_with_delimeter

def parse_data(s):
    return [x for x in s.split(" ") if x != '']

def get_card_strength(card, part1=False):
    try:
        b = int(card)
        return b
    except:
        match card:
            case 'T':
                return 10
            case 'J':
                if part1:
                    return 11
                return 1
            case 'Q':
                return 12
            case 'K':
                return 13
            case 'A':
                return 14
    return None

def get_hand_strength(hand, part1=False):
    card_count = dict()
    for card in hand:
        if not card in card_count.keys():
            card_count[card] = 0
        card_count[card] += 1
    extra = 0
    if not part1 and 'J' in card_count:
        extra = card_count['J']
        del card_count['J']
        if extra == 5:
            return 7
    cards = [v for k, v in card_count.items()]
    cards.sort(reverse=True)
    cards[0] += extra
    match cards[0]:
        case 5:
            return 7
        case 4:
            return 6
        case 3:
            if cards[1] == 2:
                return 5
            return 4
        case 2:
            if cards[1] == 2:
                return 3
            return 2
    return 1

def get_total_winnings(data, part1=False):
    ranked_hands = []
    for hand, bid in data:
        hand_strength = get_hand_strength(hand, part1=part1) * 15 **6
        total_card_strength = sum([get_card_strength(hand[i], part1=part1) * 15**(len(hand)-i) for i in range(len(hand))])
        # Since the max value for any single card or hand strength is 14
        # we can create a integer that saves the specific values in base 15 where
        # the hand score is the largest value, followed by the first card and so on.
        # Ranking the cards after that is just a matter of sorting in descending order.
        unique_hand_score = hand_strength + total_card_strength
        ranked_hands.append((unique_hand_score, int(bid)))
    ranked_hands.sort()
    total_winning = 0
    for (rank, (_, bid)) in enumerate(ranked_hands):
        total_winning += (rank+1)*bid
    return total_winning

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    print(get_total_winnings(data, part1=True))
    print(get_total_winnings(data))

if __name__ == "__main__":
    run()