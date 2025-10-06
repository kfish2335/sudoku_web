'use client';

import React, { useEffect, useState } from 'react';
import BoardGrid from '@/components/Board';
import { Board, cloneBoard, emptyBoard, generatePuzzle, solveBoard } from '@/lib/api';

type Diff = 'easy' | 'medium' | 'hard';

function cluesFor(diff: Diff) {
  switch (diff) {
    case 'easy': return 36;
    case 'medium': return 30;
    case 'hard': return 24;
  }
}

export default function Page() {
  const [board, setBoard] = useState<Board>(() => emptyBoard());
  const [givenMask, setGivenMask] = useState<boolean[][]>(() => Array.from({ length: 9 }, () => Array(9).fill(false)));
  const [solution, setSolution] = useState<Board | null>(null);
  const [loading, setLoading] = useState<string | null>(null);
  const [errors, setErrors] = useState<Set<string>>(new Set());
  const [difficulty, setDifficulty] = useState<Diff | null>(null);

const load = async (diff: Diff) => {
  try {
    setLoading('Generating...');
    const { puzzle, solution } = await generatePuzzle({ target_clues: cluesFor(diff), symmetry: 'rotational' });
    setBoard(puzzle);
    setSolution(solution);
    setGivenMask(puzzle.map((row) => row.map((v) => v !== 0)));
    setErrors(new Set());
    setDifficulty(diff);   // 👈 store the current difficulty
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Failed to generate';
    alert(msg);
  } finally {
    setLoading(null);
  }
};

  useEffect(() => {
    // auto-generate an easy puzzle on load
    load('easy');
  }, []);

  const handleChange = (r: number, c: number, v: number) => {
    setBoard((prev) => {
      const next = cloneBoard(prev);
      next[r][c] = v;
      return next;
    });
  };

  const checkErrors = () => {
    const errs = new Set<string>();
    // Rule: duplicates in row/col/subgrid ignoring zeros
    for (let r = 0; r < 9; r++) {
      const seen = new Map<number, number[]>();
      for (let c = 0; c < 9; c++) {
        const v = board[r][c];
        if (v === 0) continue;
        const locs = seen.get(v) || [];
        locs.push(c);
        seen.set(v, locs);
      }
      for (const [, locs] of seen) if (locs.length > 1) locs.forEach((c) => errs.add(`${r}-${c}`));
    }
    for (let c = 0; c < 9; c++) {
      const seen = new Map<number, number[]>();
      for (let r = 0; r < 9; r++) {
        const v = board[r][c];
        if (v === 0) continue;
        const locs = seen.get(v) || [];
        locs.push(r);
        seen.set(v, locs);
      }
      for (const [, locs] of seen) if (locs.length > 1) locs.forEach((r) => errs.add(`${r}-${c}`));
    }
    for (let br = 0; br < 3; br++) {
      for (let bc = 0; bc < 3; bc++) {
        const seen = new Map<number, [number, number][]>(); 
        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 3; c++) {
            const rr = br * 3 + r;
            const cc = bc * 3 + c;
            const v = board[rr][cc];
            if (v === 0) continue;
            const locs = seen.get(v) || [];
            locs.push([rr, cc]);
            seen.set(v, locs);
          }
        }
        for (const [, locs] of seen) if (locs.length > 1) locs.forEach(([rr, cc]) => errs.add(`${rr}-${cc}`));
      }
    }
    setErrors(errs);
  };

  const doSolve = async () => {
    try {
      setLoading('Solving...');
      const { solved } = await solveBoard(board);
      setBoard(solved);
      setErrors(new Set());
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Failed to solve';
      alert(msg);
    } finally {
      setLoading(null);
    }
  };

  const doReveal = () => {
    if (!solution) return;
    setBoard(solution);
    setErrors(new Set());
  };

  const doClear = () => {
    setBoard((prev) => prev.map((row, r) => row.map((v, c) => (givenMask[r][c] ? v : 0))));
    setErrors(new Set());
  };

  return (
    <div className="container">
      <h1>Sudoku</h1>
      {difficulty && (
        <p className="difficulty-label">
          Current difficulty: <strong>{difficulty.toUpperCase()}</strong>
        </p>
      )}
      <div className="toolbar">
        <button
          className={difficulty === 'easy' ? 'active' : ''}
          onClick={() => load('easy')}
          disabled={!!loading}
        >
          Easy
        </button>
        <button
          className={difficulty === 'medium' ? 'active' : ''}
          onClick={() => load('medium')}
          disabled={!!loading}
        >
          Medium
        </button>
        <button
          className={difficulty === 'hard' ? 'active' : ''}
          onClick={() => load('hard')}
          disabled={!!loading}
        >
          Hard
        </button>
        <button onClick={doClear} disabled={!!loading}>Clear</button>
        <button onClick={checkErrors} disabled={!!loading}>Check</button>
        <button onClick={doSolve} disabled={!!loading}>Solve (API)</button>
        <button onClick={doReveal} disabled={!solution || !!loading}>Reveal</button>
        <div className="status">{loading ? loading : ''}</div>
      </div>

      <BoardGrid board={board} givenMask={givenMask} onChange={handleChange} errors={errors} />

      <hr />
      <p className="small">
        Backend base URL: <code>{process.env.NEXT_PUBLIC_SUDOKU_BASE || 'http://127.0.0.1:8000'}</code> • Endpoints used: <code>POST /generate</code>, <code>POST /solve</code>.
      </p>
      <p className="small">
        Tips: Use number keys (1–9) to fill, backspace to clear. Click <kbd>Check</kbd> to highlight duplicates in rows, columns, and 3×3 boxes.
      </p>
    </div>
  );
}