import pytest
from game import initial_state, player, actions, result, winner, terminal, utility

def test_initial_and_player():
    state = initial_state(3,3)
    b, m, k = state
    assert m == 3 and k == 3
    assert player(state) == 'X'
    assert len(actions(state)) == 9

def test_result_and_player_turns():
    state = initial_state(3,3)
    state = result(state, (0,0))
    assert player(state) == 'O'
    state = result(state, (0,1))
    assert player(state) == 'X'

def test_winner_row():
    state = initial_state(3,3)
    state = result(state, (0,0))  # X
    state = result(state, (1,0))  # O
    state = result(state, (0,1))  # X
    state = result(state, (1,1))  # O
    state = result(state, (0,2))  # X wins
    assert winner(state) == 'X'
    assert terminal(state)
    assert utility(state) == 1

def test_draw():
    moves = [(0,0),(0,1),(0,2),(1,1),(1,0),(1,2),(2,1),(2,0),(2,2)]
    state = initial_state(3,3)
    for mv in moves:
        state = result(state, mv)
    assert terminal(state)
    assert winner(state) is None
    assert utility(state) == 0
