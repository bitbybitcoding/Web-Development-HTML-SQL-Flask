-- Week 5, Challenge 4: sample design (homework planner), with sample data and queries.
--     sqlite3 my-work/planner.db
--     .read week-05-database-design/Answers/challenge-4-sample.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS task_tag;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS app_user;

CREATE TABLE app_user (
    user_id    INTEGER PRIMARY KEY,
    user_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE
);

CREATE TABLE subject (
    subject_id    INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL,
    subject_name  TEXT NOT NULL,
    colour        TEXT,
    FOREIGN KEY (user_id) REFERENCES app_user (user_id)
);

CREATE TABLE task (
    task_id     INTEGER PRIMARY KEY,
    subject_id  INTEGER NOT NULL,
    title       TEXT NOT NULL,
    due_date    TEXT,
    is_done     INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (subject_id) REFERENCES subject (subject_id)
);

CREATE TABLE tag (
    tag_id    INTEGER PRIMARY KEY,
    tag_name  TEXT NOT NULL UNIQUE
);

CREATE TABLE task_tag (
    task_id  INTEGER,
    tag_id   INTEGER,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES task (task_id),
    FOREIGN KEY (tag_id)  REFERENCES tag (tag_id)
);

INSERT INTO app_user VALUES (1, 'Aisha', 'aisha@example.com');
INSERT INTO app_user VALUES (2, 'Ben',   'ben@example.com');

INSERT INTO subject VALUES (1, 1, 'Mathematics', 'blue');
INSERT INTO subject VALUES (2, 1, 'Computing',   'purple');
INSERT INTO subject VALUES (3, 1, 'Art',         'orange');      -- no tasks yet
INSERT INTO subject VALUES (4, 2, 'Physics',     'green');

INSERT INTO task VALUES (1, 1, 'Tutorial 5 questions',   '2026-11-03', 0);
INSERT INTO task VALUES (2, 1, 'Revise chapter 4',       '2026-11-05', 0);
INSERT INTO task VALUES (3, 2, 'Finish Flask project',   '2026-11-04', 0);
INSERT INTO task VALUES (4, 2, 'Read SQL notes',         '2026-10-28', 1);
INSERT INTO task VALUES (5, 4, 'Lab report',             '2026-11-04', 0);

INSERT INTO tag VALUES (1, 'exam');
INSERT INTO tag VALUES (2, 'group-work');
INSERT INTO tag VALUES (3, 'homework');

INSERT INTO task_tag VALUES (2, 1);      -- Revise chapter 4: exam
INSERT INTO task_tag VALUES (3, 2);      -- Flask project: group-work
INSERT INTO task_tag VALUES (3, 3);      --                homework
INSERT INTO task_tag VALUES (1, 3);      -- Tutorial 5:    homework
INSERT INTO task_tag VALUES (5, 3);      -- Lab report:    homework

-- Q1: tasks of user 1 due between 2026-11-02 and 2026-11-08 that are not done
SELECT t.title, s.subject_name, t.due_date
FROM app_user AS u
JOIN subject AS s ON s.user_id = u.user_id
JOIN task AS t    ON t.subject_id = s.subject_id
WHERE u.user_id = 1
  AND t.due_date BETWEEN '2026-11-02' AND '2026-11-08'
  AND t.is_done = 0
ORDER BY t.due_date;

-- Q2: unfinished tasks per subject, including subjects with none
SELECT s.subject_name, COUNT(t.task_id) AS unfinished
FROM subject AS s
LEFT JOIN task AS t ON t.subject_id = s.subject_id AND t.is_done = 0
GROUP BY s.subject_id, s.subject_name
ORDER BY unfinished DESC, s.subject_name;

-- Q3: tasks with the tag 'exam'
SELECT t.title
FROM task AS t
JOIN task_tag AS tt ON tt.task_id = t.task_id
JOIN tag AS g       ON g.tag_id = tt.tag_id
WHERE g.tag_name = 'exam';
