from const import *
from typing import List, Tuple
from random import shuffle
from itertools import combinations


def flushes(allfaces):
    f, fs = ((LFLIST, LOWFACES) if any(c == '2' for c in allfaces)
             else (FLIST, FACES))
    ordered = sorted(allfaces, key=lambda card: f.index(card))
    if ' '.join(ordered) in LOWFACES:
        return VALUES['straight flush'], ordered
    return VALUES['flush'], allfaces


def straight_or_nothing(allfaces):
    f, fs = ((LFLIST, LOWFACES) if any(c == '2' for c in allfaces)
             else (FLIST, FACES))
    ordered = sorted(allfaces, key=lambda card: f.index(card))
    if ' '.join(ordered) in LOWFACES:
        return VALUES['straight'], ordered
    return VALUES['HC'], allfaces


def pair(allfaces, allftypes):
    pair = next(c for c in allftypes if allfaces.count(c) == 2)
    allftypes.remove(pair)
    return VALUES['OP'], (pair, list(allftypes))


def foak_or_boat(allfaces, allftypes):
    for f in allftypes:
        if allfaces.count(f) == 4:
            allftypes.remove(f)
            return VALUES['FOAK'], (f, allftypes.pop())
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return VALUES['boat'], (f, allftypes.pop())


def toak_or_tp(allfaces, allftypes):
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return VALUES['TOAK'], (f, allftypes)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) == 2:
        other = (allftypes - set(pairs)).pop()
        return VALUES['TP'], (sorted(pairs, key=lambda f: CARDVALUES[f]), other)


def rank(hand: List[Card]):
    """
    :param hand:
    :return: score, hand
    """
    allstypes = {s for f, s in hand}
    allfaces = [f for f, s in hand]

    if len(allstypes) == 1:
        return flushes(allfaces)
    allftypes = set(allfaces)
    x = len(allftypes)

    if x == 5:
        return straight_or_nothing(allfaces)

    elif x == 4:
        return pair(allfaces, allftypes)

    elif x == 2:
        return foak_or_boat(allfaces, allftypes)

    elif x == 3:
        return toak_or_tp(allfaces, allftypes)

    return VALUES['HC'], allfaces


def parse(cards: str):
    """
    Generate cards for string (e.g. AD 5H = [A♦, 5♥])
    :param cards:
    :return:
    """
    hand = []
    cards = cards.lower()
    for card in cards.split():
        f, s = card[:-1], card[-1]
        assert f in FLIST, "Invalid: Don't understand card face %r" % f
        assert s in SUIT, "Invalid: Don't understand card suit %r" % s
        hand.append(Card(f, s))
    return tuple(hand)


def deal(deck: List[Card], n_board=5):
    """
    Function to get opponent cards and board
    :param deck: list of remaining cards
    :param n_board: number of cards to be dealt for the board
    :return: villain, board
    """
    shuffle(deck)
    return tuple(deck[:2]), tuple(deck[2:2+n_board])


def win_tie_list(your_tie, vill_tie):
    for j, card in enumerate(your_tie):
        temp = win_tie_card(card, vill_tie[j])
        if temp: return temp
    return 0


def win_tie_card(yc, vc):
    if CARDVALUES[yc] > CARDVALUES[vc]:
        return 1
    elif CARDVALUES[yc] < CARDVALUES[vc]:
        return -1
    return 0


def simulate(your_hand: Tuple[Card], board: Tuple[Card] = (), n_runs=100000, opp_range=100):
    """
    Simulate a run with given parameters
    :param your_hand: your cards
    :param board: cards on the board
    :param n_runs: number of runs to simulate
    :param opp_range: TO BE IMPLEMENTED
    :return:
    """
    deck = DECK.copy()

    for c in your_hand + board:
        deck.remove(c)
    n = 5-len(board)
    w, l = 0, 0
    for i in range(n_runs):
        villain, draws = deal(deck, n)
        newboard = board + draws
        best = max((x for x in combinations(your_hand+newboard, 5)), key=lambda x: rank(x)[0])
        his = max((x for x in combinations(villain+newboard, 5)), key=lambda x: rank(x)[0])
        your_score, your_tie = rank(best)
        vill_score, vill_tie = rank(his)
        if your_score > vill_score:
            w += 1
            continue
        elif vill_score > your_score:
            l += 1
            continue
        else:
            if your_score >= 5 or your_score == 1:
                temp = win_tie_list(sorted(your_tie, key=lambda c: CARDVALUES[c]),
                                    sorted(vill_tie, key=lambda c: CARDVALUES[c]))
                if temp == -1:
                    l += 1
                elif temp == 1:
                    w += 1
                continue

            elif your_score == VALUES['TP']:
                temp = win_tie_list(your_tie[0], vill_tie[0])
                if temp == -1:
                    l += 1
                elif temp == 1:
                    w += 1
                else:
                    temp = win_tie_card(your_tie[1], vill_tie[1])
                    if temp == -1:
                        l += 1
                    elif temp == 1:
                        w += 1

            else:
                temp = win_tie_card(your_tie[0], vill_tie[0])
                if temp == -1:
                    l += 1
                elif temp == 1:
                    w += 1
                else:
                    temp = win_tie_list(sorted(your_tie[1], key=lambda c: CARDVALUES[c]),
                                        sorted(vill_tie[1], key=lambda c: CARDVALUES[c]))
                    if temp == -1:
                        l += 1
                    elif temp == 1:
                        w += 1

    return w, l, n_runs


# if temp == -1:
#     print(your_score, your_tie, vill_tie)
