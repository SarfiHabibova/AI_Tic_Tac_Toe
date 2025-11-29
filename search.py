"""search.py

Implements minimax, minimax_ab, and depth-limited search with alpha-beta pruning.
Includes optional move ordering and instrumentation for node counting.
Deterministic tie-breaking: actions sorted lexicographically when equal.
"""
from typing import Tuple, Optional, List
from game import BoardMeta, player, actions, result, terminal, utility
from heuristic import evaluate
import time

# Instrumentation container
class Instrument:
    def __init__(self):
        self.node_count = 0
    def tick(self):
        self.node_count += 1
    def reset(self):
        self.node_count = 0

def _order_moves(state: BoardMeta, use_heuristic_probe: bool = True) -> List[Tuple[int, int]]:
    """Order moves: center -> corners -> edges -> then by shallow heuristic probe (if enabled).
    Deterministic tie-breaking kept by including the action itself in the key.
    """
    moves = actions(state)
    board, m, k = state
    center = (m // 2, m // 2)

    def priority(a):
        r, c = a
        # geometric priority
        if a == center:
            base = 0
        elif (r in (0, m - 1) and c in (0, m - 1)):
            base = 1
        elif r in (0, m - 1) or c in (0, m - 1):
            base = 2
        else:
            base = 3
        probe = 0.0
        if use_heuristic_probe:
            try:
                probe = evaluate(result(state, a))
            except Exception:
                probe = 0.0
        # lower keys sorted first -> prefer smaller base, larger probe (thus -probe), then lexicographic action
        return (base, -probe, a)

    moves.sort(key=priority)
    return moves

def minimax(state: BoardMeta, instrument: Optional[Instrument] = None) -> Tuple[int, Tuple[int, int]]:
    """Plain minimax search returning (value, action) for current player.
    This is complete search (no depth limit); intended as oracle for m=3,k=3.
    """
    if instrument is None:
        instrument = Instrument()
    instrument.reset()

    cur = player(state)

    def max_value(s):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return u
        v = float('-inf')
        for a in actions(s):
            v = max(v, min_value(result(s, a)))
        return v

    def min_value(s):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return u
        v = float('inf')
        for a in actions(s):
            v = min(v, max_value(result(s, a)))
        return v

    best_action = None
    if cur == 'X':
        best_val = float('-inf')
        for a in actions(state):
            v = min_value(result(state, a))
            if v > best_val or (v == best_val and (best_action is None or a < best_action)):
                best_val = v
                best_action = a
        return best_val, best_action
    else:
        best_val = float('inf')
        for a in actions(state):
            v = max_value(result(state, a))
            if v < best_val or (v == best_val and (best_action is None or a < best_action)):
                best_val = v
                best_action = a
        return best_val, best_action

def minimax_ab(state: BoardMeta, instrument: Optional[Instrument] = None, use_ordering: bool = True) -> Tuple[int, Tuple[int, int]]:
    """Minimax with Alpha-Beta pruning. Returns (value, action).
    use_ordering toggles move ordering to measure its effect.
    """
    if instrument is None:
        instrument = Instrument()
    instrument.reset()

    cur = player(state)

    def max_value(s, alpha, beta):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return u
        v = float('-inf')
        moves = _order_moves(s, use_ordering)
        for a in moves:
            v = max(v, min_value(result(s, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s, alpha, beta):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return u
        v = float('inf')
        moves = _order_moves(s, use_ordering)
        for a in moves:
            v = min(v, max_value(result(s, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    if cur == 'X':
        best_val = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for a in _order_moves(state, use_ordering):
            val = min_value(result(state, a), alpha, beta)
            if val > best_val or (val == best_val and (best_action is None or a < best_action)):
                best_val = val
                best_action = a
            alpha = max(alpha, best_val)
        return best_val, best_action
    else:
        best_val = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for a in _order_moves(state, use_ordering):
            val = max_value(result(state, a), alpha, beta)
            if val < best_val or (val == best_val and (best_action is None or a < best_action)):
                best_val = val
                best_action = a
            beta = min(beta, best_val)
        return best_val, best_action

def search(state: BoardMeta, depth: int, eval_fn=evaluate, instrument: Optional[Instrument] = None, use_ordering: bool = True) -> Tuple[float, Tuple[int, int]]:
    """Depth-limited alpha-beta search using eval_fn at cutoff.
    Returns (value, action) for the current player.
    """
    if instrument is None:
        instrument = Instrument()
    instrument.reset()

    cur = player(state)

    def max_value(s, alpha, beta, d):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return float(u)
        if d == 0:
            return eval_fn(s)
        v = float('-inf')
        moves = _order_moves(s, use_ordering)
        for a in moves:
            v = max(v, min_value(result(s, a), alpha, beta, d - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s, alpha, beta, d):
        if instrument: instrument.tick()
        u = utility(s)
        if u is not None:
            return float(u)
        if d == 0:
            return eval_fn(s)
        v = float('inf')
        moves = _order_moves(s, use_ordering)
        for a in moves:
            v = min(v, max_value(result(s, a), alpha, beta, d - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_action = None
    if cur == 'X':
        best_val = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for a in _order_moves(state, use_ordering):
            val = min_value(result(state, a), alpha, beta, depth - 1)
            if val > best_val or (val == best_val and (best_action is None or a < best_action)):
                best_val = val
                best_action = a
            alpha = max(alpha, best_val)
        return best_val, best_action
    else:
        best_val = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for a in _order_moves(state, use_ordering):
            val = max_value(result(state, a), alpha, beta, depth - 1)
            if val < best_val or (val == best_val and (best_action is None or a < best_action)):
                best_val = val
                best_action = a
            beta = min(beta, best_val)
        return best_val, best_action
