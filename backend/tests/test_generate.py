from sudoku.generator import generate
from sudoku.solver import has_unique_solution

def test_generate_unique():
    puzzle, solution = generate(target_clues=32, symmetry="rotational", seed=123)
    assert has_unique_solution(puzzle)
    # ensure shapes are correct
    assert len(puzzle) == 9 and len(solution) == 9
    assert all(len(r) == 9 for r in puzzle) and all(len(r) == 9 for r in solution)
