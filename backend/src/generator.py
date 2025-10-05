from __future__ import annotations
from typing import Tuple, Optional, List
import random
from .models import Board
from .utils import copy_board, is_valid
from .solver import has_unique_solution

def _solve_random(board: Board, rng: random.Random) -> bool:
    # Simple randomized backtracking to fill a full valid board
    # Find first empty
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                rng.shuffle(nums)
                for n in nums:
                    if is_valid(board, r, c, n):
                        board[r][c] = n
                        if _solve_random(board, rng):
                            return True
                        board[r][c] = 0
                return False
    return True

def _full_solution(rng: random.Random) -> Board:
    board: Board = [[0]*9 for _ in range(9)]
    assert _solve_random(board, rng), "Failed to build full solution"
    return board

def _sym_points(r: int, c: int, symmetry: str) -> List[Tuple[int,int]]:
    pts = {(r, c)}
    if symmetry == "mirror":
        pts.add((r, 8 - c))
    elif symmetry == "rotational":
        pts.add((8 - r, 8 - c))
    return list(pts)

def generate(target_clues: int = 30, symmetry: str = "rotational", seed: Optional[int] = None) -> Tuple[Board, Board]:
    target = max(17, min(81, target_clues))
    rng = random.Random(seed)
    solution = _full_solution(rng)
    puzzle = copy_board(solution)

    order = [(r, c) for r in range(9) for c in range(9)]
    rng.shuffle(order)

    clues = 81
    for r, c in order:
        if clues <= target:
            break
        if puzzle[r][c] == 0:
            continue
        pts = _sym_points(r, c, symmetry)
        backup = [(rr, cc, puzzle[rr][cc]) for rr, cc in pts]
        for rr, cc, _ in backup:
            puzzle[rr][cc] = 0

        # Keep removal only if uniqueness holds
        if has_unique_solution(puzzle):
            clues -= len(backup)
        else:
            for rr, cc, v in backup:
                puzzle[rr][cc] = v

    return puzzle, solution
