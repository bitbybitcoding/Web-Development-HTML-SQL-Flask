# Week 3 Demo: The relational model and SELECT

**Time:** 45 minutes. Students type along in the terminal.
**Finished script:** [demo/demo.sql](demo/demo.sql)

---

## Part 1: The relational model (10 min)

### Why a database?

A text file or spreadsheet becomes painful when the data grows: duplicated information, no rules, hard to search, hard to share safely. A **relational database** stores data in **tables** that are linked together, and **SQL** (Structured Query Language) is how we ask questions.

### The school database

Draw this on the board. It is the database students will use for the next four weeks.

```
students                       scores                          subjects
+------------+                 +------------+                  +------------+
| student_id | PK  <---------- | student_id | FK               | subject_id | PK
| name       |                 | subject_id | FK ------------> | name       |
| class      |                 | score      |                  | teacher    |
| gender     |                 +------------+                  +------------+
| dob        |                 (PK is student_id + subject_id)
| email      |
+------------+
      ^
      |                        student_cca                       ccas
      |                        +------------+                  +------------+
      +----------------------- | student_id | FK               | cca_id     | PK
                               | cca_id     | FK ------------> | name       |
                               | role       |                  | category   |
                               +------------+                  | day        |
                                                               +------------+
```

### Vocabulary

| Everyday word | Formal (H2) word | Meaning |
|---------------|------------------|---------|
| Table | Relation | A set of rows with the same columns, for one kind of thing (students, subjects) |
| Row | Record, tuple | One item: one student |
| Column | Field, attribute | One property: `name`, `class` |
| Primary key (PK) | | A column (or set of columns) that **uniquely identifies** each row and is never NULL |
| Foreign key (FK) | | A column that holds the primary key of a row in **another** table, linking the two |
| Composite key | | A primary key made of two or more columns, such as `(student_id, subject_id)` in `scores` |
| NULL | | "No value / unknown". Not zero. Not an empty string |

Ask: *Why is `name` a bad primary key for `students`?* (Two students can share a name.) *What does the `scores` table link together?*

### Open the database

```bash
sqlite3 school.db
```

```sql
.tables
.schema students
.headers on
.mode column
```

Lines starting with a dot are **shell commands** for the sqlite3 program, not SQL. SQL statements end with a semicolon. Exit with `.quit`.

---

## Part 2: SELECT (35 min)

### Choosing columns

```sql
SELECT * FROM students;                       -- every column
SELECT name, class FROM students;             -- only these columns
SELECT name AS "Student", class AS "Class"
FROM students;                                -- AS renames a column in the output
```

`SELECT` chooses **columns**, `FROM` says which table. `*` means "all columns". Write the clauses on separate lines once the query gets long.

### Filtering rows with WHERE

```sql
SELECT name FROM students WHERE class = '3A';
SELECT name FROM students WHERE class = '3B' AND gender = 'F';
SELECT name FROM students WHERE class = '3A' OR class = '3B';
SELECT name FROM students WHERE NOT class = '3C';
```

- `WHERE` chooses **rows**. Text goes in single quotes, numbers do not.
- Comparison operators: `=`, `<>` (or `!=`), `<`, `>`, `<=`, `>=`.
- **Precedence trap:** `AND` is evaluated before `OR`. Run both and compare:

```sql
SELECT name, class, gender FROM students
WHERE class = '3A' OR class = '3B' AND gender = 'F';

SELECT name, class, gender FROM students
WHERE (class = '3A' OR class = '3B') AND gender = 'F';
```

The first returns every 3A student (any gender) plus the 3B girls. Always use brackets when mixing `AND` and `OR`.

### Sorting with ORDER BY

```sql
SELECT name FROM students ORDER BY name;                 -- A to Z (ASC is the default)
SELECT name, dob FROM students ORDER BY dob DESC;        -- youngest first
SELECT name, class FROM students ORDER BY class, name;   -- by class, then by name inside each class
```

### Pattern matching with LIKE

```sql
SELECT name FROM students WHERE name LIKE 'T%';      -- starts with T
SELECT name FROM students WHERE name LIKE '%Lee';    -- ends with Lee
SELECT name FROM students WHERE name LIKE '%an%';    -- contains "an"
SELECT name FROM students WHERE name LIKE '_a%';     -- second letter is a
```

`%` means "any number of characters (including none)". `_` means "exactly one character". In SQLite, `LIKE` ignores upper/lower case for English letters.

### IN and BETWEEN

```sql
SELECT name FROM students WHERE class IN ('3A', '3C');
SELECT student_id, subject_id, score FROM scores WHERE score BETWEEN 80 AND 89;
SELECT name, dob FROM students WHERE dob BETWEEN '2010-01-01' AND '2010-06-30';
```

- `IN (...)` is a tidy way to write several `OR`s.
- `BETWEEN a AND b` **includes both ends**.
- Dates are stored as text in `YYYY-MM-DD` form, so they sort and compare correctly as text. That is why the format matters.

### DISTINCT and LIMIT

```sql
SELECT class FROM students;                   -- 30 rows, lots of repeats
SELECT DISTINCT class FROM students;          -- each class once
SELECT name, dob FROM students ORDER BY dob LIMIT 5;     -- the 5 oldest students
```

`LIMIT` only makes sense with `ORDER BY`. Without it, "the first 5" has no defined meaning.

### NULL: "the value is unknown"

Five students have no email. Look at them:

```sql
SELECT name, email FROM students;
```

Now the trap, run it live:

```sql
SELECT name FROM students WHERE email = NULL;        -- returns NOTHING!
SELECT name FROM students WHERE email IS NULL;       -- correct
SELECT name FROM students WHERE email IS NOT NULL;
```

**Why?** NULL means "unknown", and "is unknown equal to unknown?" is itself unknown, not true. A `WHERE` keeps a row only if the condition is **true**. So use `IS NULL` and `IS NOT NULL`.

More NULL behaviour to show:

```sql
-- Four scores are NULL (absent). Which rows does this return?
SELECT COUNT(*) FROM scores WHERE score < 50 OR score >= 50;     -- 116, not 120!

-- In SQLite, NULL sorts FIRST in ascending order. The "lowest" scores are not what you expect:
SELECT student_id, subject_id, score FROM scores ORDER BY score LIMIT 5;
SELECT student_id, subject_id, score FROM scores
WHERE score IS NOT NULL ORDER BY score LIMIT 5;
```

(`COUNT(*)` is next week. For now just say "it counts the rows".)

Finished script: [demo/demo.sql](demo/demo.sql)

---

## Check for understanding

1. What is the difference between `SELECT` and `WHERE`? *(columns versus rows)*
2. Write a query for students whose names end in "Lim". *(`LIKE '%Lim'`)*
3. Why does `WHERE score = NULL` return no rows?
4. Predict: `SELECT DISTINCT class FROM students ORDER BY class DESC;` *(3C, 3B, 3A)*
