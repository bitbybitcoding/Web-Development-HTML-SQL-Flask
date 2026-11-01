-- Week 9, Challenge 4: starter database for the library web app.
-- Same tables as Week 6. If you finished your Week 6 library.db you may use that instead.
-- Load it with:   sqlite3 library.db ".read library_seed.sql"      (or let your app run it, see the answer)
PRAGMA foreign_keys = ON;

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

INSERT OR IGNORE INTO book (book_id, title, author) VALUES
    (1,  'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling'),
    (2,  'The Hobbit',                                 'J.R.R. Tolkien'),
    (3,  'Charlotte''s Web',                           'E.B. White'),
    (4,  'Matilda',                                    'Roald Dahl'),
    (5,  'The Little Prince',                          'Antoine de Saint-Exupery'),
    (6,  'Wonder',                                     'R.J. Palacio'),
    (7,  'Holes',                                      'Louis Sachar'),
    (8,  'A Wrinkle in Time',                          'Madeleine L''Engle'),
    (9,  'The Giver',                                  'Lois Lowry'),
    (10, 'Hatchet',                                    'Gary Paulsen'),
    (11, 'Percy Jackson: The Lightning Thief',         'Rick Riordan'),
    (12, 'Diary of a Wimpy Kid',                       'Jeff Kinney');

-- Dates are relative to "today", so there is always something overdue when you start.
INSERT OR IGNORE INTO loan (loan_id, book_id, borrower, borrowed_on, due_on, returned_on) VALUES
    (1, 1, 'Mei Lin',  date('now', '-40 days'), date('now', '-26 days'), date('now', '-30 days')),
    (2, 1, 'Arjun',    date('now', '-20 days'), date('now', '-6 days'),  NULL),
    (3, 2, 'Zoe',      date('now', '-3 days'),  date('now', '+11 days'), NULL),
    (4, 4, 'Arjun',    date('now', '-60 days'), date('now', '-46 days'), date('now', '-50 days')),
    (5, 4, 'Mei Lin',  date('now', '-35 days'), date('now', '-21 days'), date('now', '-25 days')),
    (6, 7, 'Daniel',   date('now', '-1 days'),  date('now', '+13 days'), NULL),
    (7, 9, 'Zoe',      date('now', '-18 days'), date('now', '-4 days'),  date('now', '-5 days')),
    (8, 12,'Mei Lin',  date('now', '-8 days'),  date('now', '+6 days'),  NULL);
