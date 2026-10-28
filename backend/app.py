import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from werkzeug.exceptions import BadRequest, UnsupportedMediaType


def create_app(database=None):
    app = Flask(__name__, static_folder=None)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
    db_path = Path(database or os.environ.get("DATABASE_PATH", Path(__file__).parent / "data" / "registrations.db"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect():
        connection = sqlite3.connect(db_path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    with connect() as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 80),
            roll_number TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(roll_number) BETWEEN 1 AND 30),
            department TEXT NOT NULL CHECK(length(department) BETWEEN 1 AND 60),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

    @app.get("/")
    def index():
        return send_file(Path(__file__).parent.parent / "index.html")

    @app.get("/styles.css")
    def styles():
        return send_file(Path(__file__).parent.parent / "styles.css")

    @app.get("/app.js")
    def javascript():
        return send_file(Path(__file__).parent.parent / "app.js")

    @app.get("/api/health")
    def health():
        with connect() as connection:
            connection.execute("SELECT COUNT(*) FROM registrations").fetchone()
        return jsonify(status="ok", database="connected")

    @app.get("/api/registrations")
    def registrations():
        with connect() as connection:
            rows = connection.execute("SELECT * FROM registrations ORDER BY id DESC").fetchall()
        return jsonify([dict(row) for row in rows])

    @app.post("/api/registrations")
    def add_registration():
        try:
            data = request.get_json()
        except (BadRequest, UnsupportedMediaType):
            return jsonify(error="Send a valid JSON object."), 400
        if not isinstance(data, dict):
            return jsonify(error="Send a valid JSON object."), 400
        values = {}
        for field, limit, label in [("name", 80, "Name"), ("roll_number", 30, "Roll number"), ("department", 60, "Department")]:
            value = data.get(field)
            if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
                return jsonify(error=f"{label} is required and must be at most {limit} characters."), 400
            values[field] = value.strip()
        values["roll_number"] = values["roll_number"].upper()
        try:
            with connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO registrations (name, roll_number, department) VALUES (?, ?, ?)",
                    (values["name"], values["roll_number"], values["department"]),
                )
                row = connection.execute("SELECT * FROM registrations WHERE id = ?", (cursor.lastrowid,)).fetchone()
        except sqlite3.IntegrityError:
            return jsonify(error="That roll number is already registered."), 409
        return jsonify(dict(row)), 201

    @app.delete("/api/registrations/<int:registration_id>")
    def delete_registration(registration_id):
        with connect() as connection:
            cursor = connection.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
        if cursor.rowcount == 0:
            return jsonify(error="Registration not found."), 404
        return jsonify(message="Registration deleted.")

    @app.errorhandler(413)
    def too_large(error):
        return jsonify(error="Request is too large."), 413

    @app.errorhandler(sqlite3.Error)
    def database_error(error):
        app.logger.error("Database operation failed", exc_info=error)
        return jsonify(error="Database unavailable. Please try again."), 503

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", "8088")), debug=False)
