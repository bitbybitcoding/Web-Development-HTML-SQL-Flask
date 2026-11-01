# Week 11 Challenges

You have about 50 minutes before the presentations. Work in your own project folder. **Feature freeze: do not add features.** Commit after each challenge, and push at the end.

---

## Challenge 1: Tests ★★★

Write an automated test suite for your project in `tests/test_app.py`, using the pattern from the template and the [model project](../week-10-plan-and-build/Answers/model-capstone/tests/test_app.py).

**Requirements**

- At least **8 tests**, all passing: `python3 -m unittest discover -s tests -v`.
- Each test has a fresh temporary database and a name that says what behaviour it checks.
- Cover **all** of these kinds:
  1. the list page shows the seed data (happy path)
  2. a valid form creates a row (check the **database** as well as the page)
  3. an invalid form is rejected, shows a message and creates nothing
  4. a boundary (the largest allowed value works, one more fails)
  5. an unknown id gives a 404
  6. a data-changing route refuses GET with 405
  7. a database rule (a constraint refuses a bad row even without Python's checks)
  8. hostile input (`' OR 1=1 --` or `<script>`) does not break the app or run
- **Make one test fail on purpose.** Break your code (for example, change `<` to `<=` in a check), watch the right test go red, then fix the code and watch it go green.

---

## Challenge 2: Polish ★★

Work through [challenges/polish-checklist.md](challenges/polish-checklist.md). Fix **at least ten** problems. Fill in the table of what you fixed, and list two things you decided not to fix, with reasons. Test the layout at iPad width using your browser's developer tools (or the Ports tab on a real iPad).

---

## Challenge 3: README ★★

Copy [challenges/readme-template.md](challenges/readme-template.md) to `README.md` in your project folder and complete every section: your ER diagram, the table of pages, the instructions for running, tests, limitations and a **personal** reflection.

**Check:** ask a neighbour to read only your README and then start your app. Where did they get stuck? Fix those lines.

---

## Challenge 4: Present, and optionally deploy ★★★★

1. Complete [challenges/presentation-planner.md](challenges/presentation-planner.md). Rehearse once, aloud, with a timer. Reset the database with `flask --app app init-db` and open the tabs you need.
2. **Stretch:** deploy to PythonAnywhere following [deploy-pythonanywhere.md](deploy-pythonanywhere.md) (only if your instructor says it is possible), and put the link in your README.
3. **Stretch:** one extra test for an edge case you worried about while polishing, or one extra polish fix.

At **2:00** you present. Make sure your latest work is committed and pushed: `git status` should say "nothing to commit".
