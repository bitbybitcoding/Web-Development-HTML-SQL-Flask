"""Week 6, Challenge 3: the four functions, fixed with ? placeholders, plus the attacks that used to work.

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/Answers/challenge_3_fixed.py
"""
import sqlite3


def setup():
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


# ----------------------------- FIXED VERSIONS -----------------------------

def login(con, username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    return con.execute(query, (username, password)).fetchone() is not None


def find_student(con, name):
    # The wildcards % belong to the VALUE, so they go inside the parameter, not in the SQL text.
    query = "SELECT name, class, email FROM students WHERE name LIKE ?"
    return con.execute(query, (f"%{name}%",)).fetchall()


def update_email(con, student_id, email):
    cur = con.execute("UPDATE students SET email = ? WHERE student_id = ?", (email, student_id))
    con.commit()
    return cur.rowcount


def delete_student(con, student_id):
    cur = con.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    con.commit()
    return cur.rowcount


# -------------------- Part C: the attacks now fail, normal use works --------------------

def run_checks():
    # --- login ---
    con = setup()
    assert login(con, "admin", "S3cret!") is True                  # normal use
    assert login(con, "admin", "wrong") is False
    assert login(con, "admin", "' OR '1'='1") is False             # attack 1: always-true condition
    assert login(con, "admin' --", "anything") is False            # attack 2: comment out the password check

    # --- find_student ---
    con = setup()
    assert find_student(con, "Ben") == [("Ben Tan", "3B", "ben@example.com")]    # normal use
    assert find_student(con, "' OR 1=1 --") == []                                # attack: dump every student
    assert find_student(con, "zzz' UNION SELECT username, password, role FROM users --") == []   # attack: steal other tables

    # --- update_email ---
    con = setup()
    assert update_email(con, 1, "new@example.com") == 1                          # normal use
    assert update_email(con, "1 OR 1=1", "hacked@example.com") == 0              # attack: change everybody
    emails = [r[0] for r in con.execute("SELECT email FROM students ORDER BY student_id")]
    assert emails == ["new@example.com", "ben@example.com", "cara@example.com"]

    # --- delete_student ---
    con = setup()
    assert delete_student(con, "1 OR 1=1") == 0                                  # attack: delete everybody
    assert con.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 3
    assert delete_student(con, 2) == 1                                           # normal use
    assert con.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 2

    print("All checks passed: every attack now fails and normal use still works.")


if __name__ == "__main__":
    run_checks()
