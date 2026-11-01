# Week 10 Mini-assessment

**Weighting:** 20% of the course · **Time:** 30 minutes · **Total:** 25 marks · **Held:** the last 30 minutes of Week 10 (2:30 to 3:00) · **Rules:** individual, closed notes, no cheatsheet, no internet. Write on paper (code may be handwritten: do not worry about tiny syntax slips, but the logic must be clear).

**The system.** A club lends out equipment. Three tables (primary keys underlined by `PK`, foreign keys marked `FK`):

```
category(category_id PK, name)
kit(kit_id PK, name, category_id FK, total_qty)
loan(loan_id PK, kit_id FK, borrower, qty, borrowed_on, due_on, returned_on)    -- returned_on is NULL while the kit is out
```

---

## Section A: Short answers (10 marks)

**A1** [2] Explain the difference between a primary key and a foreign key. State what the foreign key `loan.kit_id` prevents.

**A2** [2] A student suggests dropping the `kit` table and putting `kit_name` and `category_name` straight into every `loan` row. Name **one** problem this causes (give a concrete example) and state which normal form is broken.

**A3** [2] Explain why the "Return this kit" button should send a POST request and not be a link.

**A4** [2] The form on the borrow page has `<input type="number" min="1" max="5" name="qty" required>`. Explain why the server must still check `qty`.

**A5** [2] A borrower types `<b>Hi</b>` as their name. The page shows `<b>Hi</b>` as plain text rather than bold text. Explain what Jinja did, and name the attack this helps to prevent.

---

## Section B: Debug this route (8 marks)

The route below lets a user borrow a kit. It has at least **five** faults. Find **four**. For each, state what is wrong (1 mark) and write the corrected line or lines (1 mark).

```python
@app.route("/kits/<int:kit_id>/borrow")
def borrow(kit_id):
    borrower = request.form["borrower"]
    qty = request.form["qty"]
    db = get_db()
    db.execute(f"INSERT INTO loan (kit_id, borrower, qty, borrowed_on, due_on) "
               f"VALUES ({kit_id}, '{borrower}', {qty}, date('now'), date('now', '+7 days'))")
    return render_template("kit.html")
```

---

## Section C: Write code (7 marks)

**C1** [3] Write one SQL query that lists every kit's `name` with the number **currently available** (`total_qty` minus the quantity currently on loan), including kits that have never been borrowed.

**C2** [4] Write a Flask route `delete_kit(kit_id)` that accepts POST only. It must: refuse (with a flash message) and redirect back if the kit has **any** loan records; otherwise delete the kit and redirect to the home page. Use a `?` placeholder and `with db:`. Assume `get_db()` exists.

---

*End of paper.* Hand in your answers. Marking guide: [Answers/mini-assessment-answers.md](Answers/mini-assessment-answers.md) (instructors: see the note in the Week 10 README about using a variant).
