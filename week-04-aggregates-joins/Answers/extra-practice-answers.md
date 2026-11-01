# Week 4 Extra Practice: Answers

## 1 and 2. Subqueries and self-joins

### 1.1

*Students who scored above the overall average in at least one subject.*

```sql
SELECT name
FROM students
WHERE student_id IN (SELECT student_id
                     FROM scores
                     WHERE score > (SELECT AVG(score) FROM scores));
```

Result:

```
name
--------------
Tabitha Lim
Thaddeus Ong
Priya Nair
Muhammad Irfan
Tiffany Goh
Chloe Tay
Arjun Menon
Nur Aisyah
Samuel Teo
Lim Jia Hui
Rahul Sharma
Wong Kai Xin
... (29 rows in total, first 12 shown)
```

The innermost query returns one number (about 67.4). The middle query returns the ids of students with at least one score above it. The outer query turns those ids into names. A join with `SELECT DISTINCT` would also work.

### 1.2a

*No CCA, using NOT IN.*

```sql
SELECT name
FROM students
WHERE student_id NOT IN (SELECT student_id FROM student_cca);
```

Result:

```
name
--------------
Muhammad Irfan
Chloe Tay
Ethan Koh
Deepa Krishnan
Lau Zi Xuan
Daniel Chua
Kavya Reddy
Jasmine Ho
```

Safe here because `student_cca.student_id` is part of the primary key and so is never NULL. (If the subquery could return NULL, `NOT IN` would return nothing at all; see Week 3 extra practice.)

### 1.2b

*No CCA, using NOT EXISTS.*

```sql
SELECT name
FROM students AS st
WHERE NOT EXISTS (SELECT 1
                  FROM student_cca AS x
                  WHERE x.student_id = st.student_id);
```

Result:

```
name
--------------
Muhammad Irfan
Chloe Tay
Ethan Koh
Deepa Krishnan
Lau Zi Xuan
Daniel Chua
Kavya Reddy
Jasmine Ho
```

The subquery refers to `st` from the outer query (a *correlated* subquery). `EXISTS` is true if the subquery returns at least one row. The `SELECT 1` is a convention: the value does not matter, only whether a row exists.

### 1.3

*CCAs with at least one member (EXISTS).*

```sql
SELECT name
FROM ccas AS c
WHERE EXISTS (SELECT 1
              FROM student_cca AS x
              WHERE x.cca_id = c.cca_id);
```

Result:

```
name
-----------------
Badminton
Basketball
Chinese Orchestra
Debate Society
Drama Club
Photography Club
Robotics Club
```

Seven CCAs. Chess Club is missing.

### 1.4

*Highest Mathematics score.*

```sql
SELECT st.name, sc.score
FROM scores AS sc
JOIN students AS st ON st.student_id = sc.student_id
WHERE sc.subject_id = 1
  AND sc.score = (SELECT MAX(score) FROM scores WHERE subject_id = 1);
```

Result:

```
name       score
---------  -----
Ethan Koh  98
```

More than one student can appear because several students may share the highest mark (a tie).

### 2.1

*Classmates of Tan Wei Jie (self-join).*

```sql
SELECT s2.name
FROM students AS s1
JOIN students AS s2 ON s2.class = s1.class
WHERE s1.name = 'Tan Wei Jie'
  AND s2.student_id <> s1.student_id
ORDER BY s2.name;
```

Result:

```
name
--------------
Arjun Menon
Chloe Tay
Muhammad Irfan
Nur Aisyah
Priya Nair
Samuel Teo
Tabitha Lim
Thaddeus Ong
Tiffany Goh
```

`s1` is the "me" row, `s2` is every other student in the same class. The condition `s2.student_id <> s1.student_id` removes Tan Wei Jie himself.

### 2.2

*Pairs of students in the same CCA (stretch).*

```sql
SELECT c.name AS cca, s1.name AS student_1, s2.name AS student_2
FROM student_cca AS a
JOIN student_cca AS b ON a.cca_id = b.cca_id AND a.student_id < b.student_id
JOIN students AS s1 ON s1.student_id = a.student_id
JOIN students AS s2 ON s2.student_id = b.student_id
JOIN ccas AS c ON c.cca_id = a.cca_id
ORDER BY c.name, s1.name, s2.name;
```

