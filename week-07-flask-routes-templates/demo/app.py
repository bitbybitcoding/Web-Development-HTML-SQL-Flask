"""Week 7 demo: our first Flask app.

Run from this folder with:   flask --app app run --debug
Then open the forwarded port 5000 (Codespaces shows a pop-up, or use the Ports tab).
"""
from flask import Flask, abort, render_template, request

app = Flask(__name__)

# Pretend data for now. In Week 9 this will come from school.db.
STUDENTS = [
    {"id": 1, "name": "Tan Wei Jie",   "class": "3A", "scores": {"Maths": 78, "Computing": 91, "Physics": 64}},
    {"id": 2, "name": "Tabitha Lim",   "class": "3A", "scores": {"Maths": 55, "Computing": 72, "Physics": 60}},
    {"id": 3, "name": "Tay Jun Hao",   "class": "3B", "scores": {"Maths": 88, "Computing": 69, "Physics": 81}},
    {"id": 4, "name": "Tan Ming Yang", "class": "3C", "scores": {"Maths": 47, "Computing": 58, "Physics": 52}},
    {"id": 5, "name": "Deepa Krishnan", "class": "3B", "scores": {"Maths": 93, "Computing": 97, "Physics": 90}},
]


def average(student):
    scores = student["scores"].values()
    return round(sum(scores) / len(scores), 1)


# ---- Part 1: routes that return text -------------------------------------
@app.route("/")
def index():
    return render_template("index.html", total=len(STUDENTS))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/hello/<name>")
def hello(name):
    # Jinja escapes <name> automatically, so <script> tricks are shown as text.
    return render_template("hello.html", name=name)


@app.route("/square/<int:n>")
def square(n):
    # <int:n> means Flask converts n to an int, and returns 404 if it is not a number.
    return f"{n} squared is {n * n}"


# ---- Part 2: routes that use templates and data ---------------------------
@app.route("/students")
def students():
    # /students?class=3A  -> only that class (request.args holds the query string)
    wanted = request.args.get("class")
    shown = [s for s in STUDENTS if wanted is None or s["class"] == wanted]
    classes = sorted({s["class"] for s in STUDENTS})
    return render_template("students.html", students=shown, classes=classes,
                           wanted=wanted, average=average)


@app.route("/students/<int:student_id>")
def student(student_id):
    for s in STUDENTS:
        if s["id"] == student_id:
            return render_template("student.html", s=s, avg=average(s))
    abort(404)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
