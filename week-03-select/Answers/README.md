# Week 3 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenges 1 to 4, with real output | [challenge-answers.md](challenge-answers.md) |
| All challenge queries in one runnable file | [solutions.sql](solutions.sql) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) |

Check the whole file runs: `sqlite3 school.db < week-03-select/Answers/solutions.sql`

## Warm-up answers

1. `name`.
2. The same `name` (that is what makes them mutually exclusive; each radio has a different `value`).
3. GET puts the data in the URL (visible, bookmarkable); POST puts it in the request body (not visible in the URL).
4. `#menu` (an id selector beats a class selector).
5. Content, padding, border, margin.

## Common mistakes to watch for

- **Double quotes around text:** `WHERE class = "3A"` often works in SQLite by accident, but it is wrong. Use single quotes.
- **`= NULL`:** the most common error of the week. Use `IS NULL`.
- **Mixing `AND` and `OR` without brackets** (see Extra practice, written question 5).
- **`ORDER BY` before `WHERE`:** the clause order is fixed: `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`.
- **Forgetting the semicolon** and staring at the `...>` prompt. Type `;` and press Enter.
- **Challenge 1, Q9:** forgetting that NULLs sort first.
