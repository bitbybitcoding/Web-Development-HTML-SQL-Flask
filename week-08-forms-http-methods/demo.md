# Week 8 Demo: Forms and HTTP methods

**Time:** 45 minutes. Students type along.
**Code:** [demo/](demo/): `app.py`, `templates/`, `static/style.css`

Work in `my-work/week08/`. You can copy the Week 7 `base.html` and `style.css` as a starting point.

---

## Part 1: A GET form: search (10 min)

```html
<form action="{{ url_for('search') }}" method="get">
  <label for="q">Name contains</label>
  <input type="search" id="q" name="q" value="{{ q }}">
  <button type="submit">Search</button>
</form>
```

```python
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = [s for s in STUDENTS if q.lower() in s["name"].lower()] if q else []
    return render_template("search.html", q=q, results=results)
```

Points to make:

- Submit the form and **look at the address bar**: `/search?q=tan`. The form fields became the **query string**.
- `name="q"` is what Python sees: `request.args["q"]`. The `id` and `for` only connect the label.
- Use `request.args.get("q", "")`, not `request.args["q"]`: if the field is missing, the second form crashes with **400 Bad Request**.
- `value="{{ q }}"` keeps what the user typed.
- A GET search is good: you can **bookmark** or **share** the URL.

## Part 2: The same URL, two methods: echo (10 min)

```python
@app.route("/echo", methods=["GET", "POST"])
def echo():
    return render_template("echo.html", method=request.method, args=request.args, form=request.form)
```

The page has two forms. Send each and compare:

| | GET | POST |
|---|---|---|
| Data appears | in the URL (`request.args`) | in the request body (`request.form`) |
| Meant for | asking to see something | making a change |
| Bookmarkable | yes | no |
| Repeating it | harmless | may repeat the change |
| Size limit | short (URL length) | large |

Ask: *what would happen if a "Delete my account" action used a link (GET)?* A search-engine robot or browser pre-loader could follow the link and delete accounts. **Actions that change data must be POST.**

Also: try visiting `/echo` after a POST by retyping the URL: it is a GET. Remove `"POST"` from `methods` and send the POST form: **405 Method Not Allowed**.

## Part 3: A real form with validation (15 min)

```python
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    errors = {}
    form = {"name": "", "rating": "", "comment": ""}
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        if not 2 <= len(form["name"]) <= 50:
            errors["name"] = "Please enter your name (2 to 50 characters)."
        if form["rating"] not in {"1", "2", "3", "4", "5"}:
            errors["rating"] = "Please choose a rating from 1 to 5."
        if len(form["comment"]) > 200:
            errors["comment"] = "Please keep your comment under 200 characters."
        if not errors:
            FEEDBACK.append({...})
            flash("Thank you!")
            return redirect(url_for("feedback_list"))
    return render_template("feedback.html", form=form, errors=errors)
```

The recipe, which students should learn by heart:

1. **GET** → show an empty form.
2. **POST** → read the fields, **clean** them (`strip()`), **validate** them.
3. **Errors?** → show the *same form* again with messages, and the values the user typed.
4. **No errors?** → do the work (save), `flash()` a message, then **redirect**.

Template parts: `{% if errors.name %}<p class="error">{{ errors.name }}</p>{% endif %}`, `value="{{ form.name }}"`, and for a drop-down: `{{ 'selected' if form.rating == n|string }}`.

**Never trust the form.** The `<select>` only offers 1 to 5, yet the server checks it again: a user can send anything with a script, with browser tools, or by editing the page. Validation in the browser (`required`, `type="email"`) is for convenience; validation on the server is for safety. We therefore added `novalidate` to see the server messages.

## Part 4: Post/Redirect/Get and flash messages (10 min)

**The problem.** If the POST route returns a page directly, pressing refresh asks "Resubmit the form?" and the feedback is saved twice. Try it by temporarily replacing `redirect(...)` with `return render_template("feedback_list.html", ...)`.

**The fix: Post/Redirect/Get.**

```
browser --POST /feedback--> server saves, answers "302: go to /feedback/all"
browser --GET /feedback/all--> server shows the list
```

Now refresh only repeats the harmless GET.

**Flash messages** carry a one-time message across the redirect:

```python
app.secret_key = "dev-only-change-me"     # needed: flash stores the message in a signed cookie
flash("Thank you!")
```

```html
{% for message in get_flashed_messages() %}<p class="flash">{{ message }}</p>{% endfor %}
```

Put the loop in `base.html`, so every page can show messages. Refresh once more: the message is gone (it is shown only once).

## Part 5: Stop and think (before the challenges)

1. Restart the server (save any file). What happens to the feedback list? (It is empty: it lived in a Python list in memory.) *Next week we use SQLite so it survives.*
2. Type `<b>bold</b>` as a comment. Why is it shown as text? (Jinja escapes it.)
3. Which of these should be POST: login, search, "like" button, change password, open a product page?

(Answers: login, like, change password: POST. Search and product page: GET. Login is a POST because the password must not be in the URL, which is saved in history and logs.)
