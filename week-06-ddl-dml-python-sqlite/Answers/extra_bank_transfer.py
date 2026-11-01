"""Week 6, Extra practice 2: transactions and rollback.

Run from the repository root:   python3 week-06-ddl-dml-python-sqlite/Answers/extra_bank_transfer.py
"""
import sqlite3


def make_db():
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
    return con


def total(con):
    return con.execute("SELECT SUM(balance) FROM account").fetchone()[0]


# ----------------------------------------------------------------------------
# The BUGGY version: two separate changes, committed together with no safety check
# ----------------------------------------------------------------------------
def transfer_buggy(con, from_id, to_id, amount):
    con.execute("UPDATE account SET balance = balance - ? WHERE id = ?", (amount, from_id))
    con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (amount, to_id))   # id 99 matches NO rows, and raises no error
    con.commit()


# ----------------------------------------------------------------------------
# The FIXED version: one transaction. Either BOTH changes happen, or NEITHER does.
# "with con:" commits if the block finishes normally and rolls back if it raises an exception.
# ----------------------------------------------------------------------------
def transfer(con, from_id, to_id, amount):
    with con:
        cur = con.execute("UPDATE account SET balance = balance - ? WHERE id = ?", (amount, from_id))
        if cur.rowcount != 1:
            raise ValueError("No such source account.")
        cur = con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (amount, to_id))
        if cur.rowcount != 1:
            raise ValueError("No such destination account.")   # this undoes the first UPDATE too


if __name__ == "__main__":
    con = make_db()
    print("Start: total money =", total(con))

    transfer_buggy(con, 1, 99, 30)                      # account 99 does not exist
    print("After the buggy transfer to a missing account: total =", total(con), "  <- 30 has vanished!")

    con = make_db()
    try:
        transfer(con, 1, 99, 30)
    except ValueError as error:
        print("Fixed version raised:", error)
    print("After the fixed transfer: total =", total(con), "  <- nothing lost, the first UPDATE was rolled back")
    print("Aisha's balance:", con.execute("SELECT balance FROM account WHERE id = 1").fetchone()[0])

    transfer(con, 1, 2, 40)                             # a normal transfer works
    print("After a good transfer of 40:", con.execute("SELECT owner, balance FROM account").fetchall())

    try:
        transfer(con, 1, 2, 500)                        # would make Aisha's balance negative
    except sqlite3.IntegrityError as error:
        print("Overdraft refused by the CHECK constraint:", error)
