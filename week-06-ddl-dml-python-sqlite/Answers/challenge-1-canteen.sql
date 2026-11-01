-- Week 6, Challenge 1 solution: the canteen database with constraints.
--     sqlite3 my-work/canteen.db
--     .read week-06-ddl-dml-python-sqlite/Answers/challenge-1-canteen.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS dish;
DROP TABLE IF EXISTS stall;

CREATE TABLE stall (
    stall_id  INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,                         -- required, and no duplicate stall names
    opens_at  TEXT NOT NULL DEFAULT '07:30',                -- default when not given
    is_halal  INTEGER NOT NULL DEFAULT 0,                   -- default 0 when not given
    CONSTRAINT chk_halal CHECK (is_halal IN (0, 1))         -- only 0 or 1
);

CREATE TABLE dish (
    dish_id   INTEGER PRIMARY KEY,
    stall_id  INTEGER NOT NULL,                             -- required
    name      TEXT NOT NULL,
    price     REAL NOT NULL,
    calories  INTEGER,                                      -- may be NULL (unknown)
    CONSTRAINT chk_price    CHECK (price > 0),
    CONSTRAINT chk_calories CHECK (calories >= 0),          -- a NULL calories value passes a CHECK
    CONSTRAINT uq_dish_per_stall UNIQUE (stall_id, name),   -- same dish name only once per stall
    FOREIGN KEY (stall_id) REFERENCES stall (stall_id)      -- the stall must exist
);

-- Naming a constraint (CONSTRAINT chk_price ...) makes the error message say which rule failed.
