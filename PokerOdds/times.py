from functions import *
import timeit
import shlex
from const import *

# functions used for profiling and testing

hands = ["2h 2d 2c kc qd",
         "2h 5h 7d 8c 9s",
         "ah 2d 3c 4c 5d",
         "2h 3h 2d 3c 3d",
         "2h 7h 2d 3c 3d",
         "2h 7h 7d 7c 7s",
         "10h jh qh kh ah",
         "4s 4s ks 5d 10s",
         "qc 10c 7c 6c 4c"
         ]
handCards = [parse(x) for x in hands]
handList = [sorted([c.face for c in hand], key=lambda card: LFLIST.index(card)) for hand in handCards]
sims = 5000


def f():
    hand = parse('9s 8s')
    w, l, t, _= simulate(hand, n_runs=sims)


rep = 5
num = 10
l = timeit.repeat('f()', 'from __main__ import f', repeat=rep, number=num)
print(f'{num} loops, best of {rep}: {min(l)/num:.3f}s per loop\n'
      f'Average: {sum(l)/rep/num/sims:.4E} per simulation, {sum(l)/rep/num:.3f} per loop')
#
# for i in range(rep):
#     for i in range(num):
#         f()


