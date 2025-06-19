# SpotMap Prototype

This repository contains a local-first prototype with a Python backend and a React frontend.

## Backend

The backend uses FastAPI with a SQLite database. Posts and uploaded photos are stored locally.

Run the backend:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

The API will be available on `http://localhost:8000`.

CORS is enabled for the development frontend at `http://localhost:5173`, so the React app can make requests to the API during local development.

## Frontend

The frontend is a React app bootstrapped with Vite. Install dependencies and start the dev server:

```bash
cd frontend
npm install
npm run dev
```

The dev server requires Node.js (version 18 or newer). Once `npm run dev` is running
you should see output similar to:

```
  VITE v5.0.0  ready in xx ms
  ➜  Local:   http://localhost:5173/
```

Open the printed URL (usually `http://localhost:5173/`) in your browser. If the site
cannot be reached, double check that the dev server is still running in your
terminal and that no firewall rules block the port.

## Directory Structure

```
backend/
    app.py
    schema.sql
    uploads/
    data/
frontend/
    public/
        icons/
    src/
        components/
```

## Running Tests

Install the development dependencies and run `pytest`:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```
