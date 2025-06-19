from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "db.sqlite3"
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="SpotMap Prototype")

# Allow requests from the React dev server running on a different port
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"], allow_headers=["*"])


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db()
    with open(Path(__file__).parent / "schema.sql") as f:
        conn.executescript(f.read())

    # Migrate any stored photo paths to just filenames
    rows = conn.execute("SELECT id, photo FROM posts WHERE photo IS NOT NULL").fetchall()
    for row in rows:
        filename = Path(row["photo"]).name
        if filename != row["photo"]:
            conn.execute("UPDATE posts SET photo = ? WHERE id = ?", (filename, row["id"]))
    conn.commit()
    conn.close()

@app.get("/posts")
def list_posts():
    conn = get_db()
    posts = []
    for row in conn.execute("SELECT * FROM posts ORDER BY timestamp DESC"):
        post = dict(row)
        if post.get("photo"):
            post["photo"] = str(UPLOAD_DIR / post["photo"])
        posts.append(post)
    conn.close()
    return posts

@app.post("/posts")
def create_post(title: str, description: str = "", category: str = "",
                latitude: float = 0.0, longitude: float = 0.0,
                photo: UploadFile = File(None)):
    filename = None
    if photo:
        # Strip any path components from the uploaded filename
        filename = Path(photo.filename).name
        # Prefix the filename with a timestamp to avoid collisions
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        filename = f"{timestamp}_{filename}"
        file_path = UPLOAD_DIR / filename
        with file_path.open("wb") as f:
            f.write(photo.file.read())
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO posts (title, description, category, latitude, longitude, photo) VALUES (?, ?, ?, ?, ?, ?)",
        (title, description, category, latitude, longitude, filename)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return {"id": post_id}

@app.get("/uploads/{filename}")
def get_upload(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
