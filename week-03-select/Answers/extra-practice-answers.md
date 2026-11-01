# Week 3 Extra Practice: Answers

## 1. The NULL traps

### (a)

```sql
SELECT name FROM students WHERE email = NULL;
```

Result:

```
name
----
(no rows)
```

No rows. `= NULL` is never true.

### (b)

```sql
SELECT name FROM students WHERE email <> 's1001@student.school.edu.sg';
```

Result:

```
name
--------------
Tabitha Lim
Thaddeus Ong
Muhammad Irfan
Tiffany Goh
Chloe Tay
Arjun Menon
... (24 rows in total, first 6 shown)
```

29 students do not have this email, but only 24 are returned. The 5 students with a NULL email are missing, because `NULL <> 'x'` is unknown, not true.

### (c)

```sql
SELECT COUNT(*) FROM students WHERE email IS NULL OR email IS NOT NULL;
```

Result:

```
COUNT(*)
--------
30
```

All 30 students: every value is either NULL or not NULL.

### (d)

```sql
SELECT student_id, subject_id, score FROM scores ORDER BY score LIMIT 3;
```

Result:

```
student_id  subject_id  score
----------  ----------  -----
6           1           NULL
9           1           NULL
9           2           NULL
```

The three "lowest" are NULLs (absent students), because SQLite sorts NULL first.

### (e)

```sql
SELECT name FROM students WHERE student_id NOT IN (1, 2, NULL);
```

Result:

```
name
----
(no rows)
```

No rows! `x NOT IN (1, 2, NULL)` means `x<>1 AND x<>2 AND x<>NULL`, and the last part is never true. Never put NULL inside `NOT IN`.

### (f)

```sql
SELECT name, IFNULL(email, 'no email on record') AS email FROM students LIMIT 6;
```

Result:

```
name            email
--------------  ---------------------------
Tan Wei Jie     s1001@student.school.edu.sg
Tabitha Lim     s1002@student.school.edu.sg
Thaddeus Ong    s1003@student.school.edu.sg
Priya Nair      no email on record
Muhammad Irfan  s1005@student.school.edu.sg
Tiffany Goh     s1006@student.school.edu.sg
```

`IFNULL(x, y)` returns `x` unless it is NULL, in which case it returns `y`. (`COALESCE` does the same and accepts more than two arguments.)

## Follow-up questions

1. `SELECT name FROM students WHERE email IS NULL;`
2. Five. These are exactly the students whose email is NULL.
3. `SELECT student_id, subject_id, score FROM scores WHERE score IS NOT NULL ORDER BY score LIMIT 3;`
4. `IFNULL(x, y)` returns `x` if it is not NULL, otherwise `y`. It replaces missing values with a default.


## 2. Practise online

No answers needed. Check that students completed SQLBolt lessons 1 to 5 and the SQLZoo tutorials; ask which exercise they found hardest and go through it together next week.

## 3. More queries on school.db

### Question 1

*Names of students whose email starts with `s100`.*

```sql
SELECT name, email
FROM students
WHERE email LIKE 's100%';
```

Result:

```
name            email
--------------  ---------------------------
Tan Wei Jie     s1001@student.school.edu.sg
Tabitha Lim     s1002@student.school.edu.sg
Thaddeus Ong    s1003@student.school.edu.sg
Muhammad Irfan  s1005@student.school.edu.sg
Tiffany Goh     s1006@student.school.edu.sg
Chloe Tay       s1007@student.school.edu.sg
Arjun Menon     s1008@student.school.edu.sg
```

### Question 2

*Students not in 3A and born before 1 July 2009.*

```sql
SELECT name, class, dob
FROM students
WHERE class <> '3A' AND dob < '2009-07-01';
```

Result:

```
name           class  dob
-------------  -----  ----------
Ibrahim Yusof  3C     2009-01-23
```

### Question 3

*Subjects sorted by teacher in reverse alphabetical order.*

```sql
SELECT name, teacher
FROM subjects
ORDER BY teacher DESC;
```

Result:

```
name           teacher
-------------  ------------
Computing      Ms Rahman
Chemistry      Mrs Pillai
Mathematics    Mr Lee
General Paper  Mr Fernandez
Physics        Dr Chen
```

### Question 4

*Computing scores between 60 and 79, best first.*

```sql
SELECT student_id, score
FROM scores
WHERE subject_id = 2 AND score BETWEEN 60 AND 79
ORDER BY score DESC;
```

Result:

```
student_id  score
----------  -----
22          74
20          70
8           68
30          67
14          64
11          63
18          62
```

### Question 5

*Students whose name has exactly 11 characters.*

```sql
SELECT name
FROM students
WHERE LENGTH(name) = 11;
```

Result:

```
name
-----------
Tan Wei Jie
Tabitha Lim
Tiffany Goh
Arjun Menon
Lim Jia Hui
Tay Jun Hao
Lau Zi Xuan
Daniel Chua
Kavya Reddy
```

## 4. Exam-style written questions

1. A **primary key** is a column (or combination of columns) whose value uniquely identifies each row in a table; it can never be NULL. A **foreign key** is a column in one table that holds the primary key value of a row in another table, linking the two tables.
2. A **composite key** (a primary key made of more than one column). One column would not be enough: a student appears in `scores` once for every subject, and a subject appears once for every student, so neither `student_id` nor `subject_id` is unique on its own. Only the pair is.
3. The value `3A` is text and must be in single quotes (otherwise SQLite treats `3A` as a column name or a malformed number). Corrected: `SELECT name FROM students WHERE class = '3A';`
4. `WHERE` chooses which **rows** are included in the result (it filters). `ORDER BY` decides the **order** in which the chosen rows are shown (it sorts); it never removes rows.
5. `AND` has higher precedence than `OR`, so the query is read as `class = '3A' OR (class = '3B' AND gender = 'F')`, which returns every 3A student, boys included. Corrected: `SELECT name FROM students WHERE (class = '3A' OR class = '3B') AND gender = 'F';`
