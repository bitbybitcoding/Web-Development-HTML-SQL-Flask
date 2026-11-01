"""Model capstone: Robotics Club kit loans (the instructor's reference answer).

First time:      flask --app app init-db        (creates instance/app.db from schema.sql and seed.sql)
Run:             flask --app app run --debug
Reset the data:  flask --app app init-db        (this DELETES the database and starts again)
Test:            python3 -m unittest discover -s tests
"""
import os
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import click
from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

BASE = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")   # on a real server, set SECRET_KEY (see Week 11)
app.config["DATABASE"] = str(Path(app.instance_path) / "app.db")
app.config["TODAY"] = None            # tests set a fixed date; None means the real date
MAX_DAYS = 28


# ---- database ------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(seed=True):
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    db.executescript((BASE / "schema.sql").read_text())
    if seed:
        db.executescript((BASE / "seed.sql").read_text())
    db.commit()


@app.cli.command("init-db")
@click.option("--no-seed", is_flag=True, help="Create the empty tables only.")
def init_db_command(no_seed):
    """Delete the database and create it again."""
    init_db(seed=not no_seed)
    click.echo("Database ready.")


def today():
    return app.config["TODAY"] or date.today().isoformat()


# ---- reading --------------------------------------------------------------------------
# available = total - everything currently out. COALESCE turns "no loans" (NULL) into 0.
KITS_SQL = """
    SELECT k.kit_id, k.name, c.name AS category, k.total_qty,
           k.total_qty - COALESCE(SUM(CASE WHEN l.returned_on IS NULL THEN l.qty END), 0) AS available
    FROM kit AS k
    JOIN category AS c ON c.category_id = k.category_id
    LEFT JOIN loan AS l ON l.kit_id = k.kit_id
    WHERE k.name LIKE ? {extra}
    GROUP BY k.kit_id
    ORDER BY c.name, k.name
"""


def all_categories():
    return get_db().execute("SELECT category_id, name FROM category ORDER BY name").fetchall()


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    cat = request.args.get("category", "")
    params, extra = [f"%{q}%"], ""
    if cat.isdigit():
        extra, params = "AND k.category_id = ?", params + [int(cat)]
    kits = get_db().execute(KITS_SQL.format(extra=extra), params).fetchall()
    return render_template("index.html", kits=kits, q=q, cat=cat, categories=all_categories())


def kit_or_404(kit_id):
    row = get_db().execute(KITS_SQL.format(extra="AND k.kit_id = ?"), ("%", kit_id)).fetchone()
    if row is None:
        abort(404)
    return row


@app.route("/kits/<int:kit_id>")
def kit(kit_id):
    k = kit_or_404(kit_id)
    loans = get_db().execute("SELECT * FROM loan WHERE kit_id = ? ORDER BY borrowed_on DESC, loan_id DESC", (kit_id,)).fetchall()
    return render_template("kit.html", k=k, loans=loans, today=today(), max_days=MAX_DAYS)


@app.route("/overdue")
def overdue():
    rows = get_db().execute("""
        SELECT l.loan_id, k.kit_id, k.name, l.borrower, l.qty, l.due_on,
               CAST(julianday(?) - julianday(l.due_on) AS INTEGER) AS days_late
        FROM loan AS l JOIN kit AS k ON k.kit_id = l.kit_id
        WHERE l.returned_on IS NULL AND l.due_on < ?
        ORDER BY days_late DESC
    """, (today(), today())).fetchall()
    return render_template("overdue.html", rows=rows)


@app.route("/report")
def report():
    db = get_db()
    by_category = db.execute("""
        SELECT c.name, COUNT(DISTINCT k.kit_id) AS kits, SUM(k.total_qty) AS owned,
               COALESCE(SUM(out.qty), 0) AS out_now
        FROM category AS c
        LEFT JOIN kit AS k ON k.category_id = c.category_id
        LEFT JOIN (SELECT kit_id, SUM(qty) AS qty FROM loan WHERE returned_on IS NULL GROUP BY kit_id) AS out
               ON out.kit_id = k.kit_id
        GROUP BY c.category_id ORDER BY c.name
    """).fetchall()
    borrowers = db.execute("""
        SELECT borrower, COUNT(*) AS loans, SUM(qty) AS items
        FROM loan GROUP BY borrower ORDER BY loans DESC, borrower
    """).fetchall()
    never = db.execute("SELECT name FROM kit WHERE kit_id NOT IN (SELECT kit_id FROM loan) ORDER BY name").fetchall()
    return render_template("report.html", by_category=by_category, borrowers=borrowers, never=never)


# ---- kits: create, update, delete -----------------------------------------------------------
def clean_kit_form():
    form = {k: request.form.get(k, "").strip() for k in ("name", "category_id", "total_qty", "notes")}
    errors = {}
    if not 2 <= len(form["name"]) <= 60:
        errors["name"] = "Name must be 2 to 60 characters."
    if not form["category_id"].isdigit() or get_db().execute(
            "SELECT 1 FROM category WHERE category_id = ?", (form["category_id"],)).fetchone() is None:
        errors["category_id"] = "Choose a category."
    if not form["total_qty"].isdigit() or not 1 <= int(form["total_qty"]) <= 500:
        errors["total_qty"] = "Quantity must be a whole number from 1 to 500."
    return form, errors


