"""Capstone template: replace the example 'item' feature with your own project.

First time:      flask --app app init-db        (creates instance/app.db from schema.sql and seed.sql)
Run:             flask --app app run --debug
Reset the data:  flask --app app init-db        (this DELETES the database and starts again)
Test:            python3 -m unittest discover -s tests
"""
import sqlite3
from pathlib import Path

import click
from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

BASE = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "change-me-before-you-deploy"          # Week 11: read this from an environment variable
app.config["DATABASE"] = str(Path(app.instance_path) / "app.db")


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


# ---- pages: example CRUD on `item`, replace with your own ---------------------------------
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    items = get_db().execute("""
        SELECT i.item_id, i.name, i.quantity, c.name AS category
        FROM item AS i JOIN category AS c ON c.category_id = i.category_id
        WHERE i.name LIKE ? ORDER BY c.name, i.name
    """, (f"%{q}%",)).fetchall()
    return render_template("index.html", items=items, q=q)


def categories():
    return get_db().execute("SELECT category_id, name FROM category ORDER BY name").fetchall()


def clean_form():
    form = {k: request.form.get(k, "").strip() for k in ("name", "category_id", "quantity", "notes")}
    errors = {}
    if not 2 <= len(form["name"]) <= 60:
        errors["name"] = "Name must be 2 to 60 characters."
    if not form["category_id"].isdigit() or get_db().execute(
            "SELECT 1 FROM category WHERE category_id = ?", (form["category_id"],)).fetchone() is None:
        errors["category_id"] = "Choose a category."
    if not form["quantity"].isdigit() or int(form["quantity"]) > 10000:
        errors["quantity"] = "Quantity must be a whole number from 0 to 10000."
    return form, errors


@app.route("/items/new", methods=["GET", "POST"])
def new_item():
    form, errors = {"name": "", "category_id": "", "quantity": "1", "notes": ""}, {}
    if request.method == "POST":
        form, errors = clean_form()
        if not errors:
            db = get_db()
            with db:
                db.execute("INSERT INTO item (name, category_id, quantity, notes) VALUES (?, ?, ?, ?)",
                           (form["name"], int(form["category_id"]), int(form["quantity"]), form["notes"] or None))
            flash("Item added.")
            return redirect(url_for("index"))
    return render_template("form.html", form=form, errors=errors, categories=categories(), editing=False)


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    row = get_db().execute("SELECT * FROM item WHERE item_id = ?", (item_id,)).fetchone()
    if row is None:
        abort(404)
    form = {"name": row["name"], "category_id": str(row["category_id"]), "quantity": str(row["quantity"]), "notes": row["notes"] or ""}
    errors = {}
    if request.method == "POST":
        form, errors = clean_form()
        if not errors:
            db = get_db()
            with db:
                db.execute("UPDATE item SET name = ?, category_id = ?, quantity = ?, notes = ? WHERE item_id = ?",
                           (form["name"], int(form["category_id"]), int(form["quantity"]), form["notes"] or None, item_id))
            flash("Item updated.")
            return redirect(url_for("index"))
    return render_template("form.html", form=form, errors=errors, categories=categories(), editing=True, item_id=item_id)


@app.route("/items/<int:item_id>/delete", methods=["POST"])
def delete_item(item_id):
    db = get_db()
    with db:
        cur = db.execute("DELETE FROM item WHERE item_id = ?", (item_id,))
    if cur.rowcount == 0:
        abort(404)
    flash("Item deleted.")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
