import sqlite3
from contextlib import closing
import tempfile
import unittest
from pathlib import Path

from app import create_app


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = Path(self.folder.name) / "test.db"
        self.app = create_app(self.path)
        self.client = self.app.test_client()
        self.student = {"name": "Ananya Sharma", "roll_number": "cse101", "department": "CSE"}

    def tearDown(self):
        self.folder.cleanup()

    def test_health_reads_database(self):
        self.assertEqual(self.client.get("/api/health").json, {"status": "ok", "database": "connected"})

    def test_add_list_persist_and_delete(self):
        response = self.client.post("/api/registrations", json=self.student)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["roll_number"], "CSE101")
        row_id = response.json["id"]
        new_client = create_app(self.path).test_client()
        self.assertEqual(new_client.get("/api/registrations").json[0]["name"], "Ananya Sharma")
        self.assertEqual(new_client.delete(f"/api/registrations/{row_id}").status_code, 200)
        self.assertEqual(new_client.get("/api/registrations").json, [])
        self.assertEqual(new_client.delete(f"/api/registrations/{row_id}").status_code, 404)

    def test_duplicate_roll_number_ignores_case(self):
        self.client.post("/api/registrations", json=self.student)
        self.assertEqual(self.client.post("/api/registrations", json=dict(self.student, roll_number="CSE101")).status_code, 409)
        self.assertEqual(len(self.client.get("/api/registrations").json), 1)

    def test_invalid_input_does_not_save(self):
        for data in [None, [], {}, dict(self.student, name=" "), dict(self.student, name="x" * 81), dict(self.student, roll_number=123)]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post("/api/registrations", json=data).status_code, 400)
        self.assertEqual(self.client.get("/api/registrations").json, [])

    def test_sql_text_is_saved_as_data(self):
        value = "Robert'); DROP TABLE registrations;--"
        self.assertEqual(self.client.post("/api/registrations", json=dict(self.student, name=value)).status_code, 201)
        with closing(sqlite3.connect(self.path)) as database:
            self.assertEqual(database.execute("SELECT name FROM registrations").fetchone()[0], value)

    def test_large_request_is_rejected(self):
        self.assertEqual(self.client.post("/api/registrations", json={"name": "x" * 20000}).status_code, 413)


if __name__ == "__main__":
    unittest.main()
