# Week 8 Challenges

Work in `my-work/week08/`. Each challenge goes in its own folder with its own `app.py`, `templates/` and `static/`. Copy `base.html` and `style.css` from the demo to save time. All data lives in Python lists for now.

---

## Challenge 1: Student finder (GET) ★★

Copy [challenges/students_data.py](challenges/students_data.py) into your folder. Build a page at `/search` with a form that sends a **GET** request with three filters:

- a text box `q`: name contains (not case-sensitive)
- a drop-down `class`: Any, 3A, 3B, 3C (build the options with a loop from the data)
- radio buttons `gender`: Any, Female, Male

Show a table of matches and a line such as `3 students found`. Rules:

- Before any search, show only the form (no "0 found" message).
- All filters can be combined, and any can be left empty.
- After searching, the form must **keep the user's choices** (text, selected option and radio button).
- Show a friendly message when nothing matches.
- A URL such as `/search?q=tan&class=3A` must work when pasted into the address bar.

---

## Challenge 2: CCA sign-up (POST and validation) ★★★

Build a sign-up form with these fields and **server-side** rules:

| Field | Input | Rule |
|-------|-------|------|
| `name` | text | 2 to 50 characters after trimming spaces |
| `class` | drop-down | must be one of 3A, 3B, 3C |
| `email` | text | must look like `name@domain.tld` (no spaces, one `@`, a dot after it) |
| `cca` | radio buttons | must be one of the six CCAs in your list |
| `agree` | checkbox | must be ticked |
| (whole form) | | the same email cannot sign up twice (not case-sensitive) |

On errors, show the form again with **a message beside each wrong field** and a summary at the top (`Please fix 2 problems below`), and **keep everything the user typed**. On success, store the member in a list, `flash` a welcome message and **redirect** to a `/members` page showing everyone.

**Test like an attacker.** Use the browser's developer tools, or write a short Python script with the `requests` library (or Flask's test client), to POST bad data directly (a CCA that is not in your list, an empty form). Does your server reject it?

---

## Challenge 3: To-do list ★★★

Build a to-do list with these pages and actions:

- `/` shows the list, how many tasks are left, and an "add task" form.
- Adding a task (POST `/add`): trims the text, refuses empty text or text over 100 characters (flash a message), then redirects to `/`.
- Each task has a **Done / Undo** button (POST `/toggle/<id>`) and a **Delete** button (POST `/delete/<id>`). Done tasks have a line through them.
- The list can be filtered with the query string: `/?show=open` and `/?show=done`.
- Unknown task ids give a 404.

Every button that changes something must be inside a small `<form method="post">`. Try to visit `/delete/1` by typing it in the address bar. What does the server say, and why is that good?

---

## Challenge 4: Quiz with a leaderboard ★★★★ (open-ended)

Copy [challenges/quiz_data.py](challenges/quiz_data.py). Build a quiz website:

**Must have**

- A start page where the player enters a name (validated), and a quiz page with all questions as radio buttons.
- Submitting the quiz is a POST that **scores** the answers. If any question is unanswered, show the quiz again with a message and keep the answers already chosen.
- A result page showing the score, using Post/Redirect/Get (refreshing must not record a second attempt).
- A review of the questions answered wrongly, with the right answer.
- A leaderboard page with the top five attempts.

**Extras (choose at least one)**

- Remember the name between pages with `session["name"]`.
- Add your own questions (at least five more) to the data.
- Shuffle the questions with `random.sample` (careful: scoring must still work).
- Add a timer or a progress bar using only HTML and CSS, or a few lines of JavaScript.
- Questions with more than one correct answer (checkboxes).

**Peer review:** swap computers and try to break each other's quiz: skip every question, submit twice, edit the HTML with the inspector. Write down what you found.
