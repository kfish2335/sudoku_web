from __future__ import annotations

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as api_router  # ← mount the routes

app = FastAPI(title="Sudoku API", version="1.0")

# CORS: configure via env vars
# ALLOWED_ORIGINS: comma-separated exact origins
# ALLOWED_ORIGIN_REGEX: optional regex to allow many subdomains (e.g., preview branches)
raw_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,https://sudoku.kurkfisher.me,https://master.d3glxos4xreezv.amplifyapp.com",
)
origin_regex = os.getenv("ALLOWED_ORIGIN_REGEX", "") or None
allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

# Log effective CORS config (visible in App Runner logs)
logger = logging.getLogger("uvicorn.error")
logger.info("CORS allow_origins=%s allow_origin_regex=%s", allow_origins, origin_regex)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=origin_regex,  # used if provided
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