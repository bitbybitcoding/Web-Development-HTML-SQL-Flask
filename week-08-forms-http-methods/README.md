# Week 8: Forms and HTTP methods

**Block 3: Flask** · 3 hours · Platform: GitHub Codespaces

## By the end of this session students can

- Build HTML forms in a Flask app and read the data with `request.args` (GET) and `request.form` (POST).
- Explain GET vs POST and choose the right one: GET to *look*, POST to *change*.
- Handle two methods in one route with `methods=["GET", "POST"]` and `request.method`.
- Validate input **on the server**, show error messages and keep what the user typed.
- Use the **Post/Redirect/Get** pattern and `flash()` messages.
- Explain why user input is never trusted, and why Jinja's auto-escaping matters.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · data files in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): quiz feedback and a Flask recap

1. Hand back the SQL checkpoint quiz with section totals (see [the mark scheme](../week-06-ddl-dml-python-sqlite/Answers/checkpoint-quiz-answers.md)). Spend five minutes on the question most students lost marks on.
2. Recap on paper: *Write a Flask route `/greet/<name>` that renders `greet.html` with the name. Write the template line that shows the name in capitals.*
3. Ask: *In Week 2, which form attribute decided between `?name=Mei` in the URL and a hidden body? What was the difference?* Collect answers; today's demo makes this concrete.

## Instructor notes

- **GET vs POST in plain words.** GET asks the server for a page and can be bookmarked, shared and repeated safely. POST sends data to *do* something (save, delete, log in) and must not be repeated casually. A **link click is always a GET**: this is why a "Delete" link is dangerous, and why deleting uses a POST form with a button.
- **POST is not secret.** Data in the body does not appear in the address bar, but it is not encrypted. HTTPS does that. Do not let students think POST means secure.
- **`novalidate`.** The demo form uses `novalidate` so students can see *server* validation working. Browser `required` and `type="email"` are conveniences; anyone can bypass them with a script, so server checks are the real rule. The tests in [Answers/tests_week8.py](Answers/tests_week8.py) do exactly that.
- **Post/Redirect/Get.** Demo the problem first: submit without a redirect, press refresh, and the browser asks to resubmit (and the entry is saved twice). Then add `redirect`.
- **`secret_key`.** Needed for `flash()` and `session`, which are signed cookies. The value in the demo is for learning only; Week 11 covers keeping secrets out of the repository.
- **Data is in memory.** Everything restarts empty when the server reloads (with `--debug` every save reloads!). This is deliberate: it is the motivation for Week 9.
- **CSRF.** Mention it by name only: a real site must stop other sites from submitting its forms (CSRF tokens). Extensions such as Flask-WTF do it; the extra practice asks for a written explanation.
- **iPad.** Inputs use `font-size: 1rem` (16px) or larger so Safari does not zoom in when a field is focused; buttons are at least 44px tall.
