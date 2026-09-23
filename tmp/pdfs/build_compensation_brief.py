from __future__ import annotations

import base64
import re
from io import BytesIO
from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "Neverlost_Labs_Initial_Project_Compensation_Model.pdf"
LOGO = ROOT / "assets" / "nvlt-official-logo.svg"

PAGE_W = 792
PAGE_H = 612

NAVY = HexColor("#132033")
NAVY_DEEP = HexColor("#0B1C33")
BLACK = HexColor("#000000")
COBALT = HexColor("#1357D4")
COBALT_SOFT = HexColor("#E8F0FF")
SLATE = HexColor("#526176")
SLATE_LIGHT = HexColor("#73849A")
LINE = HexColor("#D7E1EC")
LINE_BLUE = HexColor("#C6D7EA")
ICE = HexColor("#F4F8FD")
PALE = HexColor("#EDF4FB")
WHITE = HexColor("#FFFFFF")

EXPENSE_NOTE = "Illustrative example assumes no additional direct project expenses unless otherwise stated."


def register_fonts() -> None:
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("Segoe", fonts / "segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeSemi", fonts / "seguisb.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeBold", fonts / "segoeuib.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeItalic", fonts / "segoeuii.ttf"))


def mix(a: Color, b: Color, t: float) -> Color:
    return Color(
        a.red + (b.red - a.red) * t,
        a.green + (b.green - a.green) * t,
        a.blue + (b.blue - a.blue) * t,
    )


def draw_background(c: canvas.Canvas) -> None:
    left = HexColor("#F2F7FC")
    mid = HexColor("#EAF3FC")
    right = HexColor("#FFFFFF")
    bands = 160
    band_w = PAGE_W / bands + 0.5
    for i in range(bands):
        t = i / (bands - 1)
        color = mix(left, mid, t / 0.58) if t < 0.58 else mix(mid, right, (t - 0.58) / 0.42)
        c.setFillColor(color)
        c.rect(i * PAGE_W / bands, 0, band_w, PAGE_H, stroke=0, fill=1)
    c.setFillColor(Color(1, 1, 1, alpha=0.42))
    c.rect(0, 0, PAGE_W, 95, stroke=0, fill=1)


def load_logo() -> ImageReader:
    svg = LOGO.read_text(encoding="utf-8")
    match = re.search(r"base64,([^\"]+)", svg)
    if not match:
        raise RuntimeError("Embedded official NVLT logo was not found")
    return ImageReader(BytesIO(base64.b64decode(match.group(1))))


def draw_logo(c: canvas.Canvas, logo: ImageReader, x: float, y: float, size: float) -> None:
    c.saveState()
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)
    p = c.beginPath()
    p.circle(x + size / 2, y + size / 2, size / 2)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(logo, x, y, width=size, height=size, preserveAspectRatio=True, mask="auto")
    c.restoreState()
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.circle(x + size / 2, y + size / 2, size / 2 - 0.45, stroke=1, fill=0)


def pstyle(name: str, size: float, leading: float, color=NAVY, font="Segoe", **kwargs) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
        **kwargs,
    )


BODY = pstyle("body", 7.7, 9.45)
BODY_SMALL = pstyle("body-small", 7.1, 8.55)
MUTED = pstyle("muted", 7.0, 8.45, SLATE)
NOTE = pstyle("note", 6.65, 8.1, SLATE, "SegoeItalic")


def draw_para(c: canvas.Canvas, text: str, x: float, top: float, width: float, style: ParagraphStyle, max_h=500) -> float:
    para = Paragraph(text, style)
    _, h = para.wrap(width, max_h)
    para.drawOn(c, x, top - h)
    return top - h


def eyebrow(c: canvas.Canvas, text: str, x: float, y: float, size=6.6) -> None:
    c.setFont("SegoeBold", size)
    c.setFillColor(COBALT)
    c.drawString(x, y, text.upper())


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, radius=12, fill=WHITE) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def rule(c: canvas.Canvas, x1: float, y: float, x2: float, color=LINE, width=0.65) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def right_text(c: canvas.Canvas, text: str, x: float, y: float, font="Segoe", size=7.5, color=BLACK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawRightString(x, y, text)


def table_row(c: canvas.Canvas, label: str, value: str, x: float, y: float, w: float, bold=False, size=7.35) -> None:
    font = "SegoeSemi" if bold else "Segoe"
    color = BLACK if re.search(r"\d", label) else (NAVY if bold else SLATE)
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, label)
    right_text(c, value, x + w, y, font, size, BLACK)


