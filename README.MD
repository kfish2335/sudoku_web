# Sudoku Web App

A full-stack Sudoku puzzle generator and solver built with **FastAPI (Python)** and **Next.js
(TypeScript)** — deployable via **AWS Amplify (frontend)** and **AWS App Runner (backend)**.

---

## Features

- Smart puzzle generator with adjustable difficulty

- Fast Sudoku solver using recursive backtracking

- Mobile-friendly responsive UI

- Modern minimalist design

- REST API powered by FastAPI

- Dockerized for seamless deployment

- Hosted on AWS Amplify & App Runner

---


## Backend Overview

### Framework
**FastAPI** — lightweight and async Python framework for APIs.

### Algorithms

| Task | Algorithm | Description |

|------|------------|-------------|

| Puzzle Generation | Randomized removal + backtracking | Ensures one valid solution |

| Solving | Backtracking | Efficient recursive solver | Validation |

### Endpoints

| Method | Endpoint | Description |

|---------|-----------|-------------|

| GET /health | Health check endpoint |

| GET / | Root endpoint |

| POST /generate | Generate new Sudoku puzzle |

| POST /solve | Solve given Sudoku board |

---

## n Frontend Overview

**Next.js (React + TypeScript)** app that fetches puzzles and solutions from the backend.

```ts

export const API_BASE =

process.env.NEXT_PUBLIC_SUDOKU_BASE ||

(process.env.NODE_ENV === 'production'

? 'https://pba2vssyyd.us-east-1.awsapprunner.com'

: 'http://127.0.0.1:8000');

```

---

## n Local Development

### Prerequisites

- Docker

- Node.js ≥ 18

- Python ≥ 3.10

### Run Backend

cd backend
docker build -t sudoku-backend .

docker run --rm -e PORT=8080 -p 8080:8080 sudoku-backend

### Run Frontend

cd frontend

npm install

npm run dev

---

## AWS Deployment

- Backend via **AWS App Runner**

- Frontend via **AWS Amplify**

- Env vars:

- PORT=8080

- ALLOWED_ORIGINS=https://

- NEXT_PUBLIC_SUDOKU_BASE=https://

---

## n Tech Stack

| Layer | Technology |

|--------|-------------|

| Frontend | Next.js + React + TypeScript |

| Backend | FastAPI (Python) |

| Styling | CSS + Flexbox |

| Build | Docker |

| Cloud | AWS Amplify + App Runner |

| Validation | Pydantic |

| Solver | DFS Backtracking |

---

## Author

**Kurk Fisher**

Network Technician & Software Developer

[kurkfisher.me](https://kurkfisher.me) • [GitHub](https://github.com/kfish2335)

---

## n License
MIT License — free to use, modify, and distribute.