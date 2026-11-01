# Week 4 Challenge Answers

All results were produced by running the queries on the starter `school.db`.

## Challenge 1: Report queries

### 1.1

*Students in each CCA (by id).*

```sql
SELECT cca_id, COUNT(*) AS members
FROM student_cca
GROUP BY cca_id;
```

Result:

```
cca_id  members
------  -------
1       5
2       3
3       4
4       3
5       3
6       5
7       5
```

### 1.2

*Average score for each subject (by id).*

```sql
SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id;
```

Result:

```
subject_id  average
----------  -------
1           64.2
2           65.5
3           70.1
4           71.1
5           66.5
```

### 1.3

*Average per subject name, best first.*

```sql
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
ORDER BY average DESC;
```

Result:

```
subject        average
-------------  -------
Chemistry      71.1
Physics        70.1
General Paper  66.5
Computing      65.5
Mathematics    64.2
```

### 1.4

*Students per CCA name, biggest first, ties alphabetical.*

```sql
SELECT c.name AS cca, COUNT(*) AS members
FROM student_cca AS x
JOIN ccas AS c ON x.cca_id = c.cca_id
GROUP BY c.name
ORDER BY members DESC, c.name;
```

Result:

```
cca                members
-----------------  -------
Badminton          5
Drama Club         5
Robotics Club      5
Chinese Orchestra  4
Basketball         3
Debate Society     3
Photography Club   3
```

Chess Club does not appear: it has no rows in `student_cca`, and an `INNER JOIN` only keeps matches. (Challenge 2, question 3 deals with this.)

### 1.5

*Number of students in each class.*

```sql
SELECT class, COUNT(*) AS students
FROM students
GROUP BY class;
```

Result:

```
class  students
-----  --------
3A     10
3B     10
3C     10
```

### 1.6

*Highest and lowest score per subject name.*

```sql
SELECT su.name AS subject, MAX(sc.score) AS highest, MIN(sc.score) AS lowest
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name;
```

Result:

```
subject        highest  lowest
-------------  -------  ------
Chemistry      96       45
Computing      92       40
General Paper  98       30
Mathematics    98       36
Physics        95       35
```

`MIN` and `MAX` ignore the NULL (absent) scores.

### 1.7

*Subjects with an average above 66.*

```sql
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
HAVING AVG(sc.score) > 66;
```

Result:

```
subject        average
-------------  -------
Chemistry      71.1
General Paper  66.5
Physics        70.1
```

The condition is on a group value, so it must be in `HAVING`, not `WHERE`. Note that `HAVING AVG(sc.score) > 66` uses the unrounded average; `HAVING average > 66` would also work in SQLite.

## Challenge 2: Who is missing?

### 2.1

*Students with no CCA.*

```sql
SELECT st.name, st.class
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL
ORDER BY st.class, st.name;
```

Result:

```
name            class
--------------  -----
Chloe Tay       3A
Muhammad Irfan  3A
Deepa Krishnan  3B
Ethan Koh       3B
Daniel Chua     3C
Jasmine Ho      3C
Kavya Reddy     3C
Lau Zi Xuan     3C
```

The `LEFT JOIN` keeps every student. For students with no match, the `student_cca` columns are NULL, so `sc.student_id IS NULL` finds them.

### 2.2

*How many students have no CCA?*

```sql
SELECT COUNT(*) AS no_cca
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;
```

Result:

```
no_cca
------
8
```

### 2.3

*CCAs with no members.*

```sql
SELECT c.name
FROM ccas AS c
LEFT JOIN student_cca AS sc ON sc.cca_id = c.cca_id
WHERE sc.cca_id IS NULL;
```

Result:

```
name
----------
Chess Club
```

This time the CCA table is on the **left**: we want to keep every CCA.

### 2.4

*Number of CCAs per student, including zero.*

```sql
SELECT st.name, COUNT(sc.cca_id) AS ccas
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC, st.name;
```

Result:

```
name            ccas
--------------  ----
Aaron Lee       2
Farah Hassan    2
Nur Aisyah      2
Ong Mei Ling    2
Wong Kai Xin    2
Zhang Yi Ming   2
Arjun Menon     1
Harpreet Singh  1
Ibrahim Yusof   1
Lim Jia Hui     1
Ng Shu Min      1
Nurul Huda      1
... (30 rows in total, first 12 shown)
```

`COUNT(sc.cca_id)` counts only non-NULL values, so unmatched students get 0. `COUNT(*)` would give 1, because the unmatched row still exists.

**Question 5.** An `INNER JOIN` keeps only rows that have a match in both tables, so students with no CCA (and CCAs with no members) have no match and disappear from the result. We need to *see* the unmatched rows, which only a `LEFT JOIN` keeps, with NULLs in the missing columns.

## Challenge 3: Class report card

### 3.1

*Report card for Tan Wei Jie.*

