# Capstone marking sheet

**Student(s):** ______________________ **Project:** ______________________ **Date:** __________

Total: **100 marks** (counts as 40% of the course). See the full requirements in the [capstone brief](../../week-10-plan-and-build/capstone-brief.md).

| Area | Max | Mark | Evidence and comments |
|------|-----|------|----------------------|
| **Planning and design** `PLAN.md`, user stories, ER diagram, normalisation argument, route map | 15 | | |
| **Database** tables, keys, constraints, 3NF, realistic seed data | 15 | | |
| **Functionality** CRUD, search/filter, report; matches the plan | 25 | | |
| **Robustness and security** validation, `?` placeholders, POST for changes, 404s, duplicates and deletes | 15 | | |
| **Testing** at least 8 meaningful tests, passing | 10 | | |
| **Code quality and Git** readability, structure, 10+ commits with good messages | 10 | | |
| **Presentation and README** 3-minute demo, answers to questions, README quality, reflection | 10 | | |
| **Total** | **100** | | |

## Band descriptors

| Band | Description |
|------|-------------|
| **Excellent (85-100)** | All must-haves work reliably; clear 3NF design with strong constraints; thoughtful edge cases; tests that would catch real bugs; clean code and a convincing Git history; clear README and confident presentation; at least one extension (pagination, second report, workflow, deployment) |
| **Good (70-84)** | All must-haves present and working with minor gaps; sound design; a good number of tests covering several kinds; readable code; clear README; handles questions well |
| **Satisfactory (55-69)** | Most must-haves work; a design with small flaws (for example, a stored calculated value); fewer or shallow tests; some validation or security gaps; README present but thin |
| **Developing (40-54)** | The app runs but with missing must-haves or serious gaps (no validation, string-built SQL, no tests); weak design; limited understanding when questioned |
| **Not yet (0-39)** | The app does not run, or most requirements are missing; or the student cannot explain the code |

## Area notes

**Planning and design (15).** 15: a clear problem and users; six testable user stories; ER diagram consistent with the code; a real normalisation argument; a route map. 10: complete but generic. 5: a plan written after the fact, or missing parts.

**Database (15).** Check `schema.sql`: primary keys, foreign keys, `NOT NULL`, `UNIQUE`, `CHECK`, defaults; parent-first order; nothing stored that can be calculated; no repeating groups; seed data realistic with edge cases. Deduct for data in one table that belongs in two.

**Functionality (25).** Walk through the user stories, not just the pages. 10 for CRUD on a table; 5 for search/filter; 5 for the report (`GROUP BY` or a join); 5 for matching the plan and for no crashes in normal use.

**Robustness and security (15).** Try: an empty form; a letter in a number field; a quote mark; `<b>x</b>`; a huge value; `/records/abc`; GET on a delete URL; deleting a record that is in use. Every `?` placeholder is worth looking for in the code: **any** string-built SQL caps this area at 8/15.

**Testing (10).** 8+ tests all passing = 6; add 2 for variety (happy path, invalid input, boundary, 404/405, database rule, hostile input, checking the database); add 2 if a deliberate break would be caught (ask).

**Code quality and Git (10).** `git log --oneline`: at least 10 commits across both weeks, messages that say what changed. Pairs: both authors appear. Readable names; small functions; why-comments; no debug leftovers.

**Presentation and README (10).** 3 minutes (±30 s); a demo of one story with a deliberate error; shows ER diagram, a query and a test; honest reflection. README lets a stranger run the project. A **live change** is requested during questions.

## Presentation notes

| Part | Time | Seen? | Notes |
|------|------|-------|-------|
| The problem | 30 s | | |
| Live demo with an error | 90 s | | |
| Under the hood (ER, SQL, test) | 40 s | | |
| Reflection | 20 s | | |
| Question 1 (about the code): | | | |
| Live change request: | | | Done in ___ minutes |

## Authorship check

Ask every student to **explain a function they wrote** and to make a small change live. If a student cannot explain code in their submission, discuss it privately and adjust the marks for the relevant areas.