def example_eyebrow(c: canvas.Canvas, number: str, x: float, y: float, size=6.6) -> None:
    label = "EXAMPLE"
    c.setFont("SegoeBold", size)
    c.setFillColor(COBALT)
    c.drawString(x, y, label)
    c.setFillColor(BLACK)
    c.drawString(x + pdfmetrics.stringWidth(label, "SegoeBold", size) + 3, y, number)


def draw_header(c: canvas.Canvas, logo: ImageReader) -> None:
    brand = "Neverlost Labs"
    brand_size = 20.0
    c.setFillColor(NAVY)
    c.setFont("SegoeBold", brand_size)
    c.drawCentredString(PAGE_W / 2, 571, brand)
    draw_logo(c, logo, 726, 554, 36)
    c.setFillColor(SLATE)
    c.setFont("SegoeSemi", 6.4)
    c.drawCentredString(PAGE_W / 2, 546, "SOFTWARE & APPLIED AI  |  NEVERLOST SYSTEMS")
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.8)
    c.line(30, 536, 762, 536)

    c.setFillColor(NAVY_DEEP)
    c.setFont("SegoeBold", 18.0)
    c.drawString(30, 509, "Initial Project Compensation Model")
    c.setFillColor(SLATE)
    c.setFont("Segoe", 8.2)
    c.drawString(30, 493, "Initial operating model for paid client projects")


def draw_arrow(c: canvas.Canvas, x1: float, x2: float, y: float) -> None:
    c.setStrokeColor(COBALT)
    c.setFillColor(COBALT)
    c.setLineWidth(1.0)
    c.line(x1, y, x2 - 4, y)
    p = c.beginPath()
    p.moveTo(x2, y)
    p.lineTo(x2 - 5, y + 2.5)
    p.lineTo(x2 - 5, y - 2.5)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def draw_operating_model(c: canvas.Canvas) -> None:
    eyebrow(c, "Operating Model", 30, 474)
    x, y, w, h = 30, 418, 732, 46
    card(c, x, y, w, h, radius=11, fill=Color(1, 1, 1, alpha=0.82))

    flow_x = x + 15
    flow_w = 385
    labels = ["Client Revenue", "Direct Expenses", "Approved Labor", "Remaining Margin"]
    label_w = 82
    gap = 15
    for i, label in enumerate(labels):
        lx = flow_x + i * (label_w + gap)
        c.setFillColor(NAVY if i < 3 else COBALT)
        c.setFont("SegoeSemi", 7.55)
        c.drawCentredString(lx + label_w / 2, y + 20, label)
        if i < 3:
            draw_arrow(c, lx + label_w + 2, lx + label_w + gap - 2, y + 22)

    divider_x = x + flow_w + 24
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.7)
    c.line(divider_x, y + 9, divider_x, y + h - 9)

    shares = [
        ("20%", "Neverlost Labs"),
        ("40%", "Jeff"),
        ("40%", "Neo"),
    ]
    share_x = divider_x + 17
    share_w = (x + w - share_x - 10) / 3
    for i, (pct, name) in enumerate(shares):
        cx = share_x + i * share_w + share_w / 2
        c.setFillColor(BLACK)
        c.setFont("SegoeBold", 12.0)
        c.drawCentredString(cx, y + 25, pct)
        c.setFillColor(SLATE)
        c.setFont("SegoeSemi", 6.5)
        c.drawCentredString(cx, y + 13, name)


