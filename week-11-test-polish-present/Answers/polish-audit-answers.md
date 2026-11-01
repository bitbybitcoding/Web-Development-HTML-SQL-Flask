# Polish audit: what a good audit finds

Student projects are different, so these are examples of the kind of problem found in the capstone template and the model project, with the fix. A good student audit finds ten or more items like these in **their own** project.

| Area | Problem found | Fix |
|------|---------------|-----|
| Wording | Template still says "My Project", "Add item", "Items" | Rename to the project's own words everywhere (search the whole folder for the old words) |
| Empty state | A table with only a header row when a search finds nothing | `{% if rows %}...{% else %}<p>No kits match. <a href="...">Add one?</a></p>{% endif %}` |
| Forms | A number field accepts `abc` and shows a general error | Per-field message: "Quantity must be a whole number from 1 to 500." beside the field |
| Forms | The values vanish after a validation error | `value="{{ form.name }}"` and `selected`/`checked` expressions |
| Forms | The button says "Submit" | Say what it does: "Lend", "Save kit" |
| Layout | Table runs off the screen at phone width | Wrap tables in a container with `overflow-x: auto`, or use fewer columns on small screens |
| Touch | Links in a table row are close together | Give links padding so each target is at least 44px high |
| Colour | Overdue shown only in red | Add the words "(overdue)" so colour is not the only signal |
| Safety | Delete is one click, beside the Edit button | Style it as dangerous; put it away from common actions; optionally a confirmation page |
| Robustness | A 500 error page on `/kits/abc` or an unknown id | `<int:...>` converters give a 404; `abort(404)` for missing rows; a friendly 404 template |
| Robustness | A very long name breaks the table | `CHECK (length(name) <= 60)` in the database, validation in Python, and `overflow-wrap: anywhere` in CSS |
| Data | Test rows named "asdf", "Test 1" | Replace the seed data with realistic data |
| Code | `print(...)` calls and commented-out code | Remove; Git remembers old versions |
| Code | One 60-line route with validation inside | Move the validation into `clean_form()` that returns `(form, errors)` |
| Code | A comment saying `# insert into database` | Replace with a comment that explains *why* (`# not stored: calculated from the loans so it cannot go out of step`) |
| Accessibility | An input without a label | `<label for="x">` and `id="x"` |
| Accessibility | Headings skip from `h1` to `h3` | Use `h2` |
| Accessibility | No `<title>` per page | `{% block title %}` in each page |
| Security | `app.secret_key` is a fixed string in the code | Read from the environment: `os.environ.get("SECRET_KEY", "dev-only-change-me")` and set it on the server |
| Security | The database file is in the repository | `.gitignore` (already ignores `instance/` and `*.db`); `git rm --cached` if already committed |

## Things a student may reasonably choose not to fix (with a reason)

- Pagination on a list of 12 rows ("the data is small").
- A confirmation dialog for delete ("the delete refuses when the item is in use, and I have a test for it").
- Dark mode, animations, a logo.
- A login system ("out of scope for the brief; recorded in Limitations").

The test of a good reason: it is specific, honest and about the project.
