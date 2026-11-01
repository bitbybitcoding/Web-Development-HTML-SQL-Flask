"""Challenge 2: routes with variables and converters."""
import math

from flask import Flask, abort
from markupsafe import escape

app = Flask(__name__)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return f"{a} + {b} = {a + b}"


@app.route("/area/<float:radius>")
def area(radius):
    # NOTE: <float:...> needs a decimal point, so /area/2 is a 404 but /area/2.0 works.
    return f"A circle of radius {radius} has area {math.pi * radius ** 2:.2f}"


@app.route("/day/<int:n>")
def day(n):
    if not 1 <= n <= 7:
        abort(404)
    return f"Day {n} of the week is {DAYS[n - 1]}"


@app.route("/shout/<text>")
def shout(text):
    return f"<h1>{escape(text.upper())}!</h1>"
