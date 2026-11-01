# Week 10 Extra Practice

For the homework between Week 10 and Week 11 (after the mini-assessment), spend about **two hours on your capstone**: finish the CRUD for your main table, add the search and the report. The sections below are extra: revision for your final exam-style written questions, and Git practice.

---

## 1. Peer review of a plan

Swap `PLAN.md` files with a partner (or ask someone by message). Check each item and write one improvement:

- [ ] Is it clear who the users are and what problem it solves?
- [ ] Are the user stories in the right format and testable ("I can see...", "I can add...")?
- [ ] Does the MVP fit in about 6 to 8 hours of work?
- [ ] Do the tables have primary keys? Is every foreign key written down? Any repeated data that should be in its own table?
- [ ] Does every user story map to at least one route?
- [ ] Is there at least one report that needs `GROUP BY` or a join?
- [ ] What is the biggest risk?

## 2. Git practice

1. Create a branch called `practice`, change the title in `base.html`, and commit it with a message.
2. Switch back to `main` and change the same line to something else. Commit.
3. Merge `practice` into `main`. You will get a **merge conflict**. Open the file, look for the `<<<<<<<`, `=======` and `>>>>>>>` markers, decide what the line should say, delete the markers, `git add` and `git commit`. (This is the most common problem when two people edit the same file. Practise now.)
4. Run `git log --oneline --graph`. Describe what you see.

## 3. A stretch feature

Choose one: pagination of your list page; a second report with `GROUP BY` and `HAVING`; sorting by clicking a column heading (safely: see Week 9); a status field (for example `pending`, `done`) with a button that changes it.

## 4. Written questions (exam style)

These cover the whole course. Try them in 40 minutes without notes, then mark them with [the mark scheme](Answers/extra-practice-answers.md). **Total: 40 marks.**

**Q1: HTML** [4]
(a) State the purpose of the `for` attribute of a `<label>` and the `name` attribute of an `<input>`. [2]
(b) Give **two** reasons for using semantic elements such as `<nav>` and `<main>` instead of `<div>`. [2]

**Q2: SQL queries** [6]
The tables `students(student_id, name, class)` and `scores(student_id, subject_id, score)` are used.
(a) Write a query that shows the names of students whose **average** score is above 70, highest average first. [4]
(b) Explain why `SELECT COUNT(*), COUNT(email) FROM students` can return two different numbers, and why `WHERE email = NULL` finds no rows. [2]

**Q3: Database design** [8]
A tuition centre keeps this table, with one row for each lesson taken:

`LESSON(lesson_id, student_name, student_phone, tutor_name, tutor_phone, subject, lesson_date, fee)`

Every tutor teaches one subject. A student can take lessons with many tutors.
(a) Describe **two** problems (anomalies) caused by this design, with an example for each. [2]
(b) Draw an ER diagram for a better design. [3]
(c) Give the tables in 3NF, marking primary keys and foreign keys. [3]

**Q4: Flask** [6]
(a) Describe the purpose of `render_template`, `redirect` and `url_for`. [3]
(b) A user submits a form and the server saves the data. Describe what the Post/Redirect/Get pattern does and what problem it avoids. [3]

**Q5: Security** [6]
```python
@app.route("/search")
def search():
    name = request.args.get("name")
    rows = get_db().execute(f"SELECT * FROM students WHERE name = '{name}'").fetchall()
    return "<h1>Results for " + name + "</h1>" + str(rows)
```
(a) Identify **two** security weaknesses in this code and explain how each could be exploited. [4]
(b) Rewrite the code to remove both weaknesses. [2]

**Q6: Transactions and constraints** [4]
(a) Explain the purpose of `with db:` when a route inserts a row into `loan` and updates a row in `kit`. [2]
(b) Give **two** constraints that would stop a loan being saved for a quantity of zero or for a kit that does not exist. [2]

**Q7: Testing** [3]
Describe **three** different tests for a route that creates a booking. State what each tests and what result you expect. [3]

**Q8: Evaluation** [3]
A classmate stores `available_qty` as a column of the `kit` table and updates it by hand when a kit is lent or returned. Evaluate this design and suggest an alternative. [3]
