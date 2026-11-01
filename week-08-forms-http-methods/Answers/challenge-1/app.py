"""Challenge 1: a GET search form."""
from flask import Flask, render_template, request

from students_data import STUDENTS

app = Flask(__name__)


@app.route("/")
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    chosen_class = request.args.get("class", "")
    gender = request.args.get("gender", "")
    searched = "q" in request.args or "class" in request.args or "gender" in request.args

    results = [
        s for s in STUDENTS
        if q.lower() in s["name"].lower()
        and (chosen_class == "" or s["class"] == chosen_class)
        and (gender == "" or s["gender"] == gender)
    ]
    classes = sorted({s["class"] for s in STUDENTS})
    return render_template("search.html", q=q, chosen_class=chosen_class, gender=gender,
                           results=results, classes=classes, searched=searched)