```sql
SELECT st.name, su.name AS subject, sc.score
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
JOIN subjects AS su ON su.subject_id = sc.subject_id
WHERE st.name = 'Tan Wei Jie'
ORDER BY su.name;
```

Result:

```
name         subject        score
-----------  -------------  -----
Tan Wei Jie  Chemistry      59
Tan Wei Jie  General Paper  42
Tan Wei Jie  Mathematics    47
Tan Wei Jie  Physics        61
```

`WHERE st.name = 'Tan Wei Jie'` is safe here because only one student has that name. In a real system you would filter on `student_id`.

### 3.2

*Report card for every student in 3A.*

```sql
SELECT st.name AS student, su.name AS subject, sc.score
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
JOIN subjects AS su ON su.subject_id = sc.subject_id
WHERE st.class = '3A'
ORDER BY st.name, su.name;
```

Result:

```
student         subject        score
--------------  -------------  -----
Arjun Menon     Computing      68
Arjun Menon     General Paper  68
Arjun Menon     Mathematics    65
Arjun Menon     Physics        87
Chloe Tay       Computing      41
Chloe Tay       General Paper  75
Chloe Tay       Mathematics    48
Chloe Tay       Physics        61
Muhammad Irfan  Chemistry      73
Muhammad Irfan  Computing      56
Muhammad Irfan  General Paper  64
Muhammad Irfan  Mathematics    74
... (40 rows in total, first 12 shown)
```

### 3.3

*Average score and number of scored subjects per student in 3A.*

```sql
SELECT st.name AS student,
       ROUND(AVG(sc.score), 1) AS average,
       COUNT(sc.score) AS subjects
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
WHERE st.class = '3A'
GROUP BY st.student_id, st.name
ORDER BY average DESC, st.name;
```

Result:

```
student         average  subjects
--------------  -------  --------
Tiffany Goh     79.0     3
Tabitha Lim     78.8     4
Arjun Menon     72.0     4
Muhammad Irfan  66.8     4
Samuel Teo      63.3     4
Thaddeus Ong    62.5     4
Priya Nair      58.5     4
Chloe Tay       56.3     4
Tan Wei Jie     52.3     4
Nur Aisyah      49.0     2
```

`COUNT(sc.score)` ignores absent (NULL) scores, so it counts only the subjects actually sat. Using `COUNT(*)` would also count the absent ones.

### 3.4

*Students whose average is below 60.*

```sql
SELECT st.name, st.class, ROUND(AVG(sc.score), 1) AS average
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name, st.class
HAVING AVG(sc.score) < 60
ORDER BY average;
```

Result:

```
name           class  average
-------------  -----  -------
Nur Aisyah     3A     49.0
Tan Wei Jie    3A     52.3
Chloe Tay      3A     56.3
Kavya Reddy    3C     57.3
Daniel Chua    3C     57.8
Zhang Yi Ming  3B     58.3
Priya Nair     3A     58.5
```

## Challenge 4: "Top 5" report (samples)

Students' reports will differ. Use the rubric. Three sample answers:

### Sample A

*The 5 students with the highest average score. (A teacher could use this to nominate students for a prize.)*

```sql
SELECT st.name AS student, st.class,
       ROUND(AVG(sc.score), 1) AS average
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name, st.class
ORDER BY average DESC, st.name
LIMIT 5;
```

Result:

```
student         class  average
--------------  -----  -------
Siti Nurhaliza  3B     79.8
Tiffany Goh     3A     79.0
Rahul Sharma    3B     78.8
Tabitha Lim     3A     78.8
Ng Shu Min      3C     77.0
```

Ties are broken by name. Without the second `ORDER BY` column, which tied student appears is not defined.

### Sample B

*The 3 CCAs whose members have the highest average score. (A teacher could use this to see whether some CCAs attract stronger students.)*

```sql
SELECT c.name AS cca,
       ROUND(AVG(sc.score), 1) AS average,
       COUNT(DISTINCT x.student_id) AS members
FROM ccas AS c
JOIN student_cca AS x ON x.cca_id = c.cca_id
JOIN scores AS sc ON sc.student_id = x.student_id
GROUP BY c.cca_id, c.name
ORDER BY average DESC, c.name
LIMIT 3;
```

Result:

```
cca                average  members
-----------------  -------  -------
Photography Club   76.9     3
Basketball         74.1     3
Chinese Orchestra  69.4     4
```

`COUNT(DISTINCT x.student_id)` is needed because each member appears once per subject after the join.

### Sample C

*The 5 students who belong to the most CCAs.*

```sql
SELECT st.name, COUNT(*) AS ccas
FROM students AS st
JOIN student_cca AS x ON x.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC, st.name
LIMIT 5;
```

Result:

```
name          ccas
------------  ----
Aaron Lee     2
Farah Hassan  2
Nur Aisyah    2
Ong Mei Ling  2
Wong Kai Xin  2
```
