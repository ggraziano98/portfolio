from functions import parse, simulate

# Function used for profiling and testing

def f():
    hand = parse('6s 2h')
    board = parse('3h 5s 7s')
    w, l, t, _= simulate(hand, board, n_runs=25000)

    print(f'{t} runs: {w} wins, {l} losses\n'
          f'Win: {w/t*100:.2f}%  -  Lose: {l/t*100:.2f}%  -  Tie: {(t-w-l)/t*100:.2f}%\n')


f()
