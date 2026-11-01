"""Week 6, Challenge 4: reports for the library app (sample solution).

The report functions take the connection, return rows, and never print.
Run from the repository root to print all three reports for your real library:
    python3 week-06-ddl-dml-python-sqlite/Answers/challenge_4_reports.py
"""
from datetime import date

from challenge_2_library import get_connection


def overdue_books(con, today=None):
    """Loans not yet returned whose due date is before today, most overdue first."""
    today = (today or date.today()).isoformat()
    return con.execute(
        """
        SELECT b.title, l.borrower, l.due_on,
               CAST(julianday(?) - julianday(l.due_on) AS INTEGER) AS days_overdue
        FROM loan AS l
        JOIN book AS b ON b.book_id = l.book_id
        WHERE l.returned_on IS NULL AND l.due_on < ?
        ORDER BY days_overdue DESC, b.title
        """,
        (today, today),
    ).fetchall()


def most_borrowed(con, limit=3):
    """The books borrowed most often."""
    return con.execute(
        """
        SELECT b.title, COUNT(*) AS times_borrowed
        FROM loan AS l
        JOIN book AS b ON b.book_id = l.book_id
        GROUP BY b.book_id, b.title
        ORDER BY times_borrowed DESC, b.title
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def borrower_history(con, borrower):
    """Every book a borrower has had, newest first (name match ignores case)."""
    return con.execute(
        """
        SELECT b.title, l.borrowed_on, l.returned_on
        FROM loan AS l
        JOIN book AS b ON b.book_id = l.book_id
        WHERE l.borrower = ? COLLATE NOCASE
        ORDER BY l.borrowed_on DESC
        """,
        (borrower.strip(),),
    ).fetchall()


def print_report(title, rows, columns):
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("Nothing to report.")
        return
    print("  ".join(f"{c:<22}" for c in columns))
    for row in rows:
        print("  ".join(f"{str(v) if v is not None else '-':<22}" for v in tuple(row)))


if __name__ == "__main__":
    con = get_connection()
    print_report("Overdue books", overdue_books(con), ["Title", "Borrower", "Due", "Days overdue"])
    print_report("Most borrowed", most_borrowed(con), ["Title", "Times borrowed"])
    con.close()
