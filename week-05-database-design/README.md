# Week 5: Database design: ER diagrams and normalisation

**Block 2: SQL** · 3 hours · Platform: GitHub Codespaces · This is one of the two densest weeks of the course

## By the end of this session students can

- Identify entities, attributes and relationships from a written description.
- Classify relationships as one-to-one, one-to-many or many-to-many, and draw them in an ER diagram.
- Resolve a many-to-many relationship with a junction table.
- Explain why redundancy is a problem, and name the update, insert and delete anomalies.
- Normalise a table step by step through 1NF, 2NF and 3NF.
- Turn a normalised design into SQLite tables with sample data.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · template in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): SQL recap

Three questions on paper, using `school.db`:

1. Write a query that shows the number of students in each class.
2. Explain the difference between `WHERE` and `HAVING`.
3. Which students are in no CCA? Write the query and name the join you use.

Then ask: *"Why does the school keep CCA membership in a separate `student_cca` table, instead of adding a `cca` column to `students`?"* Collect answers on the board. Students will answer this properly by the end of today.

## Instructor notes

- **Dense week.** If students fall behind, move the Challenge 3 SQL work to homework. The syllabus pacing note allows this: ER diagrams and normalisation are the exam content, and the SQL implementation is revisited in Week 6.
- **Diagrams.** ER diagrams in these notes use [Mermaid](https://mermaid.js.org), which GitHub renders directly in the web view. Students should **draw by hand** (paper, or the iPad with a stylus) during class; the Mermaid blocks are for reference.
- **`CREATE TABLE` is previewed, not taught.** Week 6 covers constraints in detail. This week, students only need to copy the pattern from the demo.
- **Normalisation language.** Use the H2 wording: *repeating group*, *partial dependency* (on part of a composite key), *transitive dependency* (non-key attribute depends on another non-key attribute). Keep a "rule of thumb" on the board: *every non-key attribute depends on the key, the whole key, and nothing but the key.*
- **Peer review** in the extra practice works best if you pair students in the last 10 minutes and give them the checklist.
