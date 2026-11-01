-- Week 6, Challenge 1: test data and the statements that MUST be rejected.
--     sqlite3 my-work/canteen.db
--     .read week-06-ddl-dml-python-sqlite/Answers/challenge-1-canteen.sql
--     .read week-06-ddl-dml-python-sqlite/Answers/challenge-1-canteen-tests.sql

PRAGMA foreign_keys = ON;

-- ===== Valid rows =====
INSERT INTO stall (name, opens_at, is_halal) VALUES ('Chicken Rice', '07:00', 1);
INSERT INTO stall (name) VALUES ('Noodles');          -- uses BOTH defaults (07:30 and 0)
INSERT INTO dish (stall_id, name, price, calories) VALUES (1, 'Roasted chicken rice', 3.50, 607);
INSERT INTO dish (stall_id, name, price, calories) VALUES (1, 'Steamed chicken rice', 3.50, 580);
INSERT INTO dish (stall_id, name, price, calories) VALUES (2, 'Wanton mee', 3.50, NULL);   -- calories unknown
INSERT INTO dish (stall_id, name, price, calories) VALUES (2, 'Fishball noodles', 3.20, 420);

SELECT * FROM stall;
SELECT * FROM dish;

-- ===== Rows that must be REJECTED =====
-- Uncomment ONE line at a time and run it. The message after '=>' is what SQLite prints.

-- Rule: stall.name is required
-- INSERT INTO stall (name) VALUES (NULL);
--   => Runtime error: NOT NULL constraint failed: stall.name

-- Rule: stall names must be unique
-- INSERT INTO stall (name) VALUES ('Noodles');
--   => Runtime error: UNIQUE constraint failed: stall.name

-- Rule: is_halal must be 0 or 1
-- INSERT INTO stall (name, is_halal) VALUES ('Drinks', 2);
--   => Runtime error: CHECK constraint failed: chk_halal

-- Rule: price must be greater than 0 (zero)
-- INSERT INTO dish (stall_id, name, price) VALUES (1, 'Free lunch', 0);
--   => Runtime error: CHECK constraint failed: chk_price

-- Rule: price must be greater than 0 (negative)
-- INSERT INTO dish (stall_id, name, price) VALUES (1, 'Mystery', -1.5);
--   => Runtime error: CHECK constraint failed: chk_price

-- Rule: calories must not be negative
-- INSERT INTO dish (stall_id, name, price, calories) VALUES (1, 'Anti-food', 2.00, -5);
--   => Runtime error: CHECK constraint failed: chk_calories

-- Rule: the stall must exist
-- INSERT INTO dish (stall_id, name, price) VALUES (99, 'Ghost dish', 2.00);
--   => Runtime error: FOREIGN KEY constraint failed

-- Rule: stall_id is required
-- INSERT INTO dish (stall_id, name, price) VALUES (NULL, 'Orphan', 2.00);
--   => Runtime error: NOT NULL constraint failed: dish.stall_id

-- Rule: dish name must be unique within a stall
-- INSERT INTO dish (stall_id, name, price) VALUES (1, 'Roasted chicken rice', 4.00);
--   => Runtime error: UNIQUE constraint failed: dish.stall_id, dish.name

-- Rule: dish.name is required
-- INSERT INTO dish (stall_id, name, price) VALUES (1, NULL, 2.00);
--   => Runtime error: NOT NULL constraint failed: dish.name

-- A dish name that already exists at a DIFFERENT stall is allowed (the UNIQUE rule is per stall):
INSERT INTO dish (stall_id, name, price) VALUES (2, 'Roasted chicken rice', 4.00);