@app.route("/kits/new", methods=["GET", "POST"])
def new_kit():
    form, errors = {"name": "", "category_id": "", "total_qty": "1", "notes": ""}, {}
    if request.method == "POST":
        form, errors = clean_kit_form()
        if not errors:
            db = get_db()
            try:
                with db:
                    cur = db.execute("INSERT INTO kit (name, category_id, total_qty, notes) VALUES (?, ?, ?, ?)",
                                     (form["name"], int(form["category_id"]), int(form["total_qty"]), form["notes"] or None))
            except sqlite3.IntegrityError:
                errors["name"] = "A kit with that name already exists."
            else:
                flash("Kit added.")
                return redirect(url_for("kit", kit_id=cur.lastrowid))
    return render_template("kit_form.html", form=form, errors=errors, categories=all_categories(), editing=False)


@app.route("/kits/<int:kit_id>/edit", methods=["GET", "POST"])
def edit_kit(kit_id):
    k = kit_or_404(kit_id)
    row = get_db().execute("SELECT * FROM kit WHERE kit_id = ?", (kit_id,)).fetchone()
    form = {"name": row["name"], "category_id": str(row["category_id"]), "total_qty": str(row["total_qty"]), "notes": row["notes"] or ""}
    errors = {}
    if request.method == "POST":
        form, errors = clean_kit_form()
        out_now = k["total_qty"] - k["available"]
        if not errors and int(form["total_qty"]) < out_now:
            errors["total_qty"] = f"{out_now} are out on loan, so the total cannot be lower than that."
        if not errors:
            db = get_db()
            try:
                with db:
                    db.execute("UPDATE kit SET name = ?, category_id = ?, total_qty = ?, notes = ? WHERE kit_id = ?",
                               (form["name"], int(form["category_id"]), int(form["total_qty"]), form["notes"] or None, kit_id))
            except sqlite3.IntegrityError:
                errors["name"] = "A kit with that name already exists."
            else:
                flash("Kit updated.")
                return redirect(url_for("kit", kit_id=kit_id))
    return render_template("kit_form.html", form=form, errors=errors, categories=all_categories(), editing=True, kit_id=kit_id)


@app.route("/kits/<int:kit_id>/delete", methods=["POST"])
def delete_kit(kit_id):
    k = kit_or_404(kit_id)
    db = get_db()
    history = db.execute("SELECT COUNT(*) FROM loan WHERE kit_id = ?", (kit_id,)).fetchone()[0]
    if history:
        flash(f"{k['name']} has {history} loan record{'s' if history != 1 else ''} and cannot be deleted.")
        return redirect(url_for("kit", kit_id=kit_id))
    with db:
        db.execute("DELETE FROM kit WHERE kit_id = ?", (kit_id,))
    flash("Kit deleted.")
    return redirect(url_for("index"))


# ---- categories ---------------------------------------------------------------------------------
@app.route("/categories", methods=["GET", "POST"])
def categories():
    db = get_db()
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not 2 <= len(name) <= 40:
            error = "Category name must be 2 to 40 characters."
        else:
            try:
                with db:
                    db.execute("INSERT INTO category (name) VALUES (?)", (name,))
            except sqlite3.IntegrityError:
                error = "That category already exists."
            else:
                flash("Category added.")
                return redirect(url_for("categories"))
    rows = db.execute("""
        SELECT c.category_id, c.name, COUNT(k.kit_id) AS kits
        FROM category AS c LEFT JOIN kit AS k ON k.category_id = c.category_id
        GROUP BY c.category_id ORDER BY c.name
    """).fetchall()
    return render_template("categories.html", rows=rows, error=error)


@app.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    db = get_db()
    used = db.execute("SELECT COUNT(*) FROM kit WHERE category_id = ?", (category_id,)).fetchone()[0]
    if used:
        flash("That category still has kits in it, so it cannot be deleted.")
    else:
        with db:
            cur = db.execute("DELETE FROM category WHERE category_id = ?", (category_id,))
        if cur.rowcount == 0:
            abort(404)
        flash("Category deleted.")
    return redirect(url_for("categories"))


# ---- borrowing and returning -----------------------------------------------------------------
@app.route("/kits/<int:kit_id>/borrow", methods=["POST"])
def borrow(kit_id):
    k = kit_or_404(kit_id)
    borrower = request.form.get("borrower", "").strip()
    qty, days = request.form.get("qty", ""), request.form.get("days", "")
    if not 2 <= len(borrower) <= 40:
        flash("Enter the borrower's name (2 to 40 characters).")
    elif not qty.isdigit() or not 1 <= int(qty) <= k["available"]:
        flash(f"Quantity must be a whole number from 1 to {k['available']} (the number available).")
    elif not days.isdigit() or not 1 <= int(days) <= MAX_DAYS:
        flash(f"Loan length must be from 1 to {MAX_DAYS} days.")
    else:
        due = (date.fromisoformat(today()) + timedelta(days=int(days))).isoformat()
        db = get_db()
        with db:
            db.execute("INSERT INTO loan (kit_id, borrower, qty, borrowed_on, due_on) VALUES (?, ?, ?, ?, ?)",
                       (kit_id, borrower, int(qty), today(), due))
        flash(f"{borrower} borrowed {qty} x {k['name']}, due {due}.")
    return redirect(url_for("kit", kit_id=kit_id))


@app.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    db = get_db()
    row = db.execute("SELECT kit_id, returned_on FROM loan WHERE loan_id = ?", (loan_id,)).fetchone()
    if row is None:
        abort(404)
    if row["returned_on"] is not None:
        flash("That loan was already returned.")
    else:
        with db:
            db.execute("UPDATE loan SET returned_on = ? WHERE loan_id = ?", (today(), loan_id))
        flash("Returned. Thank you!")
    return redirect(url_for("kit", kit_id=row["kit_id"]))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
