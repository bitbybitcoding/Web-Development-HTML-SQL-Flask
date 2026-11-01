"""Self-check for the Week 9 demo and Answers. Run:  python3 week-09-flask-sqlite-crud/Answers/tests_week9.py

Every test works on a throw-away COPY of the database, so nothing in the repository is changed.
"""
import importlib.util
import pathlib
import re
import shutil
import sqlite3
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
DEMO = HERE.parent / "demo"
ROOT = HERE.parents[1]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="week9-"))


def load(folder, name, seed_school=True):
    sys.path.insert(0, str(folder))
    sys.modules.pop("db", None)                    # each folder has its own db.py
    spec = importlib.util.spec_from_file_location(name, folder / "app.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    sys.path.pop(0)
    path = TMP / f"{name}.db"
    if seed_school:
        shutil.copy(ROOT / "school.db", path)
    module.app.config["DATABASE"] = str(path)      # use a private copy for the test
    return module, module.app.test_client(), path


def body(r, status=200):
    assert r.status_code == status, f"expected {status}, got {r.status_code}"
    return r.get_data(as_text=True)


def rows(path, sql, params=()):
    con = sqlite3.connect(path)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


GOOD = {"name": "Test Kid", "class": "3A", "gender": "F", "dob": "2009-01-02", "email": ""}


def test_demo():
    m, c, db = load(DEMO, "demo9")
    assert len(re.findall(r"/students/\d+", body(c.get("/")))) == 30
    t = body(c.get("/?q=tan&class=3A"))
    assert "Tan Wei Jie" in t and "Tan Ming Yang" not in t
    assert len(re.findall(r"/students/\d+", body(c.get("/?q=' OR 1=1 --")))) == 0       # injection attempt finds nothing
    assert "Tan Wei Jie" in body(c.get("/students/1")) and c.get("/students/999").status_code == 404
    assert "Mathematics" in body(c.get("/report"))
    # create
    t = body(c.post("/students/new", data=dict(GOOD, name="x", **{"class": "9"}, gender="Z", dob="no", email="bad")))
    assert t.count('class="error"') == 5 and rows(db, "SELECT COUNT(*) FROM students")[0][0] == 30
    r = c.post("/students/new", data=GOOD)
    assert r.status_code == 302
    new_id = int(r.headers["Location"].rsplit("/", 1)[1])
    assert rows(db, "SELECT name, email FROM students WHERE student_id = ?", (new_id,)) == [("Test Kid", None)]   # '' stored as NULL
    # update
    r = c.post(f"/students/{new_id}/edit", data=dict(GOOD, name="Renamed", email="a@b.sg"))
    assert r.status_code == 302 and rows(db, "SELECT name, email FROM students WHERE student_id = ?", (new_id,)) == [("Renamed", "a@b.sg")]
    assert "Renamed" in body(c.get(f"/students/{new_id}/edit"))
    # delete needs POST, and removes child rows first
    assert c.get("/students/1/delete").status_code == 405
    assert c.post("/students/1/delete").status_code == 302
    assert rows(db, "SELECT COUNT(*) FROM students WHERE student_id = 1")[0][0] == 0
    assert rows(db, "SELECT COUNT(*) FROM scores WHERE student_id = 1")[0][0] == 0
    assert rows(db, "SELECT COUNT(*) FROM student_cca WHERE student_id = 1")[0][0] == 0
    assert c.post("/students/1/delete").status_code == 404
    # the database itself refuses orphans (foreign keys are ON for every connection)
    with m.app.app_context():
        try:
            m.get_db().execute("INSERT INTO scores (student_id, subject_id, score) VALUES (9999, 1, 50)")
            raise AssertionError("foreign key was not enforced")
        except sqlite3.IntegrityError:
            pass
    assert "<script>" not in body(c.post("/students/new", data=dict(GOOD, name="<script>alert(1)</script>", email="bad")))


def test_challenges_1_to_3():
    m, c, db = load(HERE / "challenges-1-3-school", "school9")
    # Challenge 1: read
    t = body(c.get("/ccas"))
    assert "Chess Club" in t and "no members yet" in t
    robotics = rows(db, "SELECT cca_id, COUNT(*) FROM student_cca WHERE cca_id = 1")[0]
    assert f"/ccas/{robotics[0]}" in t
    t = body(c.get("/ccas?category=Sports"))
    assert "Basketball" in t and "Robotics" not in t
    t = body(c.get("/ccas/1"))
    assert "Robotics Club" in t and f"{robotics[1]} member" in t and "Leader" in t
    assert c.get("/ccas/99").status_code == 404
    # Challenge 2: create
    chess_before = rows(db, "SELECT COUNT(*) FROM student_cca WHERE cca_id = 8")[0][0]
    assert chess_before == 0
    r = c.post("/ccas/8/join", data={"student_id": "1", "role": "Leader"})
    assert r.status_code == 302 and rows(db, "SELECT role FROM student_cca WHERE cca_id = 8 AND student_id = 1") == [("Leader",)]
    assert "Tan Wei Jie" not in body(c.get("/ccas/8")).split("Add a member")[1]            # no longer offered
    assert "already in this CCA" in body(c.post("/ccas/8/join", data={"student_id": "1", "role": "Member"}, follow_redirects=True))
    assert "Choose a student" in body(c.post("/ccas/8/join", data={"student_id": "9999", "role": "Member"}, follow_redirects=True))
    assert "Choose a student" in body(c.post("/ccas/8/join", data={"student_id": "1 OR 1=1", "role": "Member"}, follow_redirects=True))
    assert "Choose a role" in body(c.post("/ccas/8/join", data={"student_id": "2", "role": "Boss"}, follow_redirects=True))
    assert rows(db, "SELECT COUNT(*) FROM student_cca WHERE cca_id = 8")[0][0] == 1
    # Challenge 3: update scores (blank -> NULL, invalid -> error, new row via upsert)
    rows_before = rows(db, "SELECT COUNT(*) FROM scores WHERE student_id = 1")[0][0]
    data = {f"score_{i}": str(60 + i) for i in range(1, 6)}
    data["score_2"] = ""
    r = c.post("/students/1/scores", data=data)
    assert r.status_code == 302
    saved = dict(rows(db, "SELECT subject_id, score FROM scores WHERE student_id = 1"))
    assert saved[1] == 61 and saved[2] is None and saved[5] == 65 and len(saved) == 5
    t = body(c.post("/students/1/scores", data=dict(data, score_1="101", score_3="abc")))
    assert t.count('class="error"') == 2 and 'value="101"' in t
    assert rows(db, "SELECT score FROM scores WHERE student_id = 1 AND subject_id = 1") == [(61,)]   # unchanged
    assert body(c.get("/students/1/scores")).count('type="text"') == 5
    # leave a CCA
    assert c.post("/ccas/8/leave/1").status_code == 302
    assert c.post("/ccas/8/leave/1").status_code == 404
    # delete a CCA: refused while it has members, allowed when empty
    assert "still has" in body(c.post("/ccas/1/delete", follow_redirects=True))
    assert rows(db, "SELECT COUNT(*) FROM ccas WHERE cca_id = 1")[0][0] == 1
    assert c.get("/ccas/8/delete").status_code == 405
    assert "Deleted Chess Club" in body(c.post("/ccas/8/delete", follow_redirects=True))
    assert rows(db, "SELECT COUNT(*) FROM ccas")[0][0] == 7
    # the demo features still work
    assert c.post("/students/new", data=GOOD).status_code == 302


def test_challenge_4_library():
    m, c, db = load(HERE / "challenge-4-library", "library9", seed_school=False)
    t = body(c.get("/"))
    assert t.count("/books/") >= 12 and "12 books" in t
    assert "overdue" in t and "Arjun" in t
    assert "1 book" in body(c.get("/?status=overdue")) and "Harry Potter" in body(c.get("/?status=overdue"))
    assert "Diary of a Wimpy Kid" in body(c.get("/?status=on loan"))
    assert "Matilda" in body(c.get("/?q=roald")) and "Hobbit" not in body(c.get("/?q=roald"))
    assert "0 books" in body(c.get("/?q=%25' OR 1=1 --"))
    # borrow / return
    assert "Lent to Mei" in body(c.post("/books/5/borrow", data={"borrower": "Mei"}, follow_redirects=True))
    assert "already on loan" in body(c.post("/books/5/borrow", data={"borrower": "Zoe"}, follow_redirects=True))
    assert "name (2 to 40" in body(c.post("/books/6/borrow", data={"borrower": " "}, follow_redirects=True))
    assert rows(db, "SELECT COUNT(*) FROM loan WHERE book_id = 5")[0][0] == 1
    assert "Book returned" in body(c.post("/books/5/return", data={}, follow_redirects=True))
    assert "not on loan" in body(c.post("/books/5/return", data={}, follow_redirects=True))
    assert rows(db, "SELECT returned_on IS NOT NULL FROM loan WHERE book_id = 5") == [(1,)]
    # reports
    t = body(c.get("/overdue"))
    assert "Harry Potter" in t and ">6<" in t and "Diary" not in t
    t = body(c.get("/stats"))
    assert t.index("Mei Lin") < t.index("Daniel") and "Wonder" in t.split("Never borrowed")[1]
    # create, duplicate, edit, delete rules
    r = c.post("/books/new", data={"title": "<b>New</b>", "author": "A. Writer"})
    assert r.status_code == 302
    new_id = int(r.headers["Location"].rsplit("/", 1)[1])
    assert "&lt;b&gt;New" in body(c.get(f"/books/{new_id}"))
    assert "already in the library" in body(c.post("/books/new", data={"title": "<b>New</b>", "author": "A. Writer"}))
    assert "required" in body(c.post("/books/new", data={"title": "", "author": ""}))
    assert c.post(f"/books/{new_id}/edit", data={"title": "Renamed", "author": "A. Writer"}).status_code == 302
    assert "already in the library" in body(c.post(f"/books/{new_id}/edit", data={"title": "The Hobbit", "author": "J.R.R. Tolkien"}))
    assert "cannot be deleted" in body(c.post("/books/2/delete", follow_redirects=True))      # has loan history
    assert c.post(f"/books/{new_id}/delete").status_code == 302 and c.get(f"/books/{new_id}").status_code == 404
    assert c.get("/books/999").status_code == 404


if __name__ == "__main__":
    failed = 0
    try:
        for name, fn in list(globals().items()):
            if name.startswith("test_"):
                try:
                    fn(); print("PASS", name)
                except AssertionError as e:
                    failed += 1; print("FAIL", name, e)
                except Exception as e:
                    failed += 1; print("ERROR", name, type(e).__name__, e)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
        for inst in HERE.parent.rglob("instance"):
            shutil.rmtree(inst, ignore_errors=True)
    sys.exit(1 if failed else 0)
