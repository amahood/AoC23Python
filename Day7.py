from enum import Enum

# class syntax
class HandType(Enum):
    UNSCORED = 10
    FIVEOFKIND = 7
    FOUROFKIND = 6
    FULLHOUSE = 5
    THREEOFKIND = 4
    TWOPAIR = 3
    ONEPAIR = 2
    HC = 1

def classify_hand(h):
    hand_type = HandType.UNSCORED
    unique_cards = []
    
    for c in h[0]:
        seen_before = False
        for s in unique_cards:
            if s[0] == c:
                seen_before = True
        if seen_before==False:
            unique_cards.append((c, h[0].count(c)))

    keep_scoring = True
    for uc in unique_cards:
        if keep_scoring == True:
            if uc[1] == 5:
                hand_type = HandType.FIVEOFKIND
                keep_scoring = False
            elif uc[1] == 4:
                hand_type = HandType.FOUROFKIND
                keep_scoring = False
            elif uc[1] == 3 and (hand_type == HandType.UNSCORED or hand_type == HandType.HC):
                hand_type = HandType.THREEOFKIND
            elif uc[1] == 3 and hand_type == HandType.ONEPAIR:
                hand_type = HandType.FULLHOUSE
                keep_scoring = False
            elif uc[1] == 2 and (hand_type == HandType.UNSCORED or hand_type == HandType.HC):
                hand_type = HandType.ONEPAIR
            elif uc[1] == 2 and hand_type == HandType.THREEOFKIND:
                hand_type = HandType.FULLHOUSE
                keep_scoring = False
            elif uc[1] == 2 and hand_type == HandType.ONEPAIR:
                hand_type = HandType.TWOPAIR
                keep_scoring = False
            elif uc[1] == 1 and (hand_type == HandType.HC or hand_type == HandType.UNSCORED):
                hand_type = HandType.HC
    return hand_type

def tiebreak(h1,h2):
    still_tied = True
    i = 0
    winner = 0
    while still_tied == True:
        if card_reference.index(h1[0][i]) == card_reference.index(h2[0][i]):
            still_tied = True
        elif card_reference.index(h1[0][i])> card_reference.index(h2[0][i]):
            still_tied = False
            winner = 2
        elif card_reference.index(h1[0][i])<card_reference.index(h2[0][i]):
            still_tied = False
            winner = 1
        i = i + 1
    return winner

def jokify_jand(h):
    num_jokers = h[0].count('J')
    
    if h[2] == HandType.HC and num_jokers == 1:
        h = (h[0],h[1],HandType.ONEPAIR)
    
    elif (h[2] == HandType.ONEPAIR):
        if num_jokers == 1:
            h = (h[0],h[1],HandType.THREEOFKIND)
        elif num_jokers == 2:
            h = (h[0],h[1],HandType.THREEOFKIND)   
        #3 would have come in as full house 

    elif (h[2] == HandType.TWOPAIR):
        if num_jokers == 1:
            h = (h[0],h[1],HandType.FULLHOUSE)
        elif num_jokers == 2:
            h = (h[0],h[1],HandType.FOUROFKIND)
        #3 would have come in as full house, 4/5 would have come in as x of kind

    elif (h[2] == HandType.THREEOFKIND):
        if num_jokers == 1 or num_jokers == 3:
            h = (h[0],h[1],HandType.FOUROFKIND)
        #two jokers would have come in as full house and 4 would have come in as four of kind

    elif (h[2] == HandType.FULLHOUSE):
        if num_jokers == 2 or num_jokers == 3:
            h = (h[0],h[1],HandType.FIVEOFKIND)
        #one joker not possible, 4 not possible, five not possi ble

    elif (h[2] == HandType.FOUROFKIND):
        if num_jokers == 1 or num_jokers == 4:
            h = (h[0],h[1],HandType.FIVEOFKIND)
            
    return h

#f = open("Day7TestInput.txt")
f = open("Day7Input.txt")
card_reference = ['A','K','Q','T','9','8','7','6','5','4','3','2','J']

hand_list = []
for l in f:
    hand_list.append((l.split(" ")[0], int(l.split(" ")[1])))

hand_list_classified = []
for h in hand_list:
    hand_type = classify_hand(h)
    hand_list_classified.append((h[0],h[1],hand_type))

hand_list_jokified = []
for h in hand_list_classified:
    h = jokify_jand(h)
    hand_list_jokified.append(h)

hand_list_sorted = []
hand_list_sorted.append(hand_list_jokified[0])

first_loop = True
for hc in hand_list_jokified:
    ss = len(hand_list_sorted)
    insert_tracker = 0
    keep_sorting = True
    i = 0
    if first_loop == False:
        while i < ss and keep_sorting == True:
            if hc[2].value > hand_list_sorted[i][2].value:
                insert_tracker = i
                keep_sorting = False
            elif hc[2].value == hand_list_sorted[i][2].value:
                winner = tiebreak(hc,hand_list_sorted[i])
                if winner == 1:
                    insert_tracker = i
                    keep_sorting = False
                if winner == 2:
                    insert_tracker = i+1
                    keep_sorting = True
            elif hc[2].value < hand_list_sorted[i][2].value:
                insert_tracker = i+1   
            i = i + 1
        hand_list_sorted.insert(insert_tracker, hc)
    first_loop = False

running_sum = 0
max_pts = len(hand_list_sorted)
for hs in hand_list_sorted:
    running_sum = running_sum + hs[1] * max_pts
    max_pts = max_pts - 1

print("total winnings - " + str(running_sum))


