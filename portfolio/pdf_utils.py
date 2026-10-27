from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, FrameBreak, HRFlowable, KeepInFrame,
    NextPageTemplate, PageTemplate, Paragraph, Spacer,
)

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm
GAP = 8 * mm

# ==========================================
# SECTION ORDER BASED ON CV TYPE
# ==========================================
SECTION_ORDER = {
    "academic": ["education", "projects", "skills", "experience"],
    "job":      ["experience", "skills", "projects", "education"],
    "faculty":  ["education", "experience", "projects", "skills"],
}

# --------------------------------------------------------------------------
# Data Collection
# --------------------------------------------------------------------------
def _collect(user):
    """Fetch user data to populate the PDF."""
    profile = getattr(user, "profile", None)
    return {
        "name": (user.get_full_name() or user.username).strip(),
        "email": user.email or "",
        "phone": getattr(profile, "phone", "") or "",
        "bio": getattr(profile, "bio", "") or "",
        "educations": list(user.educations.all().order_by("-passing_year")),
        "experiences": list(user.experiences.all().order_by("-start_date")),
        "skills": list(user.skills.all()),
        "projects": list(user.projects.all()),
        "links": list(user.social_links.all()),
    }

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def _t(value):
    return escape(str(value)) if value not in (None, "") else ""

def _multiline(value):
    return _t(value).replace("\n", "<br/>")

def _d(value):
    return value.strftime("%b %Y") if value else ""

def _dates(exp):
    return f"{_d(exp.start_date)} - {_d(exp.end_date) or 'Present'}"

def _href(url):
    return escape(str(url), {'"': "&quot;"})

def _styles(body, muted, heading, accent, link, name_color=None, contact_color=None, name_size=24):
    hx = colors.HexColor
    def ps(name, font="Helvetica", **kw):
        return ParagraphStyle(name, fontName=font, **kw)
    return {
        "accent": accent,
        "link": link,
        "name": ps("name", "Helvetica-Bold", fontSize=name_size, leading=name_size + 4, textColor=hx(name_color or heading)),
        "contact": ps("contact", fontSize=9, leading=12.5, textColor=hx(contact_color or muted)),
        "h2": ps("h2", "Helvetica-Bold", fontSize=10.5, leading=13, textColor=hx(heading), spaceBefore=9, spaceAfter=2),
        "h3": ps("h3", "Helvetica-Bold", fontSize=10, leading=12.5, textColor=hx(heading)),
        "meta": ps("meta", fontSize=8.5, leading=11.5, textColor=hx(muted), spaceAfter=1),
        "body": ps("body", fontSize=9, leading=12.5, textColor=hx(body)),
    }

def _section(title, body, st):
    if not body: return []
    return [Paragraph(title.upper(), st["h2"]), HRFlowable(width="100%", thickness=0.8, color=colors.HexColor(st["accent"]), spaceBefore=0, spaceAfter=5)] + body

# --------------------------------------------------------------------------
# Content Blocks
# --------------------------------------------------------------------------
def _profile_block(data, st):
    return [Paragraph(_multiline(data["bio"]), st["body"])] if data["bio"] else []

def _contact_block(data, st):
    out = []
    if data["email"]: out.append(Paragraph(_t(data["email"]), st["body"]))
    if data["phone"]: out.append(Paragraph(_t(data["phone"]), st["body"]))
    return out

def _experience_block(data, st):
    out = []
    for exp in data["experiences"]:
        out.append(Paragraph(_t(exp.designation), st["h3"]))
        out.append(Paragraph(f"{_t(exp.company)} | {_dates(exp)}", st["meta"]))
        if exp.description: out.append(Paragraph(_multiline(exp.description), st["body"]))
        out.append(Spacer(1, 6))
    return out

def _education_block(data, st):
    out = []
    for edu in data["educations"]:
        out.append(Paragraph(_t(edu.degree), st["h3"]))
        parts = [_t(edu.institute), _t(edu.passing_year)]
        if edu.cgpa not in (None, ""): parts.append(f"CGPA {_t(edu.cgpa)}")
        out.append(Paragraph(" | ".join(p for p in parts if p), st["meta"]))
        out.append(Spacer(1, 5))
    return out

def _skills_block(data, st, as_lines=False):
    names = [_t(s.skill_name) for s in data["skills"] if s.skill_name]
    if not names: return []
    if as_lines: return [Paragraph(n, st["body"]) for n in names]
    return [Paragraph(", ".join(names), st["body"])]

