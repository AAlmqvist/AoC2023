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

def getTotalWinnings(data, part1=False):
    ranked_hands = []
    for hand, bid in data:
        strength = get_hand_strength(hand, part1=part1)
        ind = len(ranked_hands)
        for i in range(len(ranked_hands)):
            _, in_hand, in_str = ranked_hands[i]
            if strength < in_str:
                ind = i
                break
            if strength > in_str:
                continue
            found = False
            str1 = [get_card_strength(c, part1=part1) for c in hand]
            str2 = [get_card_strength(c, part1=part1) for c in in_hand]
            found = False
            for j in range(len(str1)):
                if str1[j] < str2[j]:
                    ind = i
                    found = True
                    break
                if str1[j] > str2[j]:
                    break
            if found:
                break
        ranked_hands.insert(ind, (int(bid), hand, strength))
    total_winning = 0
    for (rank, (bid, _, _)) in enumerate(ranked_hands):
        total_winning += (rank+1)*bid
    return total_winning

def run():
    data = read_by_line("input.txt", parse_func=parse_data)
    print(getTotalWinnings(data, part1=True))
    print(getTotalWinnings(data))

if __name__ == "__main__":
    run()