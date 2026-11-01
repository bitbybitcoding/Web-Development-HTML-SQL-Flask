"""Challenge 3 starter: class results site. Copy this folder to my-work/week07/challenge-3/."""
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

# TODO 1: route "/"  -> home page template
# TODO 2: route "/students" -> table of all students (loop in the template)
# TODO 3: route "/students/<int:student_id>" -> detail page; abort(404) if there is no such student
# TODO 4: route "/class/<code>" -> only the students in that class (e.g. 3B)
# TODO 5: custom 404 page with @app.errorhandler(404)
