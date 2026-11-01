"""Week 9 demo: a Flask app with SQLite. Full CRUD on the students table.

Run from this folder with:   flask --app app run --debug
The first run copies school.db into ./instance/ (that copy is yours to change).
To start again from scratch, stop the server and delete the instance/ folder.
"""
import sqlite3

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from db import get_db, init_app

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
init_app(app)

CLASSES = ["3A", "3B", "3C"]


# ---- READ ----------------------------------------------------------------------
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    chosen = request.args.get("class", "")
    sql = """
        SELECT s.student_id, s.name, s.class, s.email,
               ROUND(AVG(sc.score), 1) AS average
        FROM students AS s
        LEFT JOIN scores AS sc ON sc.student_id = s.student_id
        WHERE s.name LIKE ?
    """
    params = [f"%{q}%"]
    if chosen in CLASSES:
        sql += " AND s.class = ?"
        params.append(chosen)
    sql += " GROUP BY s.student_id ORDER BY s.class, s.name"
    students = get_db().execute(sql, params).fetchall()
    return render_template("index.html", students=students, q=q, chosen=chosen, classes=CLASSES)


def get_student_or_404(student_id):
    student = get_db().execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    if student is None:
        abort(404)
    return student


@app.route("/students/<int:student_id>")
def student(student_id):
    db = get_db()
    s = get_student_or_404(student_id)
    scores = db.execute("""
        SELECT su.name AS subject, su.teacher, sc.score
        FROM scores AS sc JOIN subjects AS su ON su.subject_id = sc.subject_id
        WHERE sc.student_id = ? ORDER BY su.name
    """, (student_id,)).fetchall()
    ccas = db.execute("""
        SELECT c.name, sc.role FROM student_cca AS sc JOIN ccas AS c ON c.cca_id = sc.cca_id
        WHERE sc.student_id = ? ORDER BY c.name
    """, (student_id,)).fetchall()
    return render_template("student.html", s=s, scores=scores, ccas=ccas)


@app.route("/report")
def report():
    rows = get_db().execute("""
        SELECT su.name, su.teacher, COUNT(sc.score) AS sat, ROUND(AVG(sc.score), 1) AS average,
               MAX(sc.score) AS best, MIN(sc.score) AS lowest
        FROM subjects AS su LEFT JOIN scores AS sc ON sc.subject_id = su.subject_id
        GROUP BY su.subject_id ORDER BY average DESC
    """).fetchall()
    return render_template("report.html", rows=rows)


# ---- validation shared by create and update ---------------------------------------
def clean_form():
    form = {key: request.form.get(key, "").strip() for key in ("name", "class", "gender", "dob", "email")}
    errors = {}
    if not 2 <= len(form["name"]) <= 60:
        errors["name"] = "Name must be 2 to 60 characters."
    if form["class"] not in CLASSES:
        errors["class"] = "Choose a class."
    if form["gender"] not in ("M", "F"):
        errors["gender"] = "Choose M or F."
    if len(form["dob"]) != 10 or form["dob"][4] != "-" or form["dob"][7] != "-":
        errors["dob"] = "Date of birth must look like 2009-06-17."
    if form["email"] and ("@" not in form["email"] or " " in form["email"]):
        errors["email"] = "That does not look like an email address (or leave it empty)."
    return form, errors


# ---- CREATE --------------------------------------------------------------------
@app.route("/students/new", methods=["GET", "POST"])
def create():
    form, errors = {"name": "", "class": "", "gender": "", "dob": "", "email": ""}, {}
    if request.method == "POST":
        form, errors = clean_form()
        if not errors:
            db = get_db()
            with db:                                                   # commit, or roll back on error
                cur = db.execute(
                    "INSERT INTO students (name, class, gender, dob, email) VALUES (?, ?, ?, ?, ?)",
                    (form["name"], form["class"], form["gender"], form["dob"], form["email"] or None))
            flash(f"Added {form['name']}.")
            return redirect(url_for("student", student_id=cur.lastrowid))
    return render_template("form.html", form=form, errors=errors, classes=CLASSES, editing=False)


# ---- UPDATE --------------------------------------------------------------------
@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit(student_id):
    s = get_student_or_404(student_id)
    form, errors = dict(s), {}
    form["email"] = form["email"] or ""
    if request.method == "POST":
        form, errors = clean_form()
        if not errors:
            db = get_db()
            with db:
                db.execute("UPDATE students SET name = ?, class = ?, gender = ?, dob = ?, email = ? WHERE student_id = ?",
                           (form["name"], form["class"], form["gender"], form["dob"], form["email"] or None, student_id))
            flash("Changes saved.")
            return redirect(url_for("student", student_id=student_id))
    return render_template("form.html", form=form, errors=errors, classes=CLASSES, editing=True, student_id=student_id)


# ---- DELETE --------------------------------------------------------------------
@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete(student_id):
    s = get_student_or_404(student_id)
    db = get_db()
    with db:                                                             # all three deletes, or none
        db.execute("DELETE FROM scores WHERE student_id = ?", (student_id,))       # children first
        db.execute("DELETE FROM student_cca WHERE student_id = ?", (student_id,))
        db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))     # then the parent
    flash(f"Deleted {s['name']}.")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(sqlite3.IntegrityError)
def integrity_error(error):
    # A safety net: the checks above should stop bad data, but the database is the final guard.
    return render_template("404.html", message=f"The database refused that change: {error}"), 400