def _projects_block(data, st):
    out = []
    for p in data["projects"]:
        out.append(Paragraph(_t(p.project_name), st["h3"]))
        if p.description: out.append(Paragraph(_multiline(p.description), st["body"]))
        if p.live_link: out.append(Paragraph(f'<link href="{_href(p.live_link)}" color="{st["link"]}">{_t(p.live_link)}</link>', st["meta"]))
        out.append(Spacer(1, 6))
    return out

def _links_block(data, st):
    out = []
    for l in data["links"]:
        out.append(Paragraph(f'<b>{_t(l.platform)}</b><br/><link href="{_href(l.url)}" color="{st["link"]}">{_t(l.url)}</link>', st["body"]))
        out.append(Spacer(1, 3))
    return out

def _links_inline(data, st):
    if not data["links"]: return None
    parts = [f'<link href="{_href(l.url)}" color="{st["link"]}">{_t(l.platform)}</link>' for l in data["links"]]
    return Paragraph("  |  ".join(parts), st["contact"])

# --------------------------------------------------------------------------
# Document Layout Engine
# --------------------------------------------------------------------------
def _doc(buf, data):
    return BaseDocTemplate(buf, pagesize=A4, leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0, title=f"{data['name']} - CV", author=data["name"])

def _frame(fid, x, y, w, h):
    return Frame(x, y, w, h, id=fid, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

def _fit(items, w, h):
    return KeepInFrame(w, h, items or [Spacer(1, 1)], mode="shrink")

def _contact_line(data):
    return "  |  ".join(x for x in (_t(data["email"]), _t(data["phone"])) if x)

def _two_column(buf, data, *, st, band, left, right, left_ratio, header_extra=None):
    header_h = 38 * mm if band else 34 * mm
    total_w = PAGE_W - 2 * MARGIN
    left_w = (total_w - GAP) * left_ratio
    right_w = total_w - GAP - left_w
    body_h = PAGE_H - header_h - MARGIN - 6 * mm

    def on_page(c, _doc):
        c.saveState()
        if band:
            c.setFillColor(colors.HexColor(band))
            c.rect(0, PAGE_H - header_h, PAGE_W, header_h, stroke=0, fill=1)
        else:
            c.setStrokeColor(colors.HexColor(st["accent"]))
            c.setLineWidth(1.2)
            c.line(MARGIN, PAGE_H - header_h, PAGE_W - MARGIN, PAGE_H - header_h)
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.setLineWidth(0.6)
        x = MARGIN + left_w + GAP / 2
        c.line(x, MARGIN, x, MARGIN + body_h)
        c.restoreState()

    doc = _doc(buf, data)
    doc.addPageTemplates([PageTemplate(id="main", frames=[
        _frame("head", MARGIN, PAGE_H - header_h + 4 * mm, total_w, header_h - 8 * mm),
        _frame("left", MARGIN, MARGIN, left_w, body_h),
        _frame("right", MARGIN + left_w + GAP, MARGIN, right_w, body_h),
    ], onPage=on_page)])

    head = [Paragraph(_t(data["name"]), st["name"])]
    if _contact_line(data): head.append(Paragraph(_contact_line(data), st["contact"]))
    if header_extra is not None: head.append(header_extra)

    doc.build(head + [FrameBreak(), _fit(left, left_w, body_h), FrameBreak(), _fit(right, right_w, body_h)])

# --------------------------------------------------------------------------
# Three PDF Layouts
# --------------------------------------------------------------------------

def _classic(buf, data, cv_type):
    st = _styles(body="#1f2937", muted="#6b7280", heading="#1e3a8a", accent="#1e3a8a", link="#1d4ed8", name_color="#ffffff", contact_color="#dbeafe", name_size=26)
    
    sections = {
        "profile": _section("Profile", _profile_block(data, st), st),
        "education": _section("Education", _education_block(data, st), st),
        "experience": _section("Experience", _experience_block(data, st), st),
        "skills": _section("Skills", _skills_block(data, st, as_lines=True), st),
        "projects": _section("Projects", _projects_block(data, st), st),
        "links": _section("Links", _links_block(data, st), st),
    }
    
    left_flow = sections["profile"]
    right_flow = []
    for key in SECTION_ORDER.get(cv_type, SECTION_ORDER["job"]):
        right_flow += sections[key]

    # Classic: Single column with a beautiful blue header band
    header_h = 38 * mm
    total_w = PAGE_W - 2 * MARGIN
    body_h = PAGE_H - header_h - MARGIN - 6 * mm

    def on_page(c, _doc):
        c.saveState()
        c.setFillColor(colors.HexColor("#1e3a8a"))
        c.rect(0, PAGE_H - header_h, PAGE_W, header_h, stroke=0, fill=1)
        c.restoreState()

    doc = _doc(buf, data)
    doc.addPageTemplates([PageTemplate(id="main", frames=[
        _frame("head", MARGIN, PAGE_H - header_h + 4 * mm, total_w, header_h - 8 * mm),
        _frame("body", MARGIN, MARGIN, total_w, body_h),
    ], onPage=on_page)])

    head = [Paragraph(_t(data["name"]), st["name"])]
    if _contact_line(data): head.append(Paragraph(_contact_line(data), st["contact"]))
    
    body = left_flow + right_flow
    doc.build(head + [FrameBreak(), _fit(body, total_w, body_h)])


def _minimal(buf, data, cv_type):
    st = _styles(body="#374151", muted="#6b7280", heading="#111827", accent="#111827", link="#2563eb", name_size=26)
    
    sections = {
        "profile": _section("Profile", _profile_block(data, st), st),
        "education": _section("Education", _education_block(data, st), st),
        "experience": _section("Experience", _experience_block(data, st), st),
        "skills": _section("Skills", _skills_block(data, st), st),
        "projects": _section("Projects", _projects_block(data, st), st),
    }

    order = SECTION_ORDER.get(cv_type, SECTION_ORDER["job"])
    left = sections["profile"]
    right = []
    
    for i, key in enumerate(order):
        if i < 2: left += sections[key]
        else: right += sections[key]

    _two_column(buf, data, st=st, band=None, left=left, right=right, left_ratio=0.5, header_extra=_links_inline(data, st))


def _modern(buf, data, cv_type):
    sb_w = 66 * mm
    side = _styles(body="#e5e7eb", muted="#9ca3af", heading="#ffffff", accent="#38bdf8", link="#7dd3fc")
    main = _styles(body="#374151", muted="#6b7280", heading="#111827", accent="#0ea5e9", link="#0369a1", name_size=28)
    side_x, side_w = 9 * mm, sb_w - 18 * mm
    main_x = sb_w + 10 * mm
    main_w = PAGE_W - main_x - MARGIN
    full_h = PAGE_H - 2 * MARGIN

    def on_page(c, _doc):
        c.saveState()
        c.setFillColor(colors.HexColor("#1f2937"))
        c.rect(0, 0, sb_w, PAGE_H, stroke=0, fill=1)
        c.restoreState()

    doc = _doc(buf, data)
    doc.addPageTemplates([
        PageTemplate(id="first", onPage=on_page, frames=[_frame("side", side_x, MARGIN, side_w, full_h), _frame("main", main_x, MARGIN, main_w, full_h)]),
        PageTemplate(id="later", onPage=on_page, frames=[_frame("main2", main_x, MARGIN, main_w, full_h)]),
    ])

    sidebar = _section("Contact", _contact_block(data, side), side) + _section("Skills", _skills_block(data, side, as_lines=True), side) + _section("Links", _links_block(data, side), side)
    
    content = [Paragraph(_t(data["name"]), main["name"]), Spacer(1, 4)]
    
    sections = {
        "profile": _section("Profile", _profile_block(data, main), main),
        "education": _section("Education", _education_block(data, main), main),
        "experience": _section("Experience", _experience_block(data, main), main),
        "projects": _section("Projects", _projects_block(data, main), main),
    }
    
    for key in SECTION_ORDER.get(cv_type, SECTION_ORDER["job"]):
        if key in sections:
            content += sections[key]

    doc.build([NextPageTemplate("later"), _fit(sidebar, side_w, full_h), FrameBreak()] + content)


_BUILDERS = {"classic": _classic, "modern": _modern, "minimal": _minimal}

def build_cv_pdf(user, cv_type="job", template_slug=None):
    """Returns a BytesIO buffer containing the PDF."""
    if not template_slug:
        template_slug = getattr(user.profile, "pdf_template", "classic")
    data = _collect(user)
    buf = BytesIO()
    _BUILDERS.get(template_slug or "classic", _classic)(buf, data, cv_type)
    buf.seek(0)
    return buf