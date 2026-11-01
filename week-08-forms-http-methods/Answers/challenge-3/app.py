"""Challenge 3: to-do list. Every change is a POST followed by a redirect."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

TASKS = []          # each task: {"id": int, "text": str, "done": bool}
next_id = 1


def find_task(task_id):
    for t in TASKS:
        if t["id"] == task_id:
            return t
    abort(404)


@app.route("/")
def todo():
    filter_by = request.args.get("show", "all")
    shown = [t for t in TASKS
             if filter_by == "all" or (filter_by == "done") == t["done"]]
    remaining = sum(1 for t in TASKS if not t["done"])
    return render_template("todo.html", tasks=shown, remaining=remaining, filter_by=filter_by)


@app.route("/add", methods=["POST"])
def add():
    global next_id
    text = request.form.get("text", "").strip()
    if not text:
        flash("Type something first.")
    elif len(text) > 100:
        flash("Keep tasks under 100 characters.")
    else:
        TASKS.append({"id": next_id, "text": text, "done": False})
        next_id += 1
        flash("Task added.")
    return redirect(url_for("todo"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    task = find_task(task_id)
    task["done"] = not task["done"]
    return redirect(url_for("todo"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = find_task(task_id)
    TASKS.remove(task)
    flash("Task deleted.")
    return redirect(url_for("todo"))