def draw_working_rules(c: canvas.Canvas) -> None:
    x, y, w, h = 30, 72, 243, 335
    card(c, x, y, w, h)
    eyebrow(c, "Working Rules", x + 15, y + h - 21)

    c.setFillColor(COBALT_SOFT)
    c.roundRect(x + 14, y + h - 68, w - 28, 32, 8, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.setFont("SegoeBold", 13.0)
    c.drawString(x + 25, y + h - 56, "$50/hour")
    c.setFillColor(NAVY)
    c.setFont("SegoeSemi", 7.25)
    c.drawString(x + 91, y + h - 55, "initial internal labor rate")
    c.setFillColor(SLATE)
    c.setFont("Segoe", 6.65)
    c.drawString(x + 91, y + h - 65, "for Jeff and Neo")

    rules = [
        "Jeff tracks documented sales/business-development and project-management hours.",
        "Neo provides estimated technical hours before acceptance.",
        "Both parties approve compensated-hour budgets before starting.",
        "Neither rate nor labor budget changes without mutual approval.",
        "Actual hours are always recorded.",
        "Finishing below estimate increases project margin.",
        "Client scope increases require mutual approval and, where appropriate, a change order.",
        "Direct project expenses and additional developers are deducted before margin distribution.",
    ]
    top = y + h - 83
    for text in rules:
        c.setFillColor(COBALT)
        c.circle(x + 18.5, top - 4.4, 1.55, stroke=0, fill=1)
        new_top = draw_para(c, text, x + 26, top, w - 41, BODY, max_h=60)
        top = new_top - 7.0


def draw_example_one(c: canvas.Canvas) -> None:
    x, y, w, h = 283, 72, 234, 335
    card(c, x, y, w, h)
    example_eyebrow(c, "1", x + 15, y + h - 21)
    c.setFillColor(BLACK)
    c.setFont("SegoeBold", 11.0)
    c.drawString(x + 15, y + h - 41, "$3,000 Strategic First Project")

    top = y + h - 57
    top = draw_para(c, "<b>Actual Jeff hours:</b> <font color='#000000'>50</font> &nbsp;&nbsp; <b>Actual Neo hours:</b> <font color='#000000'>50</font>", x + 15, top, w - 30, BODY_SMALL)
    top -= 3
    top = draw_para(c, "<b>Normal labor value at <font color='#000000'>$50/hour</font>:</b> <font color='#000000'>$5,000</font>", x + 15, top, w - 30, BODY_SMALL)

    note_top = top - 8
    strategic = (
        "Because this is an intentionally strategic early project, both may mutually approve fewer "
        "compensated hours before acceptance."
    )
    para = Paragraph(strategic, pstyle("strategic", 6.9, 8.35, NAVY))
    _, ph = para.wrap(w - 46, 60)
    box_h = ph + 18
    c.setFillColor(COBALT_SOFT)
    c.roundRect(x + 14, note_top - box_h, w - 28, box_h, 8, stroke=0, fill=1)
    c.setFillColor(COBALT)
    c.rect(x + 14, note_top - box_h, 2.4, box_h, stroke=0, fill=1)
    para.drawOn(c, x + 25, note_top - ph - 9)
    top = note_top - box_h - 8

    c.setFillColor(SLATE)
    c.setFont("SegoeSemi", 6.65)
    c.drawString(x + 15, top, "EXAMPLE COMPENSATED HOURS:")
    c.setFillColor(BLACK)
    c.setFont("SegoeBold", 8.2)
    c.drawRightString(x + w - 15, top, "20 each")
    top -= 10
    rule(c, x + 15, top, x + w - 15)
    top -= 14

    table_row(c, "Jeff labor", "$1,000", x + 15, top, w - 30)
    top -= 14
    table_row(c, "Neo labor", "$1,000", x + 15, top, w - 30)
    top -= 14
    table_row(c, "Remaining margin", "$1,000", x + 15, top, w - 30, bold=True)
    top -= 10
    rule(c, x + 15, top, x + w - 15, LINE_BLUE, 0.8)
    top -= 16

    c.setFillColor(SLATE)
    c.setFont("SegoeSemi", 6.5)
    c.drawString(x + 15, top, "MARGIN DISTRIBUTION")
    top -= 20
    labels = [
        ("Neverlost Labs", "20%", "$200"),
        ("Jeff profit share", "40%", "$400"),
        ("Neo profit share", "40%", "$400"),
    ]
    col_w = (w - 30) / 3
    for i, (name, pct, amount) in enumerate(labels):
        cx = x + 15 + i * col_w + col_w / 2
        c.setFillColor(BLACK)
        c.setFont("SegoeBold", 8.2)
        c.drawCentredString(cx, top, amount)
        c.setFillColor(BLACK)
        c.setFont("SegoeSemi", 5.8)
        c.drawCentredString(cx, top - 10, f"{name}  {pct}")
    top -= 27

    c.setFillColor(ICE)
    c.roundRect(x + 14, top - 37, w - 28, 37, 8, stroke=0, fill=1)
    totals = [("Jeff total", "$1,400"), ("Neo total", "$1,400"), ("Labs retained", "$200")]
    tw = (w - 38) / 3
    for i, (label, value) in enumerate(totals):
        cx = x + 19 + i * tw + tw / 2
        c.setFillColor(SLATE)
        c.setFont("SegoeSemi", 5.9)
        c.drawCentredString(cx, top - 13, label)
        c.setFillColor(BLACK)
        c.setFont("SegoeBold", 8.0)
        c.drawCentredString(cx, top - 27, value)
    top -= 45
    draw_para(
        c,
        "The uncompensated time remains recorded and is treated as a mutually agreed strategic investment in establishing Neverlost Labs.",
        x + 15,
        top,
        w - 30,
        NOTE,
        max_h=50,
    )
    c.setFillColor(SLATE_LIGHT)
    c.setFont("SegoeItalic", 5.2)
    c.drawString(x + 15, y + 6, EXPENSE_NOTE)


def draw_example_two(c: canvas.Canvas) -> None:
    x, y, w, h = 527, 72, 235, 335
    card(c, x, y, w, h)
    example_eyebrow(c, "2", x + 15, y + h - 21)
    c.setFillColor(BLACK)
    c.setFont("SegoeBold", 11.0)
    c.drawString(x + 15, y + h - 41, "$10,000 Standard Project")

    top = y + h - 68
    c.setFillColor(ICE)
    c.roundRect(x + 14, top - 48, w - 28, 48, 8, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.setFont("Segoe", 7.4)
    c.drawString(x + 25, top - 17, "Jeff: 20 hrs x $50")
    right_text(c, "$1,000", x + w - 25, top - 17, "SegoeSemi", 7.6, BLACK)
    c.setFillColor(BLACK)
    c.setFont("Segoe", 7.4)
    c.drawString(x + 25, top - 35, "Neo: 50 hrs x $50")
    right_text(c, "$2,500", x + w - 25, top - 35, "SegoeSemi", 7.6, BLACK)
    top -= 64

    table_row(c, "Remaining margin after labor", "$6,500", x + 15, top, w - 30, bold=True, size=7.55)
    top -= 11
    rule(c, x + 15, top, x + w - 15, LINE_BLUE, 0.8)
    top -= 18
    table_row(c, "Neverlost Labs 20%", "$1,300", x + 15, top, w - 30)
    top -= 17
    table_row(c, "Jeff 40%", "$2,600", x + 15, top, w - 30)
    top -= 17
    table_row(c, "Neo 40%", "$2,600", x + 15, top, w - 30)
    top -= 16
    rule(c, x + 15, top, x + w - 15)
    top -= 20

    c.setFillColor(COBALT_SOFT)
    c.roundRect(x + 14, top - 88, w - 28, 88, 9, stroke=0, fill=1)
    c.setFillColor(COBALT)
    c.setFont("SegoeBold", 6.7)
    c.drawString(x + 25, top - 17, "FINAL DISTRIBUTION")
    final_rows = [("Jeff total", "$3,600"), ("Neo total", "$5,100"), ("Labs retained", "$1,300")]
    yy = top - 38
    for label, value in final_rows:
        c.setFillColor(NAVY)
        c.setFont("SegoeSemi", 7.6)
        c.drawString(x + 25, yy, label)
        right_text(c, value, x + w - 25, yy, "SegoeBold", 8.2, BLACK)
        yy -= 18
    c.setFillColor(SLATE_LIGHT)
    c.setFont("SegoeItalic", 5.2)
    c.drawString(x + 15, y + 6, EXPENSE_NOTE)


def draw_pilot(c: canvas.Canvas) -> None:
    x, y, w, h = 30, 19, 732, 40
    c.setFillColor(Color(1, 1, 1, alpha=0.72))
    c.setStrokeColor(LINE)
    c.setLineWidth(0.65)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    c.setFillColor(COBALT)
    c.roundRect(x, y, 3.4, h, 1.7, stroke=0, fill=1)
    eyebrow(c, "Model Review", x + 15, y + 24, 6.4)
    draw_para(
        c,
        "This compensation structure will serve as the initial operating model for Neverlost Labs. The model may be reviewed after the first completed paid project, or after additional projects if more operating data is needed. Any changes will be made by mutual agreement based on actual sales effort, development effort, project-management requirements, margins, team structure, and overall project performance.",
        x + 93,
        y + 30,
        w - 108,
        pstyle("pilot", 6.0, 7.1, SLATE),
        max_h=32,
    )


def draw_page_two_header(c: canvas.Canvas, logo: ImageReader) -> None:
    c.setFillColor(NAVY)
    c.setFont("SegoeBold", 20.0)
    c.drawCentredString(PAGE_W / 2, 571, "Neverlost Labs")
    draw_logo(c, logo, 726, 554, 36)
    c.setFillColor(SLATE)
    c.setFont("SegoeSemi", 6.4)
    c.drawCentredString(PAGE_W / 2, 546, "SOFTWARE & APPLIED AI  |  NEVERLOST SYSTEMS")
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.8)
    c.line(30, 536, 762, 536)

    c.setFillColor(NAVY_DEEP)
    c.setFont("SegoeBold", 18.0)
    c.drawString(30, 509, "Scaling the Project Model")
    c.setFillColor(SLATE)
    c.setFont("Segoe", 8.2)
    c.drawString(
        30,
        493,
        "How hourly engagements and multi-developer projects use the same internal compensation structure.",
    )


def draw_compact_value_row(
    c: canvas.Canvas,
    label: str,
    value: str,
    x: float,
    y: float,
    w: float,
    value_color=BLACK,
    size=6.7,
) -> None:
    c.setFillColor(SLATE)
    c.setFont("Segoe", size)
    c.drawString(x, y, label)
    right_text(c, value, x + w, y, "SegoeSemi", size, value_color)


def draw_hourly_section(c: canvas.Canvas) -> None:
    x, y, w, h = 30, 75, 359, 393
    card(c, x, y, w, h)
    eyebrow(c, "Hourly Client Engagements", x + 15, y + h - 21)

    top = y + h - 36
    top = draw_para(
        c,
        "<b>Hourly engagements are treated internally the same as fixed-price contracts.</b>",
        x + 15,
        top,
        w - 30,
        pstyle("hourly-principle", 8.6, 10.3, NAVY),
        max_h=36,
    )
    top -= 7
    top = draw_para(
        c,
        "For hourly client engagements, total project revenue equals the client-approved billable hours multiplied by the contracted client rate. Once that revenue is established, the standard Neverlost Labs compensation waterfall applies.",
        x + 15,
        top,
        w - 30,
        pstyle("hourly-copy", 7.05, 8.8, SLATE),
        max_h=58,
    )

    eq_y = 321
    c.setFillColor(COBALT_SOFT)
    c.roundRect(x + 14, eq_y, w - 28, 55, 9, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("SegoeSemi", 9.0)
    c.drawCentredString(x + w / 2, eq_y + 35, "Client Billable Hours  x  Client Rate  =  Project Revenue")
    rule(c, x + 28, eq_y + 25, x + w - 28, LINE_BLUE, 0.65)
    c.setFillColor(SLATE)
    c.setFont("SegoeSemi", 5.8)
    c.drawCentredString(
        x + w / 2,
        eq_y + 11,
        "Project Revenue  ->  Expenses  ->  Approved Internal Labor  ->  Remaining Margin  ->  20% Labs / 40% Jeff / 40% Neo",
    )

    callout_y = 286
    c.setFillColor(ICE)
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.65)
    c.roundRect(x + 14, callout_y, w - 28, 25, 8, stroke=1, fill=1)
    c.setFillColor(COBALT)
    c.setFont("SegoeBold", 8.1)
    c.drawCentredString(x + w / 2, callout_y + 9, "30 hours x $80/hour = $2,400 project revenue")

    ex_x, ex_y, ex_w, ex_h = x + 14, 97, w - 28, 179
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.75)
    c.roundRect(ex_x, ex_y, ex_w, ex_h, 10, stroke=1, fill=1)
    eyebrow(c, "Example 3", ex_x + 14, ex_y + ex_h - 18, 6.3)
    c.setFillColor(SLATE_LIGHT)
    c.setFont("SegoeItalic", 5.2)
    c.drawRightString(ex_x + ex_w - 14, ex_y + ex_h - 18, EXPENSE_NOTE)
    c.setFillColor(NAVY)
    c.setFont("SegoeBold", 10.0)
    c.drawString(ex_x + 14, ex_y + ex_h - 36, "Hourly Engagement")
    c.setFillColor(SLATE)
    c.setFont("Segoe", 6.9)
    c.drawString(ex_x + 14, ex_y + ex_h - 52, "Client engagement: 30 hours at $80/hour")
    c.setFillColor(COBALT)
    c.setFont("SegoeBold", 9.2)
    c.drawString(ex_x + 14, ex_y + ex_h - 70, "30 x $80 = $2,400 client revenue")

    alloc_y = ex_y + ex_h - 98
    eyebrow(c, "Margin Allocation", ex_x + 14, alloc_y + 13, 5.8)
    allocs = [("Neverlost Labs 20%", "$120"), ("Jeff 40%", "$240"), ("Neo 40%", "$240")]
    aw = (ex_w - 28) / 3
    for i, (label, value) in enumerate(allocs):
        cx = ex_x + 14 + i * aw + aw / 2
        c.setFillColor(COBALT)
        c.setFont("SegoeBold", 7.3)
        c.drawCentredString(cx, alloc_y, value)
        c.setFillColor(SLATE)
        c.setFont("SegoeSemi", 5.8)
        c.drawCentredString(cx, alloc_y - 10, label)

    split_y_top = alloc_y - 21
    rule(c, ex_x + 14, split_y_top, ex_x + ex_w - 14, LINE, 0.6)
    div_x = ex_x + ex_w / 2
    c.setStrokeColor(LINE)
    c.line(div_x, ex_y + 9, div_x, split_y_top - 7)

    left_x = ex_x + 14
    left_w = ex_w / 2 - 24
    eyebrow(c, "Approved Internal Labor", left_x, split_y_top - 14, 5.7)
    draw_compact_value_row(c, "Jeff: 6 hours x $50", "$300", left_x, split_y_top - 28, left_w)
    draw_compact_value_row(c, "Neo: 30 hours x $50", "$1,500", left_x, split_y_top - 40, left_w)
    eyebrow(c, "Remaining Margin", left_x, split_y_top - 52, 5.7)
    c.setFillColor(COBALT)
    c.setFont("SegoeBold", 6.5)
    c.drawString(left_x, split_y_top - 64, "$2,400 - $300 - $1,500 = $600")

    right_x = div_x + 12
    right_w = ex_x + ex_w - 14 - right_x
    eyebrow(c, "Final Compensation", right_x, split_y_top - 14, 5.7)
    draw_compact_value_row(c, "Jeff", "$540", right_x, split_y_top - 28, right_w, COBALT, 7.0)
    draw_compact_value_row(c, "Neo", "$1,740", right_x, split_y_top - 40, right_w, COBALT, 7.0)
    draw_compact_value_row(c, "Neverlost Labs retained", "$120", right_x, split_y_top - 52, right_w, COBALT, 6.3)

    draw_para(
        c,
        "If the client authorizes additional billable hours, project revenue increases accordingly and the same compensation waterfall continues to apply.",
        x + 15,
        91,
        w - 30,
        pstyle("hourly-note", 6.25, 7.45, SLATE, "SegoeItalic"),
        max_h=20,
    )


