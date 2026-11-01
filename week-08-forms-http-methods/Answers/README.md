# Week 8 Answers

| Task | Answer |
|------|--------|
| Challenge 1: Student finder (GET) | [challenge-1/](challenge-1/) |
| Challenge 2: CCA sign-up (POST) | [challenge-2/](challenge-2/): the `validate()` function returns a dictionary of errors |
| Challenge 3: To-do list | [challenge-3/](challenge-3/) |
| Challenge 4: Quiz | [challenge-4/](challenge-4/): one possible solution; mark against the "must have" list |
| Extra practice code | [extra_practice.py](extra_practice.py) (JSON file, password form, mystery route, pizza order) |
| Extra practice written | [extra-practice-answers.md](extra-practice-answers.md) |
| Self-check | [tests_week8.py](tests_week8.py): `python3 week-08-forms-http-methods/Answers/tests_week8.py` |

The tests send bad data **directly** to the server (bypassing the HTML form), exactly as an attacker would.

## Answers to questions in the challenges

- **Challenge 3:** typing `/delete/1` in the address bar sends a GET, and the server replies **405 Method Not Allowed**. This is good: a link, a web crawler or a browser pre-loader can never delete data by accident.
- **Challenge 2, "test like an attacker":** `requests.post("http://localhost:5000/signup", data={"cca": "Hacking Club"})` receives the form back with errors, because `validate()` checks `cca` against the list. If a student's solution only trusted the radio buttons, the invented CCA would be saved.

## Common mistakes

- `name` missing on an input: the field is not sent at all (the `id` is not enough).
- `request.form["x"]` on a missing field: **400 Bad Request**. Use `.get("x", "")`.
- Forgetting `methods=["GET", "POST"]`: the form submits to a **405 Method Not Allowed** page.
- Forgetting `app.secret_key`: `RuntimeError: The session is unavailable because no secret key was set` when using `flash`.
- `return render_template(...)` after a successful POST instead of `redirect`: refreshing saves twice.
- Comparing a number with a string: `request.form["rating"]` is always a **string**, so `form.rating == n` is false in Jinja; use `n|string`.
- Checkbox not ticked: the browser sends **nothing** for it (not `"no"`), so `request.form.get("agree")` is `None`.
- Putting `action="/signup"` by hand, then moving the route. Use `url_for`.
- Using `{{ form.class }}`. Use `form['class']`.
- Redirecting without `return` (`redirect(...)` on its own line does nothing).
