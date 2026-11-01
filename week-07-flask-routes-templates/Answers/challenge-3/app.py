"""Challenge 3: class results site with templates."""
from flask import Flask, abort, render_template

app = Flask(__name__)

STUDENTS = [
    {"id": 1, "name": "Tan Wei Jie",    "class": "3A", "scores": {"Maths": 78, "Computing": 91, "Physics": 64}},
    {"id": 2, "name": "Tabitha Lim",    "class": "3A", "scores": {"Maths": 55, "Computing": 72, "Physics": 60}},
    {"id": 3, "name": "Tay Jun Hao",    "class": "3B", "scores": {"Maths": 88, "Computing": 69, "Physics": 81}},
    {"id": 4, "name": "Tan Ming Yang",  "class": "3C", "scores": {"Maths": 47, "Computing": 58, "Physics": 52}},
    {"id": 5, "name": "Deepa Krishnan", "class": "3B", "scores": {"Maths": 93, "Computing": 97, "Physics": 90}},
    {"id": 6, "name": "Ethan Koh",      "class": "3C", "scores": {"Maths": 62, "Computing": 80, "Physics": 49}},
]


def average(student):
    values = student["scores"].values()
    return round(sum(values) / len(values), 1)


@app.route("/")
def home():
    return render_template("home.html", total=len(STUDENTS))


@app.route("/students")
def students():
    return render_template("students.html", students=STUDENTS, heading="All students", average=average)


@app.route("/students/<int:student_id>")
def student(student_id):
    for s in STUDENTS:
        if s["id"] == student_id:
            return render_template("student.html", s=s, avg=average(s))
    abort(404)


@app.route("/class/<code>")
def by_class(code):
    code = code.upper()
    found = [s for s in STUDENTS if s["class"] == code]
    if not found:
        abort(404)
    return render_template("students.html", students=found, heading=f"Class {code}", average=average)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
