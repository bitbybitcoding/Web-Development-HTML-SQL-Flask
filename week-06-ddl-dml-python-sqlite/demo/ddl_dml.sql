-- Week 6 demo: DDL (CREATE / ALTER / DROP) and DML (INSERT / UPDATE / DELETE).
-- From the repository root:   sqlite3 my-work/library.db
-- then inside the shell:      .read week-06-ddl-dml-python-sqlite/demo/ddl_dml.sql

-- SQLite does NOT enforce foreign keys unless you turn them on, once per connection.
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS member;

-- ===== DDL: CREATE TABLE with constraints =====
CREATE TABLE member (
    member_id  INTEGER PRIMARY KEY,                       -- unique row id (auto-numbered)
    name       TEXT NOT NULL,                             -- must have a value
    email      TEXT UNIQUE,                               -- no two members share an email (NULL is allowed)
    joined     TEXT NOT NULL DEFAULT (date('now')),       -- used if no value is given
    CHECK (length(name) >= 2)                             -- a rule every row must obey
);

CREATE TABLE book (
    book_id  INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    author   TEXT NOT NULL,
    year     INTEGER CHECK (year BETWEEN 1400 AND 2100),
    copies   INTEGER NOT NULL DEFAULT 1 CHECK (copies >= 0)
);

CREATE TABLE loan (
    loan_id      INTEGER PRIMARY KEY,
    book_id      INTEGER NOT NULL,
    member_id    INTEGER NOT NULL,
    borrowed_on  TEXT NOT NULL DEFAULT (date('now')),
    returned_on  TEXT,                                    -- NULL means "not returned yet"
    FOREIGN KEY (book_id)   REFERENCES book (book_id),
    FOREIGN KEY (member_id) REFERENCES member (member_id)
);

-- ===== DDL: ALTER TABLE =====
ALTER TABLE book ADD COLUMN isbn TEXT;                    -- add a column
ALTER TABLE book RENAME COLUMN isbn TO isbn13;            -- rename it
ALTER TABLE book DROP COLUMN isbn13;                      -- remove it again

-- ===== DML: INSERT =====
INSERT INTO member (name, email) VALUES ('Aisha Rahman', 'aisha@example.com');   -- joined uses the default
INSERT INTO member (name, email, joined) VALUES
    ('Ben Tan',  'ben@example.com',  '2026-01-15'),
    ('Cara Lim', NULL,               '2026-02-01');       -- several rows at once

INSERT INTO book (title, author, year, copies) VALUES
    ('Dune',                'Frank Herbert',  1965, 2),
    ('Emma',                'Jane Austen',    1815, 1),
    ('The Left Hand of Darkness', 'Ursula K. Le Guin', 1969, 1);

INSERT INTO loan (book_id, member_id, borrowed_on) VALUES (1, 1, '2026-03-01');
INSERT INTO loan (book_id, member_id, borrowed_on, returned_on) VALUES (2, 2, '2026-03-02', '2026-03-09');

SELECT * FROM member;
SELECT * FROM book;
SELECT * FROM loan;

-- ===== DML: UPDATE =====
UPDATE book SET copies = copies + 1 WHERE title = 'Emma';
UPDATE member SET email = 'cara@example.com' WHERE member_id = 3;
UPDATE loan SET returned_on = '2026-03-12' WHERE loan_id = 1;

-- !!! DANGER: an UPDATE or DELETE without WHERE changes EVERY row !!!
-- UPDATE book SET copies = 0;

-- ===== DML: DELETE =====
DELETE FROM loan WHERE loan_id = 2;
SELECT * FROM loan;

-- ===== Constraints in action: each statement below is REJECTED. Try them one at a time. =====
-- INSERT INTO member (name) VALUES (NULL);                             -- NOT NULL constraint failed
-- INSERT INTO member (name, email) VALUES ('Dan', 'aisha@example.com'); -- UNIQUE constraint failed
-- INSERT INTO member (name) VALUES ('X');                              -- CHECK constraint failed
-- INSERT INTO book (title, author, copies) VALUES ('Bad', 'Me', -1);   -- CHECK constraint failed
-- INSERT INTO loan (book_id, member_id) VALUES (99, 1);                -- FOREIGN KEY constraint failed
-- DELETE FROM member WHERE member_id = 1;                              -- FOREIGN KEY constraint failed (loan 1 uses it)

-- ===== DDL: DROP TABLE (deletes the table AND all its data) =====
-- DROP TABLE loan;
