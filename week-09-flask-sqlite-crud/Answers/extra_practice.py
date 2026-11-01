"""Week 9 extra practice 1-3: sorting with a whitelist, pagination, and a UNIQUE index.
Self-test:  python3 extra_practice.py       (works on a temporary copy of school.db)
"""
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

from flask import Flask, g, render_template_string, request

app = Flask(__name__)
SEED = Path(__file__).resolve().parents[2] / "school.db"
app.config["DATABASE"] = str(SEED)

# 1. SORTING. A column NAME cannot be a ? placeholder, so we only ever use names from our own whitelist.
SORTABLE = {"name": "s.name", "class": "s.class", "average": "average", "email": "s.email"}
PER_PAGE = 8


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


PAGE = """
{% for s in students %}<p class="row">{{ s.name }} {{ s['class'] }} {{ s.average }}</p>{% endfor %}
<p>Page {{ page }} of {{ pages }}</p>
{% if page > 1 %}<a href="{{ url_for('students', page=page - 1, sort=sort, order=order) }}">Previous</a>{% endif %}
{% if page < pages %}<a href="{{ url_for('students', page=page + 1, sort=sort, order=order) }}">Next</a>{% endif %}
"""


@app.route("/students")
def students():
    sort = request.args.get("sort", "name")
    if sort not in SORTABLE:                       # whitelist: anything else falls back to the default
        sort = "name"
    order = "DESC" if request.args.get("order") == "desc" else "ASC"
    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1

    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    pages = max(1, -(-total // PER_PAGE))          # ceiling division
    page = min(page, pages)
    sql = f"""
        SELECT s.student_id, s.name, s.class, s.email, ROUND(AVG(sc.score), 1) AS average
        FROM students AS s LEFT JOIN scores AS sc ON sc.student_id = s.student_id
        GROUP BY s.student_id
        ORDER BY {SORTABLE[sort]} {order}, s.name         -- safe: both parts come from our own constants
        LIMIT ? OFFSET ?
    """
    rows = db.execute(sql, (PER_PAGE, (page - 1) * PER_PAGE)).fetchall()
    return render_template_string(PAGE, students=rows, page=page, pages=pages, sort=sort, order=order.lower())


# 3. A UNIQUE index (SQLite cannot ADD a UNIQUE constraint with ALTER TABLE, but an index does the same job)
def add_unique_email_index(con):
    con.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_students_email ON students (email)")
    # NULLs do not count as duplicates, so students without an email are fine.


if __name__ == "__main__":
    tmp = Path(tempfile.mkdtemp()) / "school.db"
    shutil.copy(SEED, tmp)
    app.config["DATABASE"] = str(tmp)
    c = app.test_client()
    t = c.get("/students").get_data(as_text=True)
    assert t.count('class="row"') == 8 and "Page 1 of 4" in t and "Previous" not in t and "Next" in t
    t = c.get("/students?page=4").get_data(as_text=True)
    assert t.count('class="row"') == 6 and "Next" not in t and "Previous" in t
    assert "Page 4 of 4" in c.get("/students?page=999").get_data(as_text=True)      # clamped
    assert "Page 1 of 4" in c.get("/students?page=abc").get_data(as_text=True)      # bad input is ignored
    names = [p.split(" 3")[0] for p in c.get("/students?sort=name&order=desc").get_data(as_text=True).split('class="row">')[1:]]
    assert names == sorted(names, reverse=True)
    r = c.get("/students?sort=name;DROP TABLE students--")                           # not in the whitelist
    assert r.status_code == 200
    con = sqlite3.connect(tmp)
    assert con.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 30
    add_unique_email_index(con)
    try:
        con.execute("UPDATE students SET email = (SELECT email FROM students WHERE student_id = 1) WHERE student_id = 2")
        raise AssertionError("duplicate email accepted")
    except sqlite3.IntegrityError as e:
        assert "UNIQUE" in str(e)
    con.execute("UPDATE students SET email = NULL WHERE student_id IN (1, 2)")    # several NULLs are fine
    con.close()
    shutil.rmtree(tmp.parent)
    print("extra_practice.py: all checks passed")
    sys.exit(0)
