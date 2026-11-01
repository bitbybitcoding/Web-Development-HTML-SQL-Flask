# Polish checklist

Tick each item in your own project. Fix at least ten problems you find, and note two you decide *not* to fix and why.

## Content and wording
- [ ] The title, nav and footer are about **my** project (no "My Project", "item", "Lorem ipsum" or template text left)
- [ ] The same word is used for the same thing on every page
- [ ] Every page has a clear heading, and a way back or onward
- [ ] Every list has an **empty state** message that tells the user what to do
- [ ] Dates, prices and numbers are formatted consistently

## Forms
- [ ] Every field has a visible `<label>` connected with `for` and `id`
- [ ] Error messages appear **beside** the field and say how to fix it
- [ ] The values typed are kept after an error
- [ ] Input text is at least 16px; `inputmode="numeric"` where a number keyboard helps
- [ ] The first field is easy to reach; the submit button says what it does ("Add kit", not "Submit")
- [ ] After a successful POST there is a redirect and a flash message

## Looks and layout
- [ ] Works at iPad width (about 768px) and at phone width (about 375px): no sideways scrolling
- [ ] Buttons and links are at least 44px tall; there is space between them
- [ ] Colour contrast is strong enough to read in bright light; colour is never the only signal (use words as well as red/green)
- [ ] The dangerous action (delete) looks different and is a POST button
- [ ] Tables are readable on a small screen

## Robustness
- [ ] Unknown ids and URLs give a friendly 404 page with a way home
- [ ] A very long name, an empty search, a quote mark and `<b>bold</b>` do not break any page
- [ ] You cannot delete something that is still in use (or you get a clear message)
- [ ] You cannot create duplicates where they make no sense
- [ ] Running `flask --app app init-db` and then every page works from a clean start

## Code
- [ ] No debug `print()` statements or commented-out code
- [ ] Every SQL statement uses `?` placeholders
- [ ] Long routes are split into small functions with clear names (validation in its own function)
- [ ] Comments explain **why**, not what
- [ ] `requirements.txt` is up to date; no secrets in the repository

## Accessibility
- [ ] You can use every page with the keyboard only (Tab, Enter)
- [ ] Headings go in order (`h1`, then `h2`)
- [ ] Images have `alt` text (or `alt=""` if decorative)
- [ ] The page has `lang="en"` and a unique `<title>`

## What I fixed

| # | Problem | Fix |
|---|---------|-----|
| 1 | | |

## What I chose not to fix, and why

1.
2.
