# Week 11 Extra Practice and Where Next

For after the course, or for students who want to keep going.

---

## 1. Test-driven development (TDD) kata

**TDD** means writing the test *before* the code: red (the test fails) → green (write just enough code to pass) → refactor (tidy up) → repeat.

Write `validators.py` with a function `validate_booking(name, seats, available)` that returns a **dictionary of errors** (empty if everything is valid):

- `name`: required after trimming spaces, 2 to 40 characters
- `seats`: must be a whole number written as a string of digits, at least 1
- `seats` must not be more than `available`

First write `test_validators.py` with at least **ten** tests (including the boundaries 1, `available`, and `available + 1`, the strings `"abc"`, `"1.5"`, `"-2"` and `""`, and a name of 1, 2, 40 and 41 characters). Run them (all red), then write the function until they are all green. Then change `validate_booking` so that the checks are in a different order: do the tests still pass? What does that tell you?

## 2. Add tests to your own capstone

Add **five** more tests that you think of by asking "what could go wrong?" Hint: dates in the past, two users doing the same thing, a name with an apostrophe (`O'Brien`), a very large number, deleting something that is in use. If a test fails, you have found a real bug: fix it.

## 3. Refactor

Pick your longest route function. Move the validation into its own function that returns `(clean_values, errors)`. Run the tests before and after: they should still pass. Why is it safer to refactor when you have tests?

## 4. Accessibility audit

Unplug the mouse (or do not touch the screen). Can you use every page with the keyboard only (Tab, Shift+Tab, Enter, Space)? Is it always clear where the focus is? Is every image described? Zoom the page to 200%: does it still work? Write a list of the problems and fix three.

## 5. Security review

Pretend to be an attacker for ten minutes against your own project. Try: odd characters in every field; very long text; negative numbers; editing hidden fields and `<select>` values with the browser's inspector; typing `/something/1/delete` in the address bar; changing the number in `/records/3` to someone else's record. For each attack, write whether the app was safe, and fix anything that was not. (Which of these would be possible without a login? Which would need one?)

## 6. Reflection (200 words)

What was the hardest part of the course? What bug took you longest to find, and how did you find it? What would you do differently on the next project? Which Week's idea (HTML, SQL or Flask) did you find most useful?

---

## Where next?

| If you enjoyed... | Try next |
|-------------------|----------|
| **Making things look good** | CSS Grid and flexbox in depth; a framework such as Bootstrap or Tailwind; JavaScript to change the page without reloading |
| **Data and SQL** | Window functions, views, indexes and `EXPLAIN QUERY PLAN`; PostgreSQL; data analysis with Python (`pandas`) |
| **Flask and back-end** | User accounts: password hashing and sessions (Flask-Login); Flask-WTF for forms and CSRF protection; blueprints and the application factory; SQLAlchemy |
| **Building products** | Talk to real users; ship a small version; JSON APIs with Flask; deploying with a custom domain; version control with pull requests |
| **Computing as a subject** | The H2 Computing syllabus covers topics such as databases, SQL and normalisation, algorithms, data structures, networks and security: this course practised several of these (check the current syllabus document with your teacher). Ask your teacher about project ideas for a school computing showcase |

Keep your repository: employers and teachers like to see a real project with tests and a README.
