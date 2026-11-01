# Week 6: DDL, DML and Python with SQLite

**Block 2: SQL** · 3 hours · Platform: GitHub Codespaces · Ends the SQL block with a checkpoint quiz in Week 7

## By the end of this session students can

- Create tables with `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK` and `DEFAULT` constraints.
- Change a table with `ALTER`, remove one with `DROP`, and explain what `DROP` does to the data.
- Add, change and remove rows with `INSERT`, `UPDATE` and `DELETE`, and explain why `WHERE` matters.
- Enable foreign-key checking in SQLite and show a constraint rejecting bad data.
- Use Python's `sqlite3` module: connect, cursor, execute, fetch, commit.
- Write parameterised queries with `?`, and explain how SQL injection works and how placeholders stop it.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · starter files in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

**Checkpoint:** a short SQL quiz in the first 20 minutes of Week 7, worth 15% of the course. The paper is in [checkpoint-quiz.md](checkpoint-quiz.md) (answers and mark scheme in [Answers/checkpoint-quiz-answers.md](Answers/checkpoint-quiz-answers.md)). **Remind students at the end of this session**, and tell them it covers queries, joins, normalisation and injection.

## Warm-up (15 min): normalisation, in a quick-fire round

Show this table. It is the Week 5 uniform order form, but students must decide what is wrong with each version.

```
A:  ORDER(order_no, item_code, item_name, unit_price, qty)          key (order_no, item_code)
B:  STUDENT(student_id, name, class, class_teacher)                 key student_id
C:  ORDER(order_no, order_date, items)                              items = "U1 x2, U2 x1"
```

For each, students answer: *Which normal form does it break, and why?*

Then bridge: *"Last week we designed tables on paper. Today we create them for real, put data in, and talk to them from Python."*

## Instructor notes

- **`PRAGMA foreign_keys = ON`.** SQLite ignores foreign keys by default (for historical reasons). Make sure students see a foreign key **not** being enforced first, then turn it on. It must be run on every new connection, which is why the Python helper in the challenges does it each time.
- **Python version note.** If a student's code runs several statements in one `execute()`, Python 3.12 and later raise `ProgrammingError`; older versions raised `Warning`. The dev container uses 3.12.
- **The injection demo lands best when students attack first.** Let pairs try to log in as `admin` without the password for two minutes before you show the answer.
- **Pacing:** Challenge 2 (library app) is the main event and takes most of the 80 minutes. Challenge 1 should take about 20 minutes, Challenge 3 about 15, and Challenge 4 is for those who finish.
- **Common misconceptions:** forgetting `commit()` (changes vanish when the program exits); string-building SQL because "it is easier to read"; thinking `DROP TABLE` can be undone; believing `NOT NULL` and "empty string" are the same thing.
