"""Challenge 1: Hello, Flask."""
import random
from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>My first Flask site</h1>
    <ul>
      <li><a href="/about">About</a></li>
      <li><a href="/time">What time is it?</a></li>
      <li><a href="/dice">Roll a die</a></li>
      <li><a href="/hello/Mei">Say hello</a></li>
    </ul>
    """


@app.route("/about")
def about():
    return "<h1>About</h1><p>I made this in Week 7.</p><p><a href='/'>Home</a></p>"


@app.route("/time")
def time_now():
    now = datetime.now().strftime("%H:%M:%S on %A, %d %B %Y")
    return f"<h1>It is {now}</h1><p><a href='/'>Home</a></p>"


@app.route("/dice")
def dice():
    roll = random.randint(1, 6)
    return f"<h1>You rolled a {roll}</h1><p><a href='/dice'>Roll again</a> · <a href='/'>Home</a></p>"


@app.route("/hello/<name>")
def hello(name):
    # Escape user text: it is placed straight into HTML here.
    from markupsafe import escape
    return f"<h1>Hello, {escape(name).title()}!</h1><p><a href='/'>Home</a></p>"
