# Week 6 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenge 1: Canteen database | [challenge-1-canteen.sql](challenge-1-canteen.sql) (schema) and [challenge-1-canteen-tests.sql](challenge-1-canteen-tests.sql) (valid data and the rejected statements, with the exact error messages) |
| Challenge 2: Library app | [challenge_2_library.py](challenge_2_library.py) |
| Challenge 3: Injection | [challenge-3-attacks.md](challenge-3-attacks.md) (the attacks) and [challenge_3_fixed.py](challenge_3_fixed.py) (the fixes, with assertions) |
| Challenge 4: Reports | [challenge_4_reports.py](challenge_4_reports.py) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md), [extra_bank_transfer.py](extra_bank_transfer.py) |
| **Checkpoint quiz** | [checkpoint-quiz-answers.md](checkpoint-quiz-answers.md) (answers and mark scheme) |
| Self-check for all the Python answers | [tests_week6.py](tests_week6.py) |

Run the self-check from the repository root: `python3 week-06-ddl-dml-python-sqlite/Answers/tests_week6.py`. It proves that the sample solutions work **and** that the Challenge 3 starter file really is exploitable.

## Warm-up answers

- **A** `ORDER(order_no, item_code, item_name, unit_price, qty)`, key `(order_no, item_code)`: breaks **2NF**. `item_name` and `unit_price` depend only on `item_code`, which is part of the key (partial dependency).
- **B** `STUDENT(student_id, name, class, class_teacher)`, key `student_id`: breaks **3NF**. `class_teacher` depends on `class`, which is not the key (transitive dependency).
- **C** `ORDER(order_no, order_date, items)` with `items = "U1 x2, U2 x1"`: breaks **1NF**. The `items` cell holds several values (a repeating group), so it is not atomic.

## Common mistakes to watch for

- **Forgetting `PRAGMA foreign_keys = ON`**, then concluding "the foreign key does not work".
- **Forgetting `con.commit()`**: the program runs without errors, but the data is gone next time.
- **A one-value tuple without the comma:** `cur.execute("... WHERE class = ?", ("3A"))` passes the *string* `"3A"` (two characters), and fails with a confusing message about the number of bindings. It must be `("3A",)`.
- **Putting `%` wildcards in the SQL text** instead of the parameter: `LIKE '%?%'` does not work; use `LIKE ?` with `f"%{term}%"` as the value.
- **Trying to use `?` for a table or column name.** Placeholders are for values only.
- **`DELETE` or `UPDATE` without `WHERE`.**
- **Deleting parent rows before child rows.** Delete the child rows (`student_cca`) first, then the parent (`ccas`).
- **Using `input()` or `print()` inside the data functions** in Challenge 2, which makes them impossible to test.
