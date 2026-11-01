# Week 8 Extra Practice

For fast finishers, and homework for everyone else. Next week your data finally moves into SQLite.

---

## 1. Persist to a file

Your to-do list from Challenge 3 loses its data at every restart. Make it survive using a JSON file:

```python
import json
from pathlib import Path

FILE = Path("tasks.json")

def load_tasks():
    return json.loads(FILE.read_text()) if FILE.exists() else []

def save_tasks(tasks):
    FILE.write_text(json.dumps(tasks, indent=2))
```

Call `save_tasks` after every change. List **two problems** with using a file instead of a database once many users use the site at once. (Hint: two people save at the same moment; searching a big list.)

## 2. A password-change form

Build `/password` with fields `old`, `new` and `confirm`. Rules: the old password must equal a hard-coded one; `new` must be at least 8 characters, contain a digit and a letter, differ from the old one, and equal `confirm`. Show **all** errors at once, never reveal the old password, and do **not** put the passwords back into the form after an error (why not?).

## 3. Method experiments

Write a route `/mystery` that accepts GET and POST, and returns `request.method`, `request.args`, `request.form` and `request.headers["User-Agent"]`. Using the Python `requests` library in a second terminal (or `curl`), send: a GET with `?a=1`, a POST with form data, and a POST with the same field in both the URL and the body. Which one wins in `request.values`?

## 4. Dynamic form from data

Build a "pizza order" page where the list of toppings is a Python list and the form shows one checkbox per topping (all with `name="topping"`). Use `request.form.getlist("topping")` and show the order total (each topping has a price in a dict). Reject orders with more than four toppings.

## 5. Written questions (exam style)

1. State **two** differences between the GET and POST methods. [2]
2. A form contains `<input type="text" name="user">`. State where the Flask code finds the value when the form uses (a) `method="get"` and (b) `method="post"`. [2]
3. Explain why validation must be done on the server even when the HTML form already has validation attributes such as `required` and `maxlength`. [2]
4. Describe the **Post/Redirect/Get** pattern and the problem it prevents. [3]
5. A website has a link `<a href="/delete/5">Delete</a>` that deletes record 5. Explain **two** problems with this design, and describe a better one. [3]
6. Explain what **CSRF** (cross-site request forgery) is and describe one way to defend against it. [3]
7. Explain why the form values should be shown again, using `value="{{ form.name }}"`, and why this is safe in Flask but would not be safe if the HTML were built with Python string concatenation. [2]
