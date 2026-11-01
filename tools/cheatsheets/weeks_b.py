"""Cheatsheet content for Weeks 7 to 11. Format: see lib.py."""

W7 = ("week-07-flask-routes-templates", "Flask: routes and templates", "Block 3: Flask", [
    ("h", "A minimal app"),
    ("code", """from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, Flask!</h1>"
"""),
    ("code", """flask --app app run --debug    # run in the folder
                               # that holds app.py
# open the forwarded port 5000 (Ports tab)
# stop the server: Ctrl+C"""),
    ("p", "**Browser asks → Python function answers.** `--debug` reloads on every save and shows errors. Never use it on a public site."),
    ("h", "Routes and variables"),
    ("code", """@app.route("/hello/<name>")
def hello(name): ...

@app.route("/square/<int:n>")   # 404 if not int
def square(n): ...

@app.route("/about")
def about(): ..."""),
    ("table", ["Converter", "Matches"], [
        ["`<name>` (or `<string:name>`)", "Any text without `/`"],
        ["`<int:n>`", "Whole numbers (digits only)"],
        ["`<float:x>`", "Decimals, **needs** a point: `2.0`"],
        ["`<path:p>`", "Text including `/`"],
    ], [0.5, 0.5]),
    ("p", "Every function name must be **unique**. Missing page → 404. `abort(404)` makes one on purpose."),
    ("h", "Folders Flask expects"),
    ("code", """project/
  app.py
  templates/    base.html, index.html ...
  static/       style.css, images ..."""),
    ("h", "Templates (Jinja)"),
    ("code", """# in app.py
return render_template("students.html",
                       students=STUDENTS, total=5)"""),
    ("table", ["Marker", "Meaning"], [
        ["`{{ value }}`", "Print a value (escaped automatically)"],
        ["`{% ... %}`", "A statement: `if`, `for`, `extends`, `block`"],
        ["`{# ... #}`", "Comment"],
    ], [0.35, 0.65]),
    ("code", """{% for s in students %}
  <li>{{ s.name }} ({{ s['class'] }})</li>
{% else %}
  <li>Nobody here.</li>
{% endfor %}

{% if score >= 50 %}Pass{% else %}Fail{% endif %}
{{ 'good' if avg >= 70 else '' }}"""),
    ("bullets", [
        "`s.name` and `s['name']` both read a dictionary key. Use `s['class']`.",
        "Filters: `{{ name|title }}`  `|upper`  `|length`  `|round(1)`  `|join(', ')`  `|default('n/a')`.",
        "Jinja turns `<` into `&lt;`, so user text cannot run as HTML (stops XSS).",
    ]),
    ("h", "One layout for all pages"),
    ("code", """<!-- templates/base.html -->
<title>{% block title %}Site{% endblock %}</title>
<link rel="stylesheet"
  href="{{ url_for('static',
  filename='style.css') }}">
<nav><a href="{{ url_for('index') }}">Home</a></nav>
{% block content %}{% endblock %}

<!-- templates/page.html -->
{% extends "base.html" %}
{% block content %}<h1>Page</h1>{% endblock %}"""),
    ("h", "Links and errors"),
    ("code", """url_for('student', student_id=3)   # /students/3
url_for('students', **{'class': '3A'})
                                # /students?class=3A

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404"""),
    ("tip", "Use `url_for('function_name')`, not typed paths. If the route changes, every link follows. Always add `, 404` to the error page, or the browser is told the page was found."),
    ("h", "Top mistakes"),
    ("bullets", [
        "Running `flask run` from the wrong folder (\"Could not import app\").",
        "Folder not called exactly `templates` (`TemplateNotFound`).",
        "Forgetting `return`.",
        "Missing `{% endfor %}` or `{% endif %}`.",
    ]),
])

