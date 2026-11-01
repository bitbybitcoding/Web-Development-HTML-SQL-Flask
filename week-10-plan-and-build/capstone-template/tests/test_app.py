"""Starter tests. Run from the project folder:   python3 -m unittest discover -s tests -v

Each test gets a fresh temporary database, so tests never affect your real data (instance/app.db).
Week 11 teaches how to write more of these. For now, copy the pattern for each new feature.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import app as project            # noqa: E402  (the import must come after the sys.path line)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        project.app.config["DATABASE"] = str(Path(self.tmp.name) / "test.db")
        project.app.config["TESTING"] = True
        with project.app.app_context():
            project.init_db(seed=True)
        self.client = project.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()


class TestPages(AppTestCase):
    def test_home_lists_the_seed_items(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Screwdriver set", r.data)

    def test_search_filters(self):
        r = self.client.get("/?q=chess")
        self.assertIn(b"Chess set", r.data)
        self.assertNotIn(b"Glue gun", r.data)

    def test_unknown_page_is_404(self):
        self.assertEqual(self.client.get("/nope").status_code, 404)


class TestAddItem(AppTestCase):
    def test_valid_item_is_saved_then_redirects(self):
        r = self.client.post("/items/new", data={"name": "Laptop", "category_id": "1", "quantity": "2", "notes": ""})
        self.assertEqual(r.status_code, 302)
        self.assertIn(b"Laptop", self.client.get("/").data)

    def test_invalid_item_is_rejected_and_not_saved(self):
        r = self.client.post("/items/new", data={"name": "x", "category_id": "999", "quantity": "-1", "notes": ""})
        self.assertEqual(r.status_code, 200)               # the form is shown again
        self.assertIn(b"Choose a category", r.data)
        self.assertNotIn(b">x<", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()
