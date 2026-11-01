# Week 6, Challenge 3: the attacks

All of these have been run against [../challenges/vulnerable.py](../challenges/vulnerable.py) and they **work** (see `test_injection_starter_is_vulnerable` in [tests_week6.py](tests_week6.py)). After the fix, none of them works ([challenge_3_fixed.py](challenge_3_fixed.py)).

## Part A: attacks

| Function | Attack input | SQL that actually runs | Result |
|----------|--------------|------------------------|--------|
| `login` | password = `' OR '1'='1` (username `admin`) | `... username = 'admin' AND password = '' OR '1'='1'` | logs in: `OR '1'='1'` is always true |
| `login` | username = `admin' --` (any password) | `... username = 'admin' --' AND password = '...'` | logs in: `--` comments out the password check |
| `find_student` | `' OR 1=1 --` | `... name LIKE '%' OR 1=1 --%'` | returns **every** student |
| `find_student` | `zzz' UNION SELECT username, password, role FROM users --` | `... LIKE '%zzz' UNION SELECT username, password, role FROM users --%'` | returns the **users table** (the usernames, passwords and roles) in place of students. A `UNION` must have the same number of columns, so the attacker matches the three columns of the original query |
| `update_email` | `student_id = "1 OR 1=1"`, any email | `UPDATE students SET email = '...' WHERE student_id = 1 OR 1=1` | changes **every** student's email |
| `update_email` | `email = "x', class='HACKED"` | `UPDATE students SET email = 'x', class='HACKED' WHERE student_id = 1` | changes a column the function was never meant to touch |
| `delete_student` | `student_id = "1 OR 1=1"` | `DELETE FROM students WHERE student_id = 1 OR 1=1` | deletes **every** student |

## Part B: the fix

Every query becomes a fixed piece of SQL with `?`, and the values are passed separately. For the `LIKE` search, the wildcards go **inside the value**:

```python
con.execute("SELECT name, class, email FROM students WHERE name LIKE ?", (f"%{name}%",))
```

See [challenge_3_fixed.py](challenge_3_fixed.py) for all four functions.

## Part C: the checks

`challenge_3_fixed.py` ends with `run_checks()`, which asserts that each attack above now fails and that normal use still works.

## "Why was `update_email(con, "1 OR 1=1", ...)` dangerous even though the id is just a number?"

Because Python does not check types here. The function pasted whatever it was given into the SQL text: a string that *looks* like a number can carry extra SQL (`OR 1=1`). In the SQL text, a number has no quotes around it, so the attacker did not even need to type a quote. Numbers are values like any other and must go through `?` too. A second defence is to validate input (for example `int(student_id)` raises `ValueError` for `"1 OR 1=1"`), but validation is **in addition to** placeholders, never instead of them.

## Why does `execute("...; DROP TABLE users; --")` not work in Python?

Python's `sqlite3` module refuses to run more than one statement in a single `execute()` (`ProgrammingError` in Python 3.12 and later; `Warning` in older versions). That blocks the classic "drop the table" attack, but it does **not** stop the attacks above (which are all a *single* statement), and `executescript()` and other databases do allow several statements. Placeholders are the only complete defence.
