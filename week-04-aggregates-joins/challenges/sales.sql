-- Small practice table for Week 4, Extra Practice 3 (hand-tracing GROUP BY).
-- From the repository root:   sqlite3 my-work/sales.db
-- then inside the sqlite3 shell:   .read week-04-aggregates-joins/challenges/sales.sql

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id      INTEGER PRIMARY KEY,
    region  TEXT,
    product TEXT,
    amount  INTEGER
);

INSERT INTO sales VALUES (1, 'North', 'pens',  12);
INSERT INTO sales VALUES (2, 'North', 'books', 30);
INSERT INTO sales VALUES (3, 'South', 'pens',   8);
INSERT INTO sales VALUES (4, 'South', 'books', 25);
INSERT INTO sales VALUES (5, 'South', 'books', 40);
INSERT INTO sales VALUES (6, 'East',  'pens',  15);
INSERT INTO sales VALUES (7, 'East',  'pens',  20);
INSERT INTO sales VALUES (8, 'North', 'pens',   5);

.headers on
.mode column
SELECT * FROM sales;
