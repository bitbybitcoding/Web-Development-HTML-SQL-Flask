# Week 7 Extra Practice

For fast finishers, and homework for everyone else. Next week (Week 8) adds **forms and POST requests**.

---

## 1. Debug this app

This program has **six bugs**. Copy it, fix them one by one, and write what each error looked like.

```python
from flask import Flask, render_template

app = Flask(__name__)

STUDENTS = [{"name": "Mei", "class": "3A"}, {"name": "Arjun", "class": "3B"}]

@app.route("/")
def index()
    return render_template("index.html", students=STUDENTS)

@app.route("/student/<id>")
def student(id):
    return render_template("student.html", s=STUDENTS[id])

@app.route("/index")
def index():
    return "Home again"

@app.route("/count")
def count():
    render_template("count.html", n=len(STUDENTS))
```

and `templates/index.html` (inside a folder named `template`):

```html
<ul>
{% for s in students %}
  <li>{{ s.name }} ({{ s.class }})
{% endfor %}
</ul>
```

---

## 2. Jinja filters and macros

1. Using only filters in the template, show a list of names as `MEI, ARJUN, ZOE` from `["mei", "arjun", "zoe"]`. (Hint: `upper`, `join`.)
2. Show `Score: n/a` when a score is `None`, and `Score: 78.5` for `78.456`. (Hint: `default`, `round`.)
3. Write a **macro** (a function in a template) `card(title, text)` that draws a styled box, then use it three times.

---

## 3. A tiny JSON API

Add a route `/api/students` that returns the student list as JSON, using `jsonify`. Then add `/api/students/<int:id>` which returns JSON for one student, or a JSON error `{"error": "not found"}` with status 404. Open them in the browser. Why might a phone app prefer this to an HTML page?

---

## 4. Your own site

Choose a topic you love (a game, a sport, a band, a recipe collection) and build a three-page Flask site about it. It must have a base template, a static stylesheet, a list page and a detail page generated from a Python list of dictionaries.

---

## 5. Written questions (exam style)

1. State what is meant by a **route** in Flask. [1]
2. Explain the purpose of using a **template** instead of building HTML in a Python string. [2]
3. Describe, in order, what happens from the moment a browser requests `/students/3` until the page is shown. [3]
4. State **one** difference between `GET` requests and the other kinds of request, and explain why a link click is a `GET`. [2]
5. Explain why Flask templates automatically convert `<` into `&lt;`, and name the type of attack this helps to prevent. [2]
6. A student writes `@app.route("/user/<id>")` and visits `/user/abc`. The function uses `id + 1`. State what happens and how to prevent it. [2]
