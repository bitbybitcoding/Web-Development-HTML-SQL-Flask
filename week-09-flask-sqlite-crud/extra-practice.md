# Week 9 Extra Practice

For fast finishers, and homework for everyone else. Next week begins the capstone project, so keep your code from the challenges: you will reuse the patterns.

---

## 1. Sorting by column heading, safely

Make the column headings in the student list clickable (`?sort=name`, `?sort=class`, `?sort=average`, with `&order=desc`).

A column name **cannot** be a `?` placeholder (placeholders are for values only), so many beginners write `f"ORDER BY {sort}"`. Explain why that is an injection risk, and fix it with a **whitelist**: a dictionary of allowed names, falling back to a default.

## 2. Pagination

Show eight students per page with Previous and Next links, using `LIMIT ? OFFSET ?`. Show "Page 2 of 4". Handle a page number that is too large, zero, or not a number (`?page=abc`) without crashing.

## 3. Stop duplicate emails

Two students should never share an email. SQLite cannot add `UNIQUE` to an existing table with `ALTER TABLE`, but a unique index does the same thing:

```sql
CREATE UNIQUE INDEX idx_students_email ON students (email);
```

Run it in your `instance/school.db`. Then change the create and edit routes to catch `sqlite3.IntegrityError` and show "That email is already used." on the form. Several students with a `NULL` email must still be allowed. Why?

## 4. Class summary page

Add `/classes`: for each class, the number of students, the class average, the highest and lowest individual scores, and the name of the top student. Use one query for the first four (`GROUP BY`) and think about how to find the top student (a correlated subquery, or a second query). Use the Answers only after trying.

## 5. A soft delete

Instead of removing a student, add a column `archived INTEGER NOT NULL DEFAULT 0` and an "Archive" button that sets it to 1. Update every query so archived students disappear from lists, and add an "Archived" page with a "Restore" button. Discuss: why do real systems often prefer this to `DELETE`? What new bug can happen if you forget the `WHERE archived = 0` in one query?

## 6. Written questions (exam style)

1. State the SQL statement and the HTTP method normally used for each CRUD operation. [4]
2. Explain why a new database connection is opened for each request in the demo rather than one connection shared for the whole program. [2]
3. The route below contains a security flaw. Identify it, explain how it could be exploited, and rewrite the line.
   ```python
   db.execute(f"DELETE FROM students WHERE student_id = {student_id}")
   ```
   (Assume `student_id` is a string taken from `request.form`.) [3]
4. A table `scores(student_id, subject_id, score)` has foreign keys to `students` and `subjects`. A programmer deletes a student without deleting the student's scores, and the program raises an error. Explain why the error occurs and why it is a good thing. State **two** ways to fix the program. [4]
5. Explain what `with db:` does, and why it is better than calling `db.commit()` at the end of the function. [2]
6. Explain why storing a missing email as `NULL` is better than storing an empty string. [2]
7. A form's "Delete" button sends the POST to `/students/12/delete`. State two checks the server should make before running the `DELETE`. [2]
