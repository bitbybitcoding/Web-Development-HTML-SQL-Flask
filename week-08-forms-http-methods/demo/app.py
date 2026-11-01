"""Week 8 demo: forms, GET vs POST, validation, flash messages and Post/Redirect/Get.

Run from this folder with:   flask --app app run --debug
"""
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"   # needed for flash(); a real site keeps this secret (Week 11)

STUDENTS = [
    {"id": 1, "name": "Tan Wei Jie",    "class": "3A"},
    {"id": 2, "name": "Tabitha Lim",    "class": "3A"},
    {"id": 3, "name": "Tay Jun Hao",    "class": "3B"},
    {"id": 4, "name": "Tan Ming Yang",  "class": "3C"},
    {"id": 5, "name": "Deepa Krishnan", "class": "3B"},
]

FEEDBACK = []   # lives in memory only: it disappears when the server restarts (Week 9 fixes this)


@app.route("/")
def index():
    return render_template("index.html")


# ---- Part 1: GET form (search) -------------------------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = []
    if q:
        results = [s for s in STUDENTS if q.lower() in s["name"].lower()]
    return render_template("search.html", q=q, results=results)


# ---- Part 2: the same URL, two methods ------------------------------------
@app.route("/echo", methods=["GET", "POST"])
def echo():
    return render_template("echo.html", method=request.method,
                           args=request.args, form=request.form)


# ---- Part 3: validation, flash and Post/Redirect/Get ------------------------
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    errors = {}
    form = {"name": "", "rating": "", "comment": ""}
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}

        if not 2 <= len(form["name"]) <= 50:
            errors["name"] = "Please enter your name (2 to 50 characters)."
        if form["rating"] not in {"1", "2", "3", "4", "5"}:
            errors["rating"] = "Please choose a rating from 1 to 5."
        if len(form["comment"]) > 200:
            errors["comment"] = "Please keep your comment under 200 characters."

        if not errors:
            FEEDBACK.append({"name": form["name"], "rating": int(form["rating"]), "comment": form["comment"]})
            flash(f"Thank you, {form['name']}! Your feedback was saved.")
            return redirect(url_for("feedback_list"))      # Post/Redirect/Get
    return render_template("feedback.html", form=form, errors=errors)


@app.route("/feedback/all")
def feedback_list():
    average = round(sum(f["rating"] for f in FEEDBACK) / len(FEEDBACK), 1) if FEEDBACK else None
    return render_template("feedback_list.html", feedback=FEEDBACK, average=average)
