# Week 10 Answers

| Task | Answer |
|------|--------|
| Capstone reference project | [model-capstone/](model-capstone/): Robotics Club kit loans. Three tables, full CRUD, search, filter, two reports, validation, and 21 automated tests. **Not for students to copy.** |
| Mini-assessment marking guide | [mini-assessment-answers.md](mini-assessment-answers.md) |
| Extra practice written questions | [extra-practice-answers.md](extra-practice-answers.md) |

Run the reference project:

```bash
cd week-10-plan-and-build/Answers/model-capstone
flask --app app init-db
flask --app app run --debug
python3 -m unittest discover -s tests -v       # 21 tests, all pass
```

## Plan approval checklist (use in the build time)

Sign off a plan only if you can answer "yes" to each question. Otherwise, say exactly which line to change.

1. **Scope:** can a student finish the MVP in about 6 to 8 hours? (A common error is to plan a whole app: logins, payments, email. Cut it.)
2. **Tables:** at least two, related by a foreign key? Is there anything that should be its own table (data repeated in many rows)? Is a many-to-many relationship resolved with a junction table?
3. **Keys and rules:** each table has a primary key; foreign keys are named; at least three real constraints (`NOT NULL`, `UNIQUE`, `CHECK`, defaults).
4. **Calculated values:** nothing is stored that can be calculated (totals, ages, availability).
5. **User stories:** each is testable and maps to a route.
6. **Requirement coverage:** CRUD on one table, a search/filter, one report with `GROUP BY` or a join. Is each in the MVP or a clearly labelled stretch? (The requirements must be in the MVP.)
7. **Route map:** data-changing actions are POST; every URL has a method; every page has a SQL statement.
8. **Realistic seed data** is planned, with edge cases (a NULL, an empty parent, an overdue record).

## Common problems in this week

- **One table only.** Ask: "what is repeated?" The repeated thing is the second table.
- **Storing lists in a cell** ("Maths, Physics"). That is a repeating group (1NF). Make a junction table.
- **Storing derived data** (age instead of date of birth, `available` instead of `total` and loans).
- **Foreign key order in `schema.sql`:** create the parent table first, and `DROP` in the reverse order. Otherwise `init-db` fails or `DROP` is refused.
- **Forgetting that `init-db` deletes everything.** Tell students: data typed into the app is lost when they re-run it. Keep important sample data in `seed.sql`.
- **A database file committed to Git.** `.gitignore` covers `instance/`. If a student already committed one, `git rm --cached <file>`.
- **Editing `schema.sql` but not re-running `init-db`**: the page says "no such column". Run it again.
- **Template placeholders left behind:** "My Project", "Add item", "Items". Do a find and replace before the presentation.
- **Git:** committing from the wrong folder (`fatal: not a git repository`), forgetting `git add`, and detached confusion after `git switch` with uncommitted changes (commit or `git stash` first).
