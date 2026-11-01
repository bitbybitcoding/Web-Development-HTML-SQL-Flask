"""Challenge 4: CCA showcase site."""
from flask import Flask, abort, render_template

from cca_data import CCAS

app = Flask(__name__)


def categories():
    return sorted({c["category"] for c in CCAS})


@app.context_processor
def inject_categories():
    # Makes `categories` available in every template (used by the navigation).
    return {"categories": categories()}


def find(slug):
    for c in CCAS:
        if c["slug"] == slug:
            return c
    return None


@app.route("/")
def home():
    biggest = max(CCAS, key=lambda c: c["members"])
    return render_template("home.html", biggest=biggest, total=sum(c["members"] for c in CCAS), count=len(CCAS))


@app.route("/ccas")
def ccas():
    return render_template("ccas.html", ccas=CCAS, heading="All CCAs")


@app.route("/ccas/<slug>")
def cca(slug):
    c = find(slug)
    if c is None:
        abort(404)
    same_day = [o for o in CCAS if o["day"] == c["day"] and o["slug"] != slug]
    return render_template("cca.html", c=c, same_day=same_day)


@app.route("/category/<name>")
def category(name):
    found = [c for c in CCAS if c["category"].lower() == name.lower()]
    if not found:
        abort(404)
    return render_template("ccas.html", ccas=found, heading=found[0]["category"])


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
