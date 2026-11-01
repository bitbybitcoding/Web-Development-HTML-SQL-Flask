# Week 3 Extra Practice

For fast finishers, and homework for everyone else. Use `school.db` unless told otherwise.

---

## 1. The NULL traps

Predict the result of each query **before** running it, then run it and explain any surprise.

```sql
-- a
SELECT name FROM students WHERE email = NULL;

-- b
SELECT name FROM students WHERE email <> 's1001@student.school.edu.sg';

-- c
SELECT COUNT(*) FROM students WHERE email IS NULL OR email IS NOT NULL;

-- d
SELECT student_id, subject_id, score FROM scores ORDER BY score LIMIT 3;

-- e
SELECT name FROM students WHERE student_id NOT IN (1, 2, NULL);

-- f
SELECT name, IFNULL(email, 'no email on record') AS email FROM students LIMIT 6;
```

Then answer:

1. Rewrite (a) so that it returns what the author probably wanted.
2. In (b), how many students are *missing* from the result because their email is NULL?
3. Rewrite (d) to return the three lowest scores of students who sat the exam.
4. What does `IFNULL(x, y)` do?

## 2. Practise online

Do these free interactive tutorials. Make a note of anything you could not solve.

- **SQLBolt** (`https://sqlbolt.com`): lessons 1 to 5 (SELECT basics, constraints, filtering and sorting, and the review).
- **SQLZoo** (`https://sqlzoo.net`): the "SELECT basics" and "SELECT from WORLD" tutorials.

## 3. More queries on school.db

1. List the names of students whose email starts with `s100` (hint: `LIKE`).
2. List the names of students who are **not** in class 3A and were born before 1 July 2009 (or write "none" if there are none).
3. Show the name and teacher of the subjects, sorted by teacher name in reverse alphabetical order.
4. Show the `student_id` and `score` of Computing results (`subject_id = 2`) between 60 and 79, best first.
5. Show the names of students whose name has **exactly 11 characters** (hint: `_` wildcards, or `LENGTH(name)`).

## 4. Exam-style written questions

1. Define the terms **primary key** and **foreign key**.
2. The `scores` table has the primary key `(student_id, subject_id)`. State the name of this type of key and explain why a single column would not be enough.
3. A student writes `SELECT name FROM students WHERE class = 3A;`. State what is wrong and write the corrected statement.
4. State the difference between `WHERE` and `ORDER BY`.
5. The result of `SELECT name FROM students WHERE class = '3A' OR class = '3B' AND gender = 'F';` contains boys. Explain why, and rewrite the query so that it only returns girls from 3A or 3B.
