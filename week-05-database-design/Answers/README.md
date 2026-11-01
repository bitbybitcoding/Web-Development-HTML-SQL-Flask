# Week 5 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenge 1: ER diagram | [challenge-1-er-diagram.md](challenge-1-er-diagram.md) |
| Challenge 2: Normalisation | [challenge-2-normalisation.md](challenge-2-normalisation.md) |
| Challenge 3: SQLite implementation | [challenge-3-uniform.sql](challenge-3-uniform.sql) |
| Challenge 4: Own database design (sample) | [challenge-4-sample.md](challenge-4-sample.md) + [challenge-4-sample.sql](challenge-4-sample.sql) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) |

The ER diagrams use Mermaid, which GitHub displays automatically when you view the `.md` files on github.com.

## Warm-up answers

1. ```sql
   SELECT class, COUNT(*) AS students
   FROM students
   GROUP BY class;
   ```
2. `WHERE` filters individual rows before grouping and cannot use aggregates. `HAVING` filters groups after `GROUP BY` and can use aggregates.
3. ```sql
   SELECT st.name
   FROM students AS st
   LEFT JOIN student_cca AS sc ON sc.student_id = st.student_id
   WHERE sc.student_id IS NULL;
   ```
   A `LEFT JOIN` (the students table is on the left).
4. Because a student can join **many** CCAs, and a CCA has **many** students. A single `cca` column in `students` can hold only one value, so we would need repeated columns (`cca1`, `cca2`, ...) or a list in one cell, which breaks 1NF. A junction table stores each membership as its own row. (It also stores the `role` of the student in that CCA.)

## Common mistakes to watch for

- **Drawing a line directly between two entities in an M:N relationship** and leaving it unresolved.
- **Putting the foreign key on the wrong side.** Rule: it goes on the "many" side.
- **Normalising by "splitting until it looks tidy"** rather than by listing functional dependencies. Insist on the dependency list: it is what the exam marks.
- **Confusing 2NF and 3NF.** Partial dependency: part of a *composite key* determines something. Transitive dependency: a *non-key* column determines something. A table with a single-column primary key cannot violate 2NF.
- **Attributes of a relationship stored in the wrong place** (for example `role` in `student`).
- **Using SQL reserved words as table names** (`order`, `group`). Use `orders` and `groups`.
- **Challenge 3:** forgetting that parent tables must be created and filled **before** child tables, and dropped **after** them.
