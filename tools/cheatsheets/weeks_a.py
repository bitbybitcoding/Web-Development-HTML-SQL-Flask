"""Cheatsheet content for Weeks 1 to 6. Format: see lib.py."""

W1 = ("week-01-html-structure", "HTML structure", "Block 1: HTML", [
    ("h", "The page skeleton"),
    ("code", """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1">
  <title>Page title (shows in the tab)</title>
</head>
<body>
  ...everything the visitor sees...
</body>
</html>"""),
    ("p", "**head** = information about the page. **body** = the page itself. Tags come in pairs: `<p>` opens, `</p>` closes. Some tags have no closing tag: `<br>`, `<hr>`, `<img>`, `<meta>`."),
    ("h", "Text"),
    ("table", ["Tag", "Use"], [
        ["`<h1>` to `<h6>`", "Headings. One `h1` per page; do not skip levels"],
        ["`<p>`", "Paragraph"],
        ["`<strong>` / `<em>`", "Important (bold) / emphasis (italic)"],
        ["`<br>` / `<hr>`", "Line break / horizontal line"],
        ["`<ul>` `<ol>` `<li>`", "Bulleted list / numbered list / list item"],
        ["`<div>` / `<span>`", "Generic block / inline container (use when no better tag exists)"],
    ], [0.38, 0.62]),
    ("h", "Links and images"),
    ("code", """<a href="about.html">About us</a>
<a href="https://example.com">Another site</a>
<img src="images/cat.png" alt="A grey cat asleep">"""),
    ("bullets", [
        "**Every image needs `alt` text.** It is read aloud by screen readers and shown if the image fails to load.",
        "`href` = where a link goes. `src` = where an image comes from.",
    ]),
    ("h", "File paths (where is the file?)"),
    ("table", ["Path", "Means"], [
        ["`page.html`", "Same folder as this file"],
        ["`images/a.png`", "Inside the sub-folder `images`"],
        ["`../index.html`", "One folder up, then the file"],
        ["`https://...`", "A whole address on the web"],
    ], [0.4, 0.6]),
    ("tip", "File names: lowercase, no spaces (`my-page.html`). The home page of a site is usually called `index.html`."),
    ("h", "Semantic layout tags"),
    ("code", """<header>  site title, logo        </header>
<nav>     main links               </nav>
<main>    the unique content       </main>
<section> a themed part of a page  </section>
<article> content that stands alone</article>
<aside>   side information         </aside>
<footer>  author, contact          </footer>"""),
    ("p", "They look the same as `<div>` on screen, but they **tell browsers, search engines and screen readers what each part is**."),
    ("h", "Attributes and special characters"),
    ("bullets", [
        "`id` is unique on the page. `class` can be shared by many tags. `lang` sets the language.",
        "Write `&lt;` for `<`, `&gt;` for `>`, `&amp;` for `&`, `&quot;` for a quote, `&copy;` for the copyright sign.",
        "Attribute values go in quotes: `class=\"card\"`.",
    ]),
    ("h", "Preview in Codespaces"),
    ("code", """python3 -m http.server 8000
# then open the forwarded port 8000"""),
    ("p", "Save the file, then refresh the preview. Stop the server with Ctrl+C."),
    ("h", "Top mistakes"),
    ("bullets", [
        "A missing closing tag or a missing quote: the page looks wrong from that point.",
        "Wrong file path: broken image icon or a \"404 Not Found\".",
        "Opening a tag in one order and closing in another. Close the **inner** tag first: `<p><em>x</em></p>`.",
        "Using `<br>` many times to make space. Use CSS (Week 2) instead.",
        "Skipping `alt`. Always describe the picture.",
    ]),
])

