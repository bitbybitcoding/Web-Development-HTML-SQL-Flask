"""Self-check for Week 11. Run:  python3 week-11-test-polish-present/Answers/tests_week11.py

It proves that (1) the demo tests pass on the good module, (2) the same tests catch exactly the two
planted boundary bugs, (3) the TDD kata solution passes, and (4) the model capstone's 21 tests pass.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEMO = HERE.parent / "demo"
MODEL = HERE.parents[1] / "week-10-plan-and-build" / "Answers" / "model-capstone"


def run(args, cwd):
    return subprocess.run([sys.executable, "-B", *args], cwd=cwd, capture_output=True, text=True)


def test_demo_tests_pass_on_good_module():
    r = run(["-m", "unittest", "test_grades"], DEMO)
    assert r.returncode == 0, r.stderr


def test_demo_tests_catch_the_two_planted_bugs():
    import shutil, tempfile
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("test_grades.py",):
            shutil.copy(DEMO / name, tmp)
        shutil.copy(DEMO / "grades_buggy.py", pathlib.Path(tmp) / "grades.py")
        r = run(["-m", "unittest", "test_grades"], tmp)
    assert r.returncode != 0
    failed_scores = sorted(re.findall(r"\(score=(\d+)\)", r.stderr))
    assert failed_scores == ["45", "65"], failed_scores
    assert "test_typical_scores" not in r.stderr          # the ordinary test does NOT notice the bugs


def test_tdd_kata():
    r = run(["-m", "unittest", "test_validators"], HERE / "extra_tdd")
    assert r.returncode == 0, r.stderr


def test_model_capstone_tests():
    r = run(["-m", "unittest", "discover", "-s", "tests"], MODEL)
    assert r.returncode == 0, r.stderr
    assert "Ran 21 tests" in r.stderr


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                failed += 1; print("FAIL", name, e)
    sys.exit(1 if failed else 0)
