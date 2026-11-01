# SQL Checkpoint Quiz: Answers and Mark Scheme

**Total: 20 marks.** Queries are marked on whether they would return the right rows. Accept any valid equivalent, ignore capitalisation and layout, and allow one minor syntax slip (a missing semicolon, for example) per question without penalty.

---

## Section A: Queries (11 marks)

### Q1 [2 marks]

```sql
SELECT name, class
FROM students
WHERE name LIKE 'T%'
ORDER BY name;
```

- 1 mark: correct `WHERE ... LIKE 'T%'`.
- 1 mark: correct columns and `ORDER BY name`.

Expected output: Tabitha Lim (3A), Tan Ming Yang (3C), Tan Wei Jie (3A), Tay Jun Hao (3B), Thaddeus Ong (3A), Tiffany Goh (3A).

### Q2 [3 marks]

```sql
SELECT su.name, ROUND(AVG(sc.score), 1) AS average
FROM subjects AS su
JOIN scores AS sc ON sc.subject_id = su.subject_id
GROUP BY su.subject_id, su.name
HAVING AVG(sc.score) > 66
ORDER BY average DESC;
```

- 1 mark: correct join on `subject_id`.
- 1 mark: `GROUP BY` with `AVG` and `ROUND`.
- 1 mark: `HAVING` (not `WHERE`) for the condition, and `ORDER BY` descending.

Expected output: Chemistry 71.1, Physics 70.1, General Paper 66.5.

*Do not award the `HAVING` mark if the answer uses `WHERE AVG(...)`.*

### Q3 [3 marks]

```sql
SELECT st.name
FROM students AS st
LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;
```

Equally valid: `WHERE student_id NOT IN (SELECT student_id FROM student_cca)` or `NOT EXISTS`.

- 1 mark: a method that keeps students without a match (`LEFT JOIN`, `NOT IN` or `NOT EXISTS`).
- 1 mark: the test for "no match" (`IS NULL` on the right-hand key, or the subquery).
- 1 mark: the correct column (`name`) and a fully correct query.

*An `INNER JOIN` answer scores 0 for the first two marks.* Expected output: 8 students (Muhammad Irfan, Chloe Tay, Ethan Koh, Deepa Krishnan, Lau Zi Xuan, Daniel Chua, Kavya Reddy, Jasmine Ho).

### Q4 [3 marks]

```
supplier  n  total
--------  -  -----
Acme      2  350
NULL      1  100
Zed       1  NULL
```

- 1 mark: the rows kept by `WHERE`: bolt, nut, screw (qty is NULL), nail. The washer (40) is excluded.
- 1 mark: the groups and values: Acme `2, 350`; Zed `1, NULL` (`SUM` ignores NULLs, and with only NULLs it returns NULL); and the NULL supplier is its own group `1, 100`.
- 1 mark: the correct order: `n DESC` puts Acme first; the two rows with `n = 1` are ordered by supplier, and NULL sorts before `Zed`.

---

## Section B: Database design (5 marks)

### Q5 [3 marks]

(a) **1NF** [1]. Accept "first normal form".

(b) It is not in 2NF because of **partial dependencies**: `student_name` depends on only `student_id`, and `subject_name` and `teacher` depend on only `subject_id`, which are each only part of the composite key `(student_id, subject_id)`. [1]

(c) [1]
```
STUDENT(student_id PK, student_name)
SUBJECT(subject_id PK, subject_name, teacher)
RESULT(student_id PK FK, subject_id PK FK, score)
```
Award the mark for three correct tables with correct keys. Do not penalise the choice of table names.

### Q6 [2 marks]

A **foreign key** is a column (or columns) in one table whose values must match the primary key of a row in another table, linking the two tables. [1]
With foreign keys on, the database **rejects** the insert and reports an error (`FOREIGN KEY constraint failed`), so no "orphan" row is stored. [1]

---

## Section C: SQL in code (4 marks)

### Q7 [2 marks]

```sql
CREATE TABLE pet (
    pet_id      INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    birth_year  INTEGER CHECK (birth_year BETWEEN 2000 AND 2030),
    owner_id    INTEGER,
    FOREIGN KEY (owner_id) REFERENCES owner (owner_id)
);
```

- 1 mark: `PRIMARY KEY` and `NOT NULL` correct.
- 1 mark: the `CHECK` with the range **and** the `FOREIGN KEY ... REFERENCES owner (owner_id)`.

### Q8 [2 marks]

(a) `' OR '1'='1` [1 mark for any working value, with an explanation]. The resulting SQL is `... WHERE class = '' OR '1'='1'`. The first quote ends the string early, and `'1'='1'` is always true, so every row is returned. (Also accept `' OR 1=1 --`.)

(b) [1]
```python
def students_in(con, class_name):
    return con.execute("SELECT name FROM students WHERE class = ?", (class_name,)).fetchall()
```
Do not award the mark if the tuple comma is missing: `(class_name)` is not a tuple.

---

## Grade boundaries (suggested)

| Marks | Comment |
|-------|---------|
| 17-20 | Secure. Ready for Flask |
| 13-16 | Mostly secure. Review the weak section |
| 9-12 | Review joins, grouping, normalisation or injection before Week 9 |
| 0-8 | Offer a catch-up session before the Flask block uses SQL heavily |

*Feedback tip:* hand back the quiz with the section totals. If many students lose marks in Q3 (the `LEFT JOIN`), or Q8, revisit it for five minutes in Week 7 before the demo.
