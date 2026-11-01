-- Small practice table for Week 3, Challenge 3.
-- From the repository root:   sqlite3 my-work/pets.db
-- then inside the sqlite3 shell:   .read week-03-select/challenges/pets.sql

DROP TABLE IF EXISTS pets;

CREATE TABLE pets (
    pet_id  INTEGER PRIMARY KEY,
    name    TEXT,
    species TEXT,
    age     INTEGER,
    owner   TEXT
);

INSERT INTO pets VALUES (1, 'Milo',  'cat',  3,    'Ali');
INSERT INTO pets VALUES (2, 'Bella', 'dog',  5,    'Ben');
INSERT INTO pets VALUES (3, 'Coco',  'cat',  NULL, 'Ali');
INSERT INTO pets VALUES (4, 'Rex',   'dog',  7,    NULL);
INSERT INTO pets VALUES (5, 'Nemo',  'fish', 1,    'Cara');
INSERT INTO pets VALUES (6, 'Luna',  'cat',  5,    'Ben');
INSERT INTO pets VALUES (7, 'Max',   'dog',  2,    'Cara');
INSERT INTO pets VALUES (8, 'Pip',   'bird', NULL, NULL);

.headers on
.mode column
.nullvalue NULL
SELECT * FROM pets;
