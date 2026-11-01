# Week 2 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenge 1: Timetable | [challenge-1-timetable.html](challenge-1-timetable.html) + [challenge-1-timetable.css](challenge-1-timetable.css) |
| Challenge 2: CCA sign-up form | [challenge-2-cca-signup.html](challenge-2-cca-signup.html) |
| Challenge 3: iPad-readable styling | [challenge-3-cca-signup.css](challenge-3-cca-signup.css) (add `<link rel="stylesheet" href="challenge-3-cca-signup.css">` to the Challenge 2 file) |
| Challenge 4: Feedback form | [challenge-4-feedback.html](challenge-4-feedback.html) + [challenge-4-feedback.css](challenge-4-feedback.css) (a sample; many designs are valid) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md), [extra-1-validation.html](extra-1-validation.html) |

To test any answer with the echo server, run it on this folder from the repository root:
`python3 week-02-tables-forms-css/demo/echo_server.py week-02-tables-forms-css/Answers`

## Warm-up answers

- **A:** only `li` may be a direct child of `ul`. Replace each `<p>` with `<li>`.
- **B:** the `img` has no `alt` attribute. Add a description, for example `alt="A tabby cat"`.
- **C:** the attribute value is unquoted and contains a space. Use `href="about-me.html"`.
- **D:** wrong nesting. Close tags in reverse order: `<strong><em>love</em></strong>`.
- **Recall:** `head` (information about the page) and `body` (what the user sees). The server replies with status `404 Not Found`.

## Challenge notes

**Challenge 1.** A common mistake is writing a cell for Monday in the 8:40 row, which pushes every later cell one column to the right. Every `tr` must account for six columns: the cells written plus the cells covered by a `rowspan` from the row above. The cells written per row are: 6, 3, 2, 6, 4.

**Challenge 2.** If a value is missing from the URL, the usual causes are:

| Missing field | Reason |
|---------------|--------|
| A text field | the input has no `name` attribute |
| The radio group | nothing was selected (unselected radios send nothing) |
| Some days | unticked checkboxes send nothing; ticked ones each send `day=...` |
| `cca=` is empty | the user left the "-- choose --" option selected (its value is empty) |

**Challenge 3.** Check for: font size of at least 16px on inputs, `width: 100%` with `box-sizing: border-box`, labels as `display: block`, `min-height: 44px` on the button and on checkbox labels, and a `flex` fieldset with `flex-wrap: wrap`. Accept equivalent approaches such as `inline-block`.

**Challenge 4.** Check that the only colours used are the three variables (plus black or white text), that the `.row` uses `flex-wrap: wrap` with `flex: 1 1 14rem` on its children, and that there is no sideways scrolling at 375px wide.
