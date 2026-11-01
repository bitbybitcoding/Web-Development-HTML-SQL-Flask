# Week 2 Demo: Tables, forms and basic CSS

**Time:** 45 minutes. Students type along.
**Finished code:** [demo/timetable.html](demo/timetable.html), [demo/register.html](demo/register.html), [demo/style.css](demo/style.css), [demo/echo_server.py](demo/echo_server.py)

**Set-up:** students build in their own folder, `week-02-tables-forms-css/my-demo/`. Start the echo server from the repository root, pointing it at that folder, so students can see what their forms send:

```bash
python3 week-02-tables-forms-css/demo/echo_server.py week-02-tables-forms-css/my-demo
```

(Leave out the folder name to serve the finished demo files instead.) The server also works as an ordinary file server for pages that do not submit anything.

---

## Part 1: Tables (10 min)

Build a small timetable. Start with the bare structure:

```html
<table>
  <tr>
    <th>Time</th>
    <th>Monday</th>
    <th>Tuesday</th>
  </tr>
  <tr>
    <th>8:00 - 8:40</th>
    <td>Mathematics</td>
    <td>English</td>
  </tr>
</table>
```

- `table` is the whole table, `tr` a row, `th` a header cell, `td` a data cell.
- Show the default ugly result, then say "we will fix that with CSS shortly".

Then improve the structure:

```html
<table>
  <caption>Term 4, Week 1</caption>
  <thead>
    <tr><th scope="col">Time</th><th scope="col">Monday</th><th scope="col">Tuesday</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">8:00 - 8:40</th><td>Mathematics</td><td>English</td></tr>
  </tbody>
</table>
```

- `caption` names the table; `thead`/`tbody` group rows; `scope` tells screen readers whether a header is for a column or a row.

### Merging cells

```html
<tr>
  <th scope="row">8:00 - 8:40</th>
  <td rowspan="2">Mathematics (double period)</td>   <!-- spans 2 rows -->
  <td>English</td>
</tr>
<tr>
  <th scope="row">8:40 - 9:20</th>
  <!-- no Monday cell here: the rowspan above already covers it -->
  <td>PE</td>
</tr>
<tr>
  <th scope="row">9:20 - 9:40</th>
  <td colspan="3">RECESS</td>                         <!-- spans 3 columns -->
</tr>
```

**Rule to teach:** every row must account for the same number of columns. Count the cells *including* the ones "taken" by a rowspan from above. This is where students go wrong.

Finished table: [demo/timetable.html](demo/timetable.html)

---

## Part 2: Forms (20 min)

### Step 1: The form element and a text input

```html
<form action="/submit" method="get">
  <label for="fullname">Full name</label>
  <input type="text" id="fullname" name="fullname">
  <button type="submit">Register</button>
</form>
```

- `form` wraps the controls. `action` is **where** to send the data and `method` is **how**.
- `label for="fullname"` is linked to the input with `id="fullname"`. Click the label and the input gets focus. This also makes the tap target bigger on an iPad.
- **`name` is what the server sees.** `id` is for CSS and labels.

### Step 2: Prove it. Watch the data being sent

Run the echo server, type a name and submit. Point at the **URL bar**:

```
/submit?fullname=Aisha+Rahman
```

- With `method="get"`, the data is attached to the URL as a **query string**: `?name=value&name2=value2`.
- Now delete `name="fullname"` from the input and submit again. The field **disappears** from the URL. *No name, no data.*

### Step 3: More input types

Add each one and submit to see its value:

```html
<input type="email"  name="email">
<input type="number" name="age" min="13" max="22">
<input type="date"   name="dob">
<input type="password" name="pw">

<select name="level">
  <option value="">-- choose --</option>
  <option value="sec3">Secondary 3</option>
  <option value="sec4">Secondary 4</option>
</select>

<fieldset>
  <legend>Gender</legend>
  <label><input type="radio" name="gender" value="F"> Female</label>
  <label><input type="radio" name="gender" value="M"> Male</label>
</fieldset>

<fieldset>
  <legend>Interests</legend>
  <label><input type="checkbox" name="interest" value="coding"> Coding</label>
  <label><input type="checkbox" name="interest" value="music"> Music</label>
</fieldset>

<textarea name="about" rows="4"></textarea>
```

Key teaching points:

- **Radio buttons share one `name`**, which is what makes them mutually exclusive. Each has a different `value`.
- **Checkboxes** with the same `name` send **several** values (`interest=coding&interest=music`). An unticked box sends nothing at all.
- The browser sends the `value`, not the text the user sees. Compare `<option value="sec3">Secondary 3</option>`.
- The right `type` gives free benefits: `email` and `number` show the right keyboard on an iPad, and `date` shows a date picker.
- `password` hides the characters on screen but **does not make the data secure**. The password is still in the URL if the method is GET. (Show this: it is the best argument for POST.)

### Step 4: GET versus POST

Change `method="get"` to `method="post"` and submit again.

- The URL no longer contains the data. The echo server page shows `POST`, and the data is in the **request body**.
- Open the **Network** tab, click the request, and look at the **Payload** (or **Request**) section.

| | GET | POST |
|---|---|---|
| Data goes in | the URL | the request body |
| Visible and bookmarkable | yes | no |
| Used for | searching, reading, anything that can be repeated safely | creating or changing data, passwords, long text |
| Refreshing | harmless | the browser asks "resubmit?" |

Finished form: [demo/register.html](demo/register.html)

---

## Part 3: Basic CSS (15 min)

Create `style.css` and link it from the `<head>`:

```html
<link rel="stylesheet" href="style.css">
```

### Selectors and colours

```css
body {                        /* element selector */
  font-family: system-ui, sans-serif;
  color: #222;                /* hex colour */
  background-color: #faf8ff;
}

h1 { color: rebeccapurple; }  /* named colour; also rgb(91, 33, 182) */

.card { border: 2px solid #c4b5fd; }   /* class selector: class="card" */

#special { background: yellow; }       /* id selector: id="special" */
```

- Syntax: `selector { property: value; }`. Each declaration ends with a semicolon.
- Specificity in one sentence: **id beats class beats element**, and later rules beat earlier ones.
- Reuse: one class on many elements, one id on one element.

### The box model

Draw this on the board, then open the developer tools and select an element to see the same picture:

```
+--------------------------------+
|            margin              |
|   +------------------------+   |
|   |        border          |   |
|   |   +----------------+   |   |
|   |   |    padding     |   |   |
|   |   |  +----------+  |   |   |
|   |   |  | content  |  |   |   |
|   |   |  +----------+  |   |   |
|   |   +----------------+   |   |
|   +------------------------+   |
+--------------------------------+
```

```css
* { box-sizing: border-box; }    /* width now includes padding and border */

.card {
  max-width: 32rem;
  margin: 1rem auto;             /* auto left/right centres it */
  padding: 1.5rem;
  border: 2px solid #c4b5fd;
  border-radius: 12px;
}
```

### Simple flexbox

```html
<div class="row">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
</div>
```

```css
.row {
  display: flex;      /* children now sit in a row */
  gap: 1rem;
  flex-wrap: wrap;    /* wrap on narrow screens */
}
.row > * { flex: 1 1 12rem; }
```

- Change `justify-content` (`center`, `space-between`) and show the effect live.
- Resize the preview and watch the boxes wrap.

Finished stylesheet with comments: [demo/style.css](demo/style.css)

---

## Check for understanding

1. A form has `<input type="text" id="user">`. The user types "Ali" and submits. What does the server receive? *(Nothing: there is no `name`.)*
2. Why do radio buttons in a group share the same `name`?
3. Which is more specific: `.card` or `#card`?
