# Week 2 Extra Practice

For fast finishers, and homework for everyone else.

---

## 1. Built-in validation

Browsers can check input **before** it is sent. Add validation attributes to your CCA sign-up form:

- `required` on name, email and preferred CCA.
- `minlength="2"` and `maxlength="50"` on the name.
- `min="13"` and `max="22"` on the age.
- A `pattern` that accepts only a Singapore mobile number of 8 digits starting with 8 or 9 on a new `type="tel"` field. Add a `title` that explains the rule.
- `autocomplete` hints, for example `autocomplete="email"`.

Test each rule by submitting bad data. Which messages does the browser show?

**Then think:** can someone still send bad data to a server without using your form? (This matters in Week 8.)

## 2. Responsive layout with flexbox

Take your feedback form (Challenge 4) and make it responsive:

- Wrap two fields (for example *Name* and *Email*) in a `div class="row"` and make the row `display: flex; flex-wrap: wrap; gap: 1rem;`.
- Give each child `flex: 1 1 14rem;` so they sit side by side when there is room and stack when there is not.
- Add one `@media (max-width: 600px)` rule that makes the card padding smaller.

Test it in device mode at an iPad width, then at a phone width.

## 3. Compare GET and POST in the Network tab

Run the echo server. Submit the same form twice, once with `method="get"` and once with `method="post"`. For each, record in a table:

| | GET | POST |
|---|---|---|
| URL shown in the address bar | | |
| Where the data appears in the request | | |
| `Content-Type` of the request (POST only) | | |
| What happens when you press refresh | | |

## 4. Tidy up the table

Improve your timetable from Challenge 1:

- Alternate row colours using `tbody tr:nth-child(even)`.
- Highlight the row under the mouse using `tr:hover`.
- Make the table scroll sideways on a narrow screen without breaking the page (hint: wrap it in a `div` with `overflow-x: auto`).

## 5. Short answers (exam style)

1. Explain the difference between the `id` and `name` attributes of an input.
2. A student's form uses `method="get"` to send a password. Give **two** reasons this is a bad idea.
3. State what `rowspan="3"` does.
4. In the box model, list the four layers from the inside to the outside.
5. Write a CSS rule that makes every element with the class `warning` red text on a pale yellow background.
