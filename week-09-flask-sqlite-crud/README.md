# Week 9: Flask and SQLite: CRUD

**Block 3: Flask** · 3 hours · Platform: GitHub Codespaces · This is where the three blocks come together

## By the end of this session students can

- Connect a Flask app to SQLite with one connection per request (`get_db()`, `flask.g`, `teardown_appcontext`).
- Read data with parameterised queries and `sqlite3.Row`, and show it in templates.
- Implement all four CRUD operations: **C**reate (`INSERT`), **R**ead (`SELECT`), **U**pdate (`UPDATE`) and **D**elete (`DELETE`), each as a route.
- Match each operation to its HTTP method and SQL statement.
- Keep data safe: `?` placeholders everywhere, validation before the database, `with db:` transactions, foreign keys switched on.
- Delete in the right order when tables are related, and explain what happens if they do not.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · seed in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): the CRUD table

Draw this table on the board and ask the students to fill in the last two columns from what they know (they have used all of these separately):

| Operation | Example | SQL | HTTP method |
|-----------|---------|-----|-------------|
| Create | add a student | `INSERT` | `POST` |
| Read | list / search students | `SELECT` | `GET` |
| Update | change an email | `UPDATE` | `POST` (HTML forms only have GET and POST) |
| Delete | remove a student | `DELETE` | `POST` |

Then ask: *Last week the feedback list vanished when the server restarted. Where should the data live? What would we have to be careful about?* (Safe queries, order of deletes, one connection per request.)

## Instructor notes

- **This week is the payoff.** Students have seen every piece. Keep the demo moving: they should *recognise* each SQL statement and feel the pieces click.
- **Work on a copy.** The demo copies `school.db` into `instance/school.db` the first time it runs (see `db.py`). Students can break their copy freely. To start again, stop the server and delete the `instance/` folder. The `instance/` folder is ignored by Git.
- **The two classic bugs:** forgetting `db.commit()` (or `with db:`), so nothing is saved, and forgetting `PRAGMA foreign_keys = ON`, so the delete "works" but leaves orphan rows. The demo's `get_db()` switches it on for **every** connection, which is the lesson.
- **Challenges 1 to 3 build on one app.** Students extend the demo app (the same folder), adding CCA routes. [Answers/challenges-1-3-school/](Answers/challenges-1-3-school/) is the finished version. Challenge 4 is a new, open-ended project.
- **Pacing.** Fast students will finish Challenges 1 to 3 and start Challenge 4. Weaker students should aim to complete Challenge 1 and 2 with understanding, then do 3 (update/delete) with a partner. Challenge 4 is the best preparation for the capstone.
- **Looking at the database.** The SQLite Viewer extension (installed in the dev container) opens `instance/school.db` by clicking it in the Explorer. It is useful for seeing what the app really did. The `sqlite3` command-line shell works too: `sqlite3 instance/school.db`.
- **Weeks 10 and 11 start now.** Remind students that Week 10 is the capstone's planning-and-build week, and the Week 10 mini-assessment will ask them to build a small CRUD feature. Today's challenges are the template.
- **Reminder:** stop and delete old codespaces.
