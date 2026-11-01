"""Week 6 demo: a live SQL injection attack, and the fix.

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/demo/injection_demo.py
Everything here uses a throw-away database in memory, so nothing real can be harmed.
"""
import sqlite3


def make_db():
    con = sqlite3.connect(":memory:")
    con.executescript("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        );
        INSERT INTO users VALUES ('admin', 'S3cret!', 'teacher');
        INSERT INTO users VALUES ('aisha', 'hunter2', 'student');
    """)
    return con


# ---------------------------------------------------------------------------
# The UNSAFE version: builds the SQL by pasting the user's text into a string
# ---------------------------------------------------------------------------
def login_unsafe(con, username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("   SQL sent to the database:", query)
    return con.execute(query).fetchone() is not None


# ---------------------------------------------------------------------------
# The SAFE version: the SQL is fixed; the values travel separately through ? placeholders
# ---------------------------------------------------------------------------
def login_safe(con, username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    return con.execute(query, (username, password)).fetchone() is not None


def show(label, ok):
    print(f"   -> {label}: {'LOGGED IN' if ok else 'rejected'}\n")


if __name__ == "__main__":
    con = make_db()

    print("1. Normal use of the unsafe function")
    show("admin / S3cret!", login_unsafe(con, "admin", "S3cret!"))
    show("admin / wrong", login_unsafe(con, "admin", "wrong"))

    print("2. ATTACK: the password is   ' OR '1'='1")
    print("   The quote closes the string early, and OR '1'='1' is always true.")
    show("admin / ' OR '1'='1", login_unsafe(con, "admin", "' OR '1'='1"))

    print("3. ATTACK: the username is   admin' --")
    print("   '--' starts a comment, so the password check disappears completely.")
    show("admin' -- / (anything)", login_unsafe(con, "admin' --", "anything"))

    print("4. Can the attacker run a second statement, such as DROP TABLE?")
    try:
        login_unsafe(con, "x'; DROP TABLE users; --", "x")
    except (sqlite3.ProgrammingError, sqlite3.Warning) as error:   # the class depends on the Python version
        print("   Python's sqlite3 refuses to run two statements in one execute():", error)
    print("   (Good, but do not rely on this. Other databases and other functions such as")
    print("   executescript() DO run several statements. Always use placeholders.)\n")

    print("5. The SAFE version, with the same attacks")
    show("admin / ' OR '1'='1", login_safe(con, "admin", "' OR '1'='1"))
    show("admin' -- / anything", login_safe(con, "admin' --", "anything"))
    show("admin / S3cret!  (real login still works)", login_safe(con, "admin", "S3cret!"))

    print("Why it works: with ? placeholders the database treats the input purely as DATA,")
    print("never as part of the SQL command, so quotes and -- have no special meaning.")
