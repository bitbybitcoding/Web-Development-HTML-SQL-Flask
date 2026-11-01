-- Week 3 demo script.   Run from the repository root:   sqlite3 school.db
-- Lines starting with a dot are sqlite3 shell commands, not SQL.

.tables
.schema students

-- 1. Choosing columns
SELECT * FROM students;
SELECT name, class FROM students;
SELECT name AS "Student", class AS "Class" FROM students;

-- 2. Filtering rows: WHERE, AND, OR, NOT
SELECT name FROM students WHERE class = '3A';
SELECT name FROM students WHERE class = '3B' AND gender = 'F';
SELECT name FROM students WHERE class = '3A' OR class = '3B';
SELECT name FROM students WHERE NOT class = '3C';

-- Precedence trap: AND is evaluated before OR
SELECT name, class, gender FROM students
WHERE class = '3A' OR class = '3B' AND gender = 'F';

SELECT name, class, gender FROM students
WHERE (class = '3A' OR class = '3B') AND gender = 'F';

-- 3. Sorting
SELECT name FROM students ORDER BY name;
SELECT name, dob FROM students ORDER BY dob DESC;
SELECT name, class FROM students ORDER BY class, name;

-- 4. Pattern matching: % = any number of characters, _ = exactly one
SELECT name FROM students WHERE name LIKE 'T%';
SELECT name FROM students WHERE name LIKE '%Lee';
SELECT name FROM students WHERE name LIKE '%an%';
SELECT name FROM students WHERE name LIKE '_a%';

-- 5. IN and BETWEEN
SELECT name FROM students WHERE class IN ('3A', '3C');
SELECT student_id, subject_id, score FROM scores WHERE score BETWEEN 80 AND 89;
SELECT name, dob FROM students WHERE dob BETWEEN '2010-01-01' AND '2010-06-30';

-- 6. DISTINCT and LIMIT
SELECT class FROM students;
SELECT DISTINCT class FROM students;
SELECT name, dob FROM students ORDER BY dob LIMIT 5;

-- 7. NULL
SELECT name, email FROM students;
SELECT name FROM students WHERE email = NULL;         -- returns nothing (the trap)
SELECT name FROM students WHERE email IS NULL;        -- correct
SELECT name FROM students WHERE email IS NOT NULL;

SELECT COUNT(*) FROM scores WHERE score < 50 OR score >= 50;   -- 116, not 120

SELECT student_id, subject_id, score FROM scores ORDER BY score LIMIT 5;   -- NULLs come first!
SELECT student_id, subject_id, score FROM scores
WHERE score IS NOT NULL ORDER BY score LIMIT 5;
