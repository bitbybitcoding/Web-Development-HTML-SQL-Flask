# Week 5 Extra Practice

For fast finishers, and homework for everyone else.

---

## 1. Spot the anomalies

For each flawed table:

- State the **primary key**.
- Write the **functional dependencies**.
- Say which is the **highest normal form** the table meets (1NF, 2NF or 3NF), and **why it fails the next one**.
- Give **one example** each of an update, insert and delete anomaly.
- Rewrite it in 3NF.

**Table A: library loans**

| loan_id | member_id | member_name | member_address | book_id | title | author | loan_date |
|---------|-----------|-------------|----------------|---------|-------|--------|-----------|
| 1 | M1 | Aisha | 12 Elm Rd | B1 | Dune | F. Herbert | 2026-02-01 |
| 2 | M1 | Aisha | 12 Elm Rd | B2 | Emma | J. Austen | 2026-02-08 |
| 3 | M2 | Ben | 5 Oak Ave | B1 | Dune | F. Herbert | 2026-02-09 |

Assume each loan is for one book.

**Table B: class results**

Primary key `(student_id, subject_id)`.

| student_id | subject_id | student_name | subject_name | score |
|------------|------------|--------------|--------------|------:|
| 1 | 1 | Tan Wei Jie | Mathematics | 72 |
| 1 | 2 | Tan Wei Jie | Computing | 80 |
| 2 | 1 | Tabitha Lim | Mathematics | 91 |

**Table C: staff**

Primary key `staff_id`.

| staff_id | staff_name | dept_code | dept_name | dept_head |
|----------|------------|-----------|-----------|-----------|
| T1 | Mr Lee | MATH | Mathematics | Dr Wong |
| T2 | Ms Rahman | COMP | Computing | Mr Sim |
| T3 | Mrs Goh | MATH | Mathematics | Dr Wong |

## 2. Exam-style design questions

**Question 1.** A clinic stores its appointments in one table:

`APPOINTMENT(appointment_id, appt_date, appt_time, patient_id, patient_name, patient_phone, doctor_id, doctor_name, doctor_room)`

(a) State the primary key. (b) List the functional dependencies. (c) Explain why the table is not in 3NF. (d) Write the 3NF tables, marking primary and foreign keys. (e) Draw the ER diagram.

**Question 2.** A tuition centre records tutors, students and classes. A tutor teaches many classes. Each class has exactly one tutor and many students. A student can attend many classes. For each class session, the centre records which students attended.

(a) Identify every entity. (b) Identify each relationship and its type. (c) Identify any relationship that needs a junction table, and name the junction table and its attributes. (d) Draw the ER diagram.

**Question 3.** Short answers:

(a) State the difference between 2NF and 3NF.
(b) Define the terms *foreign key* and *referential integrity*.
(c) A student says: "Normalisation makes a database slower, so we should not do it." Give one reason the student is partly right and one reason normalisation is still worth doing.

## 3. Reverse-engineer `school.db`

Open `school.db` and look at `.schema`.

1. Draw the ER diagram of the school database (5 tables).
2. For each relationship, state the type and say which table holds the foreign key.
3. Which tables are junction tables? Why is `scores` one, even though it has a non-key attribute (`score`)?
4. Is `school.db` in 3NF? Justify your answer table by table. (Hint: is `class` in `students` a 3NF problem? What would you need to know about classes?)

## 4. Peer review an ER diagram

Swap diagrams from Challenge 1 or Challenge 4 with a partner. Use this checklist and write one positive comment and one suggestion.

| Check | OK? |
|-------|-----|
| Every entity has a primary key | |
| Every relationship line has a cardinality marker at **both** ends | |
| There are no many-to-many lines left (all resolved with junction tables) | |
| Every foreign key is on the "many" side | |
| Attributes describing a relationship (for example `join_date`) are in the junction table | |
| Names are singular, consistent and meaningful | |
| Nothing in a table depends on a non-key column | |
