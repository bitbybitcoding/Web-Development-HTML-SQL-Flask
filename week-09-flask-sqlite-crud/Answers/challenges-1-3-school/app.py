"""Week 9 challenges 1-3: the demo app plus CCAs (read), joining a CCA (create), and editing scores / leaving / deleting (update and delete).

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


# ======================= CHALLENGE 1: READ (CCAs) =============================
@app.route("/ccas")
def ccas():
    category = request.args.get("category", "")
    db = get_db()
    categories = [r["category"] for r in db.execute("SELECT DISTINCT category FROM ccas ORDER BY category")]
    sql = """
        SELECT c.cca_id, c.name, c.category, c.day, COUNT(sc.student_id) AS members
        FROM ccas AS c LEFT JOIN student_cca AS sc ON sc.cca_id = c.cca_id
    """
    params = []
    if category in categories:
        sql += " WHERE c.category = ?"
        params.append(category)
    sql += " GROUP BY c.cca_id ORDER BY members DESC, c.name"
    rows = db.execute(sql, params).fetchall()
    return render_template("ccas.html", ccas=rows, categories=categories, category=category)


def get_cca_or_404(cca_id):
    cca = get_db().execute("SELECT * FROM ccas WHERE cca_id = ?", (cca_id,)).fetchone()
    if cca is None:
        abort(404)
    return cca


ROLES = ["Member", "Leader"]


@app.route("/ccas/<int:cca_id>")
def cca(cca_id):
    db = get_db()
    c = get_cca_or_404(cca_id)
    members = db.execute("""
        SELECT s.student_id, s.name, s.class, sc.role
        FROM student_cca AS sc JOIN students AS s ON s.student_id = sc.student_id
        WHERE sc.cca_id = ? ORDER BY sc.role DESC, s.name
    """, (cca_id,)).fetchall()
    # students who are NOT yet in this CCA (a subquery), for the join form
    available = db.execute("""
        SELECT student_id, name, class FROM students
        WHERE student_id NOT IN (SELECT student_id FROM student_cca WHERE cca_id = ?)
        ORDER BY class, name
    """, (cca_id,)).fetchall()
    return render_template("cca.html", c=c, members=members, available=available, roles=ROLES)


# ======================= CHALLENGE 2: CREATE (join a CCA) =====================
@app.route("/ccas/<int:cca_id>/join", methods=["POST"])
def join(cca_id):
    c = get_cca_or_404(cca_id)
    db = get_db()
    student_id = request.form.get("student_id", "")
    role = request.form.get("role", "")
    if not student_id.isdigit() or db.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,)).fetchone() is None:
        flash("Choose a student from the list.")
    elif role not in ROLES:
        flash("Choose a role: Member or Leader.")
    else:
        try:
            with db:
                db.execute("INSERT INTO student_cca (student_id, cca_id, role) VALUES (?, ?, ?)",
                           (int(student_id), cca_id, role))
            flash(f"Added to {c['name']}.")
        except sqlite3.IntegrityError:          # the PRIMARY KEY (student_id, cca_id) refuses duplicates
            flash("That student is already in this CCA.")
    return redirect(url_for("cca", cca_id=cca_id))


# ======================= CHALLENGE 3: UPDATE and DELETE =======================
@app.route("/students/<int:student_id>/scores", methods=["GET", "POST"])
def edit_scores(student_id):
    s = get_student_or_404(student_id)
    db = get_db()
    subjects = db.execute("SELECT subject_id, name FROM subjects ORDER BY name").fetchall()
    current = {r["subject_id"]: r["score"] for r in
               db.execute("SELECT subject_id, score FROM scores WHERE student_id = ?", (student_id,))}
    values = {sub["subject_id"]: "" if current.get(sub["subject_id"]) is None else str(current[sub["subject_id"]])
              for sub in subjects}
    errors = {}
    if request.method == "POST":
        values = {sub["subject_id"]: request.form.get(f"score_{sub['subject_id']}", "").strip() for sub in subjects}
        parsed = {}
        for sub in subjects:
            raw = values[sub["subject_id"]]
            if raw == "":
                parsed[sub["subject_id"]] = None          # blank = absent = NULL
            elif raw.isdigit() and 0 <= int(raw) <= 100:
                parsed[sub["subject_id"]] = int(raw)
            else:
                errors[sub["subject_id"]] = "Enter a whole number from 0 to 100, or leave blank for absent."
        if not errors:
            with db:
                for subject_id, score in parsed.items():
                    # INSERT ... ON CONFLICT updates the row if (student, subject) exists, otherwise adds it
                    db.execute("""
                        INSERT INTO scores (student_id, subject_id, score) VALUES (?, ?, ?)
                        ON CONFLICT (student_id, subject_id) DO UPDATE SET score = excluded.score
                    """, (student_id, subject_id, score))
            flash("Scores saved.")
            return redirect(url_for("student", student_id=student_id))
    return render_template("scores.html", s=s, subjects=subjects, values=values, errors=errors)


@app.route("/ccas/<int:cca_id>/leave/<int:student_id>", methods=["POST"])
def leave(cca_id, student_id):
    db = get_db()
    with db:
        cur = db.execute("DELETE FROM student_cca WHERE cca_id = ? AND student_id = ?", (cca_id, student_id))
    if cur.rowcount == 0:
        abort(404)
    flash("Removed from the CCA.")
    return redirect(url_for("cca", cca_id=cca_id))


@app.route("/ccas/<int:cca_id>/delete", methods=["POST"])
def delete_cca(cca_id):
    c = get_cca_or_404(cca_id)
    db = get_db()
    members = db.execute("SELECT COUNT(*) FROM student_cca WHERE cca_id = ?", (cca_id,)).fetchone()[0]
    if members > 0:
        flash(f"{c['name']} still has {members} member{'s' if members != 1 else ''}. Remove them first.")
        return redirect(url_for("cca", cca_id=cca_id))
    with db:
        db.execute("DELETE FROM ccas WHERE cca_id = ?", (cca_id,))
    flash(f"Deleted {c['name']}.")
    return redirect(url_for("ccas"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(sqlite3.IntegrityError)
def integrity_error(error):
    # A safety net: the checks above should stop bad data, but the database is the final guard.
    return render_template("404.html", message=f"The database refused that change: {error}"), 400
