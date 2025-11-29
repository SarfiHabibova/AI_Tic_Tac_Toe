"""play.py
Small CLI to play against the agent.
Agent plays 'X' by default; human plays 'O'.
"""
from game import initial_state, player, actions, result, utility
from search import minimax_ab, search
from heuristic import evaluate

def display(state):
    b, m, k = state
    for r in range(m):
        print(' '.join([cell if cell is not None else '.' for cell in b[r]]))
    print()

def human_vs_agent(m=3, k=3, depth=None):
    state = initial_state(m, k)
    while True:
        display(state)
        u = utility(state)
        if u is not None:
            if u == 1:
                print("X wins")
            elif u == -1:
                print("O wins")
            else:
                print("Draw")
            break
        cur = player(state)
        if cur == 'X':
            if m == 3 and k == 3 and depth is None:
                val, a = minimax_ab(state)
            elif depth is None:
                val, a = minimax_ab(state)
            else:
                val, a = search(state, depth)
            print('Agent (X) plays:', a)
            state = result(state, a)
        else:
            moves = actions(state)
            print('Legal:', moves)
            s = input('Your move as `r c`: ')
            try:
                r, c = map(int, s.split())
                if (r, c) not in moves:
                    print('Illegal move, try again.')
                    continue
                state = result(state, (r, c))
            except Exception:
                print('Invalid input, try `row col` like `0 2`.')

if __name__ == '__main__':
    human_vs_agent()
