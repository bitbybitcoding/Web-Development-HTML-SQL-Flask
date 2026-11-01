"""Tiny layout library for the weekly cheatsheets (A4, two columns, 1-2 pages).

Content is plain Python data (see weeks.py), so a teacher can fix a typo without knowing reportlab:
    ("h", "Heading")                         a section heading
    ("p", "Text with **bold** and `code`")   a paragraph
    ("bullets", ["item", "item"])            a bullet list
    ("code", "line 1\\nline 2")               a code block (keep lines under 54 characters)
    ("table", [header...], [[cell...]...], [col widths as fractions])   a small table
    ("tip", "Text")                          a highlighted tip box
"""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)

BLUE = colors.HexColor("#1f4e8c")
LIGHT = colors.HexColor("#eef3fa")
CODE_BG = colors.HexColor("#f3f4f6")
TIP_BG = colors.HexColor("#fff6dd")
TIP_EDGE = colors.HexColor("#e0a800")
GREY = colors.HexColor("#555555")

MAX_CODE_CHARS = 54

# ---- fonts: DejaVu if present (has arrows and symbols); otherwise the built-in Helvetica/Courier ----
_DEJAVU = [Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/share/fonts/dejavu"), Path("/usr/share/fonts/TTF")]


def _register_fonts():
    for folder in _DEJAVU:
        files = {"Sans": "DejaVuSans.ttf", "Sans-Bold": "DejaVuSans-Bold.ttf",
                 "Mono": "DejaVuSansMono.ttf", "Mono-Bold": "DejaVuSansMono-Bold.ttf"}
        if all((folder / f).exists() for f in files.values()):
            for name, f in files.items():
                pdfmetrics.registerFont(TTFont("DV-" + name, str(folder / f)))
            pdfmetrics.registerFontFamily("DV-Sans", normal="DV-Sans", bold="DV-Sans-Bold",
                                          italic="DV-Sans", boldItalic="DV-Sans-Bold")
            return "DV-Sans", "DV-Sans-Bold", "DV-Mono", True
    return "Helvetica", "Helvetica-Bold", "Courier", False


SANS, SANS_BOLD, MONO, UNICODE = _register_fonts()
_ASCII = {"→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≠": "!=", "✓": "yes",
          "✗": "no", "·": "-", "–": "-", "—": "-", "•": "*", "×": "x", "π": "pi",
          "‘": "'", "’": "'", "“": '"', "”": '"', "…": "..."}


def clean(text):
    if UNICODE:
        return text
    for k, v in _ASCII.items():
        text = text.replace(k, v)
    return text


BODY = ParagraphStyle("body", fontName=SANS, fontSize=8.2, leading=10.4, alignment=TA_LEFT, spaceAfter=2.5)
HEAD = ParagraphStyle("head", fontName=SANS_BOLD, fontSize=9.6, leading=11.5, textColor=BLUE, spaceBefore=5, spaceAfter=2, keepWithNext=1)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=9, bulletIndent=1, spaceAfter=1.2)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=7.5, leading=9.3)
CELL_HEAD = ParagraphStyle("cellhead", parent=CELL, fontName=SANS_BOLD, textColor=colors.white)
CODE_LINE = ParagraphStyle("codeline", fontName=MONO, fontSize=7.0, leading=8.6)
CODE = ParagraphStyle("code", fontName=MONO, fontSize=7.0, leading=8.6, backColor=CODE_BG, borderPadding=(2.5, 3, 2.5, 3),
                      spaceBefore=2, spaceAfter=5, leftIndent=3, rightIndent=3)


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _code(body):
    return f'<font name="{MONO}" size="7.4" color="#7a2e0e">{_esc(body)}</font>'


def rich(text):
    """Convert **bold** and `code` (also `code` inside bold) to reportlab markup, escaping &, < and >."""
    text = clean(text)
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if part.startswith("**") and part.endswith("**") and len(part) > 3:
            inner = re.split(r"(`[^`]+`)", part[2:-2])
            out.append("<b>" + "".join(_code(x[1:-1]) if x.startswith("`") and x.endswith("`") and len(x) > 1 else _esc(x)
                                       for x in inner) + "</b>")
        elif part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(_code(part[1:-1]))
        else:
            out.append(_esc(part))
    return "".join(out)


COL_W = (A4[0] - 2 * 11 * mm - 6 * mm) / 2       # width of one column


