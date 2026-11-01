# Week 4 Extra Practice

For fast finishers, and homework for everyone else. Use `school.db` unless told otherwise.

---

## 1. Subqueries (`IN`, `EXISTS`)

Write each query **twice** where asked.

1. Show the names of students who scored **above the overall average** in at least one subject. (Use a subquery with `IN`, and a scalar subquery `(SELECT AVG(score) FROM scores)`.)
2. Show the names of students who belong to **no CCA**:
   - (a) using `NOT IN (SELECT ...)`,
   - (b) using `NOT EXISTS (SELECT ...)`.
3. Show the names of CCAs that have **at least one member**, using `EXISTS`.
4. Show the name and score of every student who got the **highest Mathematics score** (`subject_id = 1`). Use a subquery with `MAX`. Why might more than one student appear?

## 2. Self-joins

A **self-join** joins a table to itself, so you must use two different aliases.

1. List the names of the classmates of **Tan Wei Jie** (the other students in his class). Use `students AS s1 JOIN students AS s2 ...`.
2. **Stretch:** list every pair of students in the same CCA, each pair once, with the CCA name. (Hint: join `student_cca` to itself with `a.cca_id = b.cca_id AND a.student_id < b.student_id`, then join `students` twice and `ccas` once.)

## 3. Hand-trace a GROUP BY query (exam skill)

Set up the small `sales` table (see `challenges/sales.sql`):

| id | region | product | amount |
|----|--------|---------|--------|
| 1 | North | pens | 12 |
| 2 | North | books | 30 |
| 3 | South | pens | 8 |
| 4 | South | books | 25 |
| 5 | South | books | 40 |
| 6 | East | pens | 15 |
| 7 | East | pens | 20 |
| 8 | North | pens | 5 |

**Without running anything**, trace this query in the order SQL really executes it:

```sql
SELECT region, COUNT(*) AS n, SUM(amount) AS total
FROM sales
WHERE amount >= 10
GROUP BY region
HAVING SUM(amount) > 40
ORDER BY total DESC;
```

Write down, in order:

1. the rows left after `WHERE`;
2. the groups formed by `GROUP BY` and their `n` and `total`;
3. the groups left after `HAVING`;
4. the final output after `ORDER BY`.

Then do the same for:

```sql
SELECT product, ROUND(AVG(amount), 1) AS average
FROM sales
GROUP BY product
ORDER BY average DESC;
```

Finally run both queries to check.

## 4. Exam-style written questions

1. State the difference between `WHERE` and `HAVING`.
2. Explain the difference between `COUNT(*)` and `COUNT(score)`.
3. A student writes `SELECT name, class, COUNT(*) FROM students GROUP BY class;`. Explain what is wrong with the query.
4. Describe, in words, the difference between an `INNER JOIN` and a `LEFT JOIN`, using `students` and `student_cca` as the example.
5. Write a query that shows each **category** of CCA and the number of CCAs in it, for categories with more than two CCAs.
6. The `scores` table has `student_id` and `subject_id` as a composite primary key. Write a query that lists each student's name with the **number of subjects they have a score for**, including students with none.
