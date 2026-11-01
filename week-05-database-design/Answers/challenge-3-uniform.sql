-- Week 5, Challenge 3 solution: the school uniform shop in 3NF.
--     sqlite3 my-work/uniform.db
--     .read week-05-database-design/Answers/challenge-3-uniform.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS classes;

-- 1. Tables (parents first)
CREATE TABLE classes (
    class          TEXT PRIMARY KEY,
    class_teacher  TEXT NOT NULL
);

CREATE TABLE student (
    student_id    TEXT PRIMARY KEY,
    student_name  TEXT NOT NULL,
    class         TEXT NOT NULL,
    FOREIGN KEY (class) REFERENCES classes (class)
);

CREATE TABLE item (
    item_code   TEXT PRIMARY KEY,
    item_name   TEXT NOT NULL,
    unit_price  REAL NOT NULL
);

CREATE TABLE orders (
    order_no    INTEGER PRIMARY KEY,
    order_date  TEXT NOT NULL,
    student_id  TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (student_id)
);

CREATE TABLE order_item (
    order_no   INTEGER,
    item_code  TEXT,
    size       TEXT,
    qty        INTEGER NOT NULL,
    PRIMARY KEY (order_no, item_code),
    FOREIGN KEY (order_no)  REFERENCES orders (order_no),
    FOREIGN KEY (item_code) REFERENCES item (item_code)
);

-- 2. Sample data (parents first)
INSERT INTO classes VALUES ('3A', 'Mr Lee');
INSERT INTO classes VALUES ('3B', 'Mrs Pillai');

INSERT INTO student VALUES ('S101', 'Aisha Rahman', '3A');
INSERT INTO student VALUES ('S102', 'Ben Tan', '3B');

INSERT INTO item VALUES ('U1', 'PE Shirt',   12.00);
INSERT INTO item VALUES ('U2', 'PE Shorts',  10.00);
INSERT INTO item VALUES ('U3', 'School Tie',  6.00);

INSERT INTO orders VALUES (501, '2026-01-05', 'S101');
INSERT INTO orders VALUES (502, '2026-01-06', 'S102');
INSERT INTO orders VALUES (503, '2026-01-08', 'S101');

INSERT INTO order_item VALUES (501, 'U1', 'M', 2);
INSERT INTO order_item VALUES (501, 'U2', 'M', 2);
INSERT INTO order_item VALUES (502, 'U1', 'L', 1);
INSERT INTO order_item VALUES (503, 'U3', 'One size', 1);
INSERT INTO order_item VALUES (503, 'U1', 'S', 1);

-- 3(a). Rebuild the original order form
SELECT o.order_no, o.order_date, s.student_name, s.class, c.class_teacher,
       i.item_name, i.unit_price, oi.size, oi.qty
FROM orders AS o
JOIN student AS s     ON s.student_id = o.student_id
JOIN classes AS c     ON c.class = s.class
JOIN order_item AS oi ON oi.order_no = o.order_no
JOIN item AS i        ON i.item_code = oi.item_code
ORDER BY o.order_no, i.item_code;

-- 3(b). Total spent by each student
SELECT s.student_name, SUM(i.unit_price * oi.qty) AS total_spent
FROM student AS s
JOIN orders AS o      ON o.student_id = s.student_id
JOIN order_item AS oi ON oi.order_no = o.order_no
JOIN item AS i        ON i.item_code = oi.item_code
GROUP BY s.student_id, s.student_name
ORDER BY total_spent DESC;

-- 4. Test the design. This statement is EXPECTED to fail:
--    "FOREIGN KEY constraint failed", because student S999 does not exist.
--    The database refuses to store an order that belongs to nobody, so there can be no
--    "orphan" rows. That is referential integrity, and it is why we use foreign keys.
-- INSERT INTO orders VALUES (504, '2026-01-10', 'S999');