W2 = ("week-02-tables-forms-css", "Tables, forms and CSS", "Block 1: HTML", [
    ("h", "Tables"),
    ("code", """<table>
  <tr><th>Day</th><th>Subject</th></tr>
  <tr><td>Mon</td><td>Maths</td></tr>
  <tr><td colspan="2">Merged cell</td></tr>
</table>"""),
    ("bullets", [
        "`<tr>` row, `<th>` heading cell, `<td>` data cell.",
        "`colspan=\"2\"` merges cells to the right; `rowspan=\"2\"` merges cells downwards. Count carefully: every row must add up to the same number of columns.",
        "Use tables for **data**, never for page layout.",
    ]),
    ("h", "Forms"),
    ("code", """<form action="/submit" method="get">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>
  <button type="submit">Send</button>
</form>"""),
    ("table", ["Element", "Notes"], [
        ["`<input type=\"text\">`", "One line of text. Also `email`, `password`, `number`, `date`"],
        ["`<input type=\"radio\">`", "Choose one. Same `name`, different `value`"],
        ["`<input type=\"checkbox\">`", "Tick any. Sends nothing if unticked"],
        ["`<select>` `<option>`", "Drop-down list"],
        ["`<textarea>`", "Several lines of text"],
        ["`<button>`", "Submits the form (`type=\"submit\"`)"],
    ], [0.45, 0.55]),
    ("bullets", [
        "**`name`** is the key the data is sent under. No `name` means the field is not sent.",
        "**`for` + `id`** join a label to its input: tapping the label focuses the field.",
        "`required`, `minlength`, `maxlength`, `min`, `max`, `pattern`, `placeholder` help the user, but are not security.",
    ]),
    ("h", "GET and POST"),
    ("table", ["", "GET", "POST"], [
        ["Data goes", "in the URL (`?name=Mei`)", "in the request body"],
        ["Use for", "searching, looking", "changing something"],
        ["Bookmark?", "yes", "no"],
    ], [0.24, 0.38, 0.38]),
    ("h", "CSS: selecting and styling"),
    ("code", """p { color: #333; }           /* every <p> */
.card { background: #eef; }  /* class="card" */
#logo { width: 120px; }      /* id="logo" */
nav a:hover { color: red; }  /* hover state */"""),
    ("code", """<!-- in the head: -->
<link rel="stylesheet" href="style.css">"""),
    ("table", ["Property", "Effect"], [
        ["`color`, `background-color`", "Text / background colour (`#1f4e8c`, `red`)"],
        ["`font-family`, `font-size`", "Font; `1rem` = the browser's base size (16px)"],
        ["`text-align`", "`left`, `center`, `right`"],
        ["`margin` / `padding`", "Space outside / inside the border"],
        ["`border`", "`1px solid #ccc`"],
        ["`width`, `max-width`", "Size; `max-width` stops lines getting too long"],
    ], [0.42, 0.58]),
    ("h", "The box model"),
    ("p", "From the inside out: **content → padding → border → margin**. Add `box-sizing: border-box;` so that `width` includes the padding and border."),
    ("h", "Flexbox: a row of boxes"),
    ("code", """.row {
  display: flex;
  gap: 1rem;            /* space between items */
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;      /* wrap on small screens */
}"""),
    ("tip", "iPad tips: text in form fields at least 16px (`1rem`) so Safari does not zoom in; buttons and links at least 44px tall; and always keep the `viewport` meta tag."),
])

