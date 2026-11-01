# Week 9 Answers

| Task | Answer |
|------|--------|
| Challenges 1 to 3 (CCAs: read, create, update/delete) | [challenges-1-3-school/](challenges-1-3-school/): the demo app plus the new routes, each marked `CHALLENGE 1/2/3` in `app.py` |
| Challenge 4: Library web app | [challenge-4-library/](challenge-4-library/): one possible solution. Mark against the "must have" list, not this design |
| Extra practice code | [extra_practice.py](extra_practice.py) (sorting whitelist, pagination, unique index) |
| Extra practice written | [extra-practice-answers.md](extra-practice-answers.md) |
| Self-check | [tests_week9.py](tests_week9.py): `python3 week-09-flask-sqlite-crud/Answers/tests_week9.py` |

The tests run every route against a **temporary copy** of the database, including attacks sent directly to the server (SQL injection text, invalid ids and roles, `GET` on delete routes).

## Answers to questions in the challenges

- **Challenge 1:** a plain `JOIN` drops CCAs with no members (Chess Club has 0 rows in `student_cca`), so the page would not show it. `LEFT JOIN` keeps every CCA; `COUNT(sc.student_id)` counts only real matches, so Chess Club shows `0`. `COUNT(*)` would wrongly give 1.
- **Challenge 2:** `student_id = "1 OR 1=1"` fails `isdigit()` so it is refused; and even if it were passed to the database, the `?` placeholder would treat it as one value, not as SQL.
- **Challenge 3, "why not delete the members and the CCA together?"** Any sensible answer is acceptable. Reasonable points: deleting members silently erases the history of who took part; a mistaken click on "Delete CCA" could remove 40 records; but when a CCA is closed, a cascade is exactly what the school wants. A good compromise is the "refuse while it has members, then remove them one by one" workflow of the solution, or asking the user to confirm, or archiving instead of deleting.

## Common mistakes

- Forgetting `with db:` / `db.commit()`: the page looks right but the data is not saved after a restart.
- `PRAGMA foreign_keys = ON` only in one place. It must run on **every** new connection (it lives in `get_db()`).
- Building SQL with f-strings "just this once".
- `("Mei")` instead of `("Mei",)`: a string, not a one-item tuple. Raises `Incorrect number of bindings supplied`.
- Returning `row` objects after the connection is closed (rare with `g`), or using `fetchone()[0]` when there is no row (`TypeError: 'NoneType' object is not subscriptable`). Check for `None`.
- Passing a `Row` to `jsonify` (not serialisable). Convert with `dict(row)`.
- Putting data-changing routes on GET.
- Redirecting before the `with db:` block has finished, or catching `IntegrityError` outside the `with` block: the rollback happens when the exception leaves the block, so the `try` must surround it.
- In templates: `s.class` (use `s['class']`); comparing a number to the string from `request.args` without converting.
- Dates: SQLite stores dates as text (`YYYY-MM-DD`), which sorts correctly. Use `date('now')` in SQL or `date.today().isoformat()` in Python, never a different format.
