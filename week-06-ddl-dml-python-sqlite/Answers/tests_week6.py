"""Instructor self-check for the Week 6 answer files.

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/Answers/tests_week6.py
It confirms that the sample solutions work, and that the Challenge 3 starter really IS vulnerable.
"""
import os
import sys
import sqlite3
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "challenges"))

import challenge_2_library as lib            # noqa: E402
import challenge_4_reports as rep            # noqa: E402
import challenge_3_fixed as fixed            # noqa: E402
import vulnerable                            # noqa: E402  (the starter file students receive)
import extra_bank_transfer as bank           # noqa: E402


def raises(exc, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc as error:
        return str(error)
    raise AssertionError(f"{func.__name__} did not raise {exc.__name__}")


def test_library():
    con = lib.get_connection(":memory:")
    dune = lib.add_book(con, "Dune", "Frank Herbert")
    emma = lib.add_book(con, "  Emma ", "Jane Austen")
    assert dune == 1 and emma == 2
    assert raises(ValueError, lib.add_book, con, "Dune", "Frank Herbert") == "That book is already in the library."
    assert raises(ValueError, lib.add_book, con, "  ", "Nobody") == "Title and author are required."

    assert [r["title"] for r in lib.search_books(con, "dUNe")] == ["Dune"]          # case-insensitive
    assert [r["title"] for r in lib.search_books(con, "austen")] == ["Emma"]        # by author
    assert len(lib.list_books(con)) == 2
    assert all(r["available"] == 1 for r in lib.list_books(con))

    due = lib.borrow_book(con, dune, "Ben", today=date(2026, 3, 1))
    assert due == "2026-03-15"
    assert lib.search_books(con, "Dune")[0]["available"] == 0
    assert raises(ValueError, lib.borrow_book, con, dune, "Cara") == "That book is already on loan."
    assert raises(ValueError, lib.borrow_book, con, 99, "Cara") == "There is no book with that id."
    assert raises(ValueError, lib.borrow_book, con, emma, "  ") == "Borrower name is required."

    lib.return_book(con, dune, today=date(2026, 3, 10))
    assert lib.search_books(con, "Dune")[0]["available"] == 1
    assert raises(ValueError, lib.return_book, con, dune) == "That book is not on loan."

    # a search term with a quote must not break anything (placeholders!)
    assert lib.search_books(con, "'; DROP TABLE book; --") == []
    assert len(lib.list_books(con)) == 2


def test_reports():
    con = lib.get_connection(":memory:")
    for title, author in [("Dune", "F. Herbert"), ("Emma", "J. Austen"), ("Ulysses", "J. Joyce")]:
        lib.add_book(con, title, author)
    lib.borrow_book(con, 1, "Ben", today=date(2026, 3, 1));  lib.return_book(con, 1, today=date(2026, 3, 5))
    lib.borrow_book(con, 1, "Cara", today=date(2026, 3, 6))                 # on loan, due 2026-03-20
    lib.borrow_book(con, 2, "Ben", today=date(2026, 3, 8))                  # on loan, due 2026-03-22
    lib.borrow_book(con, 3, "Ben", today=date(2026, 3, 9)); lib.return_book(con, 3, today=date(2026, 3, 11))

    overdue = rep.overdue_books(con, today=date(2026, 3, 25))
    assert [(r["title"], r["days_overdue"]) for r in overdue] == [("Dune", 5), ("Emma", 3)]
    assert rep.overdue_books(con, today=date(2026, 3, 15)) == []            # nothing overdue yet
    assert rep.overdue_books(con, today=date(2026, 3, 21))[0]["title"] == "Dune"

    top = rep.most_borrowed(con, limit=2)
    assert [(r["title"], r["times_borrowed"]) for r in top] == [("Dune", 2), ("Emma", 1)]

    history = rep.borrower_history(con, "ben")                               # name match ignores case
    assert [r["title"] for r in history] == ["Ulysses", "Emma", "Dune"]


def test_injection_starter_is_vulnerable():
    """The attacks MUST work against the starter file, or the challenge makes no sense."""
    con = vulnerable.setup()
    assert vulnerable.login(con, "admin", "' OR '1'='1") is True
    assert vulnerable.login(con, "admin' --", "x") is True
    con = vulnerable.setup()
    assert len(vulnerable.find_student(con, "' OR 1=1 --")) == 3
    stolen = vulnerable.find_student(con, "zzz' UNION SELECT username, password, role FROM users --")
    assert ("admin", "S3cret!", "teacher") in stolen
    con = vulnerable.setup()
    assert vulnerable.update_email(con, "1 OR 1=1", "x@example.com") == 3          # everybody changed
    con = vulnerable.setup()
    assert vulnerable.delete_student(con, "1 OR 1=1") == 3                         # everybody deleted
    con = vulnerable.setup()
    assert vulnerable.update_email(con, 1, "x', class='HACKED") == 1               # extra column changed
    assert con.execute("SELECT class FROM students WHERE student_id = 1").fetchone()[0] == "HACKED"


def test_fixed():
    fixed.run_checks()


def test_bank():
    con = bank.make_db()
    bank.transfer_buggy(con, 1, 99, 30)
    assert bank.total(con) == 120                                                  # 30 vanished
    con = bank.make_db()
    assert raises(ValueError, bank.transfer, con, 1, 99, 30) == "No such destination account."
    assert bank.total(con) == 150                                                  # rolled back
    bank.transfer(con, 1, 2, 40)
    assert dict(con.execute("SELECT owner, balance FROM account")) == {"Aisha": 60, "Ben": 90}
    assert "CHECK constraint failed" in raises(sqlite3.IntegrityError, bank.transfer, con, 1, 2, 500)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"\nAll {len(tests)} test groups passed.")
