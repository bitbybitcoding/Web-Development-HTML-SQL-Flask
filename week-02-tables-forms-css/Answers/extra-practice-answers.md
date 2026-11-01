# Week 2 Extra Practice: Answers

## 1. Built-in validation

See [extra-1-validation.html](extra-1-validation.html). Key attributes:

```html
<input type="text" name="fullname" required minlength="2" maxlength="50" autocomplete="name">
<input type="email" name="email" required autocomplete="email">
<input type="tel" name="phone" pattern="[89][0-9]{7}"
       title="8 digits, starting with 8 or 9 (for example 91234567)">
<input type="number" name="age" min="13" max="22" required>
```

- `pattern="[89][0-9]{7}"` means: first character 8 or 9, followed by exactly seven digits.
- The browser's messages depend on the browser: "Please fill out this field", "Please include an '@' in the email address", "Value must be greater than or equal to 13", and the `title` text for a failed `pattern`.

**Then think:** yes. Browser checks run in the user's browser, which the user controls. Anyone can turn them off in the developer tools, or send a request directly with a tool such as `curl`. The **server must check everything again** (Week 8: "never trust the browser").

## 2. Responsive layout with flexbox

```css
.row { display: flex; flex-wrap: wrap; gap: 0 1rem; }
.row > p { flex: 1 1 14rem; margin: 0 0 1rem; }

@media (max-width: 600px) {
  .card { margin: 1rem 0.5rem; padding: 1rem; }
}
```

See [challenge-4-feedback.css](challenge-4-feedback.css). `flex: 1 1 14rem` means: grow to share spare space (`1`), shrink if needed (`1`), and start at a base width of 14rem. When two items do not fit side by side, `flex-wrap` moves the second onto a new line.

## 3. GET versus POST in the Network tab

| | GET | POST |
|---|---|---|
| URL shown in the address bar | `/submit?fullname=Ali&age=15` (data included) | `/submit` (no data) |
| Where the data appears in the request | in the URL (query string) | in the request body (see the **Payload** tab) |
| `Content-Type` of the request | none (no body) | `application/x-www-form-urlencoded` |
| What happens on refresh | the page reloads silently | the browser asks whether to resubmit the form |

## 4. Tidy up the table

```css
.timetable tbody tr:nth-child(even) td { background: #faf8ff; }
.timetable tbody tr:hover td { background: #fef3c7; }
.scroll { overflow-x: auto; }            /* wrap the table in <div class="scroll"> */
```

See [challenge-1-timetable.css](challenge-1-timetable.css) and [challenge-1-timetable.html](challenge-1-timetable.html).

## 5. Short answers

1. `id` uniquely identifies an element on the page and is used by CSS, JavaScript and `<label for>`. `name` is the key under which the input's value is sent to the server. An input without `name` sends nothing.
2. Any two: the password appears in the URL, so it is visible on screen to anyone nearby; it is saved in the browser history and bookmarks; it is recorded in server logs; it can be copied or shared accidentally.
3. The cell stretches downwards across three table rows.
4. Content, padding, border, margin.
5. ```css
   .warning {
     color: red;
     background-color: #fffbe6;
   }
   ```
