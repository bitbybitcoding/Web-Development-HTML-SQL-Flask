"""Week 8 extra practice 1 (JSON persistence), 2 (password form), 3 (mystery) and 4 (pizza).
Run `flask --app extra_practice run --debug` from this folder, or run the self-test with `python3 extra_practice.py`.
"""
import json
import re
from pathlib import Path

from flask import Flask, flash, redirect, render_template_string, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

# ---- 1. JSON persistence (use FILE = Path("tasks.json") in a real app) ------------
FILE = Path(__file__).with_name("tasks_demo.json")


def load_tasks():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def save_tasks(tasks):
    FILE.write_text(json.dumps(tasks, indent=2))


# ---- 2. Password change ----------------------------------------------------------
CURRENT_PASSWORD = "oldpass1"


def password_errors(old, new, confirm):
    errors = []
    if old != CURRENT_PASSWORD:
        errors.append("The old password is not correct.")
    if len(new) < 8:
        errors.append("The new password must be at least 8 characters.")
    if not re.search(r"\d", new) or not re.search(r"[A-Za-z]", new):
        errors.append("The new password must contain at least one letter and one digit.")
    if new == old:
        errors.append("The new password must differ from the old one.")
    if new != confirm:
        errors.append("The two new passwords do not match.")
    return errors


PASSWORD_PAGE = """
<h1>Change password</h1>
{% for e in errors %}<p class="error">{{ e }}</p>{% endfor %}
<form method="post">
  <label>Old <input type="password" name="old"></label>
  <label>New <input type="password" name="new"></label>
  <label>Confirm <input type="password" name="confirm"></label>
  <button>Change</button>
</form>
"""


@app.route("/password", methods=["GET", "POST"])
def password():
    errors = []
    if request.method == "POST":
        errors = password_errors(request.form.get("old", ""), request.form.get("new", ""), request.form.get("confirm", ""))
        if not errors:
            flash("Password changed.")      # a real site would save a *hash* of the new password
            return redirect(url_for("password"))
    return render_template_string(PASSWORD_PAGE, errors=errors)   # inputs are not refilled on purpose


# ---- 3. Mystery ------------------------------------------------------------------
@app.route("/mystery", methods=["GET", "POST"])
def mystery():
    return {
        "method": request.method,
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "values": request.values.to_dict(),
        "user_agent": request.headers.get("User-Agent"),
    }


# ---- 4. Pizza order --------------------------------------------------------------
TOPPINGS = {"cheese": 1.5, "mushroom": 1.0, "pineapple": 0.5, "pepperoni": 2.0, "olives": 1.0}
BASE_PRICE = 8.0


@app.route("/pizza", methods=["GET", "POST"])
def pizza():
    error, total, chosen = None, None, []
    if request.method == "POST":
        chosen = [t for t in request.form.getlist("topping") if t in TOPPINGS]   # ignore invented toppings
        if len(chosen) > 4:
            error = "Choose at most 4 toppings."
        else:
            total = BASE_PRICE + sum(TOPPINGS[t] for t in chosen)
    page = """
    <form method="post">
      {% for t, price in toppings.items() %}
      <label><input type="checkbox" name="topping" value="{{ t }}" {{ 'checked' if t in chosen }}> {{ t }} (${{ '%.2f'|format(price) }})</label>
      {% endfor %}
      <button>Order</button>
    </form>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    {% if total is not none %}<p>Total: ${{ '%.2f'|format(total) }}</p>{% endif %}
    """
    return render_template_string(page, toppings=TOPPINGS, chosen=chosen, error=error, total=total)


if __name__ == "__main__":
    c = app.test_client()
    assert password_errors("oldpass1", "newpass22", "newpass22") == []
    assert len(password_errors("wrong", "short", "different")) == 4
    assert "do not match" in c.post("/password", data={"old": "oldpass1", "new": "abcdefg1", "confirm": "x"}).get_data(as_text=True)
    assert c.post("/password", data={"old": "oldpass1", "new": "abcdefg1", "confirm": "abcdefg1"}).status_code == 302
    r = c.post("/mystery?a=1&who=url", data={"who": "body"}).get_json()
    assert r["args"] == {"a": "1", "who": "url"} and r["form"] == {"who": "body"} and r["values"]["who"] == "url"
    assert "Total: $11.50" in c.post("/pizza", data={"topping": ["cheese", "pepperoni"]}).get_data(as_text=True)
    assert "$8.00" in c.post("/pizza", data={"topping": ["gold"]}).get_data(as_text=True)
    assert "at most 4" in c.post("/pizza", data={"topping": list(TOPPINGS)}).get_data(as_text=True)
    save_tasks([{"id": 1, "text": "x"}]); assert load_tasks() == [{"id": 1, "text": "x"}]; FILE.unlink()
    print("extra_practice.py: all checks passed")
