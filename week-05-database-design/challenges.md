# Week 5 Challenges

Draw your diagrams **by hand** on paper or on the iPad. Photograph or export them and save them in `my-work/`. Write your SQL in `my-work/week5.sql`.

---

## Challenge 1: ER diagram for a school club system ★★★

Read this description:

> The school runs many **clubs**. For each club we record its name, the room it meets in, and the day of the week it meets. Every club has exactly one **teacher-in-charge**. We record each teacher's name and email, and one teacher can be in charge of several clubs.
>
> **Students** (name and class) join clubs. A student may join several clubs, and a club has many students. When a student joins a club, we record the **date they joined** and their **role** (Member, Treasurer or Chairperson).
>
> Clubs organise **events** (name, date and venue). Each event is organised by exactly one club, and a club can organise many events. Students can **register** for events, and afterwards we record whether each student attended.

**Tasks**

1. List the **entities**, and for each one list its attributes and choose a **primary key** (invent an id if there is no natural one).
2. List every **relationship** in the description. Say whether each is 1:1, 1:M or M:N.
3. For every M:N relationship, add a **junction table** and decide which attributes belong in it.
4. Draw the final **ER diagram** in crow's foot notation. Mark every PK and FK, and show the cardinality at both ends of each line.
5. For each 1:M relationship, state which table holds the foreign key.

---

## Challenge 2: Normalise an order form ★★★★

The school's uniform shop uses this order form:

| order_no | order_date | student_id | student_name | class | class_teacher | items (item_code, item_name, unit_price, size, qty) |
|----------|------------|------------|--------------|-------|---------------|------|
| 501 | 2026-01-05 | S101 | Aisha Rahman | 3A | Mr Lee | (U1, PE Shirt, 12.00, M, 2), (U2, PE Shorts, 10.00, M, 2) |
| 502 | 2026-01-06 | S102 | Ben Tan | 3B | Mrs Pillai | (U1, PE Shirt, 12.00, L, 1) |
| 503 | 2026-01-08 | S101 | Aisha Rahman | 3A | Mr Lee | (U3, School Tie, 6.00, One size, 1), (U1, PE Shirt, 12.00, S, 1) |

**Tasks.** Show your working for each step.

1. Identify the **repeating group** in the unnormalised form.
2. Write the table in **1NF**. State its primary key.
3. Write down all the **functional dependencies** (what determines what).
4. Convert to **2NF**. Explain which partial dependencies you removed.
5. Convert to **3NF**. Explain which transitive dependency you removed.
6. Write the final tables in the form `TABLE(pk, column, column, fk)`, underlining or marking the primary keys and foreign keys.
7. Give **one example each** of an update, insert and delete anomaly in the **1NF** table that your 3NF design removes.

---

## Challenge 3: Implement the design in SQLite ★★★

Use your 3NF tables from Challenge 2.

1. Copy [challenges/uniform_template.sql](challenges/uniform_template.sql) to `my-work/uniform.sql` and complete the `CREATE TABLE` statements. The first table is done for you. Copy its pattern.
2. Insert the data from the three orders (students, classes, items, orders and order items).
3. Run the file: `sqlite3 my-work/uniform.db` then `.read my-work/uniform.sql`.
4. Write a query that **rebuilds the original order form** by joining all the tables.
5. Write a query that lists, for each student, the total amount spent (`unit_price * qty`, summed).
6. **Test the design.** With `PRAGMA foreign_keys = ON;`, try to insert an order for a student who does not exist. What happens, and why is that good?

---

## Challenge 4 (open-ended): Design a database for your own app idea ★★★★★

**This seeds your capstone project.** Choose an app you would like to build in Flask (a homework tracker, a cca booking system, a recipe book, a bus-arrival favourites list, a small shop, a pet adoption site...).

**Requirements**

- At least **four entities** and at least **one many-to-many** relationship, resolved with a junction table.
- Every table is in **3NF**. For each table, list its functional dependencies, so you can show that it is.
- An **ER diagram** in crow's foot notation.
- A **data dictionary**: one row per column.

  | Table | Column | Type | Key | Notes |
  |-------|--------|------|-----|-------|
  | task | task_id | INTEGER | PK | |
  | task | title | TEXT | | required |
  | task | list_id | INTEGER | FK -> list | |

- Write **three English questions** the app needs to answer (for example "Which tasks are due this week?"). For each one, say which tables you would join.
- Bonus: write the `CREATE TABLE` statements and insert a few rows of sample data.

**Self-assessment (and peer assessment, see Extra practice 4)**

| Criterion | Yes / No |
|-----------|----------|
| 4+ entities, each with a clear primary key | |
| At least one M:N relationship, correctly resolved | |
| Foreign keys are on the "many" side of every 1:M | |
| No repeating groups, partial or transitive dependencies | |
| Data dictionary complete | |
| Three useful questions the design can answer | |
