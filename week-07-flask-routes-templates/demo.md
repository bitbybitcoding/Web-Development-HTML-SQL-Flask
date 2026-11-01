# Week 7 Demo: Your first Flask app

**Time:** 45 minutes. Students type along.
**Code:** [demo/](demo/): `app.py`, `templates/`, `static/style.css`

Everything today is Python plus HTML. The data is a hard-coded Python list; in Week 9 it moves into SQLite.

---

## Part 0: Set up and run (5 min)

In the Codespaces terminal:

```bash
mkdir -p my-work/week07 && cd my-work/week07
```

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, Flask!</h1>"
```

Run it:

```bash
flask --app app run --debug
```

Codespaces shows a pop-up: **Open in Browser**. If you miss it (common on iPad), open the **Ports** tab at the bottom, find port **5000**, and tap the globe icon.

Three things to point out:

1. The terminal is now *busy*: it is the server. Stop it with **Ctrl+C** (on an iPad keyboard, use the on-screen Ctrl, or open a second terminal with **+**).
2. `--debug` reloads the server whenever you save, and shows a helpful error page when your code breaks. **Never use debug mode on a public server.**
3. The **browser asks, the Python function answers.** Every page is a function.

## Part 1: Routes (10 min)

A **route** connects a URL to a function. The function's return value is the page.

```python
@app.route("/about")
def about():
    return "<p>We are a coding club.</p>"

@app.route("/hello/<name>")
def hello(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route("/square/<int:n>")
def square(n):
    return f"{n} squared is {n * n}"
```

- Visit `/hello/Mei` and `/hello/Arjun`: one function, many pages.
- Visit `/square/12` (works), `/square/abc` (**404**: the `int:` converter rejected it).
- Ask: *what happens if you visit `/hello/` with no name?* (404: no route matches.)
- Ask: *what happens if two functions have the same name?* (Flask refuses to start. Function names must be unique because `url_for` uses them.)

### Danger: building HTML in strings

Visit `/hello/<i>Amy` with the f-string version. The browser *runs* what the user typed. This is the **cross-site scripting (XSS)** cousin of SQL injection: untrusted text mixed into code. Templates fix this, and that is why we move on.

## Part 2: Templates with Jinja (15 min)

Create a `templates/` folder (**exactly that name**, next to `app.py`). Python sends *data*; the template decides the *layout*.

`app.py`:

```python
from flask import render_template

@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

`templates/hello.html`:

```html
<h1>Hello, {{ name|title }}!</h1>
<p>Your name has {{ name|length }} characters.</p>
```

Jinja has three kinds of marker:

| Marker | Meaning | Example |
|--------|---------|---------|
| `{{ ... }}` | print a value | `{{ s.name }}` |
| `{% ... %}` | a statement (`if`, `for`, `extends`) | `{% for s in students %}` |
| `{# ... #}` | comment | `{# todo #}` |

Now revisit `/hello/<i>Amy`: the tag is displayed as text. **Jinja escapes values automatically**, so `<` becomes `&lt;`.

**Loops and conditions.** Copy the `STUDENTS` list from [demo/app.py](demo/app.py), then `templates/students.html`:

```html
{% if students %}
<table>
  {% for s in students %}
  <tr class="{{ 'good' if average(s) >= 70 else '' }}">
    <td>{{ s.name }}</td>
    <td>{{ s['class'] }}</td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p>No students found.</p>
{% endif %}
```

Notes for the board:

- `s.name` and `s['name']` do the same for dictionaries. `class` is a Python keyword-like word in some contexts, so `s['class']` is safer.
- You can pass a **function** (`average=average`) and call it in the template; but heavy logic belongs in Python.
- Common filters: `title`, `upper`, `length`, `round(1)`, `join(", ")`, `default("n/a")`.

## Part 3: Template inheritance, static files and `url_for` (10 min)

Every page repeats the `<head>`, nav and footer. Use a **base template**:

`templates/base.html` (see [demo/templates/base.html](demo/templates/base.html)) defines `{% block title %}` and `{% block content %}`. Each page starts with:

```html
{% extends "base.html" %}
{% block content %}
  ...only what is different on this page...
{% endblock %}
```

**Static files.** CSS, images and JavaScript go in a folder called `static/`. Link them with:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

**`url_for('function_name')`** builds a URL from the *function name*, so links keep working even if you change the URL later:

```html
<a href="{{ url_for('student', student_id=s.id) }}">{{ s.name }}</a>
```

Finally the detail page and a 404 page:

```python
@app.route("/students/<int:student_id>")
def student(student_id):
    for s in STUDENTS:
        if s["id"] == student_id:
            return render_template("student.html", s=s, avg=average(s))
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
```

The `, 404` matters: without it the page says "not found" but the browser is told "OK".

**Extra:** `/students?class=3A` uses `request.args.get("class")`: the part after `?` is the **query string**. This is exactly what a GET form sends (Week 2); Week 8 builds on it.

---

## Wrap-up questions

1. What is the difference between `{{ }}` and `{% %}`?
2. Why does Flask look for a folder named exactly `templates`?
3. What would happen if `base.html` had no blocks?
4. Why is `url_for` better than writing `href="/students/3"`?

Answers are in the instructor notes on [README.md](README.md).
