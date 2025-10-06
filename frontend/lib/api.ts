export type Board = number[][];

export const API_BASE =
  process.env.NEXT_PUBLIC_SUDOKU_BASE ||
  (process.env.NODE_ENV === 'production'
    ? 'https://pba2vssyyd.us-east-1.awsapprunner.com'
    : 'http://127.0.0.1:8000');

export async function generatePuzzle(opts: { target_clues?: number; symmetry?: string; seed?: number } = {}) {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      target_clues: opts.target_clues ?? 30,
      symmetry: opts.symmetry ?? "rotational",
      seed: opts.seed ?? undefined
    }),
    cache: "no-store"
  });
  if (!res.ok) throw new Error(`Generate failed: ${res.status}`);
  return (await res.json()) as { puzzle: Board; solution: Board };
}

export async function solveBoard(board: Board) {
  const res = await fetch(`${API_BASE}/solve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ board }),
    cache: "no-store"
  });
  if (!res.ok) throw new Error(`Solve failed: ${res.status}`);
  return (await res.json()) as { solved: Board; unique: boolean };
}

export function emptyBoard(): Board {
  return Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));
}

export function cloneBoard(b: Board): Board {
  return b.map((r) => r.slice());
}

export function isComplete(b: Board): boolean {
  return b.every((row) => row.every((v) => v >= 1 && v <= 9));
}