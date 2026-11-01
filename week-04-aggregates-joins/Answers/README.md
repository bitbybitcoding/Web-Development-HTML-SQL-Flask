# Week 4 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenges 1 to 4, with real output | [challenge-answers.md](challenge-answers.md) |
| All challenge and extra-practice queries in one runnable file | [solutions.sql](solutions.sql) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) |

Check the whole file runs: `sqlite3 school.db < week-04-aggregates-joins/Answers/solutions.sql`

## Warm-up answers

- **A:** `= NULL` is never true. Use `WHERE email IS NULL`.
- **B:** text must be in single quotes: `class = '3A'`.
- **C:** `AND` binds tighter than `OR`. Add brackets: `WHERE (class = '3A' OR class = '3B') AND gender = 'F'`. (Without them, all of 3A is returned, boys included.)
- **D:** NULLs sort first, so the "lowest" three are the absent students. Add `WHERE score IS NOT NULL`.

## Common mistakes to watch for

- **Putting an aggregate in `WHERE`** (`WHERE AVG(score) > 66`). Use `HAVING`.
- **Selecting a column that is not grouped or aggregated.** SQLite will not complain, so check by eye.
- **Forgetting the `ON` clause** (or writing `ON` conditions that never match). Without a proper `ON`, you get every pairing of rows, so a 30-row table joined to a 120-row table gives 3,600 rows.
- **Using `COUNT(*)` after a `LEFT JOIN`**, which counts the unmatched row as 1. Count a column from the right-hand table instead.
- **Putting the filter for a `LEFT JOIN` in `WHERE` instead of `ON`:** `WHERE sc.role = 'Leader'` removes the unmatched rows again and turns the query back into an inner join. Mention this to fast finishers.
- **Tied averages:** when two students have the same rounded average, add a second `ORDER BY` column.