Result:

```
cca         student_1      student_2
----------  -------------  -------------
Badminton   Aaron Lee      Farah Hassan
Badminton   Aaron Lee      Ong Mei Ling
Badminton   Arjun Menon    Aaron Lee
Badminton   Arjun Menon    Farah Hassan
Badminton   Arjun Menon    Ong Mei Ling
Badminton   Arjun Menon    Zhang Yi Ming
Badminton   Farah Hassan   Ong Mei Ling
Badminton   Zhang Yi Ming  Aaron Lee
Badminton   Zhang Yi Ming  Farah Hassan
Badminton   Zhang Yi Ming  Ong Mei Ling
Basketball  Lim Jia Hui    Tay Jun Hao
Basketball  Tabitha Lim    Lim Jia Hui
... (45 rows in total, first 12 shown)
```

`a.student_id < b.student_id` makes each pair appear once (without it we would see both (Ali, Ben) and (Ben, Ali), plus every student paired with themselves).

## 3. Hand-trace a GROUP BY query

### First query

```sql
SELECT region, COUNT(*) AS n, SUM(amount) AS total
FROM sales
WHERE amount >= 10
GROUP BY region
HAVING SUM(amount) > 40
ORDER BY total DESC;
```

1. **After `WHERE amount >= 10`** (rows 3 and 8 are removed, because 8 and 5 are below 10):

   | id | region | product | amount |
   |----|--------|---------|--------|
   | 1 | North | pens | 12 |
   | 2 | North | books | 30 |
   | 4 | South | books | 25 |
   | 5 | South | books | 40 |
   | 6 | East | pens | 15 |
   | 7 | East | pens | 20 |

2. **After `GROUP BY region`:**

   | region | n | total |
   |--------|---|-------|
   | North | 2 | 42 |
   | South | 2 | 65 |
   | East | 2 | 35 |

3. **After `HAVING SUM(amount) > 40`:** East (35) is removed. North (42) and South (65) remain.
4. **After `ORDER BY total DESC`** (final output):

```
region  n  total
------  -  -----
South   2  65
North   2  42
```

### Second query

```sql
SELECT product, ROUND(AVG(amount), 1) AS average
FROM sales
GROUP BY product
ORDER BY average DESC;
```

There is no `WHERE`, so all eight rows are grouped. `pens`: 12, 8, 15, 20, 5 gives an average of 60 / 5 = 12.0. `books`: 30, 25, 40 gives 95 / 3 = 31.67, rounded to 31.7.

```
product  average
-------  -------
books    31.7
pens     12.0
```

**Key lesson:** the clauses run in the order `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`. Row 3 (`South`, 8) never reaches the groups because `WHERE` removed it first. Moving that condition to `HAVING` would be a different query.

## 4. Exam-style written questions

1. `WHERE` filters individual rows **before** they are grouped, so it cannot use aggregate functions. `HAVING` filters whole groups **after** `GROUP BY`, and it can use aggregate functions.
2. `COUNT(*)` counts all the rows in each group (or table). `COUNT(score)` counts only the rows where `score` is not NULL, so it skips absent students.
3. `name` is neither in the `GROUP BY` clause nor inside an aggregate function. Each class has many students, so the query does not say *which* name to show for each class. (SQLite will run it and show an arbitrary name, but standard SQL and most other databases reject it.) Fix: remove `name`, or group by it as well.
4. An `INNER JOIN` returns only students who have at least one matching row in `student_cca`, so students with no CCA are not in the result. A `LEFT JOIN` returns **every** student; for students with no CCA the `student_cca` columns are filled with NULL.
5. ```sql
SELECT category, COUNT(*) AS ccas
FROM ccas
GROUP BY category
HAVING COUNT(*) > 2;
```

   Result on the starter data:

   ```
   category           ccas
   -----------------  ----
   Clubs & Societies  4
   ```
6. ```sql
SELECT st.name, COUNT(sc.score) AS subjects
FROM students AS st
LEFT JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name;
```

   Everybody has at least two subjects in this data, so no zeros appear, but the `LEFT JOIN` keeps the query correct if a new student with no scores is added.
