# Week 3 Challenge Answers

All results below were produced by running the queries on the starter `school.db`. Row order matters wherever the question asks for sorting; where it does not, any order is accepted.

## Challenge 1: Ten progressive queries

### Q1

*Show every column of every subject.*

```sql
SELECT * FROM subjects;
```

Result:

```
subject_id  name           teacher
----------  -------------  ------------
1           Mathematics    Mr Lee
2           Computing      Ms Rahman
3           Physics        Dr Chen
4           Chemistry      Mrs Pillai
5           General Paper  Mr Fernandez
```

### Q2

*Name and class of every student.*

```sql
SELECT name, class
FROM students;
```

Result:

```
name            class
--------------  -----
Tan Wei Jie     3A
Tabitha Lim     3A
Thaddeus Ong    3A
Priya Nair      3A
Muhammad Irfan  3A
Tiffany Goh     3A
Chloe Tay       3A
Arjun Menon     3A
Nur Aisyah      3A
Samuel Teo      3A
... (30 rows in total, first 10 shown)
```

### Q3

*Names of students in class 3B.*

```sql
SELECT name
FROM students
WHERE class = '3B';
```

Result:

```
name
--------------
Lim Jia Hui
Rahul Sharma
Wong Kai Xin
Siti Nurhaliza
Ethan Koh
Zhang Yi Ming
Deepa Krishnan
Aaron Lee
Farah Hassan
Tay Jun Hao
```

### Q4

*Names of the girls in class 3C.*

```sql
SELECT name
FROM students
WHERE class = '3C' AND gender = 'F';
```

Result:

```
name
------------
Ng Shu Min
Lau Zi Xuan
Ong Mei Ling
Kavya Reddy
Nurul Huda
Jasmine Ho
```

### Q5

*All student names in alphabetical order.*

```sql
SELECT name
FROM students
ORDER BY name;
```

Result:

```
name
--------------
Aaron Lee
Arjun Menon
Chloe Tay
Daniel Chua
Deepa Krishnan
Ethan Koh
Farah Hassan
Harpreet Singh
Ibrahim Yusof
Jasmine Ho
... (30 rows in total, first 10 shown)
```

### Q6

*Names and dates of birth of students born in 2010, oldest first.*

```sql
SELECT name, dob
FROM students
WHERE dob BETWEEN '2010-01-01' AND '2010-12-31'
ORDER BY dob;
```

Result:

```
name            dob
--------------  ----------
Zhang Yi Ming   2010-01-28
Aaron Lee       2010-02-13
Farah Hassan    2010-02-14
Kavya Reddy     2010-04-28
Siti Nurhaliza  2010-05-15
Deepa Krishnan  2010-06-15
Samuel Teo      2010-06-26
Tay Jun Hao     2010-07-17
Ng Shu Min      2010-07-19
Daniel Chua     2010-08-05
... (17 rows in total, first 10 shown)
```

Alternative: `WHERE dob LIKE '2010%'`. Both work because dates are stored as `YYYY-MM-DD` text.

### Q7

*Scores of 90 or more, highest first.*

```sql
SELECT student_id, subject_id, score
FROM scores
WHERE score >= 90
ORDER BY score DESC;
```

Result:

```
student_id  subject_id  score
----------  ----------  -----
15          1           98
24          5           98
6           4           96
19          4           96
2           3           95
14          3           93
12          4           92
21          2           92
```

### Q8

*Name and class of students in 3A or 3C, sorted by class then name.*

```sql
SELECT name, class
FROM students
WHERE class IN ('3A', '3C')
ORDER BY class, name;
```

Result:

```
name            class
--------------  -----
Arjun Menon     3A
Chloe Tay       3A
Muhammad Irfan  3A
Nur Aisyah      3A
Priya Nair      3A
Samuel Teo      3A
Tabitha Lim     3A
Tan Wei Jie     3A
Thaddeus Ong    3A
Tiffany Goh     3A
... (20 rows in total, first 10 shown)
```

