#!/usr/bin/env python3
"""Build week-NN-*/cheatsheet.pdf for all 11 weeks.

Usage (from the repository root):
    pip install reportlab
    python3 tools/build_cheatsheets.py            # all weeks
    python3 tools/build_cheatsheets.py 3 7        # only weeks 3 and 7

The text of each sheet lives in tools/cheatsheets/weeks_a.py and weeks_b.py. Edit it and run this script again.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "cheatsheets"))

from lib import UNICODE, make_pdf     # noqa: E402
from weeks import WEEKS               # noqa: E402

ROOT = HERE.parent


def main(selected):
    if not UNICODE:
        print("Note: DejaVu fonts not found, using built-in fonts (symbols are replaced by plain text).")
    for number, (folder, title, block, items) in WEEKS.items():
        if selected and number not in selected:
            continue
        out = ROOT / folder / "cheatsheet.pdf"
        pages = make_pdf(out, number, title, block, items)
        flag = "" if pages <= 2 else "   <-- more than 2 pages, shorten it"
        print(f"Week {number:2d}: {out.relative_to(ROOT)}  ({pages} page{'s' if pages != 1 else ''}){flag}")


if __name__ == "__main__":
    main({int(a) for a in sys.argv[1:]})
