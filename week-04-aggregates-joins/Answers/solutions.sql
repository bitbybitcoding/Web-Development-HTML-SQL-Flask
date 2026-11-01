-- Week 4: all answers in one runnable file.  Run:  sqlite3 school.db < week-04-aggregates-joins/Answers/solutions.sql
.headers on
.mode column
.nullvalue NULL

-- ===== Challenge 1 =====
-- 1.1: Students in each CCA (by id).
SELECT cca_id, COUNT(*) AS members
FROM student_cca
GROUP BY cca_id;

-- 1.2: Average score for each subject (by id).
SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id;

-- 1.3: Average per subject name, best first.
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
ORDER BY average DESC;

-- 1.4: Students per CCA name, biggest first, ties alphabetical.
SELECT c.name AS cca, COUNT(*) AS members
FROM student_cca AS x
JOIN ccas AS c ON x.cca_id = c.cca_id
GROUP BY c.name
ORDER BY members DESC, c.name;

-- 1.5: Number of students in each class.
SELECT class, COUNT(*) AS students
FROM students
GROUP BY class;

-- 1.6: Highest and lowest score per subject name.
SELECT su.name AS subject, MAX(sc.score) AS highest, MIN(sc.score) AS lowest
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name;

-- 1.7: Subjects with an average above 66.
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
HAVING AVG(sc.score) > 66;

-- ===== Challenge 2 =====
-- 2.1: Students with no CCA.
SELECT st.name, st.class
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL
ORDER BY st.class, st.name;

-- 2.2: How many students have no CCA?
SELECT COUNT(*) AS no_cca
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;

-- 2.3: CCAs with no members.
SELECT c.name
FROM ccas AS c
LEFT JOIN student_cca AS sc ON sc.cca_id = c.cca_id
WHERE sc.cca_id IS NULL;

-- 2.4: Number of CCAs per student, including zero.
SELECT st.name, COUNT(sc.cca_id) AS ccas
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC, st.name;

-- ===== Challenge 3 =====
-- 3.1: Report card for Tan Wei Jie.
SELECT st.name, su.name AS subject, sc.score
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
JOIN subjects AS su ON su.subject_id = sc.subject_id
WHERE st.name = 'Tan Wei Jie'
ORDER BY su.name;

-- 3.2: Report card for every student in 3A.
SELECT st.name AS student, su.name AS subject, sc.score
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
JOIN subjects AS su ON su.subject_id = sc.subject_id
WHERE st.class = '3A'
ORDER BY st.name, su.name;

-- 3.3: Average score and number of scored subjects per student in 3A.
SELECT st.name AS student,
       ROUND(AVG(sc.score), 1) AS average,
       COUNT(sc.score) AS subjects
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
WHERE st.class = '3A'
GROUP BY st.student_id, st.name
ORDER BY average DESC, st.name;

-- 3.4: Students whose average is below 60.
SELECT st.name, st.class, ROUND(AVG(sc.score), 1) AS average
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name, st.class
HAVING AVG(sc.score) < 60
ORDER BY average;

-- ===== Challenge 4 (samples) =====
-- Sample A: The 5 students with the highest average score. (A teacher could use this to nominate students for a prize.)
SELECT st.name AS student, st.class,
       ROUND(AVG(sc.score), 1) AS average
FROM students AS st
JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name, st.class
ORDER BY average DESC, st.name
LIMIT 5;

-- Sample B: The 3 CCAs whose members have the highest average score. (A teacher could use this to see whether some CCAs attract stronger students.)
SELECT c.name AS cca,
       ROUND(AVG(sc.score), 1) AS average,
       COUNT(DISTINCT x.student_id) AS members
FROM ccas AS c
JOIN student_cca AS x ON x.cca_id = c.cca_id
JOIN scores AS sc ON sc.student_id = x.student_id
GROUP BY c.cca_id, c.name
ORDER BY average DESC, c.name
LIMIT 3;

-- Sample C: The 5 students who belong to the most CCAs.
SELECT st.name, COUNT(*) AS ccas
FROM students AS st
JOIN student_cca AS x ON x.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC, st.name
LIMIT 5;

-- ===== Extra practice =====
-- 1.1: Students who scored above the overall average in at least one subject.
SELECT name
FROM students
WHERE student_id IN (SELECT student_id
                     FROM scores
                     WHERE score > (SELECT AVG(score) FROM scores));

-- 1.2a: No CCA, using NOT IN.
SELECT name
FROM students
WHERE student_id NOT IN (SELECT student_id FROM student_cca);

-- 1.2b: No CCA, using NOT EXISTS.
SELECT name
FROM students AS st
WHERE NOT EXISTS (SELECT 1
                  FROM student_cca AS x
                  WHERE x.student_id = st.student_id);

-- 1.3: CCAs with at least one member (EXISTS).
SELECT name
FROM ccas AS c
WHERE EXISTS (SELECT 1
              FROM student_cca AS x
              WHERE x.cca_id = c.cca_id);

-- 1.4: Highest Mathematics score.
SELECT st.name, sc.score
FROM scores AS sc
JOIN students AS st ON st.student_id = sc.student_id
WHERE sc.subject_id = 1
  AND sc.score = (SELECT MAX(score) FROM scores WHERE subject_id = 1);

-- 2.1: Classmates of Tan Wei Jie (self-join).
SELECT s2.name
FROM students AS s1
JOIN students AS s2 ON s2.class = s1.class
WHERE s1.name = 'Tan Wei Jie'
  AND s2.student_id <> s1.student_id
ORDER BY s2.name;

-- 2.2: Pairs of students in the same CCA (stretch).
SELECT c.name AS cca, s1.name AS student_1, s2.name AS student_2
FROM student_cca AS a
JOIN student_cca AS b ON a.cca_id = b.cca_id AND a.student_id < b.student_id
JOIN students AS s1 ON s1.student_id = a.student_id
JOIN students AS s2 ON s2.student_id = b.student_id
JOIN ccas AS c ON c.cca_id = a.cca_id
ORDER BY c.name, s1.name, s2.name;

-- W4: Written Q5: CCA categories with more than two CCAs.
SELECT category, COUNT(*) AS ccas
FROM ccas
GROUP BY category
HAVING COUNT(*) > 2;

-- W6: Written Q6: number of subjects with a score, including students with none.
SELECT st.name, COUNT(sc.score) AS subjects
FROM students AS st
LEFT JOIN scores AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name;
