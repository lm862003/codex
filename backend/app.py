from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import sqlite3
from pathlib import Path
from uuid import uuid4

DB_PATH = Path(__file__).parent / "db.sqlite3"
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="SpotMap Prototype")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db()
    with open(Path(__file__).parent / "schema.sql") as f:
        conn.executescript(f.read())
    conn.close()

@app.get("/posts")
def list_posts():
    conn = get_db()
    posts = [dict(row) for row in conn.execute("SELECT * FROM posts ORDER BY timestamp DESC")]
    conn.close()
    return posts

@app.post("/posts")
def create_post(title: str, description: str = "", category: str = "",
                latitude: float = 0.0, longitude: float = 0.0,
                photo: UploadFile = File(None)):
    photo_path = None
    if photo:
        safe_name = Path(photo.filename).name
        unique_name = f"{uuid4().hex}_{safe_name}"
        photo_path = UPLOAD_DIR / unique_name
        with photo_path.open("wb") as f:
            f.write(photo.file.read())
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO posts (title, description, category, latitude, longitude, photo) VALUES (?, ?, ?, ?, ?, ?)",
        (title, description, category, latitude, longitude, str(photo_path) if photo_path else None)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return {"id": post_id}

@app.get("/uploads/{filename}")
def get_upload(filename: str):
    requested = (UPLOAD_DIR / filename).resolve()
    if UPLOAD_DIR.resolve() not in requested.parents:
        raise HTTPException(status_code=400, detail="Invalid path")
    if not requested.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(requested)
