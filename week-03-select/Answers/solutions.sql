-- Week 3: all answers in one runnable file.  Run:  sqlite3 school.db < week-03-select/Answers/solutions.sql
.headers on
.mode column
.nullvalue NULL

-- ===== Challenge 1 =====
-- Q1: Show every column of every subject.
SELECT * FROM subjects;

-- Q2: Name and class of every student.
SELECT name, class
FROM students;

-- Q3: Names of students in class 3B.
SELECT name
FROM students
WHERE class = '3B';

-- Q4: Names of the girls in class 3C.
SELECT name
FROM students
WHERE class = '3C' AND gender = 'F';

-- Q5: All student names in alphabetical order.
SELECT name
FROM students
ORDER BY name;

-- Q6: Names and dates of birth of students born in 2010, oldest first.
SELECT name, dob
FROM students
WHERE dob BETWEEN '2010-01-01' AND '2010-12-31'
ORDER BY dob;

-- Q7: Scores of 90 or more, highest first.
SELECT student_id, subject_id, score
FROM scores
WHERE score >= 90
ORDER BY score DESC;

-- Q8: Name and class of students in 3A or 3C, sorted by class then name.
SELECT name, class
FROM students
WHERE class IN ('3A', '3C')
ORDER BY class, name;

-- Q9: The five lowest scores.
SELECT student_id, subject_id, score
FROM scores
WHERE score IS NOT NULL
ORDER BY score ASC
LIMIT 5;

-- Q10: CCAs on Tuesday or Thursday that are not Sports.
SELECT name, category, day
FROM ccas
WHERE day IN ('Tuesday', 'Thursday')
  AND NOT category = 'Sports';

-- ===== Challenge 2 =====
-- 1: Which students in Class 3A have a name that starts with T?
SELECT name
FROM students
WHERE class = '3A' AND name LIKE 'T%';

-- 2: Which students have "Tan" anywhere in their name?
SELECT name
FROM students
WHERE name LIKE '%Tan%';

-- 3: Which students have no email on record?
SELECT name
FROM students
WHERE email IS NULL;

-- 4: Which students have `a` as the second letter of their name?
SELECT name
FROM students
WHERE name LIKE '_a%';

-- 5: Which subjects are taught by a teacher whose title is exactly "Mr"?
SELECT name, teacher
FROM subjects
WHERE teacher LIKE 'Mr %';

-- 6: Which CCAs are in the Performing Arts category, alphabetically?
SELECT name
FROM ccas
WHERE category = 'Performing Arts'
ORDER BY name;

-- 7: Each class that exists, once only.
SELECT DISTINCT class
FROM students;

-- 8: Students born in the first half of 2010.
SELECT name, dob
FROM students
WHERE dob BETWEEN '2010-01-01' AND '2010-06-30';

-- ===== Challenge 4 (sample) =====
-- 1: Which students have an email that has not been recorded and are in class 3C?
SELECT name
FROM students
WHERE email IS NULL AND class = '3C';

-- 2: Who are the three youngest students, and when were they born?
SELECT name, dob
FROM students
ORDER BY dob DESC
LIMIT 3;

-- 3: Which students in 3A or 3B have a name containing 'Lim'?
SELECT name, class
FROM students
WHERE class IN ('3A', '3B') AND name LIKE '%Lim%';

-- 4: Which CCAs meet on Fridays?
SELECT DISTINCT name
FROM ccas
WHERE day = 'Friday';

-- 5: Which Chemistry (subject 4) scores are between 40 and 59, lowest first?
SELECT student_id, score
FROM scores
WHERE subject_id = 4 AND score BETWEEN 40 AND 59
ORDER BY score;
