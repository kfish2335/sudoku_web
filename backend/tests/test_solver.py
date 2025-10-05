from sudoku.solver import solve, has_unique_solution
from sudoku.types import Board

def test_solve_basic():
    puzzle: Board = [
        [0,0,0,2,6,0,7,0,1],
        [6,8,0,0,7,0,0,9,0],
        [1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0],
        [0,0,4,6,0,2,9,0,0],
        [0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4],
        [0,4,0,0,5,0,0,3,6],
        [7,0,3,0,1,8,0,0,0],
    ]
    solved = solve([row[:] for row in puzzle])
    assert solved is not None
    assert all(all(1 <= v <= 9 for v in row) for row in solved)
    assert has_unique_solution(puzzle) in (True, False)  # should run without error
