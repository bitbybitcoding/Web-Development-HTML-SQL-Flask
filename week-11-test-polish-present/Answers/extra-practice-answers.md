# Week 11 Extra Practice: Answers

## 1. TDD kata

Code and tests: [extra_tdd/validators.py](extra_tdd/validators.py) and [extra_tdd/test_validators.py](extra_tdd/test_validators.py) (10 tests, all pass: `cd extra_tdd && python3 -m unittest test_validators -v`).

The order of the red-green steps in a good solution: (1) test one thing, such as a one-letter name, and watch it fail with `ImportError` or `NameError`; (2) write the smallest function that passes; (3) add the next test (name boundaries) and fail again; (4) pass it; (5) repeat for seats, then refactor. 

*Why do the tests still pass if the order of the checks changes?* Because the function checks each field independently and returns **all** the errors, not the first. The tests describe behaviour (what comes out for what goes in), not the way the code is organised. That is exactly what makes refactoring safe: if the tests stay green, the behaviour has not changed.

Two details tests forced: `" ".isdigit()` is `False` and `"".isdigit()` is `False`, but `"0".isdigit()` is `True`, so `0` needs its own check; and `None` has to be handled (`(seats or "")`) because a missing form field gives `None` if you use `request.form.get("seats")` with no default.

## 2. Add tests to your own capstone

Examples of tests that often find bugs: a date in the past (is it accepted when it should not be?); the same record created twice (duplicate); `O'Brien` (is the apostrophe stored and shown correctly? It should be, with placeholders and Jinja); a quantity of `10**12` (integer too large for the `CHECK`); deleting something in use (is there a message, not a 500 error?). A failing test means a real bug has been found. Fix the code, not the test (unless the test was wrong).

## 3. Refactor

Moving validation into `clean_form()` that returns `(form, errors)` makes the route short and the validation testable without a web request. With tests, you can refactor with confidence: run the tests before (all green), change the structure only, run them after (still green). Without tests, you must check every page by hand, and you will miss something.

## 4. Accessibility audit

Typical findings: a link with no visible focus outline (add `:focus` styles); a `<div>` used as a button (use `<button>`); placeholder text used instead of a label; low-contrast grey text; images without `alt`; a table that does not fit at 200% zoom. Mark by the quality of the list and the three fixes.

## 5. Security review

Typical attacks and what a safe project does:

| Attack | Safe project |
|--------|--------------|
| `' OR 1=1 --` in a search | Treated as text (placeholder) |
| `<script>alert(1)</script>` in a name | Shown as text (Jinja escapes it) |
| Negative or huge numbers | Rejected by server-side validation and `CHECK` constraints |
| Editing a `<select>` or hidden field to an invalid value | Rejected: the server checks the value against the allowed list |
| Visiting `/records/3/delete` in the address bar | 405 Method Not Allowed (POST only) |
| Changing `/records/3` to `/records/4` | Without a login, every record is public by design; **with** logins, the server must check that the record belongs to the user ("insecure direct object reference" is a common real-world flaw) |

*Which would need a login?* The last one is only a problem once users have their own private records, which is why adding logins means adding **authorisation checks** on every route, not just a login page.

## 6. Reflection

Marked for honesty and specificity. A good reflection names a particular bug and how it was found, a particular decision and its consequence, and one concrete thing to do differently.