### Q9

*The five lowest scores.*

```sql
SELECT student_id, subject_id, score
FROM scores
WHERE score IS NOT NULL
ORDER BY score ASC
LIMIT 5;
```

Result:

```
student_id  subject_id  score
----------  ----------  -----
9           5           30
3           3           35
16          1           36
19          2           40
7           2           41
```

**Trap:** without `WHERE score IS NOT NULL`, the four absent students (NULL) would appear first, because SQLite sorts NULL before every number in ascending order.

### Q10

*CCAs on Tuesday or Thursday that are not Sports.*

```sql
SELECT name, category, day
FROM ccas
WHERE day IN ('Tuesday', 'Thursday')
  AND NOT category = 'Sports';
```

Result:

```
name               category         day
-----------------  ---------------  --------
Chinese Orchestra  Performing Arts  Thursday
Drama Club         Performing Arts  Thursday
```

Only two CCAs meet on Tuesday or Thursday and are not Sports. Equivalent: `category <> 'Sports'`.

## Challenge 2: From English to SQL

### Question 1

*Which students in Class 3A have a name that starts with T?*

```sql
SELECT name
FROM students
WHERE class = '3A' AND name LIKE 'T%';
```

Result:

```
name
------------
Tan Wei Jie
Tabitha Lim
Thaddeus Ong
Tiffany Goh
```

### Question 2

*Which students have "Tan" anywhere in their name?*

```sql
SELECT name
FROM students
WHERE name LIKE '%Tan%';
```

Result:

```
name
-------------
Tan Wei Jie
Tan Ming Yang
```

### Question 3

*Which students have no email on record?*

```sql
SELECT name
FROM students
WHERE email IS NULL;
```

Result:

```
name
--------------
Priya Nair
Nur Aisyah
Deepa Krishnan
Harpreet Singh
Tan Ming Yang
```

### Question 4

*Which students have `a` as the second letter of their name?*

```sql
SELECT name
FROM students
WHERE name LIKE '_a%';
```

Result:

```
name
--------------
Tan Wei Jie
Tabitha Lim
Samuel Teo
Rahul Sharma
Aaron Lee
Farah Hassan
Tay Jun Hao
Harpreet Singh
Lau Zi Xuan
Daniel Chua
Kavya Reddy
Tan Ming Yang
Jasmine Ho
```

`_` matches exactly one character, so `'_a%'` means: any first letter, then `a`, then anything.

### Question 5

*Which subjects are taught by a teacher whose title is exactly "Mr"?*

```sql
SELECT name, teacher
FROM subjects
WHERE teacher LIKE 'Mr %';
```

Result:

```
name           teacher
-------------  ------------
Mathematics    Mr Lee
General Paper  Mr Fernandez
```

**Trap:** `LIKE 'Mr%'` would also match `Mrs Pillai`. The space in `'Mr %'` fixes it.

### Question 6

*Which CCAs are in the Performing Arts category, alphabetically?*

```sql
SELECT name
FROM ccas
WHERE category = 'Performing Arts'
ORDER BY name;
```

Result:

```
name
-----------------
Chinese Orchestra
Drama Club
```

### Question 7

*Each class that exists, once only.*

```sql
SELECT DISTINCT class
FROM students;
```

Result:

```
class
-----
3A
3B
3C
```

### Question 8

*Students born in the first half of 2010.*

```sql
SELECT name, dob
FROM students
WHERE dob BETWEEN '2010-01-01' AND '2010-06-30';
```

Result:

```
name            dob
--------------  ----------
Samuel Teo      2010-06-26
Siti Nurhaliza  2010-05-15
Zhang Yi Ming   2010-01-28
Deepa Krishnan  2010-06-15
Aaron Lee       2010-02-13
Farah Hassan    2010-02-14
Kavya Reddy     2010-04-28
```

`BETWEEN` includes both ends. Alternatively: `dob >= '2010-01-01' AND dob < '2010-07-01'`.

