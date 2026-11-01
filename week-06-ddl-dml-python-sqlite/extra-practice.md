# Week 6 Extra Practice

For fast finishers, and homework for everyone else. Revise for the **checkpoint quiz** at the start of Week 7: [checkpoint-quiz.md](checkpoint-quiz.md) shows the format (try it as a practice paper, with a timer, after you have finished this page).

---

## 1. Refactor the library app into a class

Rewrite your library app as a class:

```python
class Library:
    def __init__(self, path="my-work/library.db"):
        ...                      # open the connection, store it in self.con

    def add_book(self, title, author): ...
    def search_books(self, term): ...
    def borrow_book(self, book_id, borrower, today=None): ...
    def return_book(self, book_id, today=None): ...
    def list_books(self): ...
    def close(self): ...
```

The menu loop then creates one `Library()` object and calls methods on it. What is better about this design than passing `con` to every function? What is worse?

## 2. Transactions and rollback

A **transaction** is a group of changes that must either **all** happen or **none** happen.

Run this code:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
    CREATE TABLE account (
        id      INTEGER PRIMARY KEY,
        owner   TEXT NOT NULL,
        balance REAL NOT NULL CHECK (balance >= 0)
    );
    INSERT INTO account VALUES (1, 'Aisha', 100);
    INSERT INTO account VALUES (2, 'Ben',    50);
""")

def transfer(con, from_id, to_id, amount):
    con.execute("UPDATE account SET balance = balance - ? WHERE id = ?", (amount, from_id))
    con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (amount, to_id))
    con.commit()

transfer(con, 1, 99, 30)       # account 99 does not exist!
print(con.execute("SELECT SUM(balance) FROM account").fetchone())
```

**Tasks**

1. Run it. What is the total before and after? Explain what went wrong.
2. Fix `transfer` so that the two `UPDATE`s form **one transaction** that is rolled back if the destination account does not exist. (Hint: `with con:` and `cursor.rowcount`.)
3. Check that your fix works, that a normal transfer still works, and that trying to transfer more money than the account holds is refused.
4. Explain in your own words what `commit()` and a rollback do.

## 3. Using `with` for connections

```python
with sqlite3.connect("my-work/library.db") as con:
    con.execute("INSERT INTO book (title, author) VALUES (?, ?)", ("Emma", "Jane Austen"))
```

1. What does the `with` block do when it finishes normally? What if an exception is raised inside it?
2. **Trap:** does `with sqlite3.connect(...) as con:` close the connection at the end? Test it: try to use `con` after the block. (Look up `contextlib.closing`.)
3. Rewrite `add_book` and `borrow_book` from your library app so each uses `with con:` instead of calling `con.commit()` by hand.

## 4. DDL and DML drills on a copy of `school.db`

First make a copy so the original stays untouched:

```bash
cp school.db my-work/school_copy.db
sqlite3 my-work/school_copy.db
```

Remember `PRAGMA foreign_keys = ON;`.

1. Add a column `house TEXT DEFAULT 'Unassigned'` to `students`. What value do the existing rows have?
2. Set `house` to `'Red'` for class 3A, `'Blue'` for 3B and `'Green'` for 3C. Check with a `GROUP BY` query.
3. Add a new CCA, `Coding Club` (Monday, `Clubs & Societies`), and make three students members with the role `Member`.
4. Try to `DELETE FROM students WHERE student_id = 1;`. What happens, and why? What would you have to delete first?
5. Delete the `Debate Society` CCA completely. In what **order** must you delete rows from the two tables, and why?
6. Try `UPDATE scores SET score = 150 WHERE student_id = 1 AND subject_id = 1;`. What happens?

## 5. Exam-style written questions

1. Explain the difference between **DDL** and **DML**, with one example statement of each.
2. State what each constraint does: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, `FOREIGN KEY`.
3. A programmer builds a query with `f"SELECT * FROM users WHERE name = '{name}'"`. Describe **what is wrong** and **how an attacker could exploit it**, then show the corrected code.
4. State two reasons why placeholders (`?`) are better than escaping or removing quote characters yourself.
5. What does `PRAGMA foreign_keys = ON;` do, and what happens in SQLite if you forget to run it?
6. Explain why `DELETE FROM student;` is dangerous, and describe two habits that reduce the risk.
