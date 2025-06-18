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

## Frontend

The frontend is a React app bootstrapped with Vite. Install dependencies and start the dev server:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be served at `http://localhost:5173`.

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
