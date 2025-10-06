from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as api_router  # ← mount the routes

app = FastAPI(title="Sudoku API", version="1.0")

# CORS: add your front-end origins here or via env var
origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,https://sudoku.kurkfisher.me,https://master.d3glxos4xreezv.amplifyapp.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

# Mount all Sudoku endpoints under root (change prefix here if you want)
app.include_router(api_router)