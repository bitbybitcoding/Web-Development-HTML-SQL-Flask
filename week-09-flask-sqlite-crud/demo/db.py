"""Database helpers used by the Week 9 demo (and reused by the challenges).

Every request gets its own connection through flask.g, and it is closed afterwards.
The app works on a COPY of school.db (instance/school.db), so the original starter database is never damaged.
"""
import shutil
import sqlite3
from pathlib import Path

from flask import current_app, g


def find_seed():
    """Walk up from this file until we find the starter school.db in the repository root."""
    for folder in Path(__file__).resolve().parents:
        if (folder / "school.db").exists():
            return folder / "school.db"
    raise FileNotFoundError("Cannot find school.db. Is this file inside the course repository?")


def init_app(app, seed=None):
    """Call once after creating the app. Copies the seed database the first time."""
    app.config.setdefault("DATABASE", str(Path(app.instance_path) / "school.db"))
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    if not Path(app.config["DATABASE"]).exists():
        shutil.copy(seed or find_seed(), app.config["DATABASE"])
    app.teardown_appcontext(close_db)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row            # rows behave like dictionaries: row["name"]
        g.db.execute("PRAGMA foreign_keys = ON")   # must be switched on for EVERY connection
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
