# Week 11 Demo: Test, polish, present

**Time:** 45 minutes. Four short parts, then the students finish their projects.
**Code:** [demo/](demo/) (`grades.py`, `test_grades.py`, `grades_buggy.py`) · a full example in [Answers/model-capstone](../week-10-plan-and-build/Answers/model-capstone/)

---

## Part 1: Testing (20 min)

**Why test?** Because you change your code all the time, and every change can break something you cannot see. A test is a small program that checks a small piece of your program and says PASS or FAIL. When you have fifty, you can change anything and know within a second if you broke something.

### Step 1: Unit tests for a plain function

Open [demo/grades.py](demo/grades.py) and [demo/test_grades.py](demo/test_grades.py).

```python
class TestGrade(unittest.TestCase):
    def test_typical_scores(self):
        self.assertEqual(grade(90), "A")

    def test_invalid_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            grade(101)
```

Run: `cd week-11-test-polish-present/demo && python3 -m unittest test_grades -v`

The anatomy of a test: **Arrange** (set up the input), **Act** (call the function), **Assert** (check the result). The method name says *what behaviour* is checked.

### Step 2: Watch the tests catch a bug

Copy the buggy version over the good one and run again:

```bash
cp grades.py grades_good.py && cp grades_buggy.py grades.py
python3 -m unittest test_grades -v
```

`test_typical_scores` still passes (90, 70, 60, 50, 20 are all fine), but `test_boundaries` fails for 65 and 45. **A test that only tries typical values would have missed both bugs.** The rule: *test the number on each side of every boundary.* Fix it (`>=`), restore `grades_good.py`, run again: green.

### Step 3: What to test in a web app

Open [Answers/model-capstone/tests/test_app.py](../week-10-plan-and-build/Answers/model-capstone/tests/test_app.py) and look at the pattern:

```python
def setUp(self):                      # runs BEFORE EVERY test
    self.tmp = tempfile.TemporaryDirectory()
    project.app.config.update(DATABASE=..., TESTING=True)
    with project.app.app_context():
        project.init_db(seed=False)   # a fresh, empty database each time
    self.client = project.app.test_client()    # a pretend browser
```

`test_client()` sends requests to your app **without** starting a server. Each test uses its own throw-away database, so tests cannot affect each other or your real data.

Cover these kinds of things for **every** feature (the model project has an example of each):

| Kind | Example |
|------|---------|
| Happy path | A valid loan is saved, and the redirect happens |
| Invalid input | Empty name or quantity zero: the form is shown again, nothing is saved |
| Boundary | Borrowing exactly the number available works; one more is refused |
| Not found | `/kits/999` returns 404 |
| Wrong method | `GET` on a delete route returns 405 |
| Database rule | Even if Python forgets, the `CHECK`/`FOREIGN KEY` refuses the row |
| Hostile input | `' OR 1=1 --` as a search is treated as text; `<script>` is shown, not run |

**Check the database, not just the page.** After a POST, assert on the page *and* run a `SELECT` on the test database to prove the row is there (or is not there).

Write one new test live for the template project and run the whole suite.

## Part 2: Polish (10 min)

Polish is the difference between "it works on my laptop" and "someone else can use it". Walk through [challenges/polish-checklist.md](challenges/polish-checklist.md) on the model project:

1. **Empty states:** What does the page say when there is nothing to show? ("No kits match. Add one?" not an empty table.)
2. **Helpful errors:** The message says what to fix, next to the field. "Invalid input" is not enough.
3. **Consistency:** the same words everywhere ("kit", not "item" in one place and "equipment" in another); the same button style.
4. **Touch and screen:** 16px text in inputs; buttons at least 44px tall; test at iPad width with the browser tools; labels on every field.
5. **Leftovers:** placeholder text from the template, debug prints, commented-out code, "Test 1" data.
6. **Dangerous actions:** delete is a POST button, styled as dangerous; consider a confirmation.
7. **Accessibility basics:** colours with enough contrast, `alt` text on images, headings in order, the page works with only a keyboard.

## Part 3: The README (5 min)

Your README is the first thing a reader (and your marker) sees. Use [challenges/readme-template.md](challenges/readme-template.md). Show the model project's [README](../week-10-plan-and-build/Answers/model-capstone/README.md): what it is, how to run it, the ER diagram (Mermaid renders on GitHub), what each page does, how it is tested, limits and next steps.

Rule of thumb: *someone who has never met you must be able to run your project using only your README.*

## Part 4: Going live, and presenting (10 min)

**Deployment** (stretch goal): show the shape of the process from [deploy-pythonanywhere.md](deploy-pythonanywhere.md): code from GitHub, a virtual environment, build the database with `init-db`, a WSGI file, reload. Emphasise the differences from Codespaces: debug is off, the secret key comes from the environment, and anyone can reach it.

**Presentation (3 minutes + 2 minutes of questions).** Use this order, from [challenges/presentation-planner.md](challenges/presentation-planner.md):

1. **The problem** (30 s): who has it, and why does it matter?
2. **Live demo** (90 s): follow one user story from start to finish. Include one error (type bad data on purpose).
3. **Under the hood** (40 s): show the ER diagram, one SQL query and one test.
4. **Reflection** (20 s): the hardest bug, and what you would do next.

Tips: practise once with a timer; load the pages you need in tabs beforehand; have the seed data ready; if the demo breaks, stay calm and say what you expected to see. Expect to be asked to change something small live ("make this field required").

---

## Wrap-up question

A test passes. A colleague says "so there are no bugs." What is wrong with this conclusion?

(Answer: a passing test shows only that the cases we thought of work. It cannot show that no bugs exist. That is why we choose the cases carefully: boundaries, invalid input, and the things that went wrong before.)
