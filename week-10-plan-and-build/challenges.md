# Week 10 Challenges (build time)

You have about 80 minutes. Challenge 1 comes first, and **you must show your plan to your instructor before starting Challenge 2.** Work in `my-work/capstone/`, created from [capstone-template/](capstone-template/) (see its README). Commit after every challenge.

---

## Challenge 1: Plan ★★

Copy `PLAN.md` from the template and complete **sections 1 to 6**:

- The idea, the users (at least two kinds) and **six user stories**
- The MVP and stretch goals
- The database: tables, columns, keys, rules, an ER diagram, and one sentence on why your busiest table is in 3NF
- The route map (every page, URL, method and what SQL it needs)

**Check yourself:** Does the plan have at least two related tables? Is any many-to-many relationship resolved with a junction table? Could someone else build it from your plan? Is the MVP small enough to finish by the end of next week?

**Get the plan approved.** Your instructor will check it against the capstone brief.

---

## Challenge 2: The database ★★★

1. Edit `schema.sql` so that it creates **your** tables, with all the constraints from your plan. Remember: parent tables first.
2. Edit `seed.sql` with realistic data: at least 8 rows in your main table, and a mix that shows off the edge cases (a row with a NULL, a parent with no children, a record that is overdue/full/inactive, depending on your topic).
3. Run `flask --app app init-db`. Fix any errors.
4. **Prove it works.** In `sqlite3 instance/app.db` run three queries that your application will need (for example a join that lists the main rows with the name from the parent table, a `GROUP BY` report, and a search with `LIKE`). Save them as comments in `schema.sql` or in `PLAN.md`.
5. **Try to break it.** Write three `INSERT` statements that your rules should reject (a missing required value, a foreign key that does not exist, a value that fails a `CHECK`). Run them with `PRAGMA foreign_keys = ON;` and write down the error messages.

---

## Challenge 3: First vertical slice ★★★

Build **one list page and one add form** for your main table:

- `/` lists the rows, joined with the parent table's name, with a search box (GET).
- `/new` shows a form (GET) and processes it (POST): trim, validate each field on the server, show messages beside the fields and keep what was typed, insert with `?` placeholders inside `with db:`, flash a message, redirect.
- Use `base.html`, `url_for` and the stylesheet. Customise the colours and the title so that it looks like *your* project.

Add **two tests** in `tests/test_app.py` for your new routes (the template has examples). Run them.

Commit with a good message: `git add my-work/capstone && git commit -m "..." && git push`.

---

## Challenge 4: Next slice and a branch ★★★★ (open-ended)

Pick the next user story from your MVP and build it as a second vertical slice (edit, delete, a detail page, or the first report).

**Use a branch:**

```bash
git switch -c feature/<name>
# ... build, test, commit (at least twice) ...
git switch main
git merge feature/<name>
git push
```

If time allows, start the next one. At 2:20 you must stop, commit and push everything, and tidy up: no half-finished edits that stop the app from starting.

---

## At 2:30: the mini-assessment

Close your laptop lid or switch to paper. See [mini-assessment.md](mini-assessment.md).
