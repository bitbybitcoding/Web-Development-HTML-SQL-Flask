# Week 7 Extra Practice: Answers

## 1. Debug this app

| # | Bug | Error seen | Fix |
|---|-----|-----------|-----|
| 1 | Missing colon after `def index()` | `SyntaxError: expected ':'` | `def index():` |
| 2 | Two functions both named `index` | `AssertionError: View function mapping is overwriting an existing endpoint function: index` | Rename the second to `index_again` |
| 3 | `STUDENTS[id]`: `id` is a **string** (`<id>` has no converter), and a list needs an integer | `TypeError: list indices must be integers or slices, not str` | Use `<int:student_id>` and `STUDENTS[student_id - 1]`, or search by a key; check the range and `abort(404)` |
| 4 | `count()` calls `render_template` but does not `return` it | `TypeError: The view function ... did not return a valid response` | `return render_template(...)` |
| 5 | The folder is named `template` | `jinja2.exceptions.TemplateNotFound: index.html` | Rename it to `templates` |
| 6 | `{% for %}` loop: `<li>` is not closed | No error, but sloppy HTML; also the `s.class` access can confuse Jinja | `<li>...</li>` and `{{ s['class'] }}` |

(Also: `student.html` is never created in the question, so `/student/1` would raise `TemplateNotFound` until it is.)

## 2. Jinja filters and macros

1. `{{ ["mei", "arjun", "zoe"] | map("upper") | join(", ") }}` gives `MEI, ARJUN, ZOE`. If the list is passed from Python as `names`: `{{ names | map("upper") | join(", ") }}`. Simpler, and also accepted: `{{ names | join(", ") | upper }}`.
2. `Score: {{ score | default("n/a", true) }}` shows `n/a` for `None` (the second argument `true` makes `default` also replace falsy values such as `None`). For `78.456`: `Score: {{ score | round(1) }}` gives `78.5`. Combined: `{{ "n/a" if score is none else score | round(1) }}`.
3. ```html
   {% macro card(title, text) %}
   <div class="card"><h3>{{ title }}</h3><p>{{ text }}</p></div>
   {% endmacro %}

   {{ card("Robotics", "Tuesdays") }}
   {{ card("Chess", "Wednesdays") }}
   {{ card("Choir", "Fridays") }}
   ```
   To reuse it in many pages, put the macro in `macros.html` and use `{% from "macros.html" import card %}`.

## 3. A tiny JSON API

```python
from flask import jsonify

@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

@app.route("/api/students/<int:student_id>")
def api_student(student_id):
    for s in STUDENTS:
        if s["id"] == student_id:
            return jsonify(s)
    return jsonify({"error": "not found"}), 404
```

A phone app (or any other program) wants **data**, not layout. JSON is easy to parse, small, and does not change when the page design changes.

## 4. Your own site

Mark against: base template; static stylesheet; list page and detail page both generated from the list of dictionaries (not typed out per item); `url_for` used; no crash on bad URLs.

## 5. Written questions

1. A route connects a **URL pattern** to a **Python function** (a view) that runs when the URL is requested and returns the response. [1]
2. Any two: separates the layout (HTML) from the logic (Python), so they can be changed independently; the same template can be reused with different data; templates escape user input automatically, preventing injection; HTML in Python strings is hard to read and maintain. [2]
3. [3] (1) The browser sends a GET request for `/students/3`. (2) Flask matches the URL to a route and converts `3` to an integer, calling the function with `student_id = 3`. (3) The function gets the data and calls `render_template`, which fills the Jinja template with it, producing HTML. (4) Flask sends the HTML back as the response, with status 200, and the browser displays it. (Award the marks for a correct sequence in the right order; 1 mark each for request/match, function/template, response/display.)
4. A GET request **asks for** a page and does not change anything on the server; data is sent in the URL (query string). POST (and others) send data in the body of the request and are used for actions that change something. A link click only asks to see another page, so it is a GET. [2]
5. Because HTML treats `<` as the start of a tag, a user could enter text such as `<script>...</script>` that the browser would run. Converting it to `&lt;` makes the browser display it as plain text. This prevents **cross-site scripting (XSS)**. [2]
6. `id` is a **string**, so `id + 1` raises `TypeError: can only concatenate str (not "int") to str`, and the user sees a 500 Internal Server Error. Prevent it with the `int` converter (`<int:id>`), which makes Flask return a 404 for `/user/abc`. [2]
