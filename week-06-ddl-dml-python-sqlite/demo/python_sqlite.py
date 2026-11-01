"""Week 6 demo: using SQLite from Python with the built-in sqlite3 module.

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/demo/python_sqlite.py
Each step prints what it does. In class, type the steps one at a time and run after each.
"""
import sqlite3

# ---------------------------------------------------------------------------
# Step 1: connect. This opens (or creates) a database file. ":memory:" makes a throw-away one.
# ---------------------------------------------------------------------------
con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")      # enforce foreign keys on THIS connection

# ---------------------------------------------------------------------------
# Step 2: execute SQL. A cursor runs statements and holds the results.
# ---------------------------------------------------------------------------
cur = con.cursor()
cur.execute("""
    CREATE TABLE student (
        student_id INTEGER PRIMARY KEY,
        name       TEXT NOT NULL,
        class      TEXT NOT NULL
    )
""")

# ---------------------------------------------------------------------------
# Step 3: insert rows. Use ? placeholders and pass the values as a tuple: NEVER build SQL by pasting strings.
# ---------------------------------------------------------------------------
cur.execute("INSERT INTO student (name, class) VALUES (?, ?)", ("Aisha Rahman", "3A"))
print("New row id:", cur.lastrowid)

rows = [("Ben Tan", "3B"), ("Cara Lim", "3A"), ("Dev Nair", "3C")]
cur.executemany("INSERT INTO student (name, class) VALUES (?, ?)", rows)   # many rows at once

# ---------------------------------------------------------------------------
# Step 4: commit. Changes are only saved permanently once you commit.
# ---------------------------------------------------------------------------
con.commit()

# ---------------------------------------------------------------------------
# Step 5: fetch results.  fetchall() -> list of tuples,  fetchone() -> one tuple or None
# ---------------------------------------------------------------------------
cur.execute("SELECT student_id, name, class FROM student ORDER BY name")
print("\nfetchall():")
for row in cur.fetchall():
    print("  ", row)                      # a tuple: (1, 'Aisha Rahman', '3A')

cur.execute("SELECT COUNT(*) FROM student")
print("\nfetchone():", cur.fetchone())    # (4,)
print("Another fetchone():", cur.fetchone())   # None: nothing is left to fetch

# Looping over the cursor directly also works
print("\nLoop over the cursor:")
for student_id, name, cls in con.execute("SELECT * FROM student WHERE class = ?", ("3A",)):
    print(f"   {student_id}: {name} ({cls})")

# ---------------------------------------------------------------------------
# Step 6: row_factory makes rows behave like dictionaries (columns by name)
# ---------------------------------------------------------------------------
con.row_factory = sqlite3.Row
row = con.execute("SELECT * FROM student WHERE name = ?", ("Ben Tan",)).fetchone()
print("\nBy column name:", row["name"], row["class"])

# ---------------------------------------------------------------------------
# Step 7: update and delete, and how many rows were changed
# ---------------------------------------------------------------------------
cur = con.execute("UPDATE student SET class = ? WHERE name = ?", ("3B", "Dev Nair"))
print("\nRows updated:", cur.rowcount)

cur = con.execute("DELETE FROM student WHERE name = ?", ("Nobody Here",))
print("Rows deleted (should be 0):", cur.rowcount)
con.commit()

# ---------------------------------------------------------------------------
# Step 8: errors. A broken rule raises an exception, which we can catch.
# ---------------------------------------------------------------------------
try:
    con.execute("INSERT INTO student (name, class) VALUES (?, ?)", (None, "3A"))
except sqlite3.IntegrityError as error:
    print("\nCaught:", error)             # NOT NULL constraint failed: student.name

# Step 9: close the connection when you are finished
con.close()
