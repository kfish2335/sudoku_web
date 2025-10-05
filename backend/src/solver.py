from __future__ import annotations
from typing import Optional, List
from .models import Board
from .utils import copy_board, is_valid, find_empty_mrv

def solve(board: Board) -> Optional[Board]:
    cell = find_empty_mrv(board)
    if not cell:
        return board
    r, c, cands = cell
    if not cands:
        return None
    for n in cands:
        board[r][c] = n
        if solve(board):
            return board
        board[r][c] = 0
    return None

def count_solutions(board: Board, limit: int = 2) -> int:
    cell = find_empty_mrv(board)
    if not cell:
        return 1
    r, c, cands = cell
    if not cands:
        return 0
    total = 0
    for n in cands:
        board[r][c] = n
        total += count_solutions(board, limit)
        board[r][c] = 0
        if total >= limit:
            break
    return total

def has_unique_solution(board: Board) -> bool:
    return count_solutions(copy_board(board), 2) == 1
