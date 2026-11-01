# Week 3: The relational model and SELECT

**Block 2: SQL** · 3 hours · Platform: GitHub Codespaces · Database: `school.db` in the repository root

## By the end of this session students can

- Describe a relational database using the terms table, row, column, primary key and foreign key.
- Open a SQLite database from the command line and inspect its tables and schema.
- Write `SELECT` queries with `WHERE`, `AND`/`OR`/`NOT`, `ORDER BY`, `LIKE`, `IN`, `BETWEEN`, `DISTINCT` and `LIMIT`.
- Explain how `NULL` behaves and avoid the common traps around it.
- Predict the output of a query by hand.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · script in [demo/demo.sql](demo/demo.sql) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · data in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Before the session

From the repository root, check that the database opens:

```bash
sqlite3 school.db "SELECT COUNT(*) FROM students;"     # should print 30
```

If `school.db` is missing, rebuild it with `python3 tools/make_school_db.py`.

## Warm-up (15 min): HTML recap quiz

Last week was forms and CSS. Five quick questions, answered on mini whiteboards or in the chat:

1. Which attribute decides the name under which a form field's value is sent to the server?
2. Radio buttons in one group share what?
3. What is the difference between `method="get"` and `method="post"`? Give one visible difference.
4. Which CSS selector is more specific: `#menu` or `.menu`?
5. Name the four layers of the box model from the inside out.

Then bridge to today: *"Every website you use stores data somewhere, and that 'somewhere' is almost always a database. Today we learn to ask a database questions."*

## Instructor notes

- **Use the terminal.** Students run the `sqlite3` command-line shell, not a GUI. The dev container's `~/.sqliterc` already turns on column headers, column mode and `NULL` display. If a student's output looks messy, run `.headers on` and `.mode column` by hand.
- **Strings use single quotes.** `'3A'` is a string; `"3A"` is an identifier in standard SQL (SQLite is forgiving, which hides mistakes). Insist on single quotes.
- **Keywords are not case sensitive, but write them in capitals** and put each clause on its own line, so the quality of the reading habit carries into the exam.
- **Pacing:** the NULL section is the part students remember least. Leave 10 minutes for it and do the `= NULL` trap live.
- **Challenge 3 is paper first.** Students must write a prediction *before* running the query. The learning is in the gap between prediction and result.
