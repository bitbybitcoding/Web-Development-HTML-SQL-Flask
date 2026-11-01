# Week 4 Challenges

Work in `sqlite3 school.db`. Keep your queries in `my-work/week4.sql`, with a comment above each one.

**Database reminder**

```
students(student_id PK, name, class, gender, dob, email)
subjects(subject_id PK, name, teacher)
scores(student_id FK, subject_id FK, score)             PK = (student_id, subject_id)
ccas(cca_id PK, name, category, day)
student_cca(student_id FK, cca_id FK, role)             PK = (student_id, cca_id)
```

---

## Challenge 1: Report queries ★★

Write one query for each report. Round every average to **1 decimal place**.

1. The number of students in each CCA, showing `cca_id` and the count.
2. The average score for each subject, showing `subject_id` and the average.
3. Repeat (2), but show the **subject name** instead of the id, with the best subject first.
4. Repeat (1), but show the **CCA name**, with the biggest CCA first (break ties alphabetically).
5. The number of students in each class.
6. For each subject (by name), the highest score and the lowest score.
7. Only the subjects whose average score is above 66, with their averages.

---

## Challenge 2: Who is missing? (LEFT JOIN) ★★★

1. List the name and class of every student who belongs to **no** CCA, sorted by class and then name.
2. Write a query that returns the **number** of students who belong to no CCA.
3. List the CCAs that have **no members**.
4. For every student, show their name and the number of CCAs they belong to, **including students with zero**. Sort by number of CCAs (highest first), then name.
5. **Explain in two sentences** why an `INNER JOIN` cannot answer questions 1 to 3.

---

## Challenge 3: Class report card (three tables) ★★★★

1. Show a report card for **Tan Wei Jie**: his name, each subject name, and his score, sorted by subject name.
2. Show the report card for **every student in class 3A**: student name, subject name and score, sorted by student name then subject name.
3. For class 3A, show each student's **average score** (rounded to 1 decimal place) and how many subjects they have a score in, best average first. Break ties by name.
4. Find the students (name and class) whose average score across all their subjects is **below 60**.

**Tip:** before writing any SQL, draw the path through the schema: which tables hold the name, the score, and the subject name, and which keys connect them?

---

## Challenge 4 (open-ended): Design a "top 5" report ★★★★★

Invent a "top 5" report that is useful to a teacher or student, and write the query.

**Requirements**

- It must use **`GROUP BY`**, at least one **`JOIN`**, **`ORDER BY`**, and **`LIMIT 5`**.
- It must have meaningful column names (use `AS`).
- Write the question in English as a comment, and a one-sentence note on how a teacher could use the result.

**Ideas** (choose one or make your own):

- The 5 students with the highest average score.
- The 5 CCAs whose members have the highest average score.
- The 5 students who are members of the most CCAs.
- The 5 (class, subject) pairs with the lowest average.

**Self-assessment**

| Criterion | Yes / No |
|-----------|----------|
| Query uses `GROUP BY`, a `JOIN`, `ORDER BY` and `LIMIT 5` | |
| Every `SELECT` column is either grouped or aggregated | |
| Averages are rounded; columns have clear names | |
| Ties are handled (a second `ORDER BY` column) | |
| The English question matches what the query really does | |
