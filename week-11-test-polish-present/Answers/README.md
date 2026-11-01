# Week 11 Answers

| Task | Answer |
|------|--------|
| Challenge 1: Tests | A full example suite: [model-capstone/tests/test_app.py](../../week-10-plan-and-build/Answers/model-capstone/tests/test_app.py) (21 tests). A student's suite need not match it. Check the eight kinds listed in the challenge |
| Challenge 2: Polish | [polish-audit-answers.md](polish-audit-answers.md): what a good audit finds, with before and after examples |
| Challenge 3: README | [model README](../../week-10-plan-and-build/Answers/model-capstone/README.md) |
| Challenge 4: Presentation | [capstone-marking-sheet.md](capstone-marking-sheet.md) (the 100-mark sheet and presentation notes) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) · TDD kata code in [extra_tdd/](extra_tdd/) |
| Self-check | [tests_week11.py](tests_week11.py): `python3 week-11-test-polish-present/Answers/tests_week11.py` |

## Checking a student's test suite quickly

1. Run it. Do all the tests pass? How long does it take (should be a second or two)?
2. Count and list the **kinds** of test: happy path, invalid input, boundary, 404, wrong method (405), database rule, hostile input, and checking the database rather than just the page.
3. **Break the code on purpose** (change a `<` to `<=` in a validation check, or remove a `WHERE`). Does a test fail? If nothing fails, the tests are not testing that rule: ask the student to add one.
4. Look for tests that would pass even if the feature did nothing (only `status_code == 200`), tests that depend on the real date, and tests that share state (they use your real database, not a temporary one).

## Common problems

- Tests that use the real `instance/app.db`: they pass on one run and fail on the next, and they can delete real data. Each test must use a temporary database.
- `ModuleNotFoundError: No module named 'app'` when running tests: run `python3 -m unittest discover -s tests` from the **project folder** (the template's `tests/test_app.py` adds the parent folder to `sys.path`).
- Tests pass but the website is broken: the tests never open the page the user sees. Add a test that requests each page.
- A flash message appears on the *next* page after the redirect: assert on the page you land on (`follow_redirects=True`), not on the 302.
- README says "run `python app.py`", but the project needs `flask --app app run`: someone who follows the README must succeed. Try it.
- Presentation overruns: the demo tries to show everything. Cut to one user story and one error.
