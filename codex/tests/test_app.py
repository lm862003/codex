from fastapi.testclient import TestClient
import backend.app as backend_app


def test_create_and_list_posts(tmp_path, monkeypatch):
    # Use a temporary database and uploads directory
    db_path = tmp_path / "test.db"
    upload_dir = tmp_path / "uploads"
    monkeypatch.setattr(backend_app, "DB_PATH", db_path)
    monkeypatch.setattr(backend_app, "UPLOAD_DIR", upload_dir)
    upload_dir.mkdir()

    with TestClient(backend_app.app) as client:
        response = client.post(
            "/posts",
            data={"title": "Test Post"}
        )
        assert response.status_code == 200

        response = client.get("/posts")
        assert response.status_code == 200
        posts = response.json()
        assert any(p["title"] == "Test Post" for p in posts)