W8 = ("week-08-forms-http-methods", "Forms and HTTP methods", "Block 3: Flask", [
    ("h", "Reading form data"),
    ("code", """from flask import request

request.args.get("q", "")    # GET: ?q=... in URL
request.form.get("name", "")       # POST: in the body
request.method                     # "GET" or "POST"
request.form.getlist("topping")    # all ticked boxes"""),
    ("bullets", [
        "Use `.get(key, default)`. `request.form['x']` on a missing field gives **400 Bad Request**.",
        "Everything from a form is a **string**: convert with `int()` after checking `.isdigit()`.",
        "A ticked checkbox sends its value; an unticked one sends **nothing**.",
    ]),
    ("h", "GET or POST?"),
    ("table", ["", "GET", "POST"], [
        ["Purpose", "Look (read)", "Change (write)"],
        ["Where", "URL query string", "Request body"],
        ["Safe to repeat?", "Yes", "No: may repeat the change"],
        ["Bookmark?", "Yes", "No"],
        ["Examples", "Search, filter, view", "Add, edit, delete, login"],
    ], [0.24, 0.38, 0.38]),
    ("p", "A **link is always a GET**. Anything that changes data must be a POST form with a button."),
    ("h", "One URL, two methods"),
    ("code", """@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    errors, form = {}, {"name": ""}
    if request.method == "POST":
        form = {"name":
            request.form.get("name", "").strip()}
        if not 2 <= len(form["name"]) <= 50:
            errors["name"] = "2 to 50 letters."
        if not errors:
            ...save...
            flash("Thank you!")
            return redirect(url_for("thanks"))
    return render_template("feedback.html",
                           form=form, errors=errors)"""),
    ("h", "The recipe"),
    ("bullets", [
        "**GET** → show an empty form.",
        "**POST** → read the fields, `strip()`, **validate on the server**.",
        "**Errors?** Show the **same form** again: messages beside the fields, and the values the user typed.",
        "**No errors?** Do the work, `flash()`, then **redirect**.",
    ]),
    ("h", "Post / Redirect / Get"),
    ("p", "After a successful POST, `redirect()` to a GET page. Then refresh or Back repeats only a harmless GET, not the POST (no double save)."),
    ("h", "Flash messages"),
    ("code", """app.secret_key = "dev-only-change-me"   # needed!
flash("Saved.")      # in the route, before redirect

{% for m in get_flashed_messages() %}
  <p class="flash">{{ m }}</p>
{% endfor %}          {# put in base.html #}"""),
    ("h", "Form snippets in Jinja"),
    ("code", """<input type="text" name="name"
       value="{{ form.name }}">
{% if errors.name %}
  <p class="error">{{ errors.name }}</p>{% endif %}

<option value="{{ n }}"
  {{ 'selected' if form.rating == n|string }}>
  {{ n }}</option>
<input type="radio" name="g" value="F"
  {{ 'checked' if form.g == 'F' }}>"""),
    ("tip", "Never trust the form. A `<select>` only offers some choices, but anyone can send anything: check the value on the server. `required` and `type=\"email\"` are conveniences, not safety."),
    ("h", "Errors you will meet"),
    ("table", ["Error", "Usual cause"], [
        ["**400** Bad Request", "`request.form['x']` for a missing field"],
        ["**405** Method Not Allowed", "Route lacks `methods=[\"POST\"]` (or GET sent to a POST route)"],
        ["`RuntimeError ... secret key`", "`flash` used without `app.secret_key`"],
        ["Page saves twice on refresh", "No redirect after POST"],
    ], [0.4, 0.6]),
])

