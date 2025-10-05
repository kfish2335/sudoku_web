from __future__ import annotations
from typing import List, Optional, Tuple
from .models import Board

def copy_board(b: Board) -> Board:
    return [row[:] for row in b]

def empty_board() -> Board:
    return [[0 for _ in range(9)] for _ in range(9)]

def print_board(board: Board) -> None:
    for r in range(9):
        row = []
        for c in range(9):
            v = board[r][c]
            row.append(str(v) if v != 0 else ".")
            if c % 3 == 2 and c != 8:
                row.append("|")
        print(" ".join(row))
        if r % 3 == 2 and r != 8:
            print("------+-------+------")

def is_valid(board: Board, row: int, col: int, num: int) -> bool:
    # Row / Col
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Box
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == num:
                return False
    return True

def find_empty_mrv(board: Board) -> Optional[Tuple[int,int,list[int]]]:
    best = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                cands = [n for n in range(1,10) if is_valid(board, r, c, n)]
                if not cands:
                    return (r, c, cands)
                if best is None or len(cands) < len(best[2]):
                    best = (r, c, cands)
                    if len(cands) == 1:
                        return best
    return best