def draw_multi_developer_section(c: canvas.Canvas) -> None:
    x, y, w, h = 403, 75, 359, 393
    card(c, x, y, w, h)
    eyebrow(c, "Multi-Developer Projects", x + 15, y + h - 21)

    top = y + h - 36
    top = draw_para(
        c,
        "As Neverlost Labs takes on larger engagements, additional developers may be brought into the project under Neo's technical leadership. Their compensation is treated as direct project labor before profit distribution.",
        x + 15,
        top,
        w - 30,
        pstyle("multi-copy", 7.05, 8.8, SLATE),
        max_h=58,
    )

    emphasis_y = 365
    c.setFillColor(COBALT_SOFT)
    c.roundRect(x + 14, emphasis_y, w - 28, 27, 8, stroke=0, fill=1)
    draw_para(
        c,
        "<b>Additional developers are compensated as direct project labor and do not participate in the Jeff/Neo profit distribution unless separately agreed in writing.</b>",
        x + 25,
        emphasis_y + 19,
        w - 50,
        pstyle("multi-emphasis", 7.15, 8.5, NAVY),
        max_h=24,
    )
    draw_para(
        c,
        "Their rates are agreed separately and deducted as project labor costs before the remaining margin is distributed.",
        x + 15,
        355,
        w - 30,
        pstyle("multi-rates", 6.85, 8.4, SLATE),
        max_h=25,
    )

    ex_x, ex_y, ex_w, ex_h = x + 14, 77, w - 28, 247
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE_BLUE)
    c.setLineWidth(0.75)
    c.roundRect(ex_x, ex_y, ex_w, ex_h, 10, stroke=1, fill=1)
    eyebrow(c, "Example 4", ex_x + 14, ex_y + ex_h - 17, 6.3)
    c.setFillColor(SLATE_LIGHT)
    c.setFont("SegoeItalic", 5.2)
    c.drawRightString(ex_x + ex_w - 14, ex_y + ex_h - 17, EXPENSE_NOTE)
    c.setFillColor(NAVY)
    c.setFont("SegoeBold", 10.0)
    c.drawString(ex_x + 14, ex_y + ex_h - 35, "$20,000 Team Project")

    assumptions_y = ex_y + ex_h - 52
    eyebrow(c, "Assumptions", ex_x + 14, assumptions_y, 5.7)
    half_w = (ex_w - 42) / 2
    left_x = ex_x + 14
    right_x = ex_x + 28 + half_w
    draw_compact_value_row(c, "Jeff: 20 hours x $50", "$1,000", left_x, assumptions_y - 15, half_w, BLACK, 6.4)
    draw_compact_value_row(c, "Neo: 40 hours x $50", "$2,000", left_x, assumptions_y - 29, half_w, BLACK, 6.4)
    draw_compact_value_row(c, "Developer A: 40 hours x $50", "$2,000", right_x, assumptions_y - 15, half_w, BLACK, 6.1)
    draw_compact_value_row(c, "Developer B: 40 hours x $50", "$2,000", right_x, assumptions_y - 29, half_w, BLACK, 6.1)

    summary_y = assumptions_y - 67
    c.setFillColor(ICE)
    c.roundRect(ex_x + 14, summary_y, ex_w - 28, 31, 7, stroke=0, fill=1)
    summaries = [
        ("Total direct labor", "$7,000"),
        ("Contract revenue", "$20,000"),
        ("Remaining margin", "$13,000"),
    ]
    sw = (ex_w - 28) / 3
    for i, (label, value) in enumerate(summaries):
        cx = ex_x + 14 + i * sw + sw / 2
        c.setFillColor(COBALT if i == 2 else BLACK)
        c.setFont("SegoeBold", 7.4)
        c.drawCentredString(cx, summary_y + 17, value)
        c.setFillColor(SLATE)
        c.setFont("SegoeSemi", 5.4)
        c.drawCentredString(cx, summary_y + 7, label)

    c.setFillColor(COBALT)
    c.setFont("SegoeBold", 6.4)
    c.drawCentredString(ex_x + ex_w / 2, summary_y - 11, "$20,000 - $7,000 = $13,000")

    margin_y = summary_y - 22
    eyebrow(c, "Margin Distribution", ex_x + 14, margin_y, 5.7)
    margins = [("Neverlost Labs 20%", "$2,600"), ("Jeff 40%", "$5,200"), ("Neo 40%", "$5,200")]
    for i, (label, value) in enumerate(margins):
        cx = ex_x + 14 + i * sw + sw / 2
        c.setFillColor(COBALT)
        c.setFont("SegoeBold", 7.2)
        c.drawCentredString(cx, margin_y - 14, value)
        c.setFillColor(SLATE)
        c.setFont("SegoeSemi", 5.5)
        c.drawCentredString(cx, margin_y - 24, label)

    table_top = margin_y - 30
    cols = [ex_x + 14, ex_x + 161, ex_x + 222, ex_x + ex_w - 14]
    headers = [("RECIPIENT", cols[0]), ("LABOR", cols[1]), ("PROFIT SHARE", cols[2]), ("TOTAL", cols[3])]
    c.setFillColor(SLATE_LIGHT)
    c.setFont("SegoeBold", 5.4)
    c.drawString(headers[0][1], table_top, headers[0][0])
    c.drawRightString(headers[1][1], table_top, headers[1][0])
    c.drawRightString(headers[2][1], table_top, headers[2][0])
    c.drawRightString(headers[3][1], table_top, headers[3][0])
    rule(c, ex_x + 14, table_top - 5, ex_x + ex_w - 14, LINE_BLUE, 0.7)

    rows = [
        ("Jeff", "$1,000", "$5,200", "$6,200"),
        ("Neo", "$2,000", "$5,200", "$7,200"),
        ("Developer A", "$2,000", "-", "$2,000"),
        ("Developer B", "$2,000", "-", "$2,000"),
        ("Neverlost Labs", "-", "-", "$2,600 retained"),
    ]
    row_y = table_top - 13
    for recipient, labor, share, total in rows:
        c.setFillColor(NAVY)
        c.setFont("SegoeSemi", 5.9)
        c.drawString(cols[0], row_y, recipient)
        right_text(c, labor, cols[1], row_y, "Segoe", 5.9, BLACK)
        right_text(c, share, cols[2], row_y, "Segoe", 5.9, BLACK)
        right_text(c, total, cols[3], row_y, "SegoeBold", 6.0, COBALT)
        row_y -= 9.4

    total_y = ex_y + 6
    c.setFillColor(COBALT_SOFT)
    c.roundRect(ex_x + 14, total_y, ex_w - 28, 17, 5, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("SegoeSemi", 6.3)
    c.drawString(ex_x + 23, total_y + 5, "Total project distribution")
    right_text(c, "$20,000", ex_x + ex_w - 23, total_y + 5, "SegoeBold", 7.0, COBALT)


def draw_bottom_principle(c: canvas.Canvas) -> None:
    x, y, w, h = 30, 14, 732, 49
    c.setFillColor(Color(1, 1, 1, alpha=0.76))
    c.setStrokeColor(LINE)
    c.setLineWidth(0.65)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    c.setFillColor(COBALT)
    c.roundRect(x, y, 3.4, h, 1.7, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.setFont("SegoeBold", 8.0)
    c.drawString(x + 15, y + 29, "One model, regardless of contract type.")
    draw_para(
        c,
        "Whether work is fixed-price, hourly, or delivered by a larger development team, Neverlost Labs uses the same internal structure: compensate approved labor first, preserve company margin, then share remaining project profit between Jeff and Neo.",
        x + 190,
        y + 35,
        w - 205,
        pstyle("bottom-principle", 6.75, 8.15, SLATE),
        max_h=34,
    )


def build() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Neverlost Labs - Initial Project Compensation Model")
    c.setAuthor("Neverlost Labs")
    c.setSubject("Initial operating model for paid client projects")
    c.setCreator("Neverlost Systems")

    draw_background(c)
    logo = load_logo()
    draw_header(c, logo)
    draw_operating_model(c)
    draw_working_rules(c)
    draw_example_one(c)
    draw_example_two(c)
    draw_pilot(c)

    c.showPage()
    draw_background(c)
    draw_page_two_header(c, logo)
    draw_hourly_section(c)
    draw_multi_developer_section(c)
    draw_bottom_principle(c)

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
