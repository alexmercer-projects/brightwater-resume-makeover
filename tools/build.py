#!/usr/bin/env python3
"""Builds docs/index.html and docs/resume.html from the content below.

Everything about Noa Brightwater is made up: the person, the employers,
the school and every number. The keyword and bullet counts shown on the
page are worked out here from the actual resume text, so they always agree.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
E = html.escape

NAME = "Noa Brightwater"
PDF = "Noa-Brightwater-resume-DEMO.pdf"
DOCX = "Noa-Brightwater-resume-DEMO.docx"

# ---------------------------------------------------------------- after
AFTER = {
    "title": "Operations Manager · E-commerce Fulfillment",
    "contact": ["Dayton, OH", "(555) 014-2290", "noa.brightwater@example.com", "linkedin.com/in/noa-b-example"],
    "summary": ("Operations manager with 8 years in warehouse and e-commerce fulfillment, most recently running "
                "a 140,000 sq ft site with 62 people across two shifts. Known for fixing the processes behind late "
                "and wrong orders, then training teams to keep them fixed. Hands-on with WMS rollouts, labor "
                "planning, carrier management and safety programs."),
    "jobs": [
        {"role": "Operations Manager", "org": "Tansywood Home Goods", "place": "Dayton, OH", "dates": "Mar 2021 – Present",
         "bullets": [
            "Run daily operations for a 140,000 sq ft fulfillment center shipping up to 4,800 orders a day, with 62 staff on two shifts and 4 supervisors reporting to me.",
            "Cut mis-picks from 1.9% to 0.6% in 9 months by re-slotting the top 300 SKUs and adding scan-to-confirm at every pack station.",
            "Led the move from spreadsheets to a cloud warehouse management system (WMS) across 2 buildings, live in 11 weeks with no missed carrier cutoffs.",
            "Raised on-time shipping from 91% to 98.5% with a labor plan built on hourly order forecasts.",
            "Lowered recordable injuries 40% year over year with a daily 10-minute safety huddle and a near-miss reporting form.",
         ]},
        {"role": "Operations Supervisor", "org": "Gallowmere Freight", "place": "Springfield, OH", "dates": "Jun 2018 – Feb 2021",
         "bullets": [
            "Supervised 25 associates on inbound receiving and cross-dock for 30+ retail accounts.",
            "Reduced dock-to-stock time from 36 to 14 hours by scheduling inbound appointments and pre-labeling pallets.",
            "Wrote 18 standard work instructions and a 5-day onboarding plan that cut new-hire ramp-up by about a week.",
            "Renegotiated LTL rates with 3 carriers, saving about $84,000 a year.",
         ]},
        {"role": "Shift Lead", "org": "Fenmarrow Supply Co.", "place": "Dayton, OH", "dates": "Aug 2016 – May 2018",
         "bullets": [
            "Led a 12-person night shift picking and packing B2B orders, holding inventory accuracy above 99.4% for 6 straight quarters.",
            "Trained 30+ associates on RF scanners, cycle counting and forklift safety.",
         ]},
    ],
    "skills": [
        ("Operations", "WMS, labor planning, slotting, cycle counting, carrier management, KPI reporting, Lean / 5S, process improvement"),
        ("Tools", "NetSuite, ShipStation, Excel (pivot tables, XLOOKUP), Google Sheets, Power BI"),
        ("People", "Hiring and onboarding, shift scheduling, coaching, OSHA safety programs"),
    ],
    "education": [
        ("B.S. Business Administration", "Lakemont State University", "2016"),
        ("Lean Six Sigma Green Belt", "", "2022"),
        ("OSHA 30-Hour General Industry", "", "2020"),
    ],
}

# ---------------------------------------------------------------- before
BEFORE = {
    "tagline": "Hard-working Team Player",
    "objective": ("Seeking a challenging position in a growing company where I can utilize my skills and experience "
                  "to grow professionally and contribute to the success of the organization."),
    "jobs": [
        ("Tansywood Home Goods ~ Ops Manager", "(2021-now)", [
            "Responsible for daily operations of warehouse",
            "In charge of supervisors and staff",
            "Worked on new system implementation",
            "Helped improve shipping times",
            "Handled safety stuff",
        ]),
        ("Gallowmere Freight, Supervisor", "June '18 - Feb 2021", [
            "Duties included supervising receiving team",
            "Worked with trucking companies on rates",
            "Wrote training documents",
        ]),
        ("Fenmarrow Supply Co / Shift lead", "2016 to 2018", [
            "Night shift lead",
            "Trained new people",
        ]),
    ],
    "skills": [("Leadership", 4), ("Microsoft Office", 5), ("Communication", 5), ("Teamwork", 5), ("Problem Solving", 4), ("Time Management", 3)],
    "hobbies": "Hiking, cooking, fantasy football",
}

# ---------------------------------------------------------------- posting
POSTING = {
    "title": "Operations Manager, Fulfillment",
    "org": "Northvane Outfitters (made up)",
    "keywords": [
        ("Fulfillment", ["fulfillment"]),
        ("Warehouse management system", ["warehouse management system", "wms"]),
        ("Labor planning", ["labor plan"]),
        ("Carrier management", ["carrier management", "carrier"]),
        ("On-time shipping", ["on-time shipping"]),
        ("Inventory accuracy", ["inventory accuracy"]),
        ("Cycle counting", ["cycle count"]),
        ("KPI reporting", ["kpi"]),
        ("Lean", ["lean"]),
        ("Process improvement", ["process improvement"]),
        ("Safety / OSHA", ["osha"]),
        ("NetSuite", ["netsuite"]),
        ("Excel", ["excel"]),
        ("Hiring and onboarding", ["onboarding"]),
        ("Supervisors / team leadership", ["supervisor"]),
        ("Shift scheduling", ["shift scheduling"]),
    ],
}

# ---------------------------------------------------------------- LinkedIn
LI = {
    "before_headline": "Operations Manager at Tansywood Home Goods",
    "after_headline": ("Operations Manager | E-commerce fulfillment and warehouse ops | WMS rollouts, labor planning, "
                       "carrier management | Cut mis-picks from 1.9% to 0.6%"),
    "before_about": ("Hardworking operations professional with a passion for excellence. I am a team player who thrives "
                     "in fast-paced environments. Open to new opportunities! Feel free to connect."),
    "after_about": [
        "I run warehouses so orders leave on time and arrive right.",
        "For the last 8 years I've worked in fulfillment and freight, from leading a night shift to managing a 140,000 sq ft e-commerce site with 62 people. The work I like most is finding the one process that causes most of the problems and fixing it for good. At Tansywood that meant re-slotting our fastest-moving SKUs and adding scan-to-confirm at pack, which took mis-picks from 1.9% to 0.6%.",
        "What I'm good at:\n• Rolling out a WMS without missing carrier cutoffs\n• Labor plans built on real order forecasts\n• Carrier rates and relationships\n• Training new hires so they're productive in their first week\n• Safety programs people actually follow",
        "I'm looking for my next operations manager role at a growing e-commerce or 3PL company. If that's you, send me a message.",
    ],
    "top_skills": ["Warehouse Management Systems", "Labor Planning", "Fulfillment Operations", "Carrier Management", "Lean Six Sigma"],
}
HEADLINE_MAX, ABOUT_MAX = 220, 2600

# ---------------------------------------------------------------- rewrites
REWRITES = [
    ("Responsible for daily operations of warehouse", 0, 0, ["Scope in numbers", "Team size"]),
    ("Helped improve shipping times", 0, 3, ["Before and after", "How it was done"]),
    ("Worked on new system implementation", 0, 2, ["Names the system", "Timeline", "Outcome"]),
    ("Handled safety stuff", 0, 4, ["Measurable result", "Specific program"]),
    ("Worked with trucking companies on rates", 1, 3, ["Dollar figure", "Industry term (LTL)"]),
]

CHANGES = [
    ("Photo and two columns", "One column, no photo",
     "Two-column layouts and text boxes can come out of an applicant tracking system in the wrong order, and in the US most recruiters would rather not see a photo. One column reads cleanly everywhere."),
    ("Contact details in a sidebar with icons", "Plain contact line under the name",
     "Icons are images, so a parser may skip them, and sidebars get separated from the name. Plain text right under the name never goes missing."),
    ("A generic objective", "A three-line summary aimed at the role",
     "An objective says what the candidate wants. A summary says what they bring, using the words from the posting they're applying to."),
    ("“My Journey”", "“Experience”",
     "Creative headings are charming and easy for software to misfile. Standard headings (Summary, Experience, Skills, Education) land in the right fields."),
    ("Duties", "Results with numbers",
     "Every bullet now starts with a verb and ends with an outcome. The numbers here are example data. On a real resume they come from the person, and I ask rather than guess."),
    ("Three different date styles", "One date format, aligned right",
     "Mixed formats like “2021-now” and “June '18” look careless and can confuse date parsing. Month and year, the same way every time."),
    ("Skill bars", "Grouped skills that match the posting",
     "A bar that's four-fifths full doesn't tell a recruiter anything, and software can't read it. Named tools and methods can be searched."),
    ("Hobbies and “references available”", "Certifications",
     "References are assumed, and hobbies rarely earn the space. That room goes to certifications the posting actually asks about."),
]

PROCESS = [
    ("Read the target job", "I start from one or two real postings the person wants, not from the old resume."),
    ("Pull the keywords", "Tools, methods and titles that appear in the posting go on a list, so the rewrite uses the same words."),
    ("Ask for the real numbers", "Team sizes, volumes, before-and-after figures. If a number isn't known, the bullet says what changed without one."),
    ("Rebuild the layout", "One column, standard headings, real text (no images of text), and a font that survives any computer."),
    ("Rewrite every bullet", "Verb first, result last, one or two lines each. Duties that don't support the target job get cut."),
    ("Check it", "Paste-to-plain-text test, PDF and Word exports, a spell check, and the same edits carried into LinkedIn."),
]

# ---------------------------------------------------------------- helpers
def after_text():
    parts = [NAME, AFTER["title"], " ".join(AFTER["contact"]), AFTER["summary"]]
    for j in AFTER["jobs"]:
        parts += [j["role"], j["org"], j["place"], j["dates"]] + j["bullets"]
    for k, v in AFTER["skills"]:
        parts += [k, v]
    for a, b, c in AFTER["education"]:
        parts += [a, b, c]
    return "\n".join(parts)

def before_text():
    parts = [NAME, BEFORE["tagline"], BEFORE["objective"]]
    for t, d, bs in BEFORE["jobs"]:
        parts += [t, d] + bs
    parts += [s for s, _ in BEFORE["skills"]] + [BEFORE["hobbies"], "Lakemont State, Business, 2016"]
    return "\n".join(parts)

def matches(text):
    t = text.lower()
    return [any(term in t for term in terms) for _, terms in POSTING["keywords"]]

HAS_NUM = re.compile(r"\d")
def count_bullets(bullets):
    return sum(1 for b in bullets if HAS_NUM.search(b)), len(bullets)

before_bullets = [b for _, _, bs in BEFORE["jobs"] for b in bs]
after_bullets = [b for j in AFTER["jobs"] for b in j["bullets"]]
BN, BT = count_bullets(before_bullets)
AN, AT = count_bullets(after_bullets)
MB, MA = matches(before_text()), matches(after_text())
KW_TOTAL = len(POSTING["keywords"])
KB, KA = sum(MB), sum(MA)
about_after_text = "\n\n".join(LI["after_about"])
HL_B, HL_A = len(LI["before_headline"]), len(LI["after_headline"])
AB_B, AB_A = len(LI["before_about"]), len(about_after_text)
assert HL_A <= HEADLINE_MAX, HL_A
for t in [after_text(), about_after_text] + [c for row in CHANGES for c in row]:
    assert "—" not in t, t

# ---------------------------------------------------------------- resume markup
def after_sheet(cls="sheet sheet--after"):
    jobs = ""
    for j in AFTER["jobs"]:
        bl = "".join(f"<li>{E(b)}</li>" for b in j["bullets"])
        jobs += (f'<div class="r-job"><div class="r-job__head"><p class="r-job__role"><b>{E(j["role"])}</b>, {E(j["org"])} '
                 f'<span class="r-job__place">· {E(j["place"])}</span></p><p class="r-job__dates">{E(j["dates"])}</p></div>'
                 f'<ul>{bl}</ul></div>')
    skills = "".join(f"<p><b>{E(k)}:</b> {E(v)}</p>" for k, v in AFTER["skills"])
    edu = "".join(f'<div class="r-edu"><p><b>{E(a)}</b>{", " + E(b) if b else ""}</p><p class="r-job__dates">{E(c)}</p></div>'
                  for a, b, c in AFTER["education"])
    contact = ' <span aria-hidden="true">·</span> '.join(E(c) for c in AFTER["contact"])
    return f'''<article class="{cls}" aria-label="After: the rebuilt resume">
  <div class="r">
    <header class="r-head"><h3 class="r-name">{E(NAME)}</h3><p class="r-title">{E(AFTER["title"])}</p><p class="r-contact">{contact}</p></header>
    <section><h4 class="r-h">Summary</h4><p>{E(AFTER["summary"])}</p></section>
    <section><h4 class="r-h">Experience</h4>{jobs}</section>
    <section><h4 class="r-h">Skills</h4><div class="r-skills">{skills}</div></section>
    <section><h4 class="r-h">Education and certifications</h4>{edu}</section>
  </div>
</article>'''

def mark(n):
    return f'<span class="pin" aria-label="Change {n}">{n}</span>'

def before_sheet():
    jobs = ""
    for i, (t, d, bs) in enumerate(BEFORE["jobs"]):
        bl = "".join(f"<li>{E(b)}</li>" for b in bs)
        pins = (mark(6) if i == 0 else "")
        pins5 = (mark(5) if i == 0 else "")
        jobs += f'<div class="b-job"><p class="b-job__t">{E(t)} <i>{E(d)}</i>{pins}</p><ul>{pins5}{bl}</ul></div>'
    bars = "".join(f'<li><span>{E(s)}</span><span class="b-bar"><span style="width:{v*20}%"></span></span></li>'
                   for s, v in BEFORE["skills"])
    return f'''<article class="sheet sheet--before" aria-label="Before: the original resume">
  <div class="b">
    <aside class="b-side">
      <div class="b-photo" aria-hidden="true">NB</div>{mark(1)}
      <p class="b-side__h">Contact {mark(2)}</p>
      <ul class="b-contact"><li><span aria-hidden="true">✉</span> noa.brightwater@example.com</li><li><span aria-hidden="true">☎</span> 555.014.2290</li><li><span aria-hidden="true">⌂</span> Dayton Ohio</li></ul>
      <p class="b-side__h">Skills {mark(7)}</p>
      <ul class="b-bars">{bars}</ul>
      <p class="b-side__h">Hobbies {mark(8)}</p>
      <p class="b-small">{E(BEFORE["hobbies"])}</p>
      <p class="b-side__h">References</p>
      <p class="b-small">Available upon request</p>
    </aside>
    <div class="b-main">
      <h3 class="b-name">{E(NAME)}</h3>
      <p class="b-tag">{E(BEFORE["tagline"])}</p>
      <p class="b-h">Objective {mark(3)}</p>
      <p class="b-obj">{E(BEFORE["objective"])}</p>
      <p class="b-h">My Journey {mark(4)}</p>
      {jobs}
      <p class="b-h">Education</p>
      <p class="b-small">Lakemont State, Business, 2016</p>
    </div>
  </div>
</article>'''

# ---------------------------------------------------------------- page sections
def kw_list(flags):
    out = ""
    for (label, _), ok in zip(POSTING["keywords"], flags):
        out += f'<li class="kw {"kw--hit" if ok else "kw--miss"}"><span class="kw__i" aria-hidden="true">{"✓" if ok else "–"}</span>{E(label)}<span class="sr">{" (found)" if ok else " (missing)"}</span></li>'
    return out

def rewrites():
    rows = ""
    for i, (b, jn, bn, tags) in enumerate(REWRITES, 1):
        a = AFTER["jobs"][jn]["bullets"][bn]
        t = "".join(f"<li>{E(x)}</li>" for x in tags)
        rows += f'''<li class="rw reveal">
  <p class="rw__n">{i:02d}</p>
  <div class="rw__b"><p class="eyebrow">Before</p><p class="rw__old">{E(b)}</p></div>
  <div class="rw__arrow" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  <div class="rw__a"><p class="eyebrow">After</p><p class="rw__new">{E(a)}</p><ul class="rw__tags">{t}</ul></div>
</li>'''
    return rows

def changes():
    out = ""
    for i, (b, a, why) in enumerate(CHANGES, 1):
        out += f'''<li class="chg reveal"><span class="pin pin--lg" aria-hidden="true">{i}</span>
  <p class="chg__ba"><s>{E(b)}</s> <span aria-hidden="true">→</span><span class="sr"> became </span> <b>{E(a)}</b></p>
  <p class="chg__why">{E(why)}</p></li>'''
    return out

def about_html(paras):
    out = ""
    for p in paras:
        out += "<p>" + "<br>".join(E(l) for l in p.split("\n")) + "</p>"
    return out

def li_card(kind):
    after = kind == "after"
    headline = LI["after_headline"] if after else LI["before_headline"]
    about = about_html(LI["after_about"]) if after else f"<p>{E(LI['before_about'])}</p>"
    hl, ab = (HL_A, AB_A) if after else (HL_B, AB_B)
    skills = ("<div class='li__skills'><p class='li__lbl'>Top skills</p><p>" + " • ".join(E(s) for s in LI["top_skills"]) + "</p></div>") if after else ""
    banner = "li__banner--after" if after else "li__banner--before"
    return f'''<article class="li li--{kind}" aria-label="{'After' if after else 'Before'}: LinkedIn profile">
  <div class="li__banner {banner}" aria-hidden="true"></div>
  <div class="li__body">
    <div class="li__avatar {'li__avatar--after' if after else ''}" aria-hidden="true">NB</div>
    <p class="li__tagline">{'After' if after else 'Before'}</p>
    <h3 class="li__name">{E(NAME)}</h3>
    <p class="li__headline">{E(headline)}</p>
    <p class="li__meta">Dayton, Ohio · Example profile</p>
    <p class="li__count"><span>Headline</span><b>{hl}</b> / {HEADLINE_MAX} characters</p>
    <div class="li__about"><p class="li__lbl">About</p>{about}{skills}</div>
    <p class="li__count"><span>About</span><b>{ab:,}</b> / {ABOUT_MAX:,} characters</p>
  </div>
</article>'''

DEMO_BAR = ('<div class="am-demo-bar" role="note" style="font:14px/1.45 system-ui,-apple-system,\'Segoe UI\',sans-serif;background:#0f0f0f;color:#f3f3ef;padding:10px 16px;display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:space-between;align-items:center;position:relative;z-index:50">'
            '<span><b>Concept demo by Alex Mercer.</b> Noa Brightwater, every employer and every number on this page are made up. Example data, not client work.</span>'
            '<a href="https://alexmercerprojects.com/" style="color:#f3f3ef;text-decoration:underline;text-underline-offset:3px">Back to Alex Mercer&#39;s portfolio</a></div>')

def plain_text_block():
    p = DOCS / "plain-text.txt"
    return E(p.read_text().strip()) if p.exists() else "(run the PDF step, then rebuild)"

def page():
    def size(name):
        f = DOCS / name
        return f" · {round(f.stat().st_size/1024)} KB" if f.exists() else ""
    pdf_size, docx_size = size(PDF), size(DOCX)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Noa Brightwater: resume and LinkedIn makeover (concept demo) · Alex Mercer</title>
  <meta name="description" content="Concept demo: a cluttered two-column resume rebuilt as a clean, ATS-friendly one-pager, with bullet rewrites, a keyword check against a sample posting, a new LinkedIn headline and About section, and a PDF. The job seeker and employers are fictional.">
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#f2efe7">
  <meta property="og:title" content="Resume and LinkedIn makeover, concept demo">
  <meta property="og:description" content="A messy resume rebuilt as a clean one-page, ATS-friendly resume plus a rewritten LinkedIn profile. Fictional person, example data.">
  <meta property="og:type" content="website">
  <link rel="preload" href="fonts/Geist.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/InstrumentSerif.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/styles.css">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231e4d45'/%3E%3Ctext x='16' y='21.5' font-family='Arial' font-size='14' font-weight='700' fill='%23f2efe7' text-anchor='middle'%3ENB%3C/text%3E%3C/svg%3E">
  <script>if(!/[?&]static\\b/.test(location.search)&&!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('anim');</script>
</head>
<body>
{DEMO_BAR}
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap top__inner">
    <a class="logo" href="#main"><span class="logo__mark" aria-hidden="true">NB</span><span class="logo__word"><span>{E(NAME)}</span><small>Resume makeover</small></span></a>
    <nav class="nav" aria-label="Sections"><a href="#compare">Before / after</a><a href="#changes">What changed</a><a href="#bullets">Bullets</a><a href="#keywords">Keywords</a><a href="#linkedin">LinkedIn</a><a href="#process">Process</a></nav>
    <a class="btn btn--solid btn--sm" href="{PDF}" download><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v10m0 0-4-4m4 4 4-4M4 16h12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>PDF</a>
  </div>
</header>

<main id="main">
<section class="hero wrap">
  <div class="hero__copy">
    <p class="eyebrow">Resume formatting + LinkedIn rewrite</p>
    <h1>Eight years of good work, <em>finally on one clean page.</em></h1>
    <p class="lede">Noa runs a busy fulfillment center, but the old resume buried that under skill bars, a photo and duties like “handled safety stuff.” Here it is rebuilt: one column, standard headings, results in every bullet, plus a LinkedIn profile that matches.</p>
    <div class="hero__cta"><a class="btn btn--solid" href="#compare">See the before and after</a><a class="btn btn--ghost" href="{PDF}" download>Download the new resume (PDF{pdf_size})</a></div>
  </div>
  <aside class="facts" aria-label="At a glance">
    <dl>
      <div><dt>Job seeker</dt><dd>{E(NAME)}</dd></div>
      <div><dt>Target role</dt><dd>Operations Manager</dd></div>
      <div><dt>Bullets with a number</dt><dd><span class="was">{BN}/{BT}</span> → <b>{AN}/{AT}</b></dd></div>
      <div><dt>Posting keywords</dt><dd><span class="was">{KB}/{KW_TOTAL}</span> → <b>{KA}/{KW_TOTAL}</b></dd></div>
      <div><dt>Layout</dt><dd>2 columns → 1 column</dd></div>
    </dl>
    <p class="stamp">● Fictional person · example data</p>
  </aside>
</section>

<section class="band" id="compare" aria-labelledby="compare-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">01 · Before and after</p><h2 id="compare-h">Same person. Same jobs.</h2></div>
      <p class="sec-head__note">The numbered pins on the old version match the eight changes below. On a wide screen both sit at letter-page proportions. On a phone the new one reflows so it stays readable.</p>
    </div>
    <div class="tabs" role="tablist" aria-label="Choose a version">
      <button role="tab" id="tab-before" aria-controls="pane-before" aria-selected="false" tabindex="-1">Before</button>
      <button role="tab" id="tab-after" aria-controls="pane-after" aria-selected="true">After</button>
    </div>
    <div class="compare">
      <figure class="pane" id="pane-before" role="tabpanel" aria-labelledby="tab-before">
        <figcaption><span class="dot dot--red"></span>Before <small>the original file</small></figcaption>
        {before_sheet()}
      </figure>
      <figure class="pane" id="pane-after" role="tabpanel" aria-labelledby="tab-after">
        <figcaption><span class="dot dot--green"></span>After <small>one column, ATS-friendly</small></figcaption>
        {after_sheet()}
      </figure>
    </div>
  </div>
</section>

<section class="wrap sec" id="changes" aria-labelledby="changes-h">
  <div class="sec-head">
    <div><p class="eyebrow">02 · What changed</p><h2 id="changes-h">Eight fixes, and why each one matters.</h2></div>
    <p class="sec-head__note">None of this is decoration. Each change makes the page easier for a recruiter to skim or for hiring software to read.</p>
  </div>
  <ol class="chgs">{changes()}</ol>
</section>

<section class="band band--ink" id="bullets" aria-labelledby="bullets-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow eyebrow--light">03 · Bullet rewrites</p><h2 id="bullets-h">From duties to results.</h2></div>
      <p class="sec-head__note">The pattern: start with a verb, say what changed, show the number. In a real job I ask for the figures. I never make them up.</p>
    </div>
    <ol class="rws">{rewrites()}</ol>
  </div>
</section>

<section class="wrap sec" id="keywords" aria-labelledby="kw-h">
  <div class="sec-head">
    <div><p class="eyebrow">04 · Keyword check</p><h2 id="kw-h">Speaking the posting’s language.</h2></div>
    <p class="sec-head__note">{KW_TOTAL} terms from a sample posting, “{E(POSTING["title"])}” at {E(POSTING["org"])}. Each one was checked against the text of both versions.</p>
  </div>
  <div class="kws">
    <div class="kwcard reveal"><div class="kwcard__top"><p>Before</p><p class="kwcard__score"><b>{KB}</b>/{KW_TOTAL}</p></div><div class="meter"><span style="width:{KB/KW_TOTAL*100:.1f}%"></span></div><ul class="kwlist">{kw_list(MB)}</ul></div>
    <div class="kwcard kwcard--after reveal"><div class="kwcard__top"><p>After</p><p class="kwcard__score"><b>{KA}</b>/{KW_TOTAL}</p></div><div class="meter meter--after"><span style="width:{KA/KW_TOTAL*100:.1f}%"></span></div><ul class="kwlist">{kw_list(MA)}</ul></div>
  </div>
  <p class="fineprint">Keywords only go in where they’re true. A skill the person doesn’t have stays off the page, even if the posting asks for it.</p>
</section>

<section class="band" id="linkedin" aria-labelledby="li-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">05 · LinkedIn</p><h2 id="li-h">A headline and About section that do some work.</h2></div>
      <p class="sec-head__note">LinkedIn fills the headline from the current job title unless you change it. The rewrite leads with the role, then the skills recruiters search for. LinkedIn allows up to {HEADLINE_MAX} characters in the headline and {ABOUT_MAX:,} in About.</p>
    </div>
    <div class="lis">{li_card("before")}{li_card("after")}</div>
  </div>
</section>

<section class="wrap sec" id="plain" aria-labelledby="plain-h">
  <div class="sec-head">
    <div><p class="eyebrow">06 · Plain-text check</p><h2 id="plain-h">What software sees.</h2></div>
    <div class="sec-head__note"><p>This is the text pulled straight out of the new PDF with pdftotext, a standard command-line tool, unedited. It comes out top to bottom, in order, with every heading and date intact. A one-column layout passes this test. Two columns often don’t.</p>
    <p class="plain__cta"><a class="btn btn--solid" href="{PDF}" download>Download the PDF{pdf_size}</a><a class="btn btn--ghost" href="{DOCX}" download>Word file{docx_size}</a></p></div>
  </div>
  <pre class="plain__txt" tabindex="0" aria-label="Plain text extracted from the PDF">{plain_text_block()}</pre>
</section>

<section class="band band--soft" id="process" aria-labelledby="process-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">07 · How I’d do it</p><h2 id="process-h">The process, start to finish.</h2></div>
      <p class="sec-head__note">A finished job comes back as a PDF and an editable Word file, plus the LinkedIn headline and About text ready to paste. Both files for this demo are above: <a href="{PDF}" download>PDF</a> and <a href="{DOCX}" download>Word</a>.</p>
    </div>
    <ol class="steps">{"".join(f'<li class="step reveal"><p class="step__n">{i:02d}</p><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i,(t,d) in enumerate(PROCESS,1))}</ol>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot__inner">
    <p><b>A concept demo by Alex Mercer.</b> Noa Brightwater, Tansywood Home Goods, Gallowmere Freight, Fenmarrow Supply Co., Lakemont State University and Northvane Outfitters are all made up, and every number is example data. Not client work.</p>
    <p><a href="mailto:alexmercer.projects@gmail.com?subject=A%20resume%20for%20Alex">alexmercer.projects@gmail.com</a> · <a href="https://alexmercerprojects.com/">alexmercerprojects.com</a></p>
  </div>
</footer>
<script src="js/app.js"></script>
</body>
</html>
'''

def resume_print():
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>{E(NAME)} resume (concept demo)</title>
<link rel="stylesheet" href="css/styles.css">
<style>@page {{ size: Letter; margin: 0.5in 0.6in 0.45in; }} html,body{{background:#fff}} body{{margin:0}}</style>
</head><body class="print">
{after_sheet("sheet sheet--print")}
<p class="print-note">Concept demo by Alex Mercer. {E(NAME)}, the employers and the school are fictional; all figures are example data.</p>
</body></html>
'''

if __name__ == "__main__":
    (DOCS / "index.html").write_text(page())
    (DOCS / "resume.html").write_text(resume_print())
    print(f"bullets with numbers {BN}/{BT} -> {AN}/{AT}; keywords {KB}/{KW_TOTAL} -> {KA}/{KW_TOTAL}; "
          f"headline {HL_B}->{HL_A}; about {AB_B}->{AB_A}")
    for (k, _), b, a in zip(POSTING["keywords"], MB, MA):
        if not a: print("  after misses:", k)
        if b: print("  before has:", k)
