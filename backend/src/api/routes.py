from __future__ import annotations

from typing import Annotated
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Absolute imports assuming you run: uvicorn src.main:app --reload
from src.models import Board                  # your alias/type if you have it; not strictly required
from src.solver import solve, has_unique_solution
from src.generator import generate

router = APIRouter()

# 9 integers per row, 9 rows per board
Row = Annotated[list[int], Field(min_length=9, max_length=9)]
BoardModel = Annotated[list[Row], Field(min_length=9, max_length=9)]

class SolveRequest(BaseModel):
    board: BoardModel  # values 0..9; 0 = blank

class GenerateRequest(BaseModel):
    target_clues: int = 30
    symmetry: str = "rotational"  # 'none' | 'mirror' | 'rotational'
    seed: int | None = None

@router.post("/solve")
def solve_endpoint(req: SolveRequest):
    board = req.board

    # Basic value check (0..9)
    for row in board:
        for v in row:
            if v < 0 or v > 9:
                raise HTTPException(400, "Board must contain integers 0..9 (0 = blank)")

    solved = solve([r[:] for r in board])  # copy to be safe
    if not solved:
        raise HTTPException(422, "No solution")

    return {"solved": solved, "unique": has_unique_solution(board)}

@router.post("/generate")
def generate_endpoint(req: GenerateRequest):
    puzzle, solution = generate(req.target_clues, req.symmetry, req.seed)
    # Expect 0 for blanks in 'puzzle'
    return {"puzzle": puzzle, "solution": solution}