def build_flowables(items, week):
    flow = []
    for item in items:
        kind = item[0]
        if kind == "h":
            flow.append(Paragraph(rich(item[1]), HEAD))
        elif kind == "p":
            flow.append(Paragraph(rich(item[1]), BODY))
        elif kind == "bullets":
            for b in item[1]:
                flow.append(Paragraph(rich(b), BULLET, bulletText="•" if UNICODE else "*"))
            flow.append(Spacer(1, 2))
        elif kind == "code":
            text = clean(item[1].strip("\n"))
            for line in text.split("\n"):
                if len(line) > MAX_CODE_CHARS:
                    raise ValueError(f"Week {week}: code line too long ({len(line)}): {line!r}")
            # one table row per line, so a long block can still split across the two columns
            rows = [[Preformatted(line if line.strip() else " ", CODE_LINE)] for line in text.split("\n")]
            heights = [CODE_LINE.leading] * len(rows)
            heights[0] += 3          # room for the top padding
            heights[-1] += 3         # room for the bottom padding
            t = Table(rows, colWidths=[COL_W], rowHeights=heights)
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("TOPPADDING", (0, 0), (-1, 0), 3), ("BOTTOMPADDING", (0, -1), (-1, -1), 3)]))
            flow += [t, Spacer(1, 5)]
        elif kind == "table":
            header, rows = item[1], item[2]
            widths = item[3] if len(item) > 3 else [1 / len(header)] * len(header)
            data = [[Paragraph(rich(h), CELL_HEAD) for h in header]]
            data += [[Paragraph(rich(c), CELL) for c in row] for row in rows]
            t = Table(data, colWidths=[COL_W * w for w in widths], repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c5cfdd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
            ]))
            flow += [t, Spacer(1, 5)]
        elif kind == "tip":
            t = Table([[Paragraph(rich(item[1]), CELL)]], colWidths=[COL_W])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TIP_BG),
                                   ("LINEBEFORE", (0, 0), (0, -1), 2, TIP_EDGE),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 3),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            flow += [t, Spacer(1, 5)]
        else:
            raise ValueError(f"unknown item kind {kind!r}")
    return flow


def _measure(items, week):
    """Total height of all content when set in one column (used to balance the two columns)."""
    return sum(f.wrap(COL_W, 10_000)[1] + getattr(f.style, "spaceBefore", 0) + getattr(f.style, "spaceAfter", 0)
               if hasattr(f, "style") else f.wrap(COL_W, 10_000)[1]
               for f in build_flowables(items, week))


def make_pdf(path, week, title, block, items):
    """Write one cheatsheet with the two columns balanced. Returns the number of pages."""
    import io
    left = right = 11 * mm
    top, bottom = 22 * mm, 13 * mm
    gap = 6 * mm
    col_w = (A4[0] - left - right - gap) / 2
    full = A4[1] - top - bottom

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BLUE)
        canvas.rect(0, A4[1] - 17 * mm, A4[0], 17 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(SANS_BOLD, 14)
        canvas.drawString(left, A4[1] - 10.5 * mm, clean(f"Week {week}: {title}"))
        canvas.setFont(SANS, 8)
        canvas.drawRightString(A4[0] - right, A4[1] - 10.5 * mm, clean(block))
        canvas.setFillColor(GREY)
        canvas.setFont(SANS, 7)
        canvas.drawString(left, 7 * mm, clean("Bit by Bit Coding \u00b7 Web Development: HTML, SQL & Flask \u00b7 Quick reference"))
        canvas.drawRightString(A4[0] - right, 7 * mm, f"Week {week} \u00b7 page {doc.page}" if UNICODE else f"Week {week} - page {doc.page}")
        canvas.restoreState()

    def build(target, height):
        y = A4[1] - top - height                      # columns start at the top and are `height` tall
        frames = [Frame(left, y, col_w, height, id="c1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0),
                  Frame(left + col_w + gap, y, col_w, height, id="c2", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)]
        doc = BaseDocTemplate(target, pagesize=A4, title=clean(f"Week {week}: {title} - cheatsheet"),
                              author="Bit by Bit Coding", subject="Web Development: HTML, SQL & Flask")
        doc.addPageTemplates([PageTemplate(id="two", frames=frames, onPage=decorate)])
        doc.build(build_flowables(items, week))
        return doc.page

    total = _measure(items, week)
    height = min(full, max(total / 2 * 1.06, 60 * mm))
    while height < full and build(io.BytesIO(), height) > 1:      # too short: the content spilled to a second page
        height = min(full, height + 4 * mm)
    return build(str(path), height)
