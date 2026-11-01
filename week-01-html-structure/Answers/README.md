# Week 1 Answers

| Task | Answer |
|------|--------|
| Warm-up | below |
| Challenge 1: Canteen menu | [challenge-1-canteen.html](challenge-1-canteen.html) |
| Challenge 2: Debug | [challenge-2-fixed.html](challenge-2-fixed.html) (bug list below) |
| Challenge 3: Three-page site | [challenge-3-site/](challenge-3-site/) |
| Challenge 4: Hobby page | [challenge-4-hobby.html](challenge-4-hobby.html) (a sample; many answers are valid) |
| Extra practice | [extra-practice-answers.md](extra-practice-answers.md) |

## Warm-up answers

1. `3`.
2. `student = {"name": "Aisha", "age": 15}` then `student["name"]`.
3. A list is ordered and accessed by position (index). A dictionary stores key/value pairs and is accessed by key.
4. Browser sends a request to a server, the server sends a response, and the browser draws the page. Accept any reasonable drawing that has a client, a server, and arrows in both directions. (DNS lookup is a bonus.)

## Challenge 2: the ten bugs

| # | Bug | Fix |
|---|-----|-----|
| 1 | No `<!DOCTYPE html>` | Add it on the first line |
| 2 | `<html>` has no `lang` attribute | `<html lang="en">` |
| 3 | `<title>` is outside `<head>` | Move it inside `<head>` |
| 4 | `<h1>` is never closed | Add `</h1>` |
| 5 | `<a>` with no `href` | Add `href="index.html"` |
| 6 | `href=about page.html` is unquoted and contains a space | `href="about-page.html"` (rename the target, avoid spaces in file names) |
| 7 | `<b><i>happy</b></i>` is wrongly nested | `<strong><em>happy</em></strong>` |
| 8 | `<img>` has no `alt` | Add a meaningful `alt` (and a `width`) |
| 9 | `<ul>` contains `<p>` items, and the `<ul>` itself is inside a `<p>` | Use `<li>` inside the `<ul>`, and close the intro `<p>` before the list |
| 10 | `<main>` is never closed | Add `</main>` before `<footer>` |

A bonus eleventh issue: the `<p>` after "We sell..." is never closed. Accept this as a bonus find.
