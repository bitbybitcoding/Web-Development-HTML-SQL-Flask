# SQL Checkpoint Quiz

**Time:** 20 minutes · **Total:** 20 marks · **Counts for:** 15% of the course
**Held:** in the first 20 minutes of Week 7. Students may use `sqlite3` and `school.db` for Section A, but no notes, no cheatsheet and no web searching. (Instructor: set the sqlite3 shell to the repository root; tell students that they may type queries to test them.)

Write your answers on this sheet or in `my-work/checkpoint.sql`.

**The school database**

```
students(student_id PK, name, class, gender, dob, email)
subjects(subject_id PK, name, teacher)
scores(student_id FK, subject_id FK, score)             PK = (student_id, subject_id)
ccas(cca_id PK, name, category, day)
student_cca(student_id FK, cca_id FK, role)             PK = (student_id, cca_id)
```

---

## Section A: Queries (11 marks)

**Q1** [2] Write a query that shows the `name` and `class` of every student whose name starts with the letter T, sorted by name.

**Q2** [3] Write a query that shows each subject's **name** and its **average score** (rounded to 1 decimal place), only for subjects whose average is **above 66**, highest average first.

**Q3** [3] Write a query that shows the names of students who belong to **no** CCA.

**Q4** [3] The table `items` contains:

| id | name | qty | supplier |
|----|------|-----|----------|
| 1 | bolt | 100 | Acme |
| 2 | nut | 250 | Acme |
| 3 | screw | NULL | Zed |
| 4 | washer | 40 | Zed |
| 5 | nail | 100 | NULL |

Write down the exact output of this query, including the order of the rows (write `NULL` where the output is NULL):

```sql
SELECT supplier, COUNT(*) AS n, SUM(qty) AS total
FROM items
WHERE qty >= 100 OR qty IS NULL
GROUP BY supplier
ORDER BY n DESC, supplier;
```

(Remember: SQLite sorts NULL before every other value.)

---

## Section B: Database design (5 marks)

**Q5** [3] A table has the primary key `(student_id, subject_id)`:

`RESULT(student_id, subject_id, student_name, subject_name, teacher, score)`

where `student_id` determines `student_name`, and `subject_id` determines `subject_name` and `teacher`.

(a) State the highest normal form the table is in. [1]
(b) Explain why it is not in the next normal form. [1]
(c) Write the tables in 3NF, underlining or marking primary keys and foreign keys. [1]

**Q6** [2] Explain what a **foreign key** is. State what the database does if you try to insert a row whose foreign key value does not exist in the referenced table (with foreign keys switched on).

---

## Section C: SQL in code (4 marks)

**Q7** [2] Write a `CREATE TABLE` statement for a table `pet` with these columns and rules:

- `pet_id`: primary key
- `name`: text, required
- `birth_year`: integer, must be between 2000 and 2030
- `owner_id`: must refer to `owner_id` in a table called `owner`

**Q8** [2] A Python function contains this code:

```python
def students_in(con, class_name):
    return con.execute(f"SELECT name FROM students WHERE class = '{class_name}'").fetchall()
```

(a) Give a value for `class_name` that makes the function return **every** student, and explain why it works. [1]
(b) Rewrite the function so that it is safe from SQL injection. [1]
