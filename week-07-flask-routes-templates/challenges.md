# Week 7 Challenges

Work in `my-work/week07/`. Each challenge goes in its own folder (`challenge-1/`, `challenge-2/` and so on) with its own `app.py`. Run with `flask --app app run --debug` **from inside that folder**, and stop the previous server first (Ctrl+C).

---

## Challenge 1: Hello, Flask ★

Build an app with these pages. Each page returns a little HTML (headings and links are fine):

| URL | Shows |
|-----|-------|
| `/` | a heading and links to all the other pages |
| `/about` | a short paragraph about you |
| `/time` | the current time and date (use `datetime.now().strftime(...)`) |
| `/dice` | a random number from 1 to 6, with a link to roll again |
| `/hello/<name>` | `Hello, Name!` with the name in title case |

**Test yourself:** visit `/hello/<script>x` or `/hello/<i>Amy`. What do you see? Fix it so that the text is shown, not run (hint: `from markupsafe import escape`).

---

## Challenge 2: Routes with variables ★★

Build these routes. Use the right *converter* for each one.

| URL | Shows |
|-----|-------|
| `/add/<a>/<b>` | `2 + 3 = 5` for `/add/2/3` |
| `/area/<radius>` | the area of a circle, to 2 decimal places (π × r²) |
| `/day/<n>` | the name of the nth day of the week (1 = Monday). Any other number gives a **404** |
| `/shout/<text>` | the text in capitals, as a heading, with `!` at the end |

Questions to answer in a comment at the top of your file:

1. What happens when you visit `/add/2/x`? Why?
2. What happens when you visit `/area/2`? And `/area/2.0`? Why? (Look up the `float` converter.)

---

## Challenge 3: Class results with templates ★★★

Copy [challenges/challenge-3/app.py](challenges/challenge-3/app.py) to `my-work/week07/challenge-3/`. It has the data and five TODOs. Build:

1. A **`base.html`** with a navigation bar, a footer and `{% block %}`s for the title and the content. Link a `static/style.css` that you write yourself (at least: a font, nav colours, a styled table).
2. **`/`**: a home page showing the number of students.
3. **`/students`**: a table of all students with name, class and **average score**. Calculate the average in Python (a function), not by hand. Rows with an average of 70 or more get a CSS class `good` with a green background.
4. **`/students/<int:student_id>`**: the detail page, with every subject and score as a list. A score below 50 shows `(needs help)`. An unknown id gives a **404**.
5. **`/class/<code>`**: only that class's students (reuse the table template!). Make `3b` work as well as `3B`. An unknown class gives a 404.
6. A **custom 404 page** that extends the base and links back home, returned with the status code 404.

Every link must use `url_for`, never typed-out paths.

---

## Challenge 4: CCA showcase website ★★★★ (open-ended)

Design a website that helps a new Secondary 1 student discover the school's CCAs. Copy [challenges/cca_data.py](challenges/cca_data.py) into your folder and `from cca_data import CCAS`.

**Must have**

- A home page, an "all CCAs" page and an "about" page.
- A **detail page for each CCA** from one route and one template (`/ccas/<slug>`).
- A page that lists CCAs of **one category** (`/category/<name>`).
- A base template, a static stylesheet and `url_for` for every link.
- A friendly custom 404 page.
- Something that changes according to the data using `{% if %}` (for example, a "New club" message when a CCA has no members yet).

**Choose at least two extras**

- Show "Also on Fridays" on a detail page: other CCAs on the same day.
- Navigation links built from the categories with a loop, so adding a CCA in the data adds the link automatically.
- A "biggest CCA" feature on the home page.
- A search page using the query string: `/search?q=club`.
- A design you are proud of: colours, cards, a responsive layout that works on an iPad.

**Peer review (last 5 minutes):** swap with a neighbour and try to break their site: odd URLs, a long name, missing data. Write down one thing that works well and one thing to improve.
