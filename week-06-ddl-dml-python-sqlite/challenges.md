# Week 6 Challenges

Work in `my-work/`. Put SQL files in `my-work/` and run them with `.read`. Remember `PRAGMA foreign_keys = ON;` at the start of every SQL session.

---

## Challenge 1: Build a database from a specification ★★★

Create `my-work/canteen.sql` that builds this database **exactly**, using constraints to enforce every rule.

**Table `stall`**

| Column | Rule |
|--------|------|
| `stall_id` | primary key |
| `name` | required; no two stalls may have the same name |
| `opens_at` | text such as `07:30`; if not given, it is `07:30` |
| `is_halal` | must be `0` or `1`; if not given, it is `0` |

**Table `dish`**

| Column | Rule |
|--------|------|
| `dish_id` | primary key |
| `stall_id` | required; must be the id of an existing stall |
| `name` | required |
| `price` | a decimal number that must be greater than 0 |
| `calories` | an integer; may be unknown (NULL) but if given must be 0 or more |
| (table rule) | the same dish name cannot appear twice at the same stall |

**Then prove that the rules work.** Write `my-work/canteen_tests.sql` with:

1. Valid rows: two stalls and four dishes. At least one dish has NULL calories, and one stall uses all the default values.
2. At least **seven INSERT statements that should be rejected**, one for each rule above. Put each one on its own line, add a comment saying which rule it breaks, and write down the error message SQLite gives.

---

## Challenge 2: Command-line library app ★★★★

Build a text-menu program backed by SQLite.

1. Copy [challenges/library_starter.py](challenges/library_starter.py) to `my-work/library.py`. It has the menu, the database set-up and empty function stubs.
2. Complete these functions. Every SQL statement must use `?` placeholders.

| Function | What it does |
|----------|--------------|
| `add_book(con, title, author)` | Adds a book. Rejects empty text and duplicates (same title and author) with a friendly `ValueError` message |
| `search_books(con, term)` | Finds books whose title **or** author contains the term, ignoring case. Shows whether each book is available |
| `borrow_book(con, book_id, borrower, today=None)` | Records a loan for 14 days. Rejects an unknown book, or one that is already on loan |
| `return_book(con, book_id, today=None)` | Marks the open loan as returned. Rejects a book that is not on loan |
| `list_books(con)` | Lists every book and whether it is available |

3. Run it with `python3 my-work/library.py`. Test all five menu options, including the error cases.
4. **Test that your data persists:** quit, restart, and check the books are still there.

**Design rules**

- Each function takes the connection as a parameter and returns a result (or raises `ValueError`). Only the `main()` menu loop uses `input()` and `print()`.
- A book is "on loan" when it has a loan row whose `returned_on` is NULL.

---

## Challenge 3: Fix the injection holes ★★★

Open [challenges/vulnerable.py](challenges/vulnerable.py). Four functions build SQL from user input. In `my-work/`, copy it to `fixed.py` and:

**Part A: Attack.** For each of `login`, `find_student`, `update_email` and `delete_student`, write down an input that makes the function do something it should not. Check: your input must really work (run it).

- `login`: log in as `admin` without knowing the password.
- `find_student`: reveal every student, then (harder) reveal the usernames and passwords from the **users** table.
- `update_email`: change **everybody's** email address with one call.
- `delete_student`: delete every student with one call.

**Part B: Fix.** Rewrite all four functions with `?` placeholders.

**Part C: Prove it.** At the bottom of your file, add `assert` statements showing that each attack from Part A now fails, and that normal use (for example `login(con, "admin", "S3cret!")`) still works.

**Think:** why was `update_email(con, "1 OR 1=1", ...)` dangerous even though the id is "just a number"?

---

## Challenge 4 (open-ended): Extend the library app with a report ★★★★★

Add a **report** option to your library app. Pick at least one:

- **Overdue books:** every loan that has not been returned and whose `due_on` date is before today, with the borrower's name and how many days overdue.
- **Most borrowed:** the three books borrowed most often, with the number of times.
- **Borrower history:** every book a named borrower has ever borrowed, newest first.

**Requirements**

- A new function that takes `con` and returns rows, plus a new menu option that prints them neatly.
- It must use `JOIN` or `GROUP BY` as appropriate, and `?` placeholders for any user input.
- Make the overdue report testable: give your function a `today=None` parameter so you can pass a fixed date when testing.
- Write three tests (with `assert`) using a database in memory (`":memory:"`).

**Self-assessment**

| Criterion | Yes / No |
|-----------|----------|
| Report function returns data and does not print | |
| Menu option prints it in a readable table | |
| Uses `?` placeholders for every input | |
| Tested with a fixed `today` | |
| Handles "nothing to report" with a friendly message | |
