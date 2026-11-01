-- Week 5, Challenge 3: the school uniform shop in 3NF.
-- Copy this file to my-work/uniform.sql, fill in every TODO, then:
--     sqlite3 my-work/uniform.db
--     .read my-work/uniform.sql

PRAGMA foreign_keys = ON;

-- Drop in reverse order of dependency so the file can be re-run
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS classes;

-- ---------------------------------------------------------------
-- 1. Tables (parents first, so a foreign key can point at them)
-- ---------------------------------------------------------------

-- DONE FOR YOU: follow this pattern.
CREATE TABLE classes (
    class          TEXT PRIMARY KEY,
    class_teacher  TEXT NOT NULL
);

-- TODO: student(student_id, student_name, class)       class is a FOREIGN KEY to classes
-- CREATE TABLE student ( ... );

-- TODO: item(item_code, item_name, unit_price)
-- CREATE TABLE item ( ... );

-- TODO: orders(order_no, order_date, student_id)       student_id is a FOREIGN KEY to student
-- CREATE TABLE orders ( ... );

-- TODO: order_item(order_no, item_code, size, qty)     composite PRIMARY KEY, two FOREIGN KEYs
-- CREATE TABLE order_item ( ... );

-- ---------------------------------------------------------------
-- 2. Sample data (parents first again)
-- ---------------------------------------------------------------

INSERT INTO classes VALUES ('3A', 'Mr Lee');
-- TODO: insert class 3B (teacher Mrs Pillai)
-- TODO: insert students S101 Aisha Rahman (3A) and S102 Ben Tan (3B)
-- TODO: insert items U1 PE Shirt 12.00, U2 PE Shorts 10.00, U3 School Tie 6.00
-- TODO: insert orders 501 (2026-01-05, S101), 502 (2026-01-06, S102), 503 (2026-01-08, S101)
-- TODO: insert the six order lines:
--       501: U1 M x2, U2 M x2        502: U1 L x1        503: U3 'One size' x1, U1 S x1

-- ---------------------------------------------------------------
-- 3. Queries
-- ---------------------------------------------------------------

-- TODO (a): rebuild the original order form: one row per order line, showing
--           order_no, order_date, student_name, class, class_teacher, item_name, unit_price, size, qty

-- TODO (b): total amount spent by each student (unit_price * qty, summed)

-- ---------------------------------------------------------------
-- 4. Test the design (this statement SHOULD fail with a FOREIGN KEY error)
-- ---------------------------------------------------------------
-- INSERT INTO orders VALUES (504, '2026-01-10', 'S999');
