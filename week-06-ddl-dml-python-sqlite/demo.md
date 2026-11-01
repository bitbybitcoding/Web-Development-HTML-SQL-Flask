# Week 6 Demo: DDL, DML and Python with SQLite

**Time:** 45 minutes. Students type along.
**Code:** [demo/ddl_dml.sql](demo/ddl_dml.sql), [demo/python_sqlite.py](demo/python_sqlite.py), [demo/injection_demo.py](demo/injection_demo.py)

---

## Part 1: DDL, creating and changing tables (15 min)

**DDL** (Data Definition Language) defines the *structure*: `CREATE`, `ALTER`, `DROP`.
**DML** (Data Manipulation Language) works with the *data*: `INSERT`, `UPDATE`, `DELETE` (and `SELECT`).

Start a fresh database: `sqlite3 my-work/library.db`

### CREATE TABLE with constraints

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE member (
    member_id  INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE,
    joined     TEXT NOT NULL DEFAULT (date('now')),
    CHECK (length(name) >= 2)
);

CREATE TABLE book (
    book_id  INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    author   TEXT NOT NULL,
    year     INTEGER CHECK (year BETWEEN 1400 AND 2100),
    copies   INTEGER NOT NULL DEFAULT 1 CHECK (copies >= 0)
);

CREATE TABLE loan (
    loan_id      INTEGER PRIMARY KEY,
    book_id      INTEGER NOT NULL,
    member_id    INTEGER NOT NULL,
    borrowed_on  TEXT NOT NULL DEFAULT (date('now')),
    returned_on  TEXT,
    FOREIGN KEY (book_id)   REFERENCES book (book_id),
    FOREIGN KEY (member_id) REFERENCES member (member_id)
);
```

| Constraint | Meaning | Fails when |
|------------|---------|------------|
| `PRIMARY KEY` | Uniquely identifies each row. In SQLite, `INTEGER PRIMARY KEY` auto-numbers | duplicate or NULL key |
| `FOREIGN KEY ... REFERENCES` | The value must exist in the other table's key | the parent row does not exist |
| `NOT NULL` | A value is required | NULL is inserted |
| `UNIQUE` | No two rows may have the same value (NULLs are allowed) | a duplicate is inserted |
| `CHECK (condition)` | The condition must be true | the rule is broken |
| `DEFAULT value` | Used when the INSERT gives no value | never fails; fills the gap |

Point out: the **data types** here are `INTEGER`, `TEXT`, `REAL`. SQLite is flexible about types, but we write sensible ones anyway because exams and other databases care.

### Foreign keys are off by default

Show this honestly, because it surprises everyone:

```sql
PRAGMA foreign_keys = OFF;
INSERT INTO loan (book_id, member_id) VALUES (99, 99);   -- accepted! There is no book 99.
DELETE FROM loan;
PRAGMA foreign_keys = ON;
INSERT INTO loan (book_id, member_id) VALUES (99, 99);   -- FOREIGN KEY constraint failed
```

Run `PRAGMA foreign_keys = ON;` at the start of **every** session or connection.

### ALTER and DROP

```sql
ALTER TABLE book ADD COLUMN isbn TEXT;              -- add a column
ALTER TABLE book RENAME COLUMN isbn TO isbn13;      -- rename it
ALTER TABLE book DROP COLUMN isbn13;                -- remove it
-- DROP TABLE loan;                                 -- deletes the table AND all its data. No undo.
```

SQLite's `ALTER` is limited: you can add, rename and drop columns, but you cannot add a constraint to an existing column. In that case, you create a new table and copy the data across.

---

## Part 2: DML, changing the data (10 min)

```sql
-- INSERT: name the columns, so the order does not matter and defaults still work
INSERT INTO member (name, email) VALUES ('Aisha Rahman', 'aisha@example.com');
INSERT INTO member (name, email, joined) VALUES
    ('Ben Tan',  'ben@example.com', '2026-01-15'),
    ('Cara Lim', NULL,              '2026-02-01');

INSERT INTO book (title, author, year, copies) VALUES ('Dune', 'Frank Herbert', 1965, 2);

-- UPDATE: change existing rows
UPDATE book SET copies = copies + 1 WHERE title = 'Dune';

