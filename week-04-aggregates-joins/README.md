# Week 4: Aggregates, grouping and joins

**Block 2: SQL** · 3 hours · Platform: GitHub Codespaces · Database: `school.db` in the repository root

## By the end of this session students can

- Summarise data with `COUNT`, `SUM`, `AVG`, `MIN` and `MAX`.
- Group rows with `GROUP BY` and filter the groups with `HAVING`.
- Explain the difference between `WHERE` and `HAVING`, and between `COUNT(*)` and `COUNT(column)`.
- Combine tables with `INNER JOIN` and `LEFT JOIN`, using table aliases.
- Join three tables in one query.
- Write a simple subquery (introduced here, practised in the extra practice).

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · script in [demo/demo.sql](demo/demo.sql) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) · data in [challenges/sales.sql](challenges/sales.sql) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): spot the bug

Each query below has one mistake from Week 3. Students find it and say what it should be.

```sql
-- A: should return students with no email
SELECT name FROM students WHERE email = NULL;

-- B: should return students in class 3A
SELECT name FROM students WHERE class = 3A;

-- C: should return the girls from 3A or 3B
SELECT name FROM students WHERE class = '3A' OR class = '3B' AND gender = 'F';

-- D: should show the 3 lowest scores that were actually sat
SELECT * FROM scores ORDER BY score LIMIT 3;
```

## Instructor notes

- **Introduce aggregates and joins separately, then combine them.** Students who see a join first get lost in the extra rows. Spend the first 20 minutes on single-table aggregates.
- **Draw the join.** Put two or three rows of `students` and `student_cca` on the board with arrows between matching ids. Then cross out rows to show what `INNER` loses and `LEFT` keeps.
- **`GROUP BY` rule of thumb:** every column in `SELECT` must either be in `GROUP BY` or be inside an aggregate function. SQLite lets you break this rule silently (and gives an arbitrary value), so students must learn the rule from you, because H2 exams assume it.
- **`HAVING` versus `WHERE`:** `WHERE` filters rows **before** grouping; `HAVING` filters groups **after**. The extra practice includes a hand trace that makes the order concrete.
- **Pacing:** Challenge 3 (three-table join) is the hardest. Let students draw the join path in the schema diagram before they write any SQL.
