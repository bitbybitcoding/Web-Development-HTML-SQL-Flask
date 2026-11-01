"""Tests for the model capstone. Run from this folder:   python3 -m unittest discover -s tests -v

Pattern used throughout: arrange (known data) -> act (send a request) -> assert (check page AND database).
Each test starts with a fresh temporary database and a fixed 'today', so results never depend on the real date.
"""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import app as project            # noqa: E402

TODAY = "2026-03-02"


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "test.db")
        project.app.config.update(DATABASE=self.db_path, TESTING=True, TODAY=TODAY)
        with project.app.app_context():
            project.init_db(seed=False)
        self.con = sqlite3.connect(self.db_path)
        self.con.executescript("""
            INSERT INTO category VALUES (1, 'Tools'), (2, 'Sensors');
            INSERT INTO kit VALUES (1, 'Multimeter', 1, 4, NULL), (2, 'Sonar', 2, 2, 'Fragile'), (3, 'Spare kit', 2, 1, NULL);
            INSERT INTO loan VALUES (1, 1, 'Mei', 3, '2026-02-10', '2026-02-17', NULL),     -- 3 out, overdue by 13 days
                                    (2, 2, 'Arjun', 1, '2026-02-20', '2026-03-10', NULL),    -- 1 out, not due yet
                                    (3, 2, 'Zoe', 1, '2026-01-01', '2026-01-08', '2026-01-05'); -- returned
        """)
        self.con.commit()
        self.client = project.app.test_client()

    def tearDown(self):
        self.con.close()
        self.tmp.cleanup()

    def one(self, sql, *params):
        return self.con.execute(sql, params).fetchone()[0]


