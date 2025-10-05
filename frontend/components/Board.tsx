'use client';

import React from 'react';
import { Board } from '@/lib/api';

type Props = {
  board: Board;
  givenMask: boolean[][];
  onChange: (r: number, c: number, v: number) => void;
  errors?: Set<string>;
};

export default function BoardGrid({ board, givenMask, onChange, errors }: Props) {
  return (
    <div className="grid">
      {board.map((row, r) =>
        row.map((val, c) => {
          const key = `${r}-${c}`;
          const isGiven = givenMask[r][c];
          const isBlockBorder = (c + 1) % 3 === 0 && c !== 8;
          const isRowStart = r % 3 === 0;
          const classNames = [
            'cell',
            isGiven ? 'given' : '',
            isRowStart ? 'row-start' : '',
            isBlockBorder ? 'block-border' : '',
            errors?.has(key) ? 'error' : ''
          ].join(' ');
          return (
            <div className={classNames} key={key}>
              {isGiven ? (
                <div>{val || ''}</div>
              ) : (
                <input
                  inputMode="numeric"
                  maxLength={1}
                  value={val || ''}
                  onChange={(e) => {
                    const ch = e.target.value.replace(/[^1-9]/g, '').slice(0, 1);
                    const num = ch ? parseInt(ch, 10) : 0;
                    onChange(r, c, num);
                  }}
                />
              )}
            </div>
          );
        })
      )}
    </div>
  );
}