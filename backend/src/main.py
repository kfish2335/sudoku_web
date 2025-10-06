from __future__ import annotations

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as api_router  # ← mount the routes

app = FastAPI(title="Sudoku API", version="1.0")

# CORS
origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,https://master.d3glxos4xreezv.amplifyapp.com,https://sudoku.kurkfisher.me,https://www.sudoku.kurkfisher.me"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "sudoku-api", "version": app.version}

@app.get("/health")
def health():
    return {"ok": True}

# Mount all Sudoku endpoints under root (change prefix here if you want)
app.include_router(api_router)