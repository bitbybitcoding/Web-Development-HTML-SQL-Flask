# Week 1: HTML structure and how the web works

**Block 1: HTML** · 3 hours · Platform: GitHub Codespaces

## By the end of this session students can

- Write a valid HTML document with `html`, `head` and `body`.
- Use headings, paragraphs, lists, links and images correctly.
- Choose semantic tags (`header`, `nav`, `main`, `footer`) instead of generic `div`s.
- Explain what happens between typing a URL and seeing a page (client, server, request, response).
- Use the browser developer tools to inspect a page and a network request.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up (below) | this page |
| 0:15–1:00 | Demo, live-coded | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Challenges (4 tasks) | [challenges.md](challenges.md) · starter files in [challenges/](challenges/) |
| 2:30–3:00 | Extra practice and homework | [extra-practice.md](extra-practice.md) |

**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): "What do you already know?"

Week 1 has no previous week to recap, so use it to check the Python prerequisite and to find out what students already know about websites.

1. What does `len(["a", "b", "c"])` return?
2. Write a dictionary for a student with a name and an age. How do you read the name back out?
3. What is the difference between a list and a dictionary?
4. Discussion: when you type `google.com` and press Enter, what do you think happens? Draw it on the board and keep the drawing for the demo.

## Instructor notes

- **Open the repository in Codespaces together.** Do this at the very start so any set-up problems are fixed before the demo. Remind students to stop and delete old codespaces at the end of every term.
- **Preview HTML files** by running `python3 -m http.server 8000` in the week folder, then opening the forwarded port 8000. Students will use this server in Part B of the demo.
- **Common misconceptions:** HTML is not a programming language (it describes structure, it does not compute); browsers silently fix broken HTML, so "it looks fine" does not mean "it is correct"; `<br>` is not for spacing.
- **Pacing:** students usually need 20 minutes for Challenge 1 if they have never written HTML. Challenge 4 is open-ended, so let fast finishers add more semantic elements rather than moving on.
