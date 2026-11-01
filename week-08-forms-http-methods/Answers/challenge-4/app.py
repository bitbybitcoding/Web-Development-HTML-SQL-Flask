"""Challenge 4: a quiz with a leaderboard."""
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from quiz_data import QUESTIONS

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

ATTEMPTS = []    # {"id", "name", "score", "total", "wrong": [question ids]}


@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not 2 <= len(name) <= 30:
            flash("Enter a name of 2 to 30 characters.")
            return render_template("start.html", name=name)
        session["name"] = name                     # remembered between requests (a cookie)
        return redirect(url_for("quiz"))
    return render_template("start.html", name=session.get("name", ""))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "name" not in session:
        return redirect(url_for("start"))
    if request.method == "POST":
        missing = [q["id"] for q in QUESTIONS if request.form.get(f"q{q['id']}") is None]
        if missing:
            flash(f"Please answer every question ({len(missing)} left).")
            return render_template("quiz.html", questions=QUESTIONS, picked=request.form), 200
        wrong, score = [], 0
        for q in QUESTIONS:
            try:
                picked = int(request.form[f"q{q['id']}"])
            except ValueError:
                abort(400)
            if picked == q["answer"]:
                score += 1
            else:
                wrong.append(q["id"])
        attempt = {"id": len(ATTEMPTS) + 1, "name": session["name"], "score": score,
                   "total": len(QUESTIONS), "wrong": wrong}
        ATTEMPTS.append(attempt)
        return redirect(url_for("result", attempt_id=attempt["id"]))
    return render_template("quiz.html", questions=QUESTIONS, picked={})


@app.route("/result/<int:attempt_id>")
def result(attempt_id):
    if not 1 <= attempt_id <= len(ATTEMPTS):
        abort(404)
    attempt = ATTEMPTS[attempt_id - 1]
    wrong_questions = [q for q in QUESTIONS if q["id"] in attempt["wrong"]]
    return render_template("result.html", a=attempt, wrong_questions=wrong_questions)


@app.route("/leaderboard")
def leaderboard():
    best = sorted(ATTEMPTS, key=lambda a: (-a["score"], a["id"]))[:5]
    return render_template("leaderboard.html", best=best)
