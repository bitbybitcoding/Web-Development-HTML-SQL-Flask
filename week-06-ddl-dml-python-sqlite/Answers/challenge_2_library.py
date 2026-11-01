"""Week 6, Challenge 2: a command-line library app backed by SQLite (solution).

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/Answers/challenge_2_library.py
"""
import os
import sqlite3
from datetime import date, timedelta

DB_FILE = "my-work/library.db"
LOAN_DAYS = 14

SCHEMA = """
CREATE TABLE IF NOT EXISTS book (
    book_id  INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    author   TEXT NOT NULL,
    UNIQUE (title, author)
);

CREATE TABLE IF NOT EXISTS loan (
    loan_id      INTEGER PRIMARY KEY,
    book_id      INTEGER NOT NULL,
    borrower     TEXT NOT NULL,
    borrowed_on  TEXT NOT NULL,          -- YYYY-MM-DD
    due_on       TEXT NOT NULL,          -- YYYY-MM-DD
    returned_on  TEXT,                   -- NULL = still on loan
    FOREIGN KEY (book_id) REFERENCES book (book_id)
);
"""

MENU = """
=== Library ===
1. Add a book
2. Search books
3. Borrow a book
4. Return a book
5. List all books
0. Quit
"""


def get_connection(path=DB_FILE):
    """Open the database, create the tables if needed, and turn foreign keys on."""
    if path != ":memory:":
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    return con


def add_book(con, title, author):
    """Add a book and return its new book_id."""
    title, author = title.strip(), author.strip()
    if not title or not author:
        raise ValueError("Title and author are required.")
    try:
        cur = con.execute("INSERT INTO book (title, author) VALUES (?, ?)", (title, author))
    except sqlite3.IntegrityError:
        raise ValueError("That book is already in the library.")
    con.commit()
    return cur.lastrowid


def search_books(con, term):
    """Books whose title or author contains the term (LIKE is case-insensitive for English letters)."""
    pattern = f"%{term.strip()}%"
    return con.execute(
        """
        SELECT b.book_id, b.title, b.author,
               NOT EXISTS (SELECT 1 FROM loan AS l
                           WHERE l.book_id = b.book_id AND l.returned_on IS NULL) AS available
        FROM book AS b
        WHERE b.title LIKE ? OR b.author LIKE ?
        ORDER BY b.title
        """,
        (pattern, pattern),
    ).fetchall()


def list_books(con):
    """Every book. An empty search term matches everything."""
    return search_books(con, "")


def borrow_book(con, book_id, borrower, today=None):
    """Record a loan for LOAN_DAYS days and return the due date as text."""
    today = today or date.today()
    borrower = borrower.strip()
    if not borrower:
        raise ValueError("Borrower name is required.")
    if con.execute("SELECT 1 FROM book WHERE book_id = ?", (book_id,)).fetchone() is None:
        raise ValueError("There is no book with that id.")
    if con.execute("SELECT 1 FROM loan WHERE book_id = ? AND returned_on IS NULL", (book_id,)).fetchone():
        raise ValueError("That book is already on loan.")
    due = today + timedelta(days=LOAN_DAYS)
    con.execute(
        "INSERT INTO loan (book_id, borrower, borrowed_on, due_on) VALUES (?, ?, ?, ?)",
        (book_id, borrower, today.isoformat(), due.isoformat()),
    )
    con.commit()
    return due.isoformat()


def return_book(con, book_id, today=None):
    """Mark the open loan for this book as returned."""
    today = today or date.today()
    cur = con.execute(
        "UPDATE loan SET returned_on = ? WHERE book_id = ? AND returned_on IS NULL",
        (today.isoformat(), book_id),
    )
    if cur.rowcount == 0:
        raise ValueError("That book is not on loan.")
    con.commit()


def show_books(rows):
    if not rows:
        print("No books found.")
        return
    for row in rows:
        status = "available" if row["available"] else "ON LOAN"
        print(f"  [{row['book_id']}] {row['title']} by {row['author']}  ({status})")


def main():
    con = get_connection()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                new_id = add_book(con, input("Title: "), input("Author: "))
                print(f"Added book {new_id}.")
            elif choice == "2":
                show_books(search_books(con, input("Search for: ")))
            elif choice == "3":
                due = borrow_book(con, int(input("Book id: ")), input("Borrower name: "))
                print(f"Borrowed. Due back on {due}.")
            elif choice == "4":
                return_book(con, int(input("Book id: ")))
                print("Returned. Thank you!")
            elif choice == "5":
                show_books(list_books(con))
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please choose 0 to 5.")
        except ValueError as error:
            print("Sorry:", error)
    con.close()


if __name__ == "__main__":
    main()
