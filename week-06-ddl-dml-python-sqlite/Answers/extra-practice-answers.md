# Week 6 Extra Practice: Answers

## 1. Refactor the library app into a class

```python
class Library:
    def __init__(self, path="my-work/library.db"):
        self.con = get_connection(path)

    def add_book(self, title, author):
        title, author = title.strip(), author.strip()
        if not title or not author:
            raise ValueError("Title and author are required.")
        try:
            cur = self.con.execute("INSERT INTO book (title, author) VALUES (?, ?)", (title, author))
        except sqlite3.IntegrityError:
            raise ValueError("That book is already in the library.")
        self.con.commit()
        return cur.lastrowid

    # ... the other methods are the same as the functions, with con replaced by self.con ...

    def close(self):
        self.con.close()
```

- **Better:** the connection is stored once, so methods need fewer parameters; the data and the functions that work on it are kept together; it is easy to swap in a test database with `Library(":memory:")`.
- **Worse:** more code for a small program; harder to share a single connection between different parts of a larger program. (In Flask, Week 9, we will manage the connection per request, which is yet another design.)

## 2. Transactions and rollback

Full working code: [extra_bank_transfer.py](extra_bank_transfer.py).

1. The total is **150** before and **120** afterwards. The first `UPDATE` took 30 from Aisha. The second `UPDATE ... WHERE id = 99` matches **no rows**, which is not an error in SQL, so it silently did nothing. Then `commit()` saved the half-finished transfer: 30 disappeared.
2. ```python
   def transfer(con, from_id, to_id, amount):
       with con:                    # commit at the end, or roll back if an exception is raised
           cur = con.execute("UPDATE account SET balance = balance - ? WHERE id = ?", (amount, from_id))
           if cur.rowcount != 1:
               raise ValueError("No such source account.")
           cur = con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (amount, to_id))
           if cur.rowcount != 1:
               raise ValueError("No such destination account.")
   ```
3. `transfer(con, 1, 99, 30)` raises `ValueError` and the total stays 150 (the first `UPDATE` is undone). `transfer(con, 1, 2, 40)` leaves Aisha with 60 and Ben with 90. `transfer(con, 1, 2, 500)` raises `sqlite3.IntegrityError` because the `CHECK (balance >= 0)` rule fails, and again nothing changes.
4. `commit()` makes all the changes since the transaction began permanent. A **rollback** throws them all away and returns the database to how it was at the start of the transaction. Together they make a group of changes **atomic**: all or nothing.

## 3. Using `with` for connections

1. When the block finishes normally, the changes are **committed**. If an exception is raised inside the block, the changes are **rolled back** and the exception continues to propagate.
2. **No.** `with sqlite3.connect(...) as con:` only manages the *transaction*. The connection stays open and `con` is still usable after the block. To close it as well, use `contextlib.closing`:
   ```python
   from contextlib import closing
   with closing(sqlite3.connect("my-work/library.db")) as con:
       with con:                       # transaction
           con.execute(...)
   ```
3. ```python
   def add_book(con, title, author):
       title, author = title.strip(), author.strip()
       if not title or not author:
           raise ValueError("Title and author are required.")
       try:
           with con:
               cur = con.execute("INSERT INTO book (title, author) VALUES (?, ?)", (title, author))
       except sqlite3.IntegrityError:
           raise ValueError("That book is already in the library.")
       return cur.lastrowid
   ```

## 4. DDL and DML drills

1. `ALTER TABLE students ADD COLUMN house TEXT DEFAULT 'Unassigned';` Existing rows get the default: all 30 show `Unassigned`.
2. ```sql
   UPDATE students SET house = 'Red'   WHERE class = '3A';
   UPDATE students SET house = 'Blue'  WHERE class = '3B';
   UPDATE students SET house = 'Green' WHERE class = '3C';
   SELECT class, house, COUNT(*) FROM students GROUP BY class, house;   -- 10 in each
   ```
3. ```sql
   INSERT INTO ccas (cca_id, name, category, day) VALUES (9, 'Coding Club', 'Clubs & Societies', 'Monday');
   INSERT INTO student_cca (student_id, cca_id, role) VALUES (1, 9, 'Member'), (2, 9, 'Member'), (3, 9, 'Member');
   ```
4. `FOREIGN KEY constraint failed`. Student 1 has rows in `scores` (and possibly in `student_cca`) that refer to it. Deleting the student would leave **orphan rows**. First delete the student's rows from `student_cca` and `scores`, then the student.
5. Delete the **child** rows first, then the parent:
   ```sql
   DELETE FROM student_cca WHERE cca_id = (SELECT cca_id FROM ccas WHERE name = 'Debate Society');
   DELETE FROM ccas WHERE name = 'Debate Society';
   ```
   Deleting the CCA first fails with `FOREIGN KEY constraint failed`, because `student_cca` rows still refer to it.
6. `CHECK constraint failed: score BETWEEN 0 AND 100`. The row is not changed.

## 5. Exam-style written questions

1. **DDL** (Data Definition Language) defines and changes the *structure* of the database: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`. **DML** (Data Manipulation Language) works with the *data* inside the tables: `INSERT`, `UPDATE`, `DELETE` (and `SELECT`).
2. `PRIMARY KEY`: uniquely identifies each row (never NULL). `NOT NULL`: a value must be given. `UNIQUE`: no two rows may have the same value in that column (or combination). `CHECK`: a condition that must be true for every row. `DEFAULT`: the value used when none is supplied. `FOREIGN KEY`: the value must match an existing primary key in another table.
3. The query is built by inserting the user's text directly into the SQL string, so the user's input can change the *structure* of the SQL. For example, a name of `' OR '1'='1` makes the condition always true, returning every user; `x' --` comments out the rest of the query. Fixed:
   ```python
   con.execute("SELECT * FROM users WHERE name = ?", (name,))
   ```
4. Any two: the database separates the command from the data, so there is no way for the data to become part of the command; escaping rules are easy to get wrong, and attackers find the cases you missed; placeholders also handle quotes in genuine data (for example the name `O'Brien`) correctly; the code is shorter and easier to read.
5. It makes SQLite **enforce** foreign key constraints for that connection. If you forget, SQLite accepts rows whose foreign key refers to a row that does not exist, and lets you delete a parent row that is still referred to, so the data can become inconsistent without any error.
6. It deletes **every** row in the table. Two habits: write the `WHERE` clause first (or run the same condition as a `SELECT` first and check the rows); and use transactions or work on a copy/backup, so a mistake can be rolled back or recovered.