W9 = ("week-09-flask-sqlite-crud", "Flask and SQLite: CRUD", "Block 3: Flask", [
    ("h", "One connection per request"),
    ("code", """import sqlite3
from flask import g

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
        db.close()"""),
    ("p", "`g` lasts for one request. `Row` lets you write `row['name']` and `{{ row.name }}`. Foreign keys must be switched on for **every** connection."),
    ("h", "CRUD"),
    ("table", ["", "Method", "SQL"], [
        ["**C**reate", "POST", "`INSERT INTO t (a, b) VALUES (?, ?)`"],
        ["**R**ead", "GET", "`SELECT ... WHERE id = ?`"],
        ["**U**pdate", "POST", "`UPDATE t SET a = ? WHERE id = ?`"],
        ["**D**elete", "POST", "`DELETE FROM t WHERE id = ?`"],
    ], [0.2, 0.2, 0.6]),
    ("p", "HTML forms only send GET or POST, so update and delete use POST."),
    ("h", "Read"),
    ("code", """rows = get_db().execute(
    "SELECT * FROM students WHERE name LIKE ?",
    (f"%{q}%",)).fetchall()
row = db.execute(
    "SELECT * FROM students WHERE student_id = ?",
    (sid,)).fetchone()
if row is None:
    abort(404)"""),
    ("h", "Create, update, delete: with db:"),
    ("code", """db = get_db()
with db:           # commit, or roll back on error
    cur = db.execute(
        "INSERT INTO students (name, class) "
        "VALUES (?, ?)",
        (name, cls))
new_id = cur.lastrowid      # the new primary key
flash("Added.")
return redirect(url_for("student", student_id=new_id))"""),
    ("bullets", [
        "`cur.lastrowid` = new id. `cur.rowcount` = rows changed (0 → 404?).",
        "Store an empty optional field as **NULL**: `email or None`.",
        "Catch duplicates: `try: with db: ... except sqlite3.IntegrityError:` and show a friendly message.",
    ]),
    ("h", "Delete in the right order"),
    ("code", """with db:       # all three, or none
    db.execute("DELETE FROM scores "
               "WHERE student_id=?", (i,))
    db.execute("DELETE FROM student_cca "
               "WHERE student_id=?", (i,))
    db.execute("DELETE FROM students "
               "WHERE student_id=?", (i,))"""),
    ("p", "**Children first, then the parent.** With foreign keys on, deleting the parent first fails (`FOREIGN KEY constraint failed`): good. With them off, you get silent orphan rows: bad."),
    ("h", "Upsert (insert or update)"),
    ("code", """INSERT INTO scores (student_id, subject_id, score)
VALUES (?, ?, ?)
ON CONFLICT (student_id, subject_id)
DO UPDATE SET score = excluded.score;"""),
    ("h", "Sorting safely"),
    ("code", """SORTABLE = {"name": "s.name", "class": "s.class"}
col = SORTABLE.get(request.args.get("sort"), "s.name")
db.execute(f"SELECT ... ORDER BY {col}")
#                 col is OUR text, not the user's"""),
    ("tip", "A column name cannot be a `?`. Use a **whitelist** dictionary: the user chooses a key, and the SQL contains only your own text."),
    ("h", "Working copy of the database"),
    ("p", "The demo copies `school.db` to `instance/school.db`. Delete the `instance/` folder to start again. Look inside with the SQLite Viewer or `sqlite3 instance/school.db`."),
    ("h", "Checklist for every route"),
    ("bullets", [
        "`?` placeholders only. No f-strings with user data.",
        "Changes are POST, inside `with db:`, then redirect.",
        "Validate first; unknown id → 404; handle duplicates.",
    ]),
])

W10 = ("week-10-plan-and-build", "Capstone: plan and build", "Block 4: Capstone", [
    ("h", "Plan before you code"),
    ("bullets", [
        "**Users:** name at least two kinds.",
        "**User story:** *As a ___, I want to ___ so that ___.*",
        "**MVP:** the smallest version that works and meets the brief. **Stretch:** everything else.",
        "**Database:** entities → ER diagram → tables in 3NF, with keys and constraints.",
        "**Route map:** page, URL, methods, SQL.",
    ]),
    ("table", ["Page", "URL", "Method", "SQL"], [
        ["List", "`/`", "GET", "`SELECT ... JOIN`"],
        ["Add", "`/new`", "GET, POST", "`INSERT`"],
        ["Edit", "`/<id>/edit`", "GET, POST", "`UPDATE`"],
        ["Delete", "`/<id>/delete`", "POST", "`DELETE`"],
        ["Report", "`/report`", "GET", "`GROUP BY`"],
    ], [0.18, 0.30, 0.22, 0.30]),
    ("tip", "**Do not store what you can calculate** (availability, totals, age). Store the facts it is calculated from."),
    ("h", "Start from the template"),
    ("code", """cp -r week-10-plan-and-build/capstone-template \\
      my-work/capstone
cd my-work/capstone
flask --app app init-db     # builds instance/app.db
flask --app app run --debug
python3 -m unittest discover -s tests -v"""),
    ("p", "`init-db` runs `schema.sql` then `seed.sql` and **deletes the old data**. Re-run it whenever you change either file."),
    ("table", ["File", "Purpose"], [
        ["`PLAN.md`", "Your plan"],
        ["`schema.sql`", "`CREATE TABLE`: parents first"],
        ["`seed.sql`", "Realistic sample data (8+ rows)"],
        ["`app.py`", "Routes and helpers"],
        ["`templates/` `static/`", "Pages and CSS"],
        ["`tests/`", "Automated tests"],
    ], [0.38, 0.62]),
    ("h", "Build a vertical slice"),
    ("p", "One feature through every layer: **table → SQL → route → template → test**. Prove each step before the next: try the SQL in `sqlite3` first."),
    ("h", "For each form: the same four steps"),
    ("p", "**validate → `with db:` → flash → redirect**"),
    ("h", "Git: save and share"),
    ("code", """git status
git add my-work/capstone
git commit -m "Add kit list page"
#   say WHAT; start with a verb
git push

git switch -c feature/overdue       # new branch
git switch main
git merge feature/overdue
git log --oneline"""),
    ("bullets", [
        "Commit small and often, after something works. At least **10 commits** are needed.",
        "Never commit secrets or the database file (`instance/` is ignored).",
        "Merge conflict: edit the file, delete the `<<<<<<<` `=======` `>>>>>>>` lines, `git add`, `git commit`.",
    ]),
    ("h", "Capstone must-haves"),
    ("bullets", [
        "2+ related tables in 3NF with constraints and a foreign key.",
        "CRUD, a search or filter, and a `GROUP BY`/join report.",
        "Server-side validation; `?` placeholders; POST for changes; 404 page.",
        "Base template, CSS, `url_for`, flash messages; realistic seed data.",
        "Week 11: 8+ tests, a README, 10+ commits.",
    ]),
])