W3 = ("week-03-select", "SELECT: querying one table", "Block 2: SQL", [
    ("h", "Start the SQLite shell"),
    ("code", """sqlite3 school.db
.tables              -- list tables
.schema students     -- show a table's definition
.headers on          -- show column names
.mode column         -- tidy output
.read file.sql       -- run a file of SQL
.quit"""),
    ("p", "Lines starting with a dot are shell commands (no semicolon). **SQL statements end with `;`**."),
    ("h", "The school database"),
    ("code", """students(student_id, name, class, gender, dob, email)
subjects(subject_id, name, teacher)
scores(student_id, subject_id, score)
ccas(cca_id, name, category, day)
student_cca(student_id, cca_id, role)"""),
    ("h", "SELECT: the pattern"),
    ("code", """SELECT   columns
FROM     table
WHERE    condition on each row
ORDER BY column [ASC|DESC]
LIMIT    n;"""),
    ("p", "`SELECT *` = every column. `SELECT DISTINCT class` = no repeats. `SELECT name AS student` renames a column in the output."),
    ("h", "WHERE: conditions"),
    ("table", ["Write", "Meaning"], [
        ["`=  !=  <  >  <=  >=`", "Compare. One `=` in SQL"],
        ["`AND`  `OR`  `NOT`", "Combine. Use brackets with mixed AND/OR"],
        ["`BETWEEN 50 AND 70`", "Inclusive range"],
        ["`IN ('3A','3B')`", "Matches any in the list"],
        ["`LIKE 'T%'`", "Pattern: `%` any characters, `_` one character"],
        ["`IS NULL` / `IS NOT NULL`", "Missing value test"],
    ], [0.45, 0.55]),
    ("code", """SELECT name, class FROM students
WHERE class = '3A' AND name LIKE 'T%'
ORDER BY name;"""),
    ("h", "NULL means \"unknown\""),
    ("bullets", [
        "`score = NULL` **never matches**, not even NULL. Use `score IS NULL`.",
        "Any arithmetic or comparison with NULL gives NULL (not true). Rows where the condition is NULL are left out.",
        "SQLite sorts NULL **first** in `ORDER BY ... ASC`.",
    ]),
    ("h", "Useful extras"),
    ("code", """SELECT name, score + 5 AS boosted FROM ...;
SELECT UPPER(name), LENGTH(name) FROM students;
SELECT name FROM students
ORDER BY class DESC, name ASC LIMIT 5;"""),
    ("h", "Clause order you must write"),
    ("p", "**SELECT → FROM → WHERE → ORDER BY → LIMIT**"),
    ("tip", "Text is in **single quotes** (`'3A'`). Double quotes are for column or table names. In SQLite, `=` on text is **case-sensitive** (`'mei' != 'Mei'`); `LIKE` ignores the case of English letters."),
    ("h", "Top mistakes"),
    ("bullets", [
        "Forgetting the `;` (the shell waits with a `...>` prompt).",
        "Using `==` or `= NULL`.",
        "Putting `ORDER BY` before `WHERE`.",
        "`LIKE '%T'` when you wanted names that **start** with T (`'T%'`).",
    ]),
])

W4 = ("week-04-aggregates-joins", "Aggregates and joins", "Block 2: SQL", [
    ("h", "Aggregate functions"),
    ("table", ["Function", "Returns"], [
        ["`COUNT(*)`", "Number of rows"],
        ["`COUNT(col)`", "Number of rows where `col` is **not NULL**"],
        ["`SUM(col)` `AVG(col)`", "Total / mean (NULLs ignored)"],
        ["`MIN(col)` `MAX(col)`", "Smallest / largest"],
        ["`ROUND(x, 1)`", "Round to 1 decimal place"],
    ], [0.4, 0.6]),
    ("code", """SELECT COUNT(*) AS students,
       ROUND(AVG(score), 1) AS average
FROM scores;"""),
    ("h", "GROUP BY: one result row per group"),
    ("code", """SELECT class, COUNT(*) AS n
FROM students
GROUP BY class
ORDER BY n DESC;"""),
    ("bullets", [
        "Every column in `SELECT` must be **grouped** or **inside an aggregate**.",
        "`WHERE` filters **rows** before grouping. `HAVING` filters **groups** after.",
    ]),
    ("code", """SELECT subject_id, AVG(score) AS avg
FROM scores
WHERE score IS NOT NULL      -- rows
GROUP BY subject_id
HAVING AVG(score) > 66;      -- groups"""),
    ("h", "How SQL really reads a query"),
    ("p", "**FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT**. That is why a column alias cannot be used in `WHERE`."),
    ("h", "JOIN: combine tables"),
    ("code", """SELECT s.name, su.name AS subject, sc.score
FROM scores AS sc
JOIN students AS s  ON s.student_id  = sc.student_id
JOIN subjects AS su ON su.subject_id = sc.subject_id
WHERE sc.score >= 90;"""),
    ("bullets", [
        "`ON` says how rows match: usually **foreign key = primary key**.",
        "Give tables short **aliases** (`AS s`) and write `s.name` so it is clear which `name`.",
        "Forget the `ON`, and you get every combination of rows (a \"cross join\").",
    ]),
    ("table", ["Join", "Keeps"], [
        ["`JOIN` (inner)", "Only rows that match on both sides"],
        ["`LEFT JOIN`", "**All** rows from the left table; NULLs where there is no match"],
    ], [0.35, 0.65]),
    ("h", "Find rows with no match (anti-join)"),
    ("code", """SELECT st.name
FROM students AS st
LEFT JOIN student_cca AS sc
       ON sc.student_id = st.student_id
WHERE sc.student_id IS NULL;   -- in no CCA"""),
    ("h", "Count with LEFT JOIN"),
    ("code", """SELECT c.name, COUNT(sc.student_id) AS members
FROM ccas AS c
LEFT JOIN student_cca AS sc ON sc.cca_id = c.cca_id
GROUP BY c.cca_id;"""),
    ("tip", "Count a column from the **right** table (`COUNT(sc.student_id)`), not `COUNT(*)`. `COUNT(*)` would count the empty club as 1."),
    ("h", "Subqueries"),
    ("code", """SELECT name FROM students
WHERE student_id IN
  (SELECT student_id FROM scores WHERE score = 100);

SELECT name, score FROM scores
WHERE score > (SELECT AVG(score) FROM scores);"""),
])

