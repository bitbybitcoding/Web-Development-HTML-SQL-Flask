#!/usr/bin/env python3
"""Check the whole course repository. Run from anywhere:   python3 tools/check_all.py

1. Every week folder has the required parts (README, demo, challenges, extra practice, cheatsheet PDF, Answers/).
2. Every cheatsheet is a real PDF.
3. The starter database has the expected tables and rows.
4. Every automated check in the Answers folders passes (Flask apps, tests, SQL-in-Python scripts).
Exit code 0 means everything passed.
"""
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEEKS = sorted(p for p in ROOT.glob("week-[0-9][0-9]-*") if p.is_dir())

failures = []


def check(label, ok, detail=""):
    print(("  ok    " if ok else "  FAIL  ") + label + (f"   {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(label)


print("1. Week folders")
check("11 week folders", len(WEEKS) == 11, f"found {len(WEEKS)}")
for week in WEEKS:
    has_demo = (week / "demo.md").exists() or (week / "demo").is_dir()
    has_challenges = (week / "challenges.md").exists()
    has_extra = (week / "extra-practice.md").exists()
    has_answers = (week / "Answers").is_dir() and any((week / "Answers").iterdir())
    has_readme = (week / "README.md").exists()
    check(f"{week.name}: README, demo, challenges, extra practice, Answers/",
          all([has_readme, has_demo, has_challenges, has_extra, has_answers]),
          str({"README": has_readme, "demo": has_demo, "challenges": has_challenges, "extra": has_extra, "Answers": has_answers}))

print("2. Cheatsheets")
for week in WEEKS:
    pdf = week / "cheatsheet.pdf"
    ok = pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-" and pdf.stat().st_size > 5000
    check(f"{week.name}/cheatsheet.pdf", ok)

print("3. Starter database")
try:
    con = sqlite3.connect(ROOT / "school.db")
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    check("tables", tables == {"students", "subjects", "scores", "ccas", "student_cca"}, str(tables))
    check("30 students, 120 scores, 8 CCAs",
          (con.execute("SELECT COUNT(*) FROM students").fetchone()[0],
           con.execute("SELECT COUNT(*) FROM scores").fetchone()[0],
           con.execute("SELECT COUNT(*) FROM ccas").fetchone()[0]) == (30, 120, 8))
    check("no orphan rows", con.execute("PRAGMA foreign_key_check").fetchall() == [])
    con.close()
except sqlite3.Error as e:
    check("school.db opens", False, str(e))

print("4. Automated checks in the Answers folders")
SCRIPTS = [
    ("Week 6 tests", "week-06-ddl-dml-python-sqlite/Answers/tests_week6.py", []),
    ("Week 7 tests", "week-07-flask-routes-templates/Answers/tests_week7.py", []),
    ("Week 8 tests", "week-08-forms-http-methods/Answers/tests_week8.py", []),
    ("Week 8 extra practice", "week-08-forms-http-methods/Answers/extra_practice.py", []),
    ("Week 9 tests", "week-09-flask-sqlite-crud/Answers/tests_week9.py", []),
    ("Week 9 extra practice", "week-09-flask-sqlite-crud/Answers/extra_practice.py", []),
    ("Week 11 tests (also runs the model capstone's 21 tests)", "week-11-test-polish-present/Answers/tests_week11.py", []),
]
for label, script, args in SCRIPTS:
    result = subprocess.run([sys.executable, "-B", str(ROOT / script), *args], capture_output=True, text=True, cwd=ROOT)
    check(label, result.returncode == 0, (result.stdout + result.stderr).strip().splitlines()[-1:] and
          (result.stdout + result.stderr).strip().splitlines()[-1])

template = ROOT / "week-10-plan-and-build" / "capstone-template"
result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"], capture_output=True, text=True, cwd=template)
check("Capstone template tests", result.returncode == 0, result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "")

print("5. Links between the Markdown files")
import re
broken = []
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)   # ignore code blocks
    text = re.sub(r"`[^`\n]*`", "", text)                                      # ignore inline code
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = (md.parent / target.split("#")[0]).resolve()
        if not path.exists():
            broken.append(f"{md.relative_to(ROOT)} -> {target}")
check("every relative link points at a file or folder that exists", not broken, "; ".join(broken[:5]))
for b in broken:
    print("     broken:", b)

# tidy up anything the checks created
for pattern in ("__pycache__", "instance"):
    for path in ROOT.rglob(pattern):
        if path.is_dir():
            subprocess.run(["rm", "-rf", str(path)])

print()
print("ALL CHECKS PASSED" if not failures else f"{len(failures)} CHECK(S) FAILED")
sys.exit(1 if failures else 0)
