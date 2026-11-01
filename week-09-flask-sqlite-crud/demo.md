# Week 9 Demo: Flask and SQLite

**Time:** 45 minutes. Students type along, working from `my-work/week09/`.
**Code:** [demo/](demo/): `db.py`, `app.py`, `templates/`, `static/`

The goal: replace the Python lists of the last two weeks with the real `school.db`.

Start by copying the demo's `static/` and `templates/base.html`, and `db.py` into `my-work/week09/`. Then build `app.py` step by step.

---

## Part 1: Connecting Flask to SQLite (10 min)

A web server handles many requests, so **each request gets its own connection**, opened when needed and closed afterwards:

```python
import sqlite3
from flask import g, current_app

def get_db():
    if "db" not in g:                                   # g = a notebook that lasts for one request
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row                  # rows work like dictionaries
        g.db.execute("PRAGMA foreign_keys = ON")        # must be repeated for EVERY connection
    return g.db

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# in app.py:   app.teardown_appcontext(close_db)
```

- `flask.g` is a per-request storage space. The first call to `get_db()` connects; later calls in the same request reuse the connection.
- `sqlite3.Row` lets the template write `s.name` or Python write `row["name"]` instead of `row[1]`.
- `teardown_appcontext` runs after every request, even when an error happened. The connection never leaks.
- [demo/db.py](demo/db.py) also copies `school.db` into `instance/` the first time, so the original is safe.

## Part 2: Read (10 min)

```python
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    students = get_db().execute(
        "SELECT student_id, name, class FROM students WHERE name LIKE ? ORDER BY class, name",
        (f"%{q}%",)
    ).fetchall()
    return render_template("index.html", students=students, q=q)
```

- This is the Week 3 query with a Week 6 placeholder. **Never** build the SQL with an f-string. Try typing `' OR 1=1 --` in the search box: nothing is found, because it is treated as text.
- `.fetchall()` returns a list of rows, `.fetchone()` returns one row or `None` (that is how we decide on a 404).
- Show the join: [demo/app.py](demo/app.py) `index()` joins `scores` to show each student's average with `LEFT JOIN` + `GROUP BY` (Week 4), and the detail page shows the `scores` and `student_cca` rows (Week 4 joins).
- `/report` is a single `GROUP BY` query. Reports are just SQL plus a table.

## Part 3: Create (10 min)

```python
@app.route("/students/new", methods=["GET", "POST"])
def create():
    ...
    if request.method == "POST":
        form, errors = clean_form()            # Week 8: trim, validate
        if not errors:
            db = get_db()
            with db:                           # commits on success, rolls back on error
                cur = db.execute("INSERT INTO students (name, class, gender, dob, email) VALUES (?, ?, ?, ?, ?)", (...))
            flash("Added.")
            return redirect(url_for("student", student_id=cur.lastrowid))
    return render_template("form.html", form=form, errors=errors, ...)
```

- `cur.lastrowid` is the new primary key. We redirect straight to the new student's page (Post/Redirect/Get).
- Empty email is stored as `NULL`, not `''`: `form["email"] or None`. (Why? `NULL` means "unknown"; `''` would break `WHERE email IS NULL`.)
- `with db:` is the Week 6 transaction.
- Try: add a student with class `9Z` and see the validation. Then remove the validation in the code and see what the database does (the `students` table only checks `gender`, so the bad class is **accepted**). The lesson: *constraints in the database are the last line of defence; validation in Python gives friendly messages. Use both.*

## Part 4: Update and Delete (10 min)

**Update** reuses the same form template. Differences: it first loads the existing row to fill the form, and uses `UPDATE ... WHERE student_id = ?`.

```python
db.execute("UPDATE students SET name = ?, class = ?, gender = ?, dob = ?, email = ? WHERE student_id = ?",
           (..., student_id))
```

Ask: *what happens if we forget the `WHERE`?* (Every student gets the same name.) Show it on the board, not on the screen.

**Delete** is a POST (a link would be a GET: dangerous) and must respect the foreign keys:

```python
@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete(student_id):
    s = get_student_or_404(student_id)
    db = get_db()
    with db:
        db.execute("DELETE FROM scores WHERE student_id = ?", (student_id,))       # children first
        db.execute("DELETE FROM student_cca WHERE student_id = ?", (student_id,))
        db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))     # then the parent
    flash(f"Deleted {s['name']}.")
    return redirect(url_for("index"))
```

Experiment (comment out the first two deletes): the page shows an error page, `sqlite3.IntegrityError: FOREIGN KEY constraint failed`. Good: the database refused to leave orphan rows. Now comment out `PRAGMA foreign_keys = ON` and repeat: the delete "works", and the `scores` table now has rows for a student that does not exist. **Silent corruption is worse than an error.**

`with db:` wraps the three deletes in one transaction: if the third fails, the first two are undone.

## Part 5: Look inside (5 min)

Open `instance/school.db` in the Explorer (SQLite Viewer) or run `sqlite3 instance/school.db`. Check that the student you added is there. Run:

```sql
SELECT COUNT(*) FROM scores WHERE student_id NOT IN (SELECT student_id FROM students);   -- orphans: should be 0
```

---

## Summary table for the board

| CRUD | Route | Method | SQL | After success |
|------|-------|--------|-----|---------------|
| Read (list) | `/` | GET | `SELECT ... WHERE name LIKE ?` | show page |
| Read (one) | `/students/<id>` | GET | `SELECT ... WHERE student_id = ?` | 404 if no row |
| Create | `/students/new` | GET + POST | `INSERT ... VALUES (?, ?, ...)` | redirect |
| Update | `/students/<id>/edit` | GET + POST | `UPDATE ... WHERE student_id = ?` | redirect |
| Delete | `/students/<id>/delete` | POST | `DELETE ... WHERE student_id = ?` | redirect |
