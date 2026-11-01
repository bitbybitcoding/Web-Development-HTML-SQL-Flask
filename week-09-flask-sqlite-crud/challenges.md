# Week 9 Challenges

**Challenges 1 to 3 build on one app.** Copy the whole demo (`db.py`, `app.py`, `templates/`, `static/`) to `my-work/week09/school/` and extend it. Run it with `flask --app app run --debug` from inside that folder. Your copy of `school.db` is in `instance/`; if you damage it, stop the server, delete `instance/` and restart.

**Rules for every challenge:** `?` placeholders only (no f-strings in SQL); `POST` for anything that changes data; validate before the database; `with db:` for writes; redirect after a successful POST; unknown ids give a 404.

---

## Challenge 1: Read: the CCA directory ★★

Add:

- **`/ccas`**: a table of every CCA with its category, day and **number of members**. The CCA with no members must still appear (with `0` and a note). Sort by member count (largest first), then name. A `?category=Sports` query string filters by category, and links for each category are built from the database (not typed by hand).
- **`/ccas/<int:cca_id>`**: the CCA's details and a table of its members (name, class, role), leaders first. A CCA that does not exist gives a 404.
- Add "CCAs" to the navigation and link student names to their pages.

*Think:* which join keeps the empty CCA? What happens if you use `JOIN` instead of `LEFT JOIN`?

---

## Challenge 2: Create: add a member ★★★

On the CCA page, add a form to **add a student to the CCA**, with a drop-down of students (only those **not already** in it, from one SQL query with a subquery) and a role (`Member` or `Leader`).

- `POST /ccas/<id>/join`. Check that the student exists and the role is allowed. Never trust the drop-down: the server must check.
- Joining twice must give a friendly message, not a crash. The table has `PRIMARY KEY (student_id, cca_id)`; catch `sqlite3.IntegrityError`.
- Flash a success message and redirect back to the CCA page.

*Test it:* send `student_id` = `9999`, and `1 OR 1=1`, and role `Boss`, using the browser tools or Flask's test client. Nothing should be added.

---

## Challenge 3: Update and delete ★★★

1. **Edit scores.** `GET/POST /students/<id>/scores` shows one number box for each subject (pre-filled; blank when the score is `NULL`, meaning absent). Saving updates every subject in one transaction. Rules: a whole number from 0 to 100, or blank (stored as `NULL`). A student with no score row for a subject yet needs an `INSERT`, one who has needs an `UPDATE`. Look up `INSERT ... ON CONFLICT ... DO UPDATE` (an "upsert"), which does both.
2. **Leave a CCA.** A "Remove" button beside each member (POST `/ccas/<cca_id>/leave/<student_id>`). If nothing was removed, give a 404.
3. **Delete a CCA.** A "Delete this CCA" button. If the CCA still has members, **refuse** and flash how many remain; otherwise delete it.

*Think:* why not simply delete the members and the CCA together? When would that be right, and when would it be dangerous? (There is no one right answer. Discuss with a partner.)

---

## Challenge 4: Library web app ★★★★ (open-ended)

Turn the Week 6 command-line library into a website. Copy [challenges/library_seed.sql](challenges/library_seed.sql) (it contains the `book` and `loan` tables and sample data; you may use your own `library.db` from Week 6 instead). Create the database from the seed the first time the app runs.

**Must have**

- **Book list** with a status for each book: `available`, `on loan` (with the borrower and due date) or `overdue`. Search by title or author, and filter by status.
- **Book page** with the loan history, a "Lend" form (borrower name, validated) or a "Return" button, depending on the status. A book on loan cannot be lent again. A new loan is due in 14 days.
- **Add, edit and delete books.** Titles must be unique per author (friendly error, not a crash). A book with loan history cannot be deleted.
- **Overdue report** with the number of days late, most late first.
- **Statistics page** with at least two `GROUP BY` queries (for example, most borrowed books and loans per borrower), and the list of books that have *never* been borrowed.
- All the rules from the top of the page.

**Choose at least two extras**

- Pagination (`LIMIT` and `OFFSET`) on the book list.
- Click a column heading to sort. **Careful:** a column name cannot be a `?` placeholder. How will you make it safe? (See the extra practice.)
- A borrower page listing everything one person has borrowed.
- Renewals: extend the due date once by 7 days.
- A responsive layout that works well on an iPad.

**Peer review (last 5 minutes):** swap with a neighbour. Try an odd search (`%`, a quote, very long text), lend a book twice, and delete a book that has history. Write one thing that works well and one thing to improve.
