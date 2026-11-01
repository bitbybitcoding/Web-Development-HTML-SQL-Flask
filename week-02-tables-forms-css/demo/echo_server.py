"""A tiny teaching server for Week 2.

It serves the files in this folder (like `python3 -m http.server`) and, in addition,
shows exactly what a form sent:

    GET  /submit?name=Ali&age=15      -> shows the fields found in the URL
    POST anything                     -> shows the fields found in the request body

Run it from the repository root:

    python3 week-02-tables-forms-css/demo/echo_server.py                 # serves the demo folder
    python3 week-02-tables-forms-css/demo/echo_server.py my-work         # serves your own folder

Then open the forwarded port 8000 and go to the page that has your form.
"""
import functools
import html
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>What the server received</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 40rem; margin: 2rem auto; padding: 0 1rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: .4rem .6rem; text-align: left; }}
    th {{ background: #f3f0ff; }}
    code {{ background: #eee; padding: .1rem .3rem; }}
  </style>
</head>
<body>
  <h1>The server received a <code>{method}</code> request</h1>
  <p>Path: <code>{path}</code></p>
  <p>Raw data: <code>{raw}</code></p>
  <h2>Fields</h2>
  <table>
    <tr><th>name</th><th>value</th></tr>
    {rows}
  </table>
  <p><a href="/">Back to the file list</a></p>
</body>
</html>
"""


class Handler(SimpleHTTPRequestHandler):
    def _echo(self, method: str, raw: str) -> None:
        fields = parse_qs(raw, keep_blank_values=True)
        rows = "\n    ".join(
            f"<tr><td>{html.escape(k)}</td><td>{html.escape(', '.join(v))}</td></tr>"
            for k, v in fields.items()
        ) or '<tr><td colspan="2">(no fields received)</td></tr>'
        body = PAGE.format(
            method=method,
            path=html.escape(urlparse(self.path).path),
            raw=html.escape(raw) or "(empty)",
            rows=rows,
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/submit":
            self._echo("GET", url.query)
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        self._echo("POST", raw)


if __name__ == "__main__":
    folder = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
    handler = functools.partial(Handler, directory=folder)
    print(f"Serving {folder} on http://localhost:8000  (press Ctrl+C to stop)")
    HTTPServer(("", 8000), handler).serve_forever()