W5 = ("week-05-database-design", "Database design: ER diagrams and normalisation", "Block 2: SQL", [
    ("h", "From a description to a design"),
    ("bullets", [
        "**Entity** = a thing we store data about (student, CCA). It becomes a **table**.",
        "**Attribute** = a detail of an entity. It becomes a **column**.",
        "**Primary key (PK)** = identifies one row. Never NULL, never repeated.",
        "**Foreign key (FK)** = a column that holds another table's primary key.",
        "**Relationship** = how entities connect.",
    ]),
    ("h", "Types of relationship"),
    ("table", ["Type", "Example", "In tables"], [
        ["One-to-one", "Student : locker", "FK on either side (unique)"],
        ["One-to-many", "Class : students", "FK on the **many** side"],
        ["Many-to-many", "Students : CCAs", "A **junction table** with two FKs"],
    ], [0.24, 0.36, 0.40]),
    ("code", """student_cca(student_id FK, cca_id FK, role)
PK = (student_id, cca_id)       -- a composite key"""),
    ("h", "ER diagram (crow's foot)"),
    ("code", """STUDENT ||--o{ STUDENT_CCA }o--|| CCA
  one student has zero or more memberships
  one CCA has zero or more memberships"""),
    ("p", "`||` exactly one · `o|` zero or one · `o{` zero or many · `|{` one or many."),
    ("h", "Why not one big table? Anomalies"),
    ("bullets", [
        "**Update:** change a value in one row but not the other copies.",
        "**Insert:** cannot record a fact until another fact exists.",
        "**Delete:** removing one fact loses a different fact.",
        "Root cause: **redundancy**, the same fact stored many times.",
    ]),
    ("h", "Normalisation: the three normal forms"),
    ("table", ["Form", "Rule", "Fix"], [
        ["**1NF**", "Every cell holds **one** value; no repeating groups", "Put each value in its own row (maybe a new table)"],
        ["**2NF**", "1NF, and no **partial dependency**: no column depends on only **part** of a composite key", "Move it to a table keyed by that part"],
        ["**3NF**", "2NF, and no **transitive dependency**: no non-key column depends on another non-key column", "Move both to their own table"],
    ], [0.12, 0.50, 0.38]),
    ("tip", "Rule of thumb: every non-key attribute must depend on **the key, the whole key, and nothing but the key**."),
    ("h", "Worked example"),
    ("code", """ORDERS(order_no, item_code, item_name, qty)
PK (order_no, item_code)
item_name depends only on item_code -> 2NF
becomes:
  ORDER_LINE(order_no, item_code, qty)
  ITEM(item_code PK, item_name)"""),
    ("code", """STUDENT(id, name, class, class_teacher)
class_teacher depends on class -> 3NF
becomes:
  STUDENT(id, name, class FK)
  CLASS(class PK, class_teacher)"""),
    ("h", "Process"),
    ("bullets", [
        "List the nouns (entities) and their details (attributes).",
        "Find relationships; draw the ER diagram; resolve many-to-many.",
        "Choose primary keys; add foreign keys on the many side.",
        "Check 1NF, 2NF, 3NF.",
        "Do **not** store what you can calculate (age, totals).",
    ]),
])

