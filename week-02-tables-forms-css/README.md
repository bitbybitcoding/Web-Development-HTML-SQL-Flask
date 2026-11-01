# Week 2: Tables, forms and basic CSS

**Block 1: HTML** · 3 hours · Platform: GitHub Codespaces

## By the end of this session students can

- Build a table with `thead`, `tbody`, `th`, `td`, and merge cells with `colspan` and `rowspan`.
- Build a form using the common `input` types, `label`, `select`, radio buttons, checkboxes and `textarea`.
- Explain how the `name` attribute, `method` and `action` decide what the browser sends.
- Recognise a GET submission in the URL, and tell GET and POST apart.
- Write CSS rules using element, class and id selectors, and explain the box model.
- Lay out a page with simple flexbox.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): spot the bug

Show these on the board. Each has one mistake from Week 1. Students find it and say how to fix it.

```html
<!-- A -->
<ul>
  <p>Chicken rice</p>
  <p>Laksa</p>
</ul>

<!-- B -->
<img src="cat.jpg">

<!-- C -->
<a href=about me.html>About me</a>

<!-- D -->
<p>I <strong><em>love</strong></em> coding.</p>
```

Then two quick recall questions: *What are the two halves of an HTML document?* and *What does the server send back when a page cannot be found?*

## Instructor notes

- **The echo server.** The demo uses [demo/echo_server.py](demo/echo_server.py), a small Python server that serves files and shows exactly what a form submitted. It prepares students for Flask in Week 7. Start it from the repository root with `python3 week-02-tables-forms-css/demo/echo_server.py` and open forwarded port 8000.
- **iPad tip:** Safari on iPad zooms in when a user taps an input whose font size is below 16 px. This is why Challenge 3 asks for readable sizes.
- **Common misconceptions:** forgetting `name` on inputs (the value is never sent); using `<br>` and `&nbsp;` to lay out forms instead of CSS; `id` and `name` are not the same thing (`id` is for CSS and `label for`, `name` is for the server).
- **Pacing:** the CSS part of the demo is deliberately light. Students will refine their styling in the challenges.
