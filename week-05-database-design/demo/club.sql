-- Week 5 demo: resolving a many-to-many relationship with a junction table.
-- Run:   sqlite3 my-work/demo.db      then      .read week-05-database-design/demo/club.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS membership;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS club;

CREATE TABLE club (
    club_id  INTEGER PRIMARY KEY,
    name     TEXT NOT NULL
);

CREATE TABLE member (
    member_id INTEGER PRIMARY KEY,
    name      TEXT NOT NULL
);

CREATE TABLE membership (                    -- the junction table
    member_id INTEGER,
    club_id   INTEGER,
    role      TEXT,
    PRIMARY KEY (member_id, club_id),        -- composite primary key
    FOREIGN KEY (member_id) REFERENCES member (member_id),
    FOREIGN KEY (club_id)   REFERENCES club (club_id)
);

INSERT INTO club VALUES (1, 'Robotics');
INSERT INTO club VALUES (2, 'Debate');
INSERT INTO club VALUES (3, 'Chess');

INSERT INTO member VALUES (1, 'Aisha');
INSERT INTO member VALUES (2, 'Ben');
INSERT INTO member VALUES (3, 'Cara');

INSERT INTO membership VALUES (1, 1, 'Leader');
INSERT INTO membership VALUES (1, 2, 'Member');     -- Aisha is in two clubs
INSERT INTO membership VALUES (2, 1, 'Member');     -- Robotics has two members
INSERT INTO membership VALUES (3, 2, 'Leader');

-- Who is in which club?
SELECT m.name AS member, c.name AS club, ms.role
FROM membership AS ms
JOIN member AS m ON m.member_id = ms.member_id
JOIN club AS c ON c.club_id = ms.club_id
ORDER BY m.name, c.name;

-- Chess has no members yet (zero or many)
SELECT c.name
FROM club AS c
LEFT JOIN membership AS ms ON ms.club_id = c.club_id
WHERE ms.club_id IS NULL;
