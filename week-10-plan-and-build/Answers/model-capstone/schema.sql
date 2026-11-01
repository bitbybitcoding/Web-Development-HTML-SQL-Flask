-- Robotics Club kit loans: three tables.
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS kit;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    category_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE CHECK (length(name) BETWEEN 2 AND 40)
);

CREATE TABLE kit (
    kit_id      INTEGER PRIMARY KEY,
    name        TEXT NOT NULL CHECK (length(name) BETWEEN 2 AND 60),
    category_id INTEGER NOT NULL,
    total_qty   INTEGER NOT NULL CHECK (total_qty BETWEEN 1 AND 500),
    notes       TEXT,
    UNIQUE (name),
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE loan (
    loan_id     INTEGER PRIMARY KEY,
    kit_id      INTEGER NOT NULL,
    borrower    TEXT NOT NULL CHECK (length(borrower) BETWEEN 2 AND 40),
    qty         INTEGER NOT NULL CHECK (qty >= 1),
    borrowed_on TEXT NOT NULL,                 -- YYYY-MM-DD
    due_on      TEXT NOT NULL,                 -- YYYY-MM-DD
    returned_on TEXT,                          -- NULL = still out
    CHECK (due_on >= borrowed_on),
    FOREIGN KEY (kit_id) REFERENCES kit (kit_id)
);