W6 = ("week-06-ddl-dml-python-sqlite", "DDL, DML and Python with SQLite", "Block 2: SQL", [
    ("h", "DDL defines structure, DML changes data"),
    ("code", """CREATE TABLE member (
  member_id INTEGER PRIMARY KEY,
  name   TEXT NOT NULL CHECK (length(name) >= 2),
  email  TEXT UNIQUE,
  joined TEXT NOT NULL DEFAULT (date('now'))
);
ALTER TABLE member ADD COLUMN phone TEXT;
DROP TABLE member;          -- deletes the table!"""),
    ("table", ["Constraint", "Rule"], [
        ["`PRIMARY KEY`", "Unique, identifies the row"],
        ["`NOT NULL`", "A value is required"],
        ["`UNIQUE`", "No two rows the same"],
        ["`CHECK (cond)`", "Condition must be true"],
        ["`DEFAULT x`", "Used when no value is given"],
        ["`FOREIGN KEY (c) REFERENCES t (c)`", "Must match a row in `t`"],
    ], [0.5, 0.5]),
    ("tip", "Turn foreign keys on in **every** session or connection: `PRAGMA foreign_keys = ON;`. SQLite does not enforce them otherwise."),
    ("h", "DML: INSERT, UPDATE, DELETE"),
    ("code", """INSERT INTO member (name, email)
VALUES ('Mei Lin', 'mei@example.com');
UPDATE member SET email = 'new@example.com'
WHERE member_id = 1;
DELETE FROM member WHERE member_id = 1;"""),
    ("p", "**Always write the `WHERE`** on UPDATE and DELETE; without it every row changes. Test it as a `SELECT` first. Delete **child** rows before the parent."),
    ("h", "Python and SQLite"),
    ("code", """import sqlite3
con = sqlite3.connect("my-work/library.db")
con.row_factory = sqlite3.Row   # row["title"]
con.execute("PRAGMA foreign_keys = ON")

cur = con.execute(
    "SELECT * FROM book WHERE author = ?", (author,))
rows = cur.fetchall()           # list of rows
one  = cur.fetchone()           # one row or None

with con:                       # commit, or roll back
    con.execute("INSERT INTO book (title, author) "
                "VALUES (?, ?)", (title, author))
con.close()"""),
    ("bullets", [
        "`?` placeholders take **values** (never table or column names).",
        "A one-value tuple needs a comma: `(author,)`.",
        "`cur.lastrowid` = the new id. `cur.rowcount` = rows changed.",
        "`con.commit()` saves; without it, changes are lost. `with con:` commits or rolls back for you.",
    ]),
    ("h", "SQL injection"),
    ("code", """# DANGEROUS: user text becomes part of the SQL
con.execute(f"SELECT * FROM users WHERE name='{n}'")
#  n = ' OR '1'='1      -> every user returned
#  n = x' --   -> the rest becomes a comment

# SAFE: the value is passed separately
con.execute(
    "SELECT * FROM users WHERE name = ?", (n,))"""),
    ("p", "LIKE with a placeholder: `WHERE name LIKE ?` with `(f\"%{term}%\",)`."),
    ("h", "Transactions"),
    ("p", "A group of changes that must **all** happen or **none**. If an error occurs inside `with con:`, every change in the block is undone."),
    ("h", "Top mistakes"),
    ("bullets", [
        "f-strings or `+` in SQL. Use `?`.",
        "Forgetting to commit.",
        "Forgetting `PRAGMA foreign_keys = ON`.",
        "`UPDATE`/`DELETE` with no `WHERE`.",
    ]),
])
