# Week 4 Demo: Aggregates, grouping and joins

**Time:** 45 minutes. Students type along in `sqlite3 school.db`.
**Finished script:** [demo/demo.sql](demo/demo.sql)

---

## Part 1: Aggregate functions (10 min)

An **aggregate function** takes many rows and returns **one** value.

```sql
SELECT COUNT(*) FROM students;                       -- 30   number of rows
SELECT COUNT(email) FROM students;                   -- 25   number of non-NULL emails
SELECT COUNT(*) AS total, COUNT(email) AS with_email FROM students;
```

**`COUNT(*)` counts rows. `COUNT(column)` counts rows where that column is not NULL.** The difference is exactly the five students with no email.

```sql
SELECT MIN(score), MAX(score) FROM scores;
SELECT AVG(score) FROM scores;                       -- long decimal
SELECT ROUND(AVG(score), 1) AS average FROM scores;  -- tidy it up
SELECT SUM(score) FROM scores WHERE subject_id = 1;  -- total of all Maths scores
SELECT COUNT(DISTINCT class) FROM students;          -- 3
```

- Aggregates **ignore NULL**: absent students are not counted as zero. Show `COUNT(*)` versus `COUNT(score)` on `scores` (120 versus 116).
- `WHERE` is applied first, then the aggregate: `SELECT AVG(score) FROM scores WHERE subject_id = 1;` is the Maths average.

---

## Part 2: GROUP BY and HAVING (10 min)

"What is the average score **for each** subject?" The words *for each* tell you to use `GROUP BY`.

```sql
SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id;
```

```sql
SELECT class, COUNT(*) AS students
FROM students
GROUP BY class;
```

**Explain with a picture.** Draw the `students` rows being sorted into three piles (3A, 3B, 3C), and then one summary row produced per pile.

**The rule:** every column in `SELECT` must be either listed in `GROUP BY` or wrapped in an aggregate function. Show a wrong query (`SELECT name, class, COUNT(*) FROM students GROUP BY class;`) and ask: *which of the 10 names should it show for class 3A?* There is no sensible answer. (SQLite will run it and quietly pick one, which is a bug waiting to happen.)

### HAVING filters groups

```sql
SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id
HAVING AVG(score) > 66;
```

| | `WHERE` | `HAVING` |
|---|---|---|
| Filters | individual **rows** | whole **groups** |
| Runs | **before** grouping | **after** grouping |
| Can use aggregates? | no | yes |

The order SQL actually works in:

```
FROM  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  SELECT  ->  ORDER BY  ->  LIMIT
```

(While writing, though, we type `SELECT` first. Make students say this order out loud.)

---

## Part 3: Joins (20 min)

### Why join?

`scores` holds `student_id` and `subject_id`, which are just numbers. To see *names*, we must look them up in the other tables. A **join** matches rows from two tables using a condition.

```sql
SELECT * FROM scores LIMIT 3;
-- student_id  subject_id  score
-- 1           1           ...
```

### INNER JOIN

```sql
SELECT students.name, scores.subject_id, scores.score
FROM scores
INNER JOIN students ON scores.student_id = students.student_id;
```

- `ON` says how rows match: the foreign key equals the primary key.
- **Table aliases** make this shorter:

```sql
SELECT st.name, sc.subject_id, sc.score
FROM scores AS sc
JOIN students AS st ON sc.student_id = st.student_id;
```

(`JOIN` on its own means `INNER JOIN`.) When two tables have a column with the same name, you **must** prefix it (`st.student_id`).

### Joining three tables

Chain the joins. Follow the foreign keys on the schema diagram: `scores` links `students` and `subjects`.

```sql
SELECT st.name, su.name AS subject, sc.score
FROM scores AS sc
JOIN students AS st ON sc.student_id = st.student_id
JOIN subjects AS su ON sc.subject_id = su.subject_id
WHERE st.class = '3A'
ORDER BY st.name, su.name;
```

### Joins plus GROUP BY

```sql
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
ORDER BY average DESC;
```

### INNER versus LEFT JOIN

*"Which CCAs does each student belong to?"* An `INNER JOIN` returns only students who have a CCA. Eight students vanish. What if we need to **include students with no CCA**?

```sql
SELECT st.name, sc.cca_id
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id;
```

- A `LEFT JOIN` keeps **every row from the left table** (the one after `FROM`). Where there is no match, the right-hand columns are filled with **NULL**.
- Find the students with no CCA by testing for that NULL:

```sql
SELECT st.name
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;
```

- Count CCAs per student, **including zero**:

```sql
SELECT st.name, COUNT(sc.cca_id) AS ccas
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC;
```

Here `COUNT(sc.cca_id)` gives 0 for no CCA, while `COUNT(*)` would give 1, because the unmatched student still produces one row. (A nice recap of `COUNT(*)` versus `COUNT(column)`.)

### A first look at subqueries

A **subquery** is a `SELECT` inside another statement. Run the inner query first, then use its result:

```sql
SELECT AVG(score) FROM scores;                    -- about 67.4

SELECT student_id, subject_id, score
FROM scores
WHERE score > (SELECT AVG(score) FROM scores);    -- above the overall average
```

and with `IN`:

```sql
SELECT name FROM students
WHERE student_id IN (SELECT student_id FROM student_cca WHERE cca_id = 1);   -- Robotics members
```

Tell students that subqueries and `EXISTS` are the topic of today's extra practice.

---

## Check for understanding

1. What is the difference between `COUNT(*)` and `COUNT(score)`?
2. Why is `WHERE AVG(score) > 66` an error? *(`WHERE` runs before groups exist.)*
3. Which join keeps rows with no match: `INNER` or `LEFT`?
4. In a `LEFT JOIN`, how do you find the rows that did **not** match? *(`WHERE right_table.key IS NULL`)*
