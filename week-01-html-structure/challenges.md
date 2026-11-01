# Week 1 Challenges

Four tasks, easiest to hardest. Create your files inside a folder called `my-work/` in this week's folder so you do not overwrite the starter files. Preview with `python3 -m http.server 8000`.

---

## Challenge 1: School canteen menu ★

Build `my-work/canteen.html`, a menu page for the school canteen.

**Requirements**

- A correct HTML skeleton (`<!DOCTYPE html>`, `lang`, `charset`, `<title>`).
- One `h1` for the canteen name and one `h2` for each stall.
- Use an **unordered list** for each stall's menu items, with prices.
- Use an **ordered list** for a "Top 3 bestsellers" section.
- Add a short paragraph with the opening hours, with at least one word in `strong`.

**Use this data**

| Stall | Items |
|-------|-------|
| Chicken Rice | Roasted chicken rice $3.50, Steamed chicken rice $3.50, Extra drumstick $1.50 |
| Mixed Vegetable Rice | 2 veg + 1 meat $3.00, 3 veg + 1 meat $3.50, Egg $0.80 |
| Noodles | Fishball noodles $3.20, Mee soto $3.50, Wanton mee $3.50 |

Bestsellers (in order): 1. Roasted chicken rice, 2. Wanton mee, 3. Mixed vegetable rice (2 veg + 1 meat).

**Check yourself:** every `<li>` sits directly inside a `<ul>` or `<ol>`, and every tag you opened is closed.

---

## Challenge 2: Debug the broken page ★★

Open [challenges/broken.html](challenges/broken.html). It displays *almost* correctly in the browser, but the HTML is full of mistakes. There are **ten** deliberate bugs. Copy the file to `my-work/fixed.html`, then:

1. Find and fix all ten bugs.
2. Add an HTML comment `<!-- FIXED: ... -->` next to each fix saying what was wrong.

**Hints:** bugs include unclosed tags, wrong nesting, missing attributes, and content in the wrong place. Use the **Elements** tab in the developer tools to see how the browser *interpreted* the broken page.

---

## Challenge 3: A three-page site ★★★

Build a small website for a made-up school club with these files in `my-work/club-site/`:

```
club-site/
├── index.html      (Home)
├── activities.html (Activities)
└── contact.html    (Contact)
```

**Requirements**

- Every page has the same `header` with a `nav` that links to **all three** pages.
- Every page has a `main` with a heading and at least two paragraphs or a list, and a `footer`.
- All links work in both directions (you can go from any page to any other page).
- The Contact page has a link to the club's (made-up) email address using `mailto:`.
- At least one page includes an image with proper `alt` text.
- At least one link to an external website, opening in a **new tab** (`target="_blank"`, and add `rel="noopener"`).

**Challenge within the challenge:** put the pages in separate folders (for example `activities/index.html`) and fix the relative links so they still work (hint: `../`).

---

## Challenge 4 (open-ended): A page about your hobby ★★★★

Make `my-work/hobby.html`, a page about a hobby, interest or topic you care about.

**Requirements**

- Use at least **five different semantic elements** from this list: `header`, `nav`, `main`, `section`, `article`, `aside`, `figure` with `figcaption`, `footer`, `time`.
- Use at least one ordered list, one unordered list and one description list (`dl`, `dt`, `dd`).
- At least one image with `alt` text, at least one internal link (`#id`), and at least one external link.

**Marking rubric (self-assess, then swap with a partner)**

| Criterion | Yes / No |
|-----------|----------|
| Valid skeleton with `lang`, `charset`, `title` | |
| One `h1`, headings in order | |
| 5+ different semantic elements, used for their meaning | |
| All three list types used correctly | |
| Images have meaningful `alt` text | |
| No unclosed or wrongly nested tags (check in the validator) | |
