# Capstone starter project

This folder is a small, working Flask + SQLite app. **Copy it** to `my-work/capstone/` and turn it into your own project.

```bash
cp -r week-10-plan-and-build/capstone-template my-work/capstone
cd my-work/capstone
flask --app app init-db          # create instance/app.db from schema.sql and seed.sql
flask --app app run --debug      # open port 5000
python3 -m unittest discover -s tests -v     # run the tests
```

| File | Purpose |
|------|---------|
| `PLAN.md` | Your plan. Fill it in first |
| `schema.sql` | Your table definitions (`CREATE TABLE`) |
| `seed.sql` | Sample data so every page has something to show |
| `app.py` | Routes and database helpers |
| `templates/` | Jinja pages (`base.html` is the shared layout) |
| `static/style.css` | Your CSS |
| `tests/test_app.py` | Automated checks (Week 11) |

## How to adapt it

1. Write your `PLAN.md`.
2. Replace the tables in `schema.sql` and the rows in `seed.sql`. Run `flask --app app init-db` after every change (it **deletes and recreates** the database).
3. Replace the `item` routes and templates with your own, one feature at a time. Keep the same pattern for each: *validate → `with db:` → flash → redirect*.
4. Commit after each working feature (see the Git section of the Week 10 notes).
5. Rename `README.md` content to describe **your** project before Week 11.