## Challenge 3: Predict, then run

Results on the `pets` table. Marking: one point per correct prediction, including the row order. The explanation sentences matter more than the score.

### Query A

```sql
SELECT name FROM pets WHERE species = 'cat';
```

Output:

```
name
----
Milo
Coco
Luna
```

Three cats.

### Query B

```sql
SELECT name, age FROM pets WHERE age > 4 ORDER BY age DESC, name;
```

Output:

```
name   age
-----  ---
Rex    7
Bella  5
Luna   5
```

Rex is 7. Bella and Luna are both 5, so `name` breaks the tie alphabetically. Coco and Pip (age NULL) are excluded because `NULL > 4` is not true.

### Query C

```sql
SELECT DISTINCT owner FROM pets ORDER BY owner;
```

Output:

```
owner
-----
NULL
Ali
Ben
Cara
```

`DISTINCT` treats NULL as one value, and SQLite sorts NULL first.

### Query D

```sql
SELECT name FROM pets WHERE age = NULL;
```

Output:

```
name
----
(no rows)
```

Nothing: `age = NULL` is never true. Use `age IS NULL`.

### Query E

```sql
SELECT name FROM pets WHERE NOT species = 'dog' AND age IS NOT NULL;
```

Output:

```
name
----
Milo
Nemo
Luna
```

Non-dogs with a known age: Coco and Pip are excluded because their age is NULL.

### Query F

```sql
SELECT name FROM pets
WHERE species IN ('cat', 'bird') OR age BETWEEN 5 AND 7
ORDER BY name
LIMIT 3;
```

Output:

```
name
-----
Bella
Coco
Luna
```

Matching rows: Milo, Coco, Luna, Pip (cat or bird) and Bella, Rex, Luna (age 5 to 7). Sorted: Bella, Coco, Luna, Milo, Pip, Rex. `LIMIT 3` keeps the first three.

### Query G

```sql
SELECT name FROM pets WHERE owner != 'Ali';
```

Output:

```
name
-----
Bella
Nemo
Luna
Max
```

**Trap:** Rex and Pip have no owner (NULL). `NULL != 'Ali'` is unknown, so they are not returned, even though they certainly are not owned by Ali. To include them: `WHERE owner != 'Ali' OR owner IS NULL`.

## Challenge 4: Ask your own questions (sample answer)

Students' questions will differ. Check the rubric in the challenge. A sample set that meets every requirement:

### Sample question 1

*Which students have an email that has not been recorded and are in class 3C?*

```sql
SELECT name
FROM students
WHERE email IS NULL AND class = '3C';
```

Result:

```
name
--------------
Harpreet Singh
Tan Ming Yang
```

### Sample question 2

*Who are the three youngest students, and when were they born?*

```sql
SELECT name, dob
FROM students
ORDER BY dob DESC
LIMIT 3;
```

Result:

```
name         dob
-----------  ----------
Lim Jia Hui  2010-12-17
Nurul Huda   2010-11-16
Arjun Menon  2010-11-11
```

### Sample question 3

*Which students in 3A or 3B have a name containing 'Lim'?*

```sql
SELECT name, class
FROM students
WHERE class IN ('3A', '3B') AND name LIKE '%Lim%';
```

Result:

```
name         class
-----------  -----
Tabitha Lim  3A
Lim Jia Hui  3B
```

### Sample question 4

*Which CCAs meet on Fridays?*

```sql
SELECT DISTINCT name
FROM ccas
WHERE day = 'Friday';
```

Result:

```
name
--------------
Debate Society
Chess Club
```

### Sample question 5

*Which Chemistry (subject 4) scores are between 40 and 59, lowest first?*

```sql
SELECT student_id, score
FROM scores
WHERE subject_id = 4 AND score BETWEEN 40 AND 59
ORDER BY score;
```

Result:

```
student_id  score
----------  -----
10          45
4           51
16          51
17          55
21          55
1           59
```
