# Week 9 Extra Practice: Answers

## 1. Sorting by column heading, safely

Code: [extra_practice.py](extra_practice.py) (`SORTABLE` and `students()`).

`f"ORDER BY {sort}"` puts text from the URL straight into the SQL, so a visitor can add anything: `?sort=(SELECT password FROM users)` or `?sort=1; DROP TABLE students`. A `?` cannot protect it, because a placeholder is always a **value**, never a column or table name. The fix is a whitelist: `SORTABLE = {"name": "s.name", "class": "s.class", ...}`; the user's text only chooses a **key**, and the SQL contains our own constant text. Anything not in the dictionary falls back to the default. The direction is also checked: `"DESC" if request.args.get("order") == "desc" else "ASC"`.

## 2. Pagination

Code: [extra_practice.py](extra_practice.py). `total = SELECT COUNT(*)`, `pages = ceil(total / PER_PAGE)`, `OFFSET = (page - 1) * PER_PAGE`. Convert the page with `int()` inside a `try/except ValueError`, then clamp it with `max(1, ...)` and `min(page, pages)`. Always include a stable `ORDER BY`, otherwise rows may repeat or vanish between pages.

## 3. Stop duplicate emails

```python
try:
    with db:
        db.execute("INSERT INTO students (...) VALUES (...)", values)
except sqlite3.IntegrityError:
    errors["email"] = "That email is already used."
else:
    flash("Added."); return redirect(...)
```

(In the edit route the same pattern surrounds the `UPDATE`.) The `try` surrounds the `with` block so that the rollback has happened before the message is shown.

Several `NULL` emails are allowed because in SQL `NULL` means "unknown", and two unknowns are not known to be equal (`NULL = NULL` is not true), so a unique index does not treat them as duplicates. That is the same NULL rule from Week 3.

## 4. Class summary page

```sql
-- summary per class
SELECT s.class, COUNT(DISTINCT s.student_id) AS students, ROUND(AVG(sc.score), 1) AS average,
       MAX(sc.score) AS highest, MIN(sc.score) AS lowest
FROM students AS s LEFT JOIN scores AS sc ON sc.student_id = s.student_id
GROUP BY s.class ORDER BY s.class;
```

| class | students | average | highest | lowest |
|-------|----------|---------|---------|--------|
| 3A | 10 | 64.2 | 96 | 30 |
| 3B | 10 | 71.1 | 98 | 36 |
| 3C | 10 | 66.7 | 98 | 41 |

`COUNT(*)` would count a row per score (about 50), so we count `DISTINCT s.student_id`.

Top student, option A: a second query per class (simplest, and fine for three classes):

```sql
SELECT s.name, ROUND(AVG(sc.score), 1) AS average
FROM students AS s JOIN scores AS sc ON sc.student_id = s.student_id
WHERE s.class = ? GROUP BY s.student_id ORDER BY average DESC, s.name LIMIT 1;
```

Result: 3A Tiffany Goh (79.0), 3B Siti Nurhaliza (79.8), 3C Ng Shu Min (77.0).

Option B: one query with a correlated subquery:

```sql
SELECT s.class, s.name, ROUND(AVG(sc.score), 1) AS average
FROM students AS s JOIN scores AS sc ON sc.student_id = s.student_id
GROUP BY s.student_id
HAVING AVG(sc.score) = (SELECT MAX(a) FROM (SELECT AVG(sc2.score) AS a
                                             FROM students AS s2 JOIN scores AS sc2 ON sc2.student_id = s2.student_id
                                             WHERE s2.class = s.class GROUP BY s2.student_id))
ORDER BY s.class;
```

Compare the **unrounded** `AVG(...)` in `HAVING`. Comparing the rounded alias to the unrounded maximum loses the 3B winner (79.8 vs 79.83...). A tie would return two students per class, which is usually what you want.

## 5. A soft delete

```sql
ALTER TABLE students ADD COLUMN archived INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0, 1));
UPDATE students SET archived = 1 WHERE student_id = ?;   -- archive
UPDATE students SET archived = 0 WHERE student_id = ?;   -- restore
```

Every list, search, report and `COUNT` that should ignore archived students needs `WHERE archived = 0` (in joins, put it in the `ON` or the `WHERE` carefully).

Real systems prefer it because: data can be restored after a mistake; history (scores, past records) stays consistent; there are no foreign-key problems; and records may have to be kept for legal reasons. The bug: forgetting the `WHERE archived = 0` in just one query makes "deleted" people reappear in that report (and possibly show private information). Also, unique constraints still apply to archived rows (an archived student's email stays "used").

## 6. Written questions

1. [4, one mark each] Create: `INSERT`, `POST`. Read: `SELECT`, `GET`. Update: `UPDATE`, `POST` (HTML forms only support GET and POST; `PUT`/`PATCH` are used by JavaScript clients and APIs). Delete: `DELETE`, `POST` (same reason; never GET).
2. A web server handles many requests, possibly at the same time. A connection shared by all would be used by several requests at once, mixing up transactions and risking errors (SQLite connections in Python are tied to a thread by default). [1] A connection per request is created when needed, used by that request only, and closed at the end, so nothing is left open and requests do not interfere. [1]
3. The flaw is **SQL injection**. [1] The value is placed into the SQL text, so a user who sends `1 OR 1=1` makes the statement `DELETE FROM students WHERE student_id = 1 OR 1=1`, which deletes every student. [1] Fix: `db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))`. [1]
4. `PRAGMA foreign_keys = ON` makes the database check that each `scores.student_id` matches an existing student. Deleting the student would leave scores that refer to a student who does not exist (orphan rows), so SQLite raises `IntegrityError: FOREIGN KEY constraint failed`. [2] It is good because it stops the data becoming inconsistent. [1] Two fixes: delete the student's scores first (child rows), then the student, in one transaction; or define the foreign key with `ON DELETE CASCADE`; or refuse to delete a student who has scores; or archive instead (any two). [1]
5. `with db:` starts a transaction and **commits** it when the block finishes, or **rolls back** all of its changes if an exception is raised inside the block. [1] With `db.commit()` at the end, an error in the middle leaves the earlier statements applied but not committed, and a forgotten or skipped commit loses data; `with` handles both cases in one line, so it is safer. [1]
6. `NULL` means "no value / unknown", so it can be tested with `IS NULL`, is ignored by aggregate functions such as `COUNT(email)`, and does not clash with a `UNIQUE` constraint. An empty string is an actual value that looks like data, breaks `UNIQUE` (two empty emails are equal), and is counted by `COUNT(email)`. [2]
7. Any two [1 each]: the record with that id exists (otherwise 404); the user is logged in and allowed to delete it; the request is a POST (not GET); the record has no related rows (or they are deleted first); a CSRF token is valid; optionally the user confirmed the action.
