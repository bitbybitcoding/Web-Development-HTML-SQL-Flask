# Week 2 Challenges

Four tasks, easiest to hardest. Work in a folder called `my-work/` and link a stylesheet where asked. To test forms, run the echo server on your folder from the repository root: `python3 week-02-tables-forms-css/demo/echo_server.py week-02-tables-forms-css/my-work`. Your form's `action` must be `/submit`.

---

## Challenge 1: Recreate the timetable ★★

Build `timetable.html` so it looks **exactly** like this layout. Cells shown as `↕` are merged with the cell above (use `rowspan`). `RECESS` spans all five day columns (use `colspan`).

| Time | Monday | Tuesday | Wednesday | Thursday | Friday |
|------|--------|---------|-----------|----------|--------|
| 8:00 - 8:40 | Mathematics | English | Computing | Physics | General Paper |
| 8:40 - 9:20 | ↕ | PE | ↕ | ↕ | Chemistry |
| 9:20 - 9:40 | **RECESS** (spans all five day columns) | | | | |
| 9:40 - 10:20 | Chemistry | Mathematics | Physics | English | Computing |
| 10:20 - 11:00 | ↕ | Library | Mother Tongue | Mother Tongue | ↕ |

**Requirements**

- Use `caption`, `thead` and `tbody`. Column headers use `th scope="col"`, time headers use `th scope="row"`.
- Monday, Wednesday and Thursday in the first two periods are single merged cells (double periods). Monday and Friday in the last two periods are also merged.
- Add a stylesheet: borders on every cell, a coloured header row, and a different colour for the recess row.

**Check yourself:** count the cells in each `tr` of your HTML. Remember that a cell taken by a `rowspan` from the row above is *not* written again.

---

## Challenge 2: CCA sign-up form ★★★

Build `cca-signup.html` containing a form with **at least six different input types**. Suggested fields:

| Field | Control |
|-------|---------|
| Full name | `type="text"` |
| Email | `type="email"` |
| Age | `type="number"` |
| Preferred CCA | `select` (Robotics, Basketball, Chinese Orchestra, Debate, Photography, Badminton, Drama) |
| Do you have prior experience? | radio buttons (Yes / No) |
| Days available | checkboxes (Mon to Fri) |
| Why do you want to join? | `textarea` |
| Submit | `button type="submit"` |

**Requirements**

- Every control has a `label` correctly linked with `for` and `id`.
- Every control has a meaningful `name`.
- Group the radios and the checkboxes with `fieldset` and `legend`.
- Use `method="get"` and submit it. Look at the URL: can you find **every** field's value in it? If any are missing, find out why.

---

## Challenge 3: Make it readable on an iPad ★★★

Create `cca-signup.css` and link it to your sign-up form.

**Requirements**

- Body text and all inputs are at least **16px** (so Safari on iPad does not zoom in when you tap).
- The form sits in a card with a maximum width, centred on the page, with padding and a rounded border.
- Each label sits **above** its input, and inputs fill the width of the card.
- Buttons and checkboxes are easy to tap (at least about 44px tall for the button).
- Text has good contrast against its background.
- Radio buttons and checkboxes sit in a row (use `display: flex` with `gap` and `flex-wrap: wrap`, or `inline-block`).

**Test:** open the page in the browser's **responsive / device mode** (iPad size) and confirm nothing overflows sideways.

---

## Challenge 4 (open-ended): Feedback form for a made-up app ★★★★

Invent a small app (for example a homework planner, a bus-arrival tracker, or a recipe finder) and design a **feedback form** for it.

**Requirements**

- At least five different controls, including a rating (for example radio buttons 1 to 5, or `input type="range"`), a `select`, a `textarea`, and one `type="email"` that is optional.
- A consistent colour scheme: pick **three** colours (a main colour, an accent and a neutral) and use only those. Define them once as CSS variables:

  ```css
  :root {
    --main: #5b21b6;
    --accent: #f59e0b;
    --neutral: #f5f3ff;
  }
  ```

  and use them with `var(--main)`.
- A header with the app's name, and a footer.
- Looks good on both a wide screen and a narrow one. Use flexbox so that two fields can sit side by side on wide screens and stack on narrow ones.

**Self-assessment**

| Criterion | Yes / No |
|-----------|----------|
| Valid HTML, every input has a `name` and a linked `label` | |
| Only three colours used, via CSS variables | |
| Readable text size and contrast | |
| Works on a narrow screen without sideways scrolling | |
| Fields are grouped logically | |
