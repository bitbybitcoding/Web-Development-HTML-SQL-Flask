"""Week 6, Challenge 2: a command-line library app backed by SQLite.

Copy this file to my-work/library.py and complete every TODO.
Run it from the repository root:   python3 my-work/library.py
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
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)   # make sure my-work/ exists
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row              # lets us write row["title"]
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    return con


# ---------------------------------------------------------------------------
# TODO: complete these functions. Use ? placeholders in EVERY query.
# They take the connection as a parameter, and return data or raise ValueError.
# They must NOT call input() or print().
# ---------------------------------------------------------------------------

def add_book(con, title, author):
    """Add a book and return its new book_id.

    Raise ValueError("Title and author are required.") if either is empty (after .strip()).
    Raise ValueError("That book is already in the library.") for a duplicate.
    Hint: catch sqlite3.IntegrityError.  Remember to commit.
    """
    raise NotImplementedError


def search_books(con, term):
    """Return rows (book_id, title, author, available) for books whose title OR author contains term.

    `available` should be 1 if the book has no open loan (returned_on IS NULL), else 0.
    Hint: LIKE ?  with  f"%{term}%"  as the parameter, and NOT EXISTS (SELECT 1 FROM loan ...).
    """
    raise NotImplementedError


def list_books(con):
    """Return every book in the same format as search_books."""
    raise NotImplementedError


def borrow_book(con, book_id, borrower, today=None):
    """Record a loan lasting LOAN_DAYS days and return the due date as text.

    today defaults to date.today(). Raise ValueError for an unknown book,
    an empty borrower name, or a book that is already on loan.
    """
    today = today or date.today()
    raise NotImplementedError


def return_book(con, book_id, today=None):
    """Mark the open loan for this book as returned.

    Raise ValueError("That book is not on loan.") if there is no open loan.
    Hint: UPDATE ... WHERE book_id = ? AND returned_on IS NULL, then check cursor.rowcount.
    """
    today = today or date.today()
    raise NotImplementedError


# ---------------------------------------------------------------------------
# The menu. This part is finished for you.
# ---------------------------------------------------------------------------

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
