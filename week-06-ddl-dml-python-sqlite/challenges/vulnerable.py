"""Week 6, Challenge 3: four functions that are vulnerable to SQL injection.

Do NOT use these as examples of good code!
Copy this file to my-work/fixed.py, attack each function, then fix it.
Run it from the repository root:   python3 my-work/fixed.py
"""
import sqlite3


def setup():
    """A throw-away database in memory, so you cannot hurt anything real."""
    con = sqlite3.connect(":memory:")
    con.executescript("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        );
        INSERT INTO users VALUES ('admin', 'S3cret!', 'teacher');
        INSERT INTO users VALUES ('aisha', 'hunter2', 'student');

        CREATE TABLE students (
            student_id INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            class      TEXT NOT NULL,
            email      TEXT
        );
        INSERT INTO students VALUES (1, 'Aisha Rahman', '3A', 'aisha@example.com');
        INSERT INTO students VALUES (2, 'Ben Tan',      '3B', 'ben@example.com');
        INSERT INTO students VALUES (3, 'Cara Lim',     '3A', 'cara@example.com');
    """)
    return con


def login(con, username, password):
    """Return True if the username and password match a user."""
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return con.execute(query).fetchone() is not None


def find_student(con, name):
    """Return (name, class, email) for every student whose name contains the text."""
    query = "SELECT name, class, email FROM students WHERE name LIKE '%" + name + "%'"
    return con.execute(query).fetchall()


def update_email(con, student_id, email):
    """Change one student's email address. Returns the number of rows changed."""
    query = "UPDATE students SET email = '%s' WHERE student_id = %s" % (email, student_id)
    cur = con.execute(query)
    con.commit()
    return cur.rowcount


def delete_student(con, student_id):
    """Delete one student. Returns the number of rows deleted."""
    cur = con.execute(f"DELETE FROM students WHERE student_id = {student_id}")
    con.commit()
    return cur.rowcount


if __name__ == "__main__":
    con = setup()
    print(login(con, "admin", "S3cret!"))          # True   (normal use)
    print(find_student(con, "Ben"))                # [('Ben Tan', '3B', 'ben@example.com')]
    # TODO Part A: add your attacks here and print the results.
    # TODO Part C: add assert statements once you have fixed the functions.
