# Week 7: Your first Flask app: routes and templates

**Block 3: Flask** · 3 hours · Platform: GitHub Codespaces

## By the end of this session students can

- Create a Flask app, run it in Codespaces and view it through the forwarded port.
- Write routes, including routes with variables and converters (`<name>`, `<int:id>`).
- Explain the request-response cycle: browser asks, Python function answers.
- Use `render_template` to send data to a Jinja template, with `{{ }}`, `{% if %}` and `{% for %}`.
- Share a layout with `{% extends %}` and `{% block %}`, and link CSS from `static/`.
- Build links with `url_for`, return a 404 with `abort(404)`, and write a custom 404 page.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:20 | **SQL checkpoint quiz** (15% of the course) | [Week 6 quiz](../week-06-ddl-dml-python-sqlite/checkpoint-quiz.md) |
| 0:20–0:30 | Warm-up (below) | this page |
| 0:30–1:00 | Demo, live-coded (shortened today: see note) | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · starters in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (10 min): from Python to the web

After the quiz, ask the room:

1. *When you type a web address and press Enter, what happens?* Draw the answer on the board: **browser → request → server → response → browser**.
2. *In Week 2 a form sent `?name=Mei` to `/submit`. Who received it?* (Our little `echo_server.py`.) *Today we replace that server with Flask: a Python function runs for each URL.*

## Instructor notes

- **The demo is 30 minutes today** (quiz first). Cover Parts 0–2 live. Part 3 (inheritance, static files, `url_for`) can be shown quickly from the finished demo, and students discover the benefit in Challenge 3.
- **Quiz logistics.** Print [checkpoint-quiz.md](../week-06-ddl-dml-python-sqlite/checkpoint-quiz.md) or share it on screen; mark with [the mark scheme](../week-06-ddl-dml-python-sqlite/Answers/checkpoint-quiz-answers.md). Section totals help you decide what to revisit.
- **Run command.** The reliable one is `flask --app app run --debug` from inside the folder that holds `app.py`. The common mistake is running it from the repository root ("Could not import app").
- **iPad.** The pop-up "Open in Browser" disappears quickly. Show everyone the **Ports** tab. To stop the server, use Ctrl+C; if the terminal is hard to reach, open a second terminal with the **+** button.
- **Ports sometimes stay busy** after a crash. `Address already in use`: close the old terminal, or run `pkill -f flask`.
- **A folder named `templates`** (exactly) must sit next to `app.py`. The most common errors this week are `TemplateNotFound` (wrong folder name or place) and an indentation error in a route function.
- **Reminder:** stop and delete old codespaces (GitHub → Codespaces) to keep within the free allowance.
- **Wrap-up answers** (end of [demo.md](demo.md)): (1) `{{ }}` prints a value; `{% %}` runs a statement. (2) Flask's default `template_folder` is `templates`, and it is a convention that saves configuration. (3) The child pages would have no place to put their content: blocks in the base are the "holes" the children fill. (4) If the route changes, every `url_for` link updates by itself, and it fills in variables correctly.
