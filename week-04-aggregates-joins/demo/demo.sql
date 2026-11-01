-- Week 4 demo script.   Run from the repository root:   sqlite3 school.db

-- 1. Aggregate functions
SELECT COUNT(*) FROM students;
SELECT COUNT(email) FROM students;
SELECT COUNT(*) AS total, COUNT(email) AS with_email FROM students;
SELECT MIN(score), MAX(score) FROM scores;
SELECT AVG(score) FROM scores;
SELECT ROUND(AVG(score), 1) AS average FROM scores;
SELECT SUM(score) FROM scores WHERE subject_id = 1;
SELECT COUNT(DISTINCT class) FROM students;
SELECT COUNT(*), COUNT(score) FROM scores;                 -- 120 vs 116: NULLs are ignored

-- 2. GROUP BY and HAVING
SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id;

SELECT class, COUNT(*) AS students
FROM students
GROUP BY class;

SELECT subject_id, ROUND(AVG(score), 1) AS average
FROM scores
GROUP BY subject_id
HAVING AVG(score) > 66;

-- 3. INNER JOIN
SELECT students.name, scores.subject_id, scores.score
FROM scores
INNER JOIN students ON scores.student_id = students.student_id;

SELECT st.name, sc.subject_id, sc.score
FROM scores AS sc
JOIN students AS st ON sc.student_id = st.student_id;

-- Three tables
SELECT st.name, su.name AS subject, sc.score
FROM scores AS sc
JOIN students AS st ON sc.student_id = st.student_id
JOIN subjects AS su ON sc.subject_id = su.subject_id
WHERE st.class = '3A'
ORDER BY st.name, su.name;

-- Join + GROUP BY
SELECT su.name AS subject, ROUND(AVG(sc.score), 1) AS average
FROM scores AS sc
JOIN subjects AS su ON sc.subject_id = su.subject_id
GROUP BY su.name
ORDER BY average DESC;

-- 4. LEFT JOIN
SELECT st.name, sc.cca_id
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id;

SELECT st.name
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;

SELECT st.name, COUNT(sc.cca_id) AS ccas
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
GROUP BY st.student_id, st.name
ORDER BY ccas DESC;

-- 5. A first look at subqueries
SELECT AVG(score) FROM scores;

SELECT student_id, subject_id, score
FROM scores
WHERE score > (SELECT AVG(score) FROM scores);

SELECT name FROM students
WHERE student_id IN (SELECT student_id FROM student_cca WHERE cca_id = 1);