class TestReading(AppTestCase):
    def test_available_is_total_minus_out_on_loan(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("1 of 4", html)      # Multimeter: 4 - 3
        self.assertIn("1 of 2", html)      # Sonar: 2 - 1 (the returned loan does not count)
        self.assertIn("1 of 1", html)      # Spare kit: never borrowed

    def test_search_and_category_filter(self):
        self.assertNotIn("Sonar", self.client.get("/?q=multi").get_data(as_text=True))
        html = self.client.get("/?category=2").get_data(as_text=True)
        self.assertIn("Sonar", html)
        self.assertNotIn("Multimeter", html)

    def test_search_text_is_not_executed_as_sql(self):
        r = self.client.get("/?q=' OR 1=1 --")
        self.assertEqual(r.status_code, 200)
        self.assertNotIn(b"Multimeter", r.data)

    def test_unknown_kit_is_404(self):
        self.assertEqual(self.client.get("/kits/999").status_code, 404)

    def test_overdue_report_counts_days_late(self):
        html = self.client.get("/overdue").get_data(as_text=True)
        self.assertIn("Mei", html)
        self.assertIn(">13<", html)
        self.assertNotIn("Arjun", html)

    def test_report_totals(self):
        html = self.client.get("/report").get_data(as_text=True)
        self.assertIn("Spare kit", html.split("Never borrowed")[1])
        self.assertLess(html.index("Mei"), html.index("Zoe"))     # borrowers with equal loans are ordered by name
        # Tools: 1 kit, 4 owned, 3 out.  Sensors: 2 kits, 3 owned, 1 out.
        self.assertRegex(html, r"Tools</td><td>1</td><td>4</td><td>3</td>")
        self.assertRegex(html, r"Sensors</td><td>2</td><td>3</td><td>1</td>")


class TestBorrowAndReturn(AppTestCase):
    def borrow(self, kit_id, **data):
        return self.client.post(f"/kits/{kit_id}/borrow", data=data, follow_redirects=True).get_data(as_text=True)

    def test_valid_loan_is_saved_with_the_right_due_date(self):
        self.borrow(3, borrower="Daniel", qty="1", days="7")
        self.assertEqual(self.con.execute("SELECT borrower, qty, borrowed_on, due_on FROM loan WHERE kit_id = 3").fetchall(),
                         [("Daniel", 1, TODAY, "2026-03-09")])

    def test_cannot_borrow_more_than_available(self):
        self.assertIn("from 1 to 1", self.borrow(3, borrower="Daniel", qty="2", days="7"))
        self.assertIn("from 1 to 1", self.borrow(1, borrower="Daniel", qty="2", days="7"))
        self.assertEqual(self.one("SELECT COUNT(*) FROM loan"), 3)

    def test_bad_input_is_rejected(self):
        for data in ({"borrower": "A", "qty": "1", "days": "7"},
                     {"borrower": "Daniel", "qty": "0", "days": "7"},
                     {"borrower": "Daniel", "qty": "abc", "days": "7"},
                     {"borrower": "Daniel", "qty": "1", "days": "99"},
                     {"borrower": "Daniel", "qty": "1 OR 1=1", "days": "7"}):
            self.borrow(3, **data)
        self.assertEqual(self.one("SELECT COUNT(*) FROM loan"), 3)

    def test_return_sets_the_date_once(self):
        self.client.post("/loans/2/return")
        self.assertEqual(self.one("SELECT returned_on FROM loan WHERE loan_id = 2"), TODAY)
        project.app.config["TODAY"] = "2026-03-05"
        self.assertIn("already returned", self.client.post("/loans/2/return", follow_redirects=True).get_data(as_text=True))
        self.assertEqual(self.one("SELECT returned_on FROM loan WHERE loan_id = 2"), TODAY)
        self.assertEqual(self.client.post("/loans/99/return").status_code, 404)

    def test_returning_makes_the_kit_available_again(self):
        self.client.post("/loans/1/return")
        self.assertIn("4 of 4", self.client.get("/").get_data(as_text=True))

    def test_actions_need_post(self):
        self.assertEqual(self.client.get("/loans/1/return").status_code, 405)
        self.assertEqual(self.client.get("/kits/1/delete").status_code, 405)


class TestKitsAndCategories(AppTestCase):
    GOOD = {"name": "Oscilloscope", "category_id": "1", "total_qty": "2", "notes": ""}

    def test_create_kit(self):
        r = self.client.post("/kits/new", data=self.GOOD)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.con.execute("SELECT name, total_qty, notes FROM kit WHERE name = 'Oscilloscope'").fetchall(),
                         [("Oscilloscope", 2, None)])

    def test_invalid_kit_shows_errors_and_keeps_values(self):
        html = self.client.post("/kits/new", data={"name": "x", "category_id": "99", "total_qty": "0", "notes": "keep me"}).get_data(as_text=True)
        self.assertEqual(html.count('class="error"'), 3)
        self.assertIn("keep me", html)
        self.assertEqual(self.one("SELECT COUNT(*) FROM kit"), 3)

    def test_duplicate_kit_name_is_a_friendly_error(self):
        html = self.client.post("/kits/new", data=dict(self.GOOD, name="Multimeter")).get_data(as_text=True)
        self.assertIn("already exists", html)

    def test_cannot_lower_total_below_the_number_out(self):
        html = self.client.post("/kits/1/edit", data=dict(self.GOOD, name="Multimeter", total_qty="2")).get_data(as_text=True)
        self.assertIn("3 are out on loan", html)
        self.assertEqual(self.one("SELECT total_qty FROM kit WHERE kit_id = 1"), 4)
        self.assertEqual(self.client.post("/kits/1/edit", data=dict(self.GOOD, name="Multimeter", total_qty="5")).status_code, 302)
        self.assertEqual(self.one("SELECT total_qty FROM kit WHERE kit_id = 1"), 5)

    def test_delete_rules(self):
        self.assertIn("cannot be deleted", self.client.post("/kits/2/delete", follow_redirects=True).get_data(as_text=True))
        self.assertEqual(self.one("SELECT COUNT(*) FROM kit WHERE kit_id = 2"), 1)
        self.client.post("/kits/3/delete")
        self.assertEqual(self.one("SELECT COUNT(*) FROM kit WHERE kit_id = 3"), 0)

    def test_category_rules(self):
        self.assertEqual(self.client.post("/categories", data={"name": "Batteries"}).status_code, 302)
        self.assertIn("already exists", self.client.post("/categories", data={"name": "Tools"}).get_data(as_text=True))
        self.assertIn("2 to 40", self.client.post("/categories", data={"name": "x"}).get_data(as_text=True))
        self.assertIn("still has kits", self.client.post("/categories/1/delete", follow_redirects=True).get_data(as_text=True))
        new_id = self.one("SELECT category_id FROM category WHERE name = 'Batteries'")
        self.client.post(f"/categories/{new_id}/delete")
        self.assertEqual(self.one("SELECT COUNT(*) FROM category WHERE name = 'Batteries'"), 0)

    def test_html_in_input_is_escaped(self):
        self.client.post("/kits/new", data=dict(self.GOOD, name="<script>alert(1)</script>"))
        self.assertNotIn("<script>alert", self.client.get("/").get_data(as_text=True))


class TestDatabaseRules(AppTestCase):
    """The database itself must refuse bad data, even if the Python code forgets to check."""

    def test_foreign_key_and_check_constraints(self):
        self.con.execute("PRAGMA foreign_keys = ON")
        with self.assertRaises(sqlite3.IntegrityError):
            self.con.execute("INSERT INTO kit (name, category_id, total_qty) VALUES ('Ghost', 99, 1)")
        with self.assertRaises(sqlite3.IntegrityError):
            self.con.execute("INSERT INTO loan (kit_id, borrower, qty, borrowed_on, due_on) VALUES (1, 'Mei', 0, '2026-01-01', '2026-01-08')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.con.execute("INSERT INTO loan (kit_id, borrower, qty, borrowed_on, due_on) VALUES (1, 'Mei', 1, '2026-01-08', '2026-01-01')")


class TestSeedData(unittest.TestCase):
    def test_seed_builds_and_every_page_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            project.app.config.update(DATABASE=str(Path(tmp) / "seed.db"), TESTING=True, TODAY=None)
            with project.app.app_context():
                project.init_db(seed=True)
            client = project.app.test_client()
            for url in ("/", "/kits/1", "/overdue", "/report", "/categories", "/kits/new", "/kits/1/edit"):
                self.assertEqual(client.get(url).status_code, 200, url)
            self.assertIn("Mei Lin", client.get("/overdue").get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
