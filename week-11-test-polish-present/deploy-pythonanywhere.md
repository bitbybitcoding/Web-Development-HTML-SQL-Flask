# Deploying your Flask app on PythonAnywhere

Running in Codespaces is for developing. To let other people use your app, it must run on a **server**. PythonAnywhere has a free plan that runs Flask apps and supports SQLite, which is why we use it.

> **Instructor:** the virtual-environment, WSGI-file and "do not call `app.run()`" steps follow PythonAnywhere's own [Flask help page](https://help.pythonanywhere.com/pages/Flask). The Bash-console, static-files and Reload steps are written from general knowledge of the service and **were not re-checked**, and this course could not run a test deployment. Their pages change from time to time, so **do the whole walkthrough once with a test account before class**. Check PythonAnywhere's current terms (including the minimum age for an account and what the free plan allows, such as the number of web apps and any renewal requirement), and obtain parent or guardian consent where needed. If students cannot make accounts, run one deployment as a class demonstration. Deployment is a **stretch goal** in the marking brief: nobody loses marks if it is not possible.

## Before you start (in Codespaces)

1. Your project runs, and the tests pass.
2. `requirements.txt` lists what your app needs (the template has `Flask>=3.0,<4`).
3. There is **no** `app.run(...)` call at the top level of `app.py` (the template has none). On a server, PythonAnywhere runs your app, not you.
4. Your secret key comes from the environment (the template reads `SECRET_KEY`).
5. Your code is pushed to GitHub (`git push`).

## Steps

1. **Make an account** at pythonanywhere.com (Beginner plan).
2. **Get your code onto the server.** Open a **Bash console** (Consoles tab) and run:
   ```bash
   git clone https://github.com/<your-username>/<your-repository>.git
   cd <your-repository>/my-work/capstone        # the folder that contains app.py
   ```
3. **Make a virtual environment** and install Flask in the same console. Use a Python version that PythonAnywhere offers:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.13 capstone-env       # use a version number from the list on the Web tab
   pip install -r requirements.txt
   ```
4. **Create the database on the server.** The database is *not* in Git (it is ignored), so it is built from your SQL files:
   ```bash
   flask --app app init-db
   ```
   (This creates `instance/app.db` next to your code. Do not run it again later: it deletes the data.)
5. **Create the web app.** Web tab → *Add a new web app* → *Manual configuration* → choose the same Python version as in step 3.
6. **Virtualenv:** on the Web tab, enter `capstone-env`.
7. **WSGI file:** click the link to the *WSGI configuration file* near the top of the Web tab. Delete its contents and write:
   ```python
   import os
   import sys

   path = "/home/<your-username>/<your-repository>/my-work/capstone"      # folder that contains app.py
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ["SECRET_KEY"] = "put-a-long-random-string-here"             # keep this file private; never put it on GitHub

   from app import app as application
   ```
   Make a random key in a console: `python3 -c "import secrets; print(secrets.token_hex(32))"`.
8. **Static files:** on the Web tab, in the *Static files* section, add URL `/static/` and directory `/home/<your-username>/<your-repository>/my-work/capstone/static`. (Flask also serves static files itself, but this is faster.)
9. Press the green **Reload** button. Visit `<your-username>.pythonanywhere.com`.

## If it does not work

| Symptom | Likely cause and fix |
|---------|----------------------|
| "Something went wrong" page | Open the **error log** link on the Web tab. The last lines of the traceback tell you which line failed |
| `ModuleNotFoundError: No module named 'flask'` | The Virtualenv path on the Web tab is empty or wrong |
| `ModuleNotFoundError: No module named 'app'` | The `path` in the WSGI file does not point at the folder that holds `app.py` |
| `no such table` | Step 4 was not run (or was run in a different folder). Run `flask --app app init-db` in the project folder |
| `attempt to write a readonly database` | The `instance/` folder or file is not writable: check you cloned into your own home directory |
| Changes in GitHub do not appear | `git pull` in the Bash console, then **Reload** |
| The page looks unstyled | The static files mapping (step 8) is wrong, or the stylesheet link uses a hand-written path instead of `url_for` |
| 502 / 504 error | Something at the top level of your code runs forever (for example `app.run()`), or the app crashed on start |

## Updating a deployed app

```bash
cd ~/<your-repository>/my-work/capstone
git pull
# Web tab → Reload
```

Do not run `init-db` again unless you want to wipe the data. If you change `schema.sql`, plan a migration (`ALTER TABLE`) or accept that the data will be reset.

## What is different on a real server (talking points)

- **Debug mode is off.** `--debug` shows the source code and a console to anyone who can trigger an error: **never** run it on a public site.
- **Secrets stay out of Git.** Anything in the repository is public if the repository is public: that includes keys, passwords and databases of real people.
- **Anyone can reach it.** Every form will be tried with strange input. This is why we validate on the server and use placeholders.
- **Backups and privacy.** A real club would back up the database and think about whose data is stored. Do not enter real personal details into a class project.
- **SQLite on a server** is fine for a small project like this. A busy site would use a database server such as PostgreSQL.
