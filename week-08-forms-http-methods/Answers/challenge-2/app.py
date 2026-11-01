"""Challenge 2: a POST sign-up form with server-side validation."""
import re

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

CLASSES = ["3A", "3B", "3C"]
CCAS = ["Robotics Club", "Chess Club", "Football", "Badminton", "Choir", "Scouts"]
MEMBERS = []
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate(form):
    """Return a dict of field -> error message. An empty dict means the form is valid."""
    errors = {}
    if not 2 <= len(form["name"]) <= 50:
        errors["name"] = "Name must be 2 to 50 characters."
    if form["class"] not in CLASSES:
        errors["class"] = "Choose your class."
    if not EMAIL_PATTERN.match(form["email"]):
        errors["email"] = "Enter a valid email address, like name@example.com."
    if form["cca"] not in CCAS:
        errors["cca"] = "Choose one CCA."
    if form["agree"] != "yes":
        errors["agree"] = "You must agree to attend sessions."
    if not errors and any(m["email"].lower() == form["email"].lower() for m in MEMBERS):
        errors["email"] = "That email has already signed up."
    return errors


@app.route("/", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = {"name": "", "class": "", "email": "", "cca": "", "agree": ""}
    errors = {}
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        errors = validate(form)
        if not errors:
            MEMBERS.append({k: form[k] for k in ("name", "class", "email", "cca")})
            flash(f"Welcome to {form['cca']}, {form['name']}!")
            return redirect(url_for("members"))
    return render_template("signup.html", form=form, errors=errors, classes=CLASSES, ccas=CCAS)


@app.route("/members")
def members():
    return render_template("members.html", members=MEMBERS)
