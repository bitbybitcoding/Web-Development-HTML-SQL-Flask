-- The database design for your project. `flask --app app init-db` runs this file, then seed.sql.
-- Replace the example table with YOUR tables (from your PLAN.md). Keep the habits:
--   * every table has a primary key
--   * constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) enforce your rules
--   * order matters: create parent tables before the tables that refer to them
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    category_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE
);

CREATE TABLE item (
    item_id     INTEGER PRIMARY KEY,
    name        TEXT NOT NULL CHECK (length(name) BETWEEN 2 AND 60),
    category_id INTEGER NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
    notes       TEXT,
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);
