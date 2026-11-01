# Week 3 Challenges

Work in the `sqlite3` shell on `school.db` (from the repository root: `sqlite3 school.db`). Keep your queries in a file called `my-work/week3.sql` so you can re-run them, and write the question number as a comment above each query.

**Database reminder**

```
students(student_id PK, name, class, gender, dob, email)
subjects(subject_id PK, name, teacher)
scores(student_id FK, subject_id FK, score)             PK = (student_id, subject_id)
ccas(cca_id PK, name, category, day)
student_cca(student_id FK, cca_id FK, role)             PK = (student_id, cca_id)
```

---

## Challenge 1: Ten progressive queries ★★

Write one query for each. They start easy and get harder.

1. Show every column of every subject.
2. Show only the name and class of every student.
3. Show the names of students in class `3B`.
4. Show the names of the girls (`'F'`) in class `3C`.
5. List all student names in alphabetical order.
6. List the names and dates of birth of students born in 2010, oldest first.
7. List `student_id`, `subject_id` and `score` for scores of 90 or more, highest first.
8. List the name and class of students in 3A **or** 3C, sorted by class and then by name.
9. Show the five **lowest** scores (`student_id`, `subject_id`, `score`). *Careful: think about the absent students.*
10. List the name, category and day of CCAs that meet on Tuesday or Thursday and are **not** in the `Sports` category.

---

## Challenge 2: From English to SQL ★★★

Translate each question into a single SQL query.

1. Which students in Class 3A have a name that starts with T?
2. Which students have "Tan" anywhere in their name?
3. Which students have **no** email on record?
4. Which students have `a` as the **second** letter of their name? (List names only.)
5. Which subjects are taught by a teacher whose title is exactly "Mr"? (Not "Mrs"!)
6. Which CCAs are in the `Performing Arts` category? List them alphabetically.
7. List each class that exists, once only.
8. Which students were born in the first half of 2010 (January to June)? Show name and date of birth.

---

## Challenge 3: Predict, then run ★★★

This challenge uses a small **pets** table, so you can work out answers on paper.

| pet_id | name | species | age | owner |
|--------|------|---------|-----|-------|
| 1 | Milo | cat | 3 | Ali |
| 2 | Bella | dog | 5 | Ben |
| 3 | Coco | cat | NULL | Ali |
| 4 | Rex | dog | 7 | NULL |
| 5 | Nemo | fish | 1 | Cara |
| 6 | Luna | cat | 5 | Ben |
| 7 | Max | dog | 2 | Cara |
| 8 | Pip | bird | NULL | NULL |

**Step 1 (no computer):** for each query, write down exactly what you think the output will be, including the order of rows.

```sql
-- A
SELECT name FROM pets WHERE species = 'cat';

-- B
SELECT name, age FROM pets WHERE age > 4 ORDER BY age DESC, name;

-- C
SELECT DISTINCT owner FROM pets ORDER BY owner;

-- D
SELECT name FROM pets WHERE age = NULL;

-- E
SELECT name FROM pets WHERE NOT species = 'dog' AND age IS NOT NULL;

-- F
SELECT name FROM pets
WHERE species IN ('cat', 'bird') OR age BETWEEN 5 AND 7
ORDER BY name
LIMIT 3;

-- G
SELECT name FROM pets WHERE owner != 'Ali';
```

**Step 2:** create the table and run the queries to check yourself. From the repository root:

```bash
mkdir -p my-work
sqlite3 my-work/pets.db
```

then, inside the sqlite3 shell:

```sql
.read week-03-select/challenges/pets.sql
```

and paste the queries in one at a time.

**Step 3:** for every query where your prediction was wrong, write one sentence explaining what you misunderstood.

---

## Challenge 4 (open-ended): Ask your own questions ★★★★

Look through the `school.db` tables with `SELECT * ...` and write **five new questions** about the data that you find interesting. Then answer each one with an SQL query.

**Requirements**

- Between them, your five queries must use at least: `WHERE` with `AND` or `OR`, `ORDER BY`, `LIKE`, `IN` or `BETWEEN`, and `DISTINCT` or `LIMIT`.
- At least one query must deal with `NULL` correctly.
- Write each question in English as a comment above its query.
- Swap with a partner. Run their queries. Does each query really answer the question they wrote?

**Self-assessment**

| Criterion | Yes / No |
|-----------|----------|
| Five different, clearly worded questions | |
| Required clauses all used | |
| NULL handled with `IS NULL` / `IS NOT NULL` | |
| Partner confirmed that the queries answer the questions | |
