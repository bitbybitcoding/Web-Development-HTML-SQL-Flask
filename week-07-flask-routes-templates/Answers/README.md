# Week 7 Answers

| Task | Answer |
|------|--------|
| Challenge 1: Hello, Flask | [challenge-1/app.py](challenge-1/app.py) |
| Challenge 2: Routes with variables | [challenge-2/app.py](challenge-2/app.py) |
| Challenge 3: Class results | [challenge-3/](challenge-3/) (`app.py`, `templates/`, `static/`) |
| Challenge 4: CCA showcase | [challenge-4/](challenge-4/): one possible solution. Mark against the "must have" list, not against this design |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) |
| Self-check | [tests_week7.py](tests_week7.py): `python3 week-07-flask-routes-templates/Answers/tests_week7.py` |

## Challenge 2 questions

1. `/add/2/x` → **404 Not Found**. With `<int:a>` the converter only matches digits, so no route matches. With plain `<a>` the value would be the string `"x"` and `a + b` would crash with a `TypeError` (a 500 error), or silently join strings (`"2" + "3"` = `"23"`).
2. `/area/2` → **404** and `/area/2.0` works. Flask's `float` converter requires a decimal point. If both are needed, add two route decorators on the same function.

## Common mistakes

- Running `flask run` in the wrong folder ("Could not import 'app'").
- Folder named `template` or `Templates`: `TemplateNotFound`.
- Forgetting `return` (the page shows an error: the view returned `None`).
- Using `{{ }}` where `{% %}` is needed, or the other way around, or forgetting `{% endfor %}` / `{% endif %}`.
- Writing `, 404` on the error handler: without it, the page says "not found" but the status is 200.
- Typing `href="/students/3"` instead of `url_for`; fine at first, painful when routes change.
- Two functions with the same name: `AssertionError: View function mapping is overwriting an existing endpoint function`.
- Forgetting that `s.class` works in Jinja but is fragile: prefer `s['class']`.
