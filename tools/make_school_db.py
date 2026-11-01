"""Builds the starter school.db used from Week 3 onwards.

Run from the repository root:   python3 tools/make_school_db.py
It is deterministic (fixed random seed), so everyone gets identical data.

Tables
------
students    30 students in classes 3A, 3B, 3C (some have no email -> NULL)
subjects    5 subjects
scores      one row per student per subject taken (a few scores are NULL = absent)
ccas        8 co-curricular activities (Chess Club has no members on purpose)
student_cca junction table: which student is in which CCA (some students are in none)
"""
import os
import random
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "school.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE students (
    student_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    class       TEXT NOT NULL,
    gender      TEXT NOT NULL CHECK (gender IN ('M', 'F')),
    dob         TEXT NOT NULL,           -- YYYY-MM-DD
    email       TEXT                     -- NULL if not provided
);

CREATE TABLE subjects (
    subject_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    teacher     TEXT NOT NULL
);

CREATE TABLE scores (
    student_id  INTEGER NOT NULL,
    subject_id  INTEGER NOT NULL,
    score       INTEGER CHECK (score BETWEEN 0 AND 100),   -- NULL = absent for the exam
    PRIMARY KEY (student_id, subject_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
);

CREATE TABLE ccas (
    cca_id      INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    category    TEXT NOT NULL,
    day         TEXT NOT NULL
);

CREATE TABLE student_cca (
    student_id  INTEGER NOT NULL,
    cca_id      INTEGER NOT NULL,
    role        TEXT NOT NULL DEFAULT 'Member',
    PRIMARY KEY (student_id, cca_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (cca_id) REFERENCES ccas (cca_id)
);
"""

# (name, class, gender)
STUDENTS = [
    ("Tan Wei Jie", "3A", "M"), ("Tabitha Lim", "3A", "F"), ("Thaddeus Ong", "3A", "M"),
    ("Priya Nair", "3A", "F"), ("Muhammad Irfan", "3A", "M"), ("Tiffany Goh", "3A", "F"),
    ("Chloe Tay", "3A", "F"), ("Arjun Menon", "3A", "M"), ("Nur Aisyah", "3A", "F"),
    ("Samuel Teo", "3A", "M"),
    ("Lim Jia Hui", "3B", "F"), ("Rahul Sharma", "3B", "M"), ("Wong Kai Xin", "3B", "F"),
    ("Siti Nurhaliza", "3B", "F"), ("Ethan Koh", "3B", "M"), ("Zhang Yi Ming", "3B", "M"),
    ("Deepa Krishnan", "3B", "F"), ("Aaron Lee", "3B", "M"), ("Farah Hassan", "3B", "F"),
    ("Tay Jun Hao", "3B", "M"),
    ("Ng Shu Min", "3C", "F"), ("Harpreet Singh", "3C", "M"), ("Lau Zi Xuan", "3C", "F"),
    ("Ibrahim Yusof", "3C", "M"), ("Ong Mei Ling", "3C", "F"), ("Daniel Chua", "3C", "M"),
    ("Kavya Reddy", "3C", "F"), ("Tan Ming Yang", "3C", "M"), ("Nurul Huda", "3C", "F"),
    ("Jasmine Ho", "3C", "F"),
]

NO_EMAIL = {4, 9, 17, 22, 28}   # student_ids whose email is NULL

SUBJECTS = [
    (1, "Mathematics", "Mr Lee"),
    (2, "Computing", "Ms Rahman"),
    (3, "Physics", "Dr Chen"),
    (4, "Chemistry", "Mrs Pillai"),
    (5, "General Paper", "Mr Fernandez"),
]

CCAS = [
    (1, "Robotics Club", "Clubs & Societies", "Wednesday"),
    (2, "Basketball", "Sports", "Tuesday"),
    (3, "Chinese Orchestra", "Performing Arts", "Thursday"),
    (4, "Debate Society", "Clubs & Societies", "Friday"),
    (5, "Photography Club", "Clubs & Societies", "Monday"),
    (6, "Badminton", "Sports", "Tuesday"),
    (7, "Drama Club", "Performing Arts", "Thursday"),
    (8, "Chess Club", "Clubs & Societies", "Friday"),   # deliberately has no members
]


def build(path: str = DB_PATH) -> None:
    rng = random.Random(2026)
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)

    # students
    for sid, (name, cls, gender) in enumerate(STUDENTS, start=1):
        year = rng.choice([2009, 2010])
        dob = f"{year}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
        email = None if sid in NO_EMAIL else f"s{1000 + sid}@student.school.edu.sg"
        con.execute("INSERT INTO students VALUES (?,?,?,?,?,?)", (sid, name, cls, gender, dob, email))

    con.executemany("INSERT INTO subjects VALUES (?,?,?)", SUBJECTS)
    con.executemany("INSERT INTO ccas VALUES (?,?,?,?)", CCAS)

    # scores: everyone takes Maths (1), General Paper (5) and two of Computing/Physics/Chemistry
    all_scores = []
    for sid in range(1, len(STUDENTS) + 1):
        subjects = [1, 5] + rng.sample([2, 3, 4], 2)
        for subj in sorted(subjects):
            score = max(30, min(98, int(rng.gauss(68, 15))))
            all_scores.append([sid, subj, score])
    for row in rng.sample(all_scores, 4):      # four absentees
        row[2] = None
    con.executemany("INSERT INTO scores VALUES (?,?,?)", all_scores)

    # CCA membership: 22 students join at least one CCA (not Chess Club), 6 of them join a second
    joiners = sorted(rng.sample(range(1, len(STUDENTS) + 1), 22))
    members = {}                                # cca_id -> [student_ids]
    for i, sid in enumerate(joiners):
        cca = (i % 7) + 1                       # guarantees each of CCAs 1-7 has members
        members.setdefault(cca, []).append(sid)
    for sid in rng.sample(joiners, 6):
        first = [c for c, m in members.items() if sid in m][0]
        second = rng.choice([c for c in range(1, 8) if c != first])
        members[second].append(sid)
    for cca, sids in members.items():
        for j, sid in enumerate(sorted(sids)):
            con.execute("INSERT INTO student_cca VALUES (?,?,?)",
                        (sid, cca, "Leader" if j == 0 else "Member"))

    con.commit()
    con.close()
    print(f"Created {path}")


if __name__ == "__main__":
    build()