W11 = ("week-11-test-polish-present", "Test, polish and present", "Block 4: Capstone", [
    ("h", "A unit test"),
    ("code", """import unittest
from grades import grade

class TestGrade(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(grade(75), "A")
        self.assertEqual(grade(74), "B")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            grade(101)

if __name__ == "__main__":
    unittest.main()"""),
    ("code", """python3 -m unittest -v
python3 -m unittest discover -s tests -v"""),
    ("table", ["Assertion", "Checks"], [
        ["`assertEqual(a, b)`", "`a == b`"],
        ["`assertTrue(x)` / `assertFalse(x)`", "Truth"],
        ["`assertIn(a, b)` / `assertNotIn`", "`a` is (not) inside `b`"],
        ["`assertIsNone(x)`", "`x is None`"],
        ["`assertRaises(Err)`", "Code raises that error"],
    ], [0.55, 0.45]),
    ("p", "Arrange (set up) → **Act** (call it) → **Assert** (check). `setUp` runs before **every** test. `with self.subTest(x=x):` reports each failing value."),
    ("h", "Test a Flask app"),
    ("code", """def setUp(self):
    self.tmp = tempfile.TemporaryDirectory()
    app.config.update(
        DATABASE=self.tmp.name + "/t.db",
        TESTING=True)
    with app.app_context():
        init_db(seed=True)          # fresh data
    self.client = app.test_client()

r = self.client.post("/new", data={"name": "x"})
self.assertEqual(r.status_code, 302)   # redirect
html = self.client.get("/").get_data(as_text=True)"""),
    ("bullets", [
        "Each test gets its **own temporary database**; never test on real data.",
        "Check the **database** (`SELECT`) as well as the page.",
        "`follow_redirects=True` follows the redirect to the page after it.",
    ]),
    ("h", "What to test"),
    ("table", ["Kind", "Example"], [
        ["Happy path", "Valid form saves a row"],
        ["Invalid input", "Rejected; message shown; nothing saved"],
        ["Boundary", "Largest valid value passes; one more fails"],
        ["Not found", "Unknown id → 404"],
        ["Wrong method", "GET on a POST route → 405"],
        ["Database rule", "Constraint refuses a bad row"],
        ["Hostile input", "`' OR 1=1 --`, `<script>` are harmless"],
    ], [0.3, 0.7]),
    ("tip", "Bugs hide on **boundaries**. Test the value on each side of every limit. A passing test shows only that the cases you thought of work."),
    ("h", "Polish checklist"),
    ("bullets", [
        "Wording consistent; no template text, debug prints or \"Test 1\" data left.",
        "Every list has an empty state message.",
        "Error messages are beside the field and say how to fix it.",
        "Labels on all inputs; 16px text; 44px buttons; works at iPad width.",
        "Colour is never the only signal; headings in order; `alt` text.",
        "Dangerous actions are POST buttons that look different.",
    ]),
    ("h", "README sections"),
    ("p", "Problem · Features · How to run · ER diagram and design · Design decisions · Testing · Limitations and next steps · What I learned."),
    ("h", "On a real server"),
    ("bullets", [
        "**No debug mode.** No `app.run()` at the top level.",
        "Secret key from the environment: `os.environ.get(\"SECRET_KEY\")`.",
        "Build the database with `flask --app app init-db` **once**; it is not in Git.",
        "Deploy steps: clone → virtualenv → `init-db` → WSGI file → Reload.",
    ]),
    ("h", "Present: 3 minutes"),
    ("table", ["Part", "Time"], [
        ["The problem", "30 s"],
        ["Live demo of one story, with an error", "90 s"],
        ["ER diagram, one query, one test", "40 s"],
        ["Reflection: hardest bug, next step", "20 s"],
    ], [0.75, 0.25]),
])
