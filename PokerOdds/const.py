from collections import namedtuple


class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self).upper()


SUIT = 'h d c s'.split()

# ordered strings of faces
FACES = '2 3 4 5 6 7 8 9 10 j q k a'
LOWFACES = 'a 2 3 4 5 6 7 8 9 10 j q k'

# ordered list of faces
FLIST = tuple(FACES.split())
LFLIST = tuple(LOWFACES.split())

CARDVALUES = {c: i+2 for i, c in enumerate(FLIST[::-1])}

# dict of hand values
VALUES = {
    'straight flush': 9,
    'FOAK': 8,
    'boat': 7,
    'flush': 6,
    'straight': 5,
    'TOAK': 4,
    'TP': 3,
    'OP': 2,
    'HC': 1
}

DECK = [Card(f, s) for f in FLIST for s in SUIT]

_rev = FLIST[::-1]
CARDTABLE = []
for f1 in _rev:
    row = []
    for f2 in _rev:
        r = ''
        if f2 == f1: r = f1+ ' ' + f2
        elif _rev.index(f2) < _rev.index(f1):
            r = f2 + ' ' + f1 + 'o'
        else: r = f1 + ' ' + f2 + 's'
        row.append(r)
    CARDTABLE.append(row)