-- DELETE: remove rows
DELETE FROM loan WHERE loan_id = 2;
```

### The most important rule: always use WHERE

Ask the class what `UPDATE book SET copies = 0;` does. (**Every** row is changed.) Same for `DELETE FROM loan;`. A good habit: write the `WHERE` first, or run the matching `SELECT` first and look at the rows that would be affected.

### Make the constraints fire

Run each of these one at a time and read the error message aloud:

```sql
INSERT INTO member (name) VALUES (NULL);                              -- NOT NULL constraint failed
INSERT INTO member (name, email) VALUES ('Dan', 'aisha@example.com'); -- UNIQUE constraint failed
INSERT INTO member (name) VALUES ('X');                               -- CHECK constraint failed
INSERT INTO book (title, author, copies) VALUES ('Bad', 'Me', -1);    -- CHECK constraint failed
INSERT INTO loan (book_id, member_id) VALUES (99, 1);                 -- FOREIGN KEY constraint failed
DELETE FROM member WHERE member_id = 1;                               -- FOREIGN KEY constraint failed
```

The last one is interesting: the database refuses to delete a member who still has a loan, because that would leave an orphaned loan row.

---

## Part 3: Python and sqlite3 (12 min)

Run [demo/python_sqlite.py](demo/python_sqlite.py) in pieces. The steps:

```python
import sqlite3

con = sqlite3.connect("my-work/school_copy.db")     # 1. connect (creates the file if needed)
con.execute("PRAGMA foreign_keys = ON")             #    turn on foreign keys for this connection
cur = con.cursor()                                  # 2. a cursor runs SQL and holds results

cur.execute("INSERT INTO student (name, class) VALUES (?, ?)", ("Aisha Rahman", "3A"))   # 3. execute with ?
con.commit()                                        # 4. commit: save the changes

cur.execute("SELECT student_id, name FROM student ORDER BY name")
rows = cur.fetchall()                               # 5. fetchall -> list of tuples
one  = cur.fetchone()                               #    fetchone -> one tuple, or None

con.close()                                         # 6. close
```

Teaching points:

- **`commit()` matters.** Changes are held in a *transaction*. If the program ends before `commit()`, they are lost. Show this by deleting the commit line and re-running.
- `fetchall()` returns a **list of tuples**. With `con.row_factory = sqlite3.Row`, you can use `row["name"]`.
- **`?` placeholders**: the number of `?` must equal the number of values in the tuple. A single value still needs a tuple: `("3A",)` with the trailing comma.
- `cur.lastrowid` gives the id of the row just inserted; `cur.rowcount` gives how many rows an UPDATE or DELETE changed (so `rowcount == 0` means "nothing matched").
- `executemany` inserts many rows in one call.

---

## Part 4: SQL injection, live (8 min)

Show the **unsafe** function from [demo/injection_demo.py](demo/injection_demo.py). It builds SQL by pasting the user's input into a string:

```python
def login_unsafe(con, username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return con.execute(query).fetchone() is not None
```

**Challenge the class:** *"You know the username is `admin`. Log in without the password."* Give pairs two minutes. Then reveal:

| Input | SQL the database actually receives | Why it works |
|-------|------------------------------------|--------------|
| password = `' OR '1'='1` | `... username = 'admin' AND password = '' OR '1'='1'` | the quote ends the string, then `OR '1'='1'` is always true |
| username = `admin' --` | `... username = 'admin' --' AND password = 'anything'` | `--` starts a comment, so the password test is thrown away |

**The root cause:** the user's input became part of the *program* (the SQL command), not just *data*.

### The fix: parameterised queries

```python
def login_safe(con, username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    return con.execute(query, (username, password)).fetchone() is not None
```

The SQL text is fixed. The values are sent **separately**, so the database treats `' OR '1'='1` as an ordinary (wrong) password. Run the same attacks again: they fail.

Three rules to write on the board:

1. **Never** build SQL with f-strings, `%` formatting or `+`.
2. **Always** use `?` placeholders, even for numbers.
3. Placeholders work for **values** only, not for table or column names.

(Honest footnote: storing passwords as plain text, as in this demo, is also a terrible idea. Real systems store a salted hash. That is outside this course, but worth a mention.)

---

## Check for understanding

1. Which is DDL and which is DML: `CREATE`, `INSERT`, `DROP`, `UPDATE`?
2. What happens if you forget `commit()`?
3. What does `DELETE FROM loan;` do?
4. Why can `LIKE '%' + name + '%'` be dangerous, and how do you write it safely? *(Pass `("%" + name + "%",)` as the parameter to `LIKE ?`.)*
