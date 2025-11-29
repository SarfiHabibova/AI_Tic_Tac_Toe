"""heuristic.py

Heuristic evaluation for depth-limited search.

- Symmetric: positive for X advantage, negative for O advantage.
- Immediate wins/threats dominate via exponential weighting (10^n).
"""
from typing import Tuple
from game import BoardMeta


def evaluate(state: BoardMeta, perspective: str = 'X') -> float:
    board, m, k = state

    def window_value(window):
        x_count = sum(1 for c in window if c == 'X')
        o_count = sum(1 for c in window if c == 'O')
        if x_count > 0 and o_count > 0:
            return 0.0
        if x_count > 0:
            return 10 ** x_count
        if o_count > 0:
            return - (10 ** o_count)
        return 0.0

    total = 0.0
    windows = 0

    # rows
    for r in range(m):
        row = board[r]
        for s in range(m - k + 1):
            w = row[s:s + k]
            total += window_value(w)
            windows += 1

    # cols
    for c in range(m):
        col = tuple(board[r][c] for r in range(m))
        for s in range(m - k + 1):
            w = col[s:s + k]
            total += window_value(w)
            windows += 1

    # diagonals (\)
    for start_col in range(m):
        diag = []
        r, c = 0, start_col
        while r < m and c < m:
            diag.append(board[r][c])
            r += 1
            c += 1
        if len(diag) >= k:
            for s in range(len(diag) - k + 1):
                w = tuple(diag[s:s + k])
                total += window_value(w)
                windows += 1
    for start_row in range(1, m):
        diag = []
        r, c = start_row, 0
        while r < m and c < m:
            diag.append(board[r][c])
            r += 1
            c += 1
        if len(diag) >= k:
            for s in range(len(diag) - k + 1):
                w = tuple(diag[s:s + k])
                total += window_value(w)
                windows += 1

    # anti-diagonals (/)
    for start_col in range(m):
        diag = []
        r, c = 0, start_col
        while r < m and c >= 0:
            diag.append(board[r][c])
            r += 1
            c -= 1
        if len(diag) >= k:
            for s in range(len(diag) - k + 1):
                w = tuple(diag[s:s + k])
                total += window_value(w)
                windows += 1
    for start_col in range(1, m):
        diag = []
        r, c = start_col, m - 1
        while r < m and c >= 0:
            diag.append(board[r][c])
            r += 1
            c -= 1
        if len(diag) >= k:
            for s in range(len(diag) - k + 1):
                w = tuple(diag[s:s + k])
                total += window_value(w)
                windows += 1

    if windows == 0:
        return 0.0
    score = total / windows
    return score if perspective == 'X' else -score
