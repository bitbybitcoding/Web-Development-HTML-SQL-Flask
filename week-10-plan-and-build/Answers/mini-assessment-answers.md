# Week 10 Mini-assessment: marking guide

**Total: 25 marks.** Award marks for correct ideas, not for exact wording. Handwritten code with a tiny syntax slip (a missing colon or bracket) is not penalised if the logic is clear. Use the follow-through principle: if a wrong answer is used correctly in a later part, do not penalise it twice.

## Section A: Short answers (10 marks)

**A1** [2]
- A **primary key** uniquely identifies each row of a table (never NULL, never repeated). [1]
- A **foreign key** is a column that holds the primary key of a row in another table, linking the two tables. `loan.kit_id` prevents a loan being saved for a kit that does not exist (an orphan record), and prevents deleting a kit that has loans. [1]

**A2** [2]
- Problem [1, any one with an example]: the kit and category names are **repeated** in every loan, wasting space; changing a kit's name needs updating every loan row (**update anomaly**) and missing one causes inconsistent data (for example "Arduino Uno" and "Arduino UNO"); a new kit cannot be recorded until it is lent (**insert anomaly**); deleting the only loan of a kit deletes the knowledge that the kit exists (**delete anomaly**).
- Normal form [1]: it breaks **2NF/3NF**. `kit_name` and `category_name` depend on `kit_id` (a non-key attribute) rather than on the loan itself: a transitive dependency, so 3NF is broken. Accept "3NF" and also "2NF" if the student explains a partial dependency on a composite key. Do not accept "1NF" unless the answer explains a repeating group.

**A3** [2]
- A link sends a **GET** request, which is meant only to read data and can be repeated safely; returning a kit **changes** data. [1]
- Links can be followed by search-engine crawlers, browser pre-loading or an attacker's page without the user meaning to, which would change the data. A POST form is deliberate and is not repeated by accident. [1] (Accept "a refresh would repeat the action".)

**A4** [2]
- Attributes such as `min`, `max` and `required` run in the **browser**, which the user controls. They can be removed with developer tools, or the request can be sent by a script, so the server may receive any value. [1]
- The server must therefore validate (is it a whole number, within range, no more than the number available?) before using it. [1]

**A5** [2]
- Jinja **auto-escapes** the value, converting characters such as `<` and `>` into `&lt;` and `&gt;`, so the browser displays them as text instead of treating them as HTML. [1]
- This prevents **cross-site scripting (XSS)**: a user entering a `<script>` tag that would run in other visitors' browsers. [1]

## Section B: Debug this route (8 marks)

Mark the **first four** faults found. 1 mark for identifying, 1 mark for the correction. (The student may find all five: do not give more than 8.)

| # | Fault | Correction |
|---|-------|-----------|
| 1 | The route accepts only GET (the default), but it changes data and reads `request.form`. A form POST gets **405 Method Not Allowed**. | `@app.route("/kits/<int:kit_id>/borrow", methods=["POST"])` |
| 2 | No **validation**: `request.form["borrower"]` raises a 400 error if the field is missing; the name could be empty or huge; `qty` is a string that is never checked to be a number, positive or no more than the number available. | `borrower = request.form.get("borrower", "").strip()`; check `2 <= len(borrower) <= 40`; check `qty.isdigit()` and `1 <= int(qty) <= available`; flash and redirect if not. |
| 3 | **SQL injection**: user input is placed into the SQL with an f-string. A borrower name such as `x', 1, '2026-01-01', '2026-01-02') --` changes the statement; `qty` could be `1); DELETE ...`. | `db.execute("INSERT INTO loan (kit_id, borrower, qty, borrowed_on, due_on) VALUES (?, ?, ?, date('now'), date('now', '+7 days'))", (kit_id, borrower, int(qty)))` |
| 4 | **No commit**: the insert is never committed, so it is lost when the connection closes. | Wrap in `with db:` (or call `db.commit()` after the insert). |
| 5 | **No redirect** (Post/Redirect/Get): refreshing resubmits the form and creates a second loan. Also `render_template("kit.html")` passes none of the variables the page needs, so it would fail. | `flash("Borrowed.")` then `return redirect(url_for("kit", kit_id=kit_id))` |

Other acceptable faults: the kit is not checked to exist (404); no check whether the kit is already out; the due date is fixed at 7 days and ignores user input.

## Section C: Write code (7 marks)

**C1** [3]

```sql
SELECT k.name,
       k.total_qty - COALESCE(SUM(l.qty), 0) AS available
FROM kit AS k
LEFT JOIN loan AS l ON l.kit_id = k.kit_id AND l.returned_on IS NULL
GROUP BY k.kit_id;
```

- [1] `LEFT JOIN` (so kits never borrowed are kept).
- [1] Only loans not yet returned are counted (`returned_on IS NULL`). It must be in the join condition (`ON`) when the whole query uses `LEFT JOIN`; putting it in `WHERE` would remove the kits without loans, which loses the mark for the previous point as well unless the student uses `OR l.loan_id IS NULL`.
- [1] `GROUP BY` with `SUM(qty)`, `COALESCE` (or an equivalent) for kits with no loans, and a correct subtraction from `total_qty`.

Alternative accepted: a correlated subquery:
```sql
SELECT k.name, k.total_qty - COALESCE((SELECT SUM(qty) FROM loan WHERE kit_id = k.kit_id AND returned_on IS NULL), 0) AS available
FROM kit AS k;
```
Both versions return the same result (verified on the model project's seed data: Arduino Uno 7, micro:bit v2 9, Soldering iron 2 ...).

**C2** [4]

```python
@app.route("/kits/<int:kit_id>/delete", methods=["POST"])
def delete_kit(kit_id):
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM loan WHERE kit_id = ?", (kit_id,)).fetchone()[0]
    if count > 0:
        flash("This kit has loan records and cannot be deleted.")
        return redirect(url_for("kit", kit_id=kit_id))
    with db:
        db.execute("DELETE FROM kit WHERE kit_id = ?", (kit_id,))
    flash("Kit deleted.")
    return redirect(url_for("index"))
```

- [1] `methods=["POST"]` only.
- [1] A query that counts or finds loans for the kit, with a `?` placeholder (no f-string).
- [1] Refuses with a flash message and a redirect when there are loans.
- [1] Otherwise deletes with `?` inside `with db:` and redirects to the home page.

(Do not penalise a missing check that the kit exists, though a good answer may add `abort(404)`.)

## Grade guide (suggested)

| Marks | Comment |
|-------|---------|
| 22-25 | Excellent: fluent across design, security and code |
| 18-21 | Good: small gaps; check Section B |
| 13-17 | Secure on basics; revise validation, injection and the join in C1 before Week 11 |
| 0-12 | Offer revision time before Week 11; pair with a stronger student for the capstone |
