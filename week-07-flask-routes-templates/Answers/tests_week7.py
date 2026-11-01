"""Self-check for the Week 7 demo and Answers. Run:  python3 week-07-flask-routes-templates/Answers/tests_week7.py"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEMO = HERE.parent / "demo"


def load(folder, name):
    """Import folder/app.py as a fresh module, with the folder importable."""
    sys.path.insert(0, str(folder))
    sys.modules.pop("cca_data", None)
    spec = importlib.util.spec_from_file_location(name, folder / "app.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    sys.path.pop(0)
    return module.app.test_client()


def text(client, url, status=200):
    r = client.get(url)
    assert r.status_code == status, f"{url}: expected {status}, got {r.status_code}"
    return r.get_data(as_text=True)


def test_demo():
    c = load(DEMO, "demo_app")
    assert "5 students" in text(c, "/")
    assert "Hello, Mei!" in text(c, "/hello/mei")
    assert "&lt;i&gt;Amy" in text(c, "/hello/<i>Amy") and "<i>Amy" not in text(c, "/hello/<i>Amy")
    assert text(c, "/square/12") == "12 squared is 144"
    text(c, "/square/abc", 404)
    body = text(c, "/students?class=3B")
    assert "Tay Jun Hao" in body and "Tan Wei Jie" not in body
    assert "Deepa Krishnan" in text(c, "/students/5")
    assert "404" in text(c, "/students/99", 404)
    assert "/static/style.css" in body


def test_challenge_1():
    c = load(HERE / "challenge-1", "ch1")
    for url in ["/", "/about", "/time", "/dice", "/hello/mei"]:
        text(c, url)
    assert "You rolled a" in text(c, "/dice")
    assert "<script>" not in text(c, "/hello/<script>x")


def test_challenge_2():
    c = load(HERE / "challenge-2", "ch2")
    assert text(c, "/add/2/3") == "2 + 3 = 5"
    assert "12.57" in text(c, "/area/2.0")
    text(c, "/area/2", 404)
    assert "Monday" in text(c, "/day/1") and "Sunday" in text(c, "/day/7")
    text(c, "/day/0", 404)
    text(c, "/day/8", 404)
    assert "&lt;" in text(c, "/shout/<b>hi") and "<b>" not in text(c, "/shout/<b>hi")


def test_challenge_3():
    c = load(HERE / "challenge-3", "ch3")
    assert "6 students" in text(c, "/")
    body = text(c, "/students")
    assert body.count("<tr") == 7 and body.count('class="good"') == 3  # averages >= 70: Wei Jie, Jun Hao, Deepa
    assert "Tay Jun Hao" in text(c, "/class/3b") and "Tan Wei Jie" not in text(c, "/class/3b")
    assert "needs help" in text(c, "/students/4")
    text(c, "/students/99", 404)
    text(c, "/class/9Z", 404)


def test_challenge_4():
    c = load(HERE / "challenge-4", "ch4")
    assert "6 CCAs and 160 members" in text(c, "/")
    assert "Football" in text(c, "/ccas") and "be the first member" in text(c, "/ccas")
    assert "Also on Fridays" in text(c, "/ccas/choir") and "Scouts" in text(c, "/ccas/choir")
    body = text(c, "/category/sports")
    assert "Football" in body and "Choir" not in body.split("<main>")[1]
    text(c, "/ccas/nope", 404)
    text(c, "/category/nope", 404)
    assert "Performing Arts" in text(c, "/about")  # shown in the navigation


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                failed += 1
                print("FAIL", name, e)
    sys.exit(1 if failed else 0)
