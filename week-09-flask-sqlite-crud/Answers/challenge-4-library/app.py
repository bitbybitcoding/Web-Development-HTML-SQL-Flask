"""Week 9, Challenge 4: the Week 6 library as a web app.

Run from this folder with:   flask --app app run --debug
The first run creates instance/library.db from library_seed.sql. Delete instance/ to start again.
"""
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config.setdefault("DATABASE", str(Path(app.instance_path) / "library.db"))
app.config.setdefault("TODAY", None)            # tests can set a fixed date
LOAN_DAYS = 14
SEED = Path(__file__).with_name("library_seed.sql")


# ---- database helpers -------------------------------------------------------------
def get_db():
    if "db" not in g:
        path = Path(app.config["DATABASE"])
        path.parent.mkdir(parents=True, exist_ok=True)
        first_time = not path.exists()
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        if first_time:
            g.db.executescript(SEED.read_text())
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def today():
    return app.config["TODAY"] or date.today().isoformat()


# ---- READ -------------------------------------------------------------------------
BOOKS_SQL = """
    SELECT b.book_id, b.title, b.author,
           l.loan_id, l.borrower, l.due_on,
           CASE WHEN l.loan_id IS NULL THEN 'available'
                WHEN l.due_on < :today THEN 'overdue'
                ELSE 'on loan' END AS status
    FROM book AS b
    LEFT JOIN loan AS l ON l.book_id = b.book_id AND l.returned_on IS NULL
    WHERE (b.title LIKE :q OR b.author LIKE :q)
"""


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    sql = f"SELECT * FROM ({BOOKS_SQL}) "
    params = {"today": today(), "q": f"%{q}%"}
    if status in ("available", "on loan", "overdue"):
        sql += "WHERE status = :status "
        params["status"] = status
    sql += "ORDER BY title"
    books = get_db().execute(sql, params).fetchall()
    return render_template("index.html", books=books, q=q, status=status)


def get_book_or_404(book_id):
    book = get_db().execute("SELECT * FROM book WHERE book_id = ?", (book_id,)).fetchone()
    if book is None:
        abort(404)
    return book


@app.route("/books/<int:book_id>")
def book(book_id):
    db = get_db()
    b = get_book_or_404(book_id)
    history = db.execute("SELECT * FROM loan WHERE book_id = ? ORDER BY borrowed_on DESC, loan_id DESC", (book_id,)).fetchall()
    current = next((l for l in history if l["returned_on"] is None), None)
    return render_template("book.html", b=b, history=history, current=current, today=today())


@app.route("/overdue")
def overdue():
    rows = get_db().execute("""
        SELECT b.book_id, b.title, l.borrower, l.due_on,
               CAST(julianday(?) - julianday(l.due_on) AS INTEGER) AS days_late
        FROM loan AS l JOIN book AS b ON b.book_id = l.book_id
        WHERE l.returned_on IS NULL AND l.due_on < ?
        ORDER BY days_late DESC
    """, (today(), today())).fetchall()
    return render_template("overdue.html", rows=rows)


@app.route("/stats")
def stats():
    db = get_db()
    popular = db.execute("""
        SELECT b.title, COUNT(l.loan_id) AS times
        FROM book AS b LEFT JOIN loan AS l ON l.book_id = b.book_id
        GROUP BY b.book_id ORDER BY times DESC, b.title LIMIT 5
    """).fetchall()
    readers = db.execute("""
        SELECT borrower, COUNT(*) AS loans FROM loan GROUP BY borrower ORDER BY loans DESC, borrower
    """).fetchall()
    never = db.execute("""
        SELECT title FROM book WHERE book_id NOT IN (SELECT book_id FROM loan) ORDER BY title
    """).fetchall()
    return render_template("stats.html", popular=popular, readers=readers, never=never)


# ---- CREATE / UPDATE / DELETE books ------------------------------------------------
def clean_book_form():
    form = {k: request.form.get(k, "").strip() for k in ("title", "author")}
    errors = {}
    if not 1 <= len(form["title"]) <= 120:
        errors["title"] = "Title is required (up to 120 characters)."
    if not 2 <= len(form["author"]) <= 80:
        errors["author"] = "Author is required (2 to 80 characters)."
    return form, errors


@app.route("/books/new", methods=["GET", "POST"])
def new_book():
    form, errors = {"title": "", "author": ""}, {}
    if request.method == "POST":
        form, errors = clean_book_form()
        if not errors:
            db = get_db()
            try:
                with db:
                    cur = db.execute("INSERT INTO book (title, author) VALUES (?, ?)", (form["title"], form["author"]))
            except sqlite3.IntegrityError:
                errors["title"] = "That title by that author is already in the library."
            else:
                flash("Book added.")
                return redirect(url_for("book", book_id=cur.lastrowid))
    return render_template("book_form.html", form=form, errors=errors, editing=False)


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    b = get_book_or_404(book_id)
    form, errors = {"title": b["title"], "author": b["author"]}, {}
    if request.method == "POST":
        form, errors = clean_book_form()
        if not errors:
            db = get_db()
            try:
                with db:
                    db.execute("UPDATE book SET title = ?, author = ? WHERE book_id = ?", (form["title"], form["author"], book_id))
            except sqlite3.IntegrityError:
                errors["title"] = "That title by that author is already in the library."
            else:
                flash("Book updated.")
                return redirect(url_for("book", book_id=book_id))
    return render_template("book_form.html", form=form, errors=errors, editing=True, book_id=book_id)


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    b = get_book_or_404(book_id)
    db = get_db()
    loans = db.execute("SELECT COUNT(*) FROM loan WHERE book_id = ?", (book_id,)).fetchone()[0]
    if loans:
        flash(f"'{b['title']}' has {loans} loan record{'s' if loans != 1 else ''}, so it cannot be deleted.")
        return redirect(url_for("book", book_id=book_id))
    with db:
        db.execute("DELETE FROM book WHERE book_id = ?", (book_id,))
    flash("Book deleted.")
    return redirect(url_for("index"))


# ---- borrow and return ---------------------------------------------------------------
@app.route("/books/<int:book_id>/borrow", methods=["POST"])
def borrow(book_id):
    get_book_or_404(book_id)
    db = get_db()
    borrower = request.form.get("borrower", "").strip()
    if not 2 <= len(borrower) <= 40:
        flash("Enter the borrower's name (2 to 40 characters).")
    elif db.execute("SELECT 1 FROM loan WHERE book_id = ? AND returned_on IS NULL", (book_id,)).fetchone():
        flash("That book is already on loan.")
    else:
        due = (date.fromisoformat(today()) + timedelta(days=LOAN_DAYS)).isoformat()
        with db:
            db.execute("INSERT INTO loan (book_id, borrower, borrowed_on, due_on) VALUES (?, ?, ?, ?)",
                       (book_id, borrower, today(), due))
        flash(f"Lent to {borrower}. Due on {due}.")
    return redirect(url_for("book", book_id=book_id))


@app.route("/books/<int:book_id>/return", methods=["POST"])
def return_book(book_id):
    get_book_or_404(book_id)
    db = get_db()
    with db:
        cur = db.execute("UPDATE loan SET returned_on = ? WHERE book_id = ? AND returned_on IS NULL", (today(), book_id))
    flash("Book returned." if cur.rowcount else "That book was not on loan.")
    return redirect(url_for("book", book_id=book_id))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
