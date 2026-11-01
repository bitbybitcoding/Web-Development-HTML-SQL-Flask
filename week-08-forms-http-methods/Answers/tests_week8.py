"""Self-check for the Week 8 demo and Answers. Run:  python3 week-08-forms-http-methods/Answers/tests_week8.py"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEMO = HERE.parent / "demo"


def load(folder, name):
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location(name, folder / "app.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    sys.path.pop(0)
    return module, module.app.test_client()


def body(r, status=200):
    assert r.status_code == status, f"expected {status}, got {r.status_code}"
    return r.get_data(as_text=True)


def test_demo():
    m, c = load(DEMO, "demo8")
    assert body(c.get("/search?q=tan")).count("<li>") == 2
    assert "GET" in body(c.get("/echo?x=1")) and "POST" in body(c.post("/echo", data={"secret": "s"}))
    assert "{&#39;a&#39;: &#39;1&#39;}" in body(c.get("/echo", query_string={"a": "1"}))
    t = body(c.post("/feedback", data={"name": "A", "rating": "9"}))
    assert t.count('class="error"') == 2
    r = c.post("/feedback", data={"name": "Mei", "rating": "4", "comment": "<b>hi"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/feedback/all")   # Post/Redirect/Get
    t = body(c.get("/feedback/all"))        # the flash message has not been shown yet
    assert "Thank you, Mei" in t and "&lt;b&gt;hi" in t and "4.0" in t
    assert "Thank you" not in body(c.get("/feedback/all"))     # flash is shown only once
    assert len(m.FEEDBACK) == 1
    c.post("/feedback", data={"name": "Mei", "rating": "4"})
    assert len(m.FEEDBACK) == 2                                  # a second POST adds a second row
    assert c.get("/feedback", follow_redirects=True).status_code == 200


def test_challenge_1():
    m, c = load(HERE / "challenge-1", "ch1_8")
    assert "8 students found" in body(c.get("/search?q=&class=&gender="))
    t = body(c.get("/search?q=tan&class=3A"))
    assert "1 student found" in t and "Tan Wei Jie" in t
    assert "No students match" in body(c.get("/search?q=zzz"))
    assert "3 students found" in body(c.get("/search?class=3C"))
    t = body(c.get("/search?gender=F&class=3B"))
    assert "Deepa" in t and "1 student found" in t and "checked" in t
    assert "found" not in body(c.get("/"))                      # nothing searched yet


def good_signup(**changes):
    d = {"name": "Mei Lin", "class": "3A", "email": "mei@example.com", "cca": "Choir", "agree": "yes"}
    d.update(changes)
    return d


def test_challenge_2():
    m, c = load(HERE / "challenge-2", "ch2_8")
    t = body(c.post("/signup", data={}))
    assert t.count('class="error"') >= 5 and "Please fix 5 problems" in t
    t = body(c.post("/signup", data=good_signup(email="nope", name="M")))
    assert "valid email" in t and "2 to 50" in t and 'value="nope"' in t and 'value="M"' in t   # values kept
    assert "checked" in t and 'value="3A"' in t                                                 # other fields kept
    assert "<script>" not in body(c.post("/signup", data=good_signup(name="<script>x</script>", email="bad")))
    r = c.post("/signup", data=good_signup())
    assert r.status_code == 302 and len(m.MEMBERS) == 1
    assert "Welcome to Choir, Mei Lin!" in body(c.get("/members"))
    assert "already signed up" in body(c.post("/signup", data=good_signup(name="Other Person", email="MEI@example.com")))
    assert "Choose one CCA" in body(c.post("/signup", data=good_signup(cca="Hacking Club", email="x@y.sg")))
    assert "Choose your class" in body(c.post("/signup", data=good_signup(**{"class": "9Z"}, email="x@y.sg")))
    assert len(m.MEMBERS) == 1


def test_challenge_3():
    m, c = load(HERE / "challenge-3", "ch3_8")
    assert "Nothing here" in body(c.get("/"))
    assert c.post("/add", data={"text": "  "}).status_code == 302
    assert not m.TASKS
    c.post("/add", data={"text": "Buy ink"}); c.post("/add", data={"text": "Write code"})
    t = body(c.get("/"))
    assert "Buy ink" in t and "2 tasks left" in t
    assert c.get("/add").status_code == 405                    # GET is not allowed for actions
    assert c.get("/delete/1").status_code == 405
    c.post("/toggle/1")
    t = body(c.get("/"))
    assert "1 task left" in t and 'class="done"' in t
    assert "Buy ink" not in body(c.get("/?show=open")) and "Buy ink" in body(c.get("/?show=done"))
    c.post("/delete/1")
    assert [x["text"] for x in m.TASKS] == ["Write code"]
    assert c.post("/delete/99").status_code == 404
    assert c.post("/add", data={"text": "x" * 101}).status_code == 302 and len(m.TASKS) == 1
    assert "<b>" not in body(c.post("/add", data={"text": "<b>bold"}, follow_redirects=True))


def test_challenge_4():
    m, c = load(HERE / "challenge-4", "ch4_8")
    assert c.get("/quiz").status_code == 302                       # must enter a name first
    assert "2 to 30" in body(c.post("/", data={"name": "A"}))
    assert c.post("/", data={"name": "Mei"}).status_code == 302
    full = {f"q{q['id']}": str(q["answer"]) for q in m.QUESTIONS}
    assert "Please answer every question (1 left)" in body(c.post("/quiz", data={k: v for k, v in list(full.items())[:-1]}))
    r = c.post("/quiz", data=full)
    assert r.status_code == 302
    assert "Mei, you scored 5/5" in body(c.get(r.headers["Location"]))
    bad = dict(full, q1="0", q2="0")
    r = c.post("/quiz", data=bad)
    t = body(c.get(r.headers["Location"]))
    assert "scored 3/5" in t and "Answer: &lt;h1&gt;" in t
    assert c.post("/quiz", data=dict(full, q1="x")).status_code == 400
    t = body(c.get("/leaderboard"))
    assert t.index("5/5") < t.index("3/5")
    assert c.get("/result/99").status_code == 404


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                failed += 1; print("FAIL", name, e)
            except Exception as e:
                failed += 1; print("ERROR", name, type(e).__name__, e)
    sys.exit(1 if failed else 0)
