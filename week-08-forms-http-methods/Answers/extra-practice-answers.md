# Week 8 Extra Practice: Answers

## 1. Persist to a file

Code: [extra_practice.py](extra_practice.py) (`load_tasks`, `save_tasks`). Call `save_tasks(TASKS)` after every `add`, `toggle` and `delete`, and start with `TASKS = load_tasks()`.

Two problems with a file instead of a database (any two):

- **Two requests at the same time** can both read the old file, change it, and write it back, so one change is lost (a *race condition*). A database handles concurrent changes safely with transactions.
- The **whole file is rewritten** for each change, which gets slow as it grows; a database changes only the row concerned.
- **Searching and sorting** need the whole file to be loaded; a database has indexes and `WHERE`.
- No **constraints** (unique, foreign keys) to protect the data; a crash while writing can corrupt the file.

## 2. A password-change form

Code: [extra_practice.py](extra_practice.py) (`password_errors`). Passwords are **not** put back in the form because they would appear in the page's HTML source, where someone looking at the screen or a cached copy of the page could read them. The old password is never shown. In a real site the password is stored only as a **hash** (Week 11 mentions this).

## 3. Method experiments

`request.values` combines `request.args` and `request.form`. When the same field is in both, the **URL value wins** (`args` is searched first): in the self-test, `/mystery?who=url` with a body `who=body` gives `request.values["who"] == "url"`, while `request.form["who"]` is `"body"`. Lesson: read from the place you expect; do not use `request.values`.

## 4. Dynamic form from data

Code: [extra_practice.py](extra_practice.py) (`/pizza`). `request.form.getlist("topping")` returns **all** the ticked values as a list. The solution ignores any topping that is not in the dictionary (a user can invent values) and rejects more than four.

## 5. Written questions

1. Any two [1 each]: GET sends data in the URL (query string), POST in the body of the request; GET is for retrieving, POST for changing data; GET can be bookmarked and repeated safely, POST should not be repeated; GET has a length limit; GET data is stored in history and logs.
2. (a) `request.args["user"]` (or `request.args.get("user")`). (b) `request.form["user"]` (or `.get("user")`). [1 each]
3. Attributes such as `required` and `maxlength` are checked **in the browser**, which the user controls: they can be removed with developer tools or bypassed by sending the request with a script. Only the server can enforce rules, so any rule that matters must be checked there. [2]
4. After a successful POST, the server does not return a page directly: it sends a **redirect** to a GET URL, and the browser then requests that page. [1] Without it, refreshing the result page would send the POST again (the browser warns about resubmitting), duplicating the action, such as saving the same record twice. [1] With it, refreshing only repeats a harmless GET. [1]
5. Problems [any two, 1 each]: a link is a GET, so anything that follows links (search-engine crawlers, browser pre-fetching, a malicious image tag on another site) could delete records; there is no check that the user is allowed to delete record 5; there is no confirmation; GET requests are stored in history and logs. Better design [1]: a `<form method="post" action="/delete/5">` with a button, a check that the user is logged in and allowed, and (ideally) a CSRF token.
6. A CSRF attack makes a logged-in user's browser send a request to a site without the user meaning to (for example a hidden form on another page that posts to the bank's "transfer" URL, and the browser attaches the user's login cookie). [2] Defence (any one) [1]: a secret random **CSRF token** in each form that the server checks; cookies with `SameSite=Lax/Strict`; checking the `Origin`/`Referer` header; asking for the password again for sensitive actions.
7. It lets the user correct a mistake without retyping everything. [1] Jinja automatically **escapes** `<`, `>`, `"` and `&`, so a value such as `"><script>...` cannot break out of the attribute and run; with string concatenation the quote ends the attribute and the script becomes part of the page (cross-site scripting). [1]
