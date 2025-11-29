"""game.py
Game engine for generalized Tic-Tac-Toe (m x m, k-in-a-row).

Immutable board representation: tuple-of-tuples.

Public API:
- initial_state(m=3, k=3) -> BoardMeta
- player(state) -> 'X'|'O'
- actions(state) -> list of (r,c)
- result(state, action) -> new state
- winner(state) -> 'X'|'O'|None
- terminal(state) -> bool
- utility(state) -> +1|-1|0|None
"""
from typing import Optional, Tuple, List

Cell = Optional[str]  # 'X', 'O', or None
Board = Tuple[Tuple[Cell, ...], ...]
BoardMeta = Tuple[Board, int, int]


def initial_state(m: int = 3, k: int = 3) -> BoardMeta:
    """Return an empty board state meta (board, m, k)."""
    board = tuple(tuple(None for _ in range(m)) for _ in range(m))
    return board, m, k


def player(state: BoardMeta) -> str:
    """Return current player: 'X' if X to move, else 'O'. X moves first."""
    board, m, k = state
    filled = sum(1 for r in range(m) for c in range(m) if board[r][c] is not None)
    return 'X' if filled % 2 == 0 else 'O'


def actions(state: BoardMeta) -> List[Tuple[int, int]]:
    """Return legal moves as lexicographically sorted list of (r, c)."""
    board, m, k = state
    moves = [(r, c) for r in range(m) for c in range(m) if board[r][c] is None]
    moves.sort()
    return moves


def result(state: BoardMeta, action: Tuple[int, int]) -> BoardMeta:
    """Return a new state after applying action by current player. Does not modify input."""
    board, m, k = state
    r, c = action
    if not (0 <= r < m and 0 <= c < m):
        raise ValueError('Action out of bounds')
    if board[r][c] is not None:
        raise ValueError('Action not legal')
    cur = player(state)
    new_rows = [list(row) for row in board]
    new_rows[r][c] = cur
    new_board = tuple(tuple(row) for row in new_rows)
    return new_board, m, k


def _window_winner(window: Tuple[Cell, ...]) -> Optional[str]:
    """Return 'X' or 'O' if window is uniform of that symbol, else None."""
    if all(cell == 'X' for cell in window):
        return 'X'
    if all(cell == 'O' for cell in window):
        return 'O'
    return None


def winner(state: BoardMeta) -> Optional[str]:
    """Detect k-in-a-row across rows, columns, diagonals. Returns 'X'|'O'|None."""
    board, m, k = state

    # Rows
    for r in range(m):
        row = board[r]
        for s in range(m - k + 1):
            w = row[s:s + k]
            if len(w) == k:
                wres = _window_winner(w)
                if wres:
                    return wres

    # Cols
    for c in range(m):
        col = tuple(board[r][c] for r in range(m))
        for s in range(m - k + 1):
            w = col[s:s + k]
            if len(w) == k:
                wres = _window_winner(w)
                if wres:
                    return wres

    # Diagonals (\)
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
                wres = _window_winner(w)
                if wres:
                    return wres
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
                wres = _window_winner(w)
                if wres:
                    return wres

    # Anti-diagonals (/)
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
                wres = _window_winner(w)
                if wres:
                    return wres
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
                wres = _window_winner(w)
                if wres:
                    return wres

    return None


def terminal(state: BoardMeta) -> bool:
    """True if state is win for X/O or draw (full board)."""
    if winner(state) is not None:
        return True
    board, m, k = state
    for r in range(m):
        for c in range(m):
            if board[r][c] is None:
                return False
    return True


def utility(state: BoardMeta) -> Optional[int]:
    """Return +1 if X wins, -1 if O wins, 0 if draw, None otherwise."""
    w = winner(state)
    if w == 'X':
        return 1
    if w == 'O':
        return -1
    if terminal(state):
        return 0
    return None
