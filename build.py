#!/usr/bin/env python3
"""Builds the Rafla Design static site from shared parts. Run: python3 build.py"""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
PHONE = "0409 701 575"
TEL = "+61409701575"
EMAIL = "info@rafladesign.com"
SITE = "https://rafladesign.com"
GBP = "https://maps.app.goo.gl/MREMDJzHJVCQqVCm7"

# Rafla Design "RD" mark, redrawn from the brand file (R bowl + leg, arched D)
# Rafla Design window mark (concept 2b): a 10u square, 1u struts, four panes forming a mirrored R and a D
FRAME = "M10 0H110A10 10 0 0 1 120 10V110A10 10 0 0 1 110 120H10A10 10 0 0 1 0 110V10A10 10 0 0 1 10 0Z"
PANES = ['M54 12H33A21 21 0 0 0 33 54H54Z', 'M66 12A42 42 0 0 1 108 54H66Z', 'M54 66H36L12 108H54Z', 'M66 66H108A42 42 0 0 1 66 108Z']
MARK = f'<path fill-rule="evenodd" d="{FRAME} {" ".join(PANES)}"/>'
MARK_SHAPES = PANES

ICONS = {
  "houses": '<path d="M2 44H62"/><path d="M10 44V24h44v20"/><path d="M6 26 32 10l26 16"/><path d="M27 44V33h10v11"/><path d="M15 30h7v6h-7zM42 30h7v6h-7z"/>',
  "double-storey": '<path d="M2 44H62"/><path d="M14 44V12h36v32"/><path d="M10 12h44"/><path d="M14 28h36"/><path d="M20 17h8v6h-8zM36 17h8v6h-8zM28 44V34h8v10"/>',
  "granny-flat": '<path d="M2 44H62"/><path d="M6 44V22h22v22" stroke-dasharray="3 3"/><path d="M34 44V30h24v14"/><path d="M31 31l15-9 15 9"/><path d="M42 44v-7h7v7"/>',
  "duplex": '<path d="M2 44H62"/><path d="M6 44V18h52v26"/><path d="M32 18v26"/><path d="M3 18h58"/><path d="M14 44v-9h7v9M43 44v-9h7v9"/><path d="M12 24h10v5H12zM42 24h10v5H42z"/>',
  "townhouses": '<path d="M2 44H62"/><path d="M4 44V20h18v24M22 44V14h20v30M42 44V20h18v24"/><path d="M10 44v-8h6v8M29 44v-8h6v8M48 44v-8h6v8"/>',
  "multi-dwelling": '<path d="M2 44H62"/><path d="M10 44V6h44v38"/><path d="M10 18h44M10 30h44M24 6v38M40 6v38"/>',
  "renovations": '<path d="M2 44H62"/><path d="M10 44V24h44v20"/><path d="M6 26 32 10l26 16"/><path d="M18 30h10v8H18z" stroke-dasharray="2.5 2.5"/><path d="M36 30h10v14H36z"/>',
  "extensions": '<path d="M2 44H62"/><path d="M6 44V24h30v20"/><path d="M3 26 21 12l18 14"/><path d="M36 44V30h24v14" stroke-dasharray="3 3"/><path d="M36 30h24"/><path d="M44 37h8"/>',
}

TYPES = [
  ("houses", "Single storey homes", "Family homes planned around how you live, sized to your block and budget."),
  ("double-storey", "Double storey homes", "Two-level homes that make the most of a narrow or sloping site."),
  ("granny-flat", "Granny flats", "Secondary dwellings for family or rental income, designed to approval rules."),
  ("duplex", "Duplexes", "Dual occupancy designs that work for owners, builders and resale."),
  ("townhouses", "Townhouses and villas", "Multi-unit layouts with privacy, light and parking resolved early."),
  ("multi-dwelling", "Multi-dwelling projects", "Larger developments handled with the same personal attention."),
  ("renovations", "Renovations", "Reshape and update your existing home without starting again."),
  ("extensions", "Extensions", "Add space at the back, the side or up, matched to the original house."),
]

NAV = [("./", "Home"), ("services.html", "Services"), ("process.html", "Process"),
       ("portfolio.html", "Portfolio"), ("about.html", "About"), ("contact.html", "Contact")]

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">'

def icon(key, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 64 48" aria-hidden="true">{ICONS[key]}</svg>'

GA_ID = "G-8XYZ90SLBC"
GA = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""


def head(title, desc, path):
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path == './' else path.replace('.html', '')}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0f2e29">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="site.css">
{GA}
</head>
<body>
'''

def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr" data-hdr>
  <div class="wrap hdr-in">
    <a class="brand" href="./" aria-label="Rafla Design home">
      <svg class="brand-mark" viewBox="0 0 120 120" aria-hidden="true">{MARK}</svg>
      <span class="brand-name">Rafla Design</span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">{links}</nav>
    <a class="hdr-call" href="tel:{TEL}">{PHONE}</a>
    <a class="btn btn-mint hdr-cta" href="contact.html#enquire">Free consultation</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>
<main id="main">
'''

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>'

def footer():
    return f'''</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-in">
      <div>
        <a class="brand" href="./" aria-label="Rafla Design home">
          <svg class="brand-mark" viewBox="0 0 120 120" aria-hidden="true">{MARK}</svg>
          <span class="brand-name">Rafla Design</span>
        </a>
        <p>Design, detailing and drafting for Sydney homes since 2000. A family business: Joseph and Michael Rafla.</p>
      </div>
      <div>
        <h4>Pages</h4>
        <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul>
      </div>
      <div>
        <h4>Talk to us</h4>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Mortdale, NSW</li>
          <li><a href="{GBP}" target="_blank" rel="noopener">Find us on Google</a></li>
        </ul>
      </div>
    </div>
    <div class="ftr-base">
      <span>&copy; 2026 Rafla Design. ABN 80 193 957 627</span>
      <span>Design, Detailing &amp; Drafting Services</span>
    </div>
  </div>
</footer>
<div class="mbar" aria-label="Quick contact">
  <a class="btn btn-ghost" style="border-color:rgba(255,255,255,.5);color:#fff" href="tel:{TEL}">{PHONE_SVG}Call</a>
  <a class="btn btn-mint" href="contact.html#enquire">Free consultation</a>
</div>
<script src="site.js"></script>
</body>
</html>
'''

def closer(title="Let’s get your project started", text="Your first consultation is free and comes with no obligation. Tell us what you have in mind and we’ll work out the best direction together."):
    return f'''<section class="closer on-dark arch-pattern">
  <div class="wrap closer-in">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="closer-actions">
      <a class="btn btn-mint" href="contact.html#enquire">Book a free consultation</a>
      <a class="btn btn-ghost" href="tel:{TEL}">{PHONE_SVG}{PHONE}</a>
    </div>
  </div>
</section>
'''

def chips():
    out = []
    for key, title, _ in TYPES:
        out.append(f'<label class="chip"><input type="radio" name="project_type" value="{title}" id="type-{key}"><span>{title}</span></label>')
    out.append('<label class="chip"><input type="radio" name="project_type" value="Not sure yet" id="type-unsure"><span>Not sure yet</span></label>')
    return "".join(out)

# The form posts to the site's own Worker (src/worker.js), which emails the enquiry.
def enquiry_form():
    ep = "/api/enquiry"
    hidden = '<input type="text" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">'
    return f'''<form class="form" id="enquire" data-enquiry data-endpoint="{ep}" novalidate>{hidden}
  <h3>Request a free consultation</h3>
  <p>Tell us a little about the project. We’ll call to arrange a time that suits you.</p>
  <div class="fields">
    <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
    <div class="field"><label for="f-suburb">Property suburb</label><input id="f-suburb" name="suburb" autocomplete="address-level2"></div>
    <fieldset class="field full"><legend>What are you planning?</legend><div class="chips">{chips()}</div></fieldset>
    <div class="field full"><label for="f-msg">Anything else we should know?</label><textarea id="f-msg" name="message" placeholder="Block size, number of bedrooms, timing, budget, whether you have a survey…"></textarea></div>
  </div>
  <div class="form-foot">
    <button class="btn btn-mint" type="submit">Request my free consultation</button>
    <small>Free and no obligation. Phone or email is enough.</small>
  </div>
  <div class="form-status" role="status" aria-live="polite" hidden></div>
</form>'''

def hero_sign():
    clip = "".join(f'<path d="{d}"/>' for d in PANES)
    outline = "".join(f'<path class="outline" pathLength="100" d="{d}"/>' for d in PANES)
    return f'''<svg class="arch-sign" viewBox="-2 -2 124 124" role="img" aria-label="The Rafla Design window mark, with a two-storey home designed by Rafla Design seen through its four panes">
  <defs><clipPath id="rd-clip">{clip}</clipPath></defs>
  <g class="photo" clip-path="url(#rd-clip)">
    <image href="images/house-render.webp" x="-24" y="0" width="168" height="120" preserveAspectRatio="xMidYMid slice"/>
  </g>
  <path class="panel" fill-rule="evenodd" d="{FRAME} {" ".join(PANES)}"/>
  <path class="outline" pathLength="100" d="{FRAME}"/>
  {outline}
</svg>'''

def corner():
    return f'<svg class="corner" viewBox="0 0 120 120" aria-hidden="true">{MARK}</svg>'

def page_head(h1, lead):
    return f'''<section class="page-head">
  <div class="wrap">
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
  {corner()}
</section>
'''

STEPS = [
  ("Free initial consultation", "We meet, free and without obligation. Tell us what you want, or work it out with us. If you’re happy to go ahead, a 50% deposit gets us started.", "Free, no obligation"),
  ("Survey plan", "Already have a survey? Great. If not, use your own surveyor or we’ll arrange one. Their fee goes straight to them; we add nothing on top.", "No markup on surveys"),
  ("Design consultation", "We draft design options from your brief, present them, and adjust until you’re 100% happy. Once you approve the final plan, the remaining 50% is paid.", "Revisions until you’re happy"),
  ("Council submission and approval", "We lodge the plans and deal with Council directly. If they ask for minor changes, we make them at no extra cost, all the way to approval.", "Minor Council changes included"),
  ("Start building", "You have your approval pack and you’re ready to build. We’re happy to oversee the build against the plans and stay on hand for questions.", "Build support available"),
]

SCHEMA = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"Rafla Design","description":"Home design, detailing and drafting services","url":"https://rafladesign.com","telephone":"+61409701575","email":"info@rafladesign.com","foundingDate":"2000","image":"https://rafladesign.com/images/og.jpg","address":{"@type":"PostalAddress","addressLocality":"Mortdale","addressRegion":"NSW","addressCountry":"AU"},"areaServed":"Sydney","hasMap":"https://maps.app.goo.gl/MREMDJzHJVCQqVCm7","sameAs":["https://maps.app.goo.gl/MREMDJzHJVCQqVCm7"]}</script>'

# ---------------- Pages ----------------

def page_home():
    dims = [("Family", "", "father-and-son practice, dealing with you directly"), ("2000", "", "year Joseph Rafla started the practice"),
            ("Fixed", None, "fee agreed up front"), ("Council", None, "lodgement handled for you")]
    dim_html = ""
    for v, suf, lab in dims:
        if suf is not None:
            val = f'<div class="dim-value">{v}</div>'
        else:
            val = f'<div class="dim-value">{v}</div>'
        dim_html += f'<div class="dim"><div class="dim-line" aria-hidden="true"></div>{val}<div class="dim-label">{lab}</div></div>'

    sched = "".join(
        f'<li><a href="contact.html#{k}">{icon(k)}<h3>{t}</h3><p>{d}</p><span class="go">Enquire</span></a></li>'
        for k, t, d in TYPES)

    steps = "".join(f'<li><h3>{t}</h3><p>{d.split(". ")[0]}.</p></li>' for t, d, _ in STEPS)

    return head("Rafla Design | Home design and drafting in Sydney",
                "Family-run home design and drafting since 2000. Houses, duplexes, granny flats and renovations designed, with fixed fees and Council handled for you. Book a free consultation.", "./").replace("</head>", SCHEMA + "</head>") + header("./") + f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Home designs that get approved, then get built.</h1>
      <p class="lead">Rafla Design is a father-and-son design and drafting practice. Since 2000 we’ve designed homes, duplexes, granny flats and renovations for Sydney families, and we deal with Council for you all the way to approval.</p>
      <div class="hero-actions">
        <a class="btn btn-mint" href="#enquire">Book a free consultation</a>
        <a class="btn btn-ghost" href="tel:{TEL}">{PHONE_SVG}Call {PHONE}</a>
      </div>
      <ul class="assurances">
        <li>Fixed fees</li>
        <li>No charge for minor changes</li>
        <li>No job too small</li>
      </ul>
    </div>
    <div class="hero-art">
      {hero_sign()}
    </div>
  </div>
</section>

<section class="dims" aria-label="Rafla Design at a glance">
  <div class="wrap dims-row">{dim_html}</div>
</section>

<section class="band band-white">
  <div class="wrap">
    <div class="band-head">
      <h2>What we design</h2>
      <p>New builds or changes to the home you have. Pick a project type to start an enquiry for it.</p>
    </div>
    <ul class="schedule">{sched}</ul>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <h2>Why families and builders come back to us</h2>
      <p>There are plenty of design firms. Here’s what working with a small family practice means for your project.</p>
    </div>
    <div class="reasons">
      <div class="reason"><div class="arch" aria-hidden="true"></div><div><h3>We’re a family business, so we care</h3><p>We know what makes a family home, a smart investment and a great design, and we’ll be straight with you about what will and won’t work. No false promises.</p></div></div>
      <div class="reason"><div class="arch" aria-hidden="true"></div><div><h3>You get our undivided attention</h3><p>The same people stay with you from the first meeting to approval. Your job never lands in the hands of an unfamiliar face.</p></div></div>
      <div class="reason"><div class="arch" aria-hidden="true"></div><div><h3>We deal with Council for you</h3><p>Going back and forth with Council is rarely easy. We take that on until your job is fully approved and ready to build.</p></div></div>
      <div class="reason"><div class="arch" aria-hidden="true"></div><div><h3>No surprise costs</h3><p>Fixed pricing, and no extra charge for minor changes to your plan. We work to keep you within budget.</p></div></div>
    </div>
  </div>
</section>

<section class="band band-white">
  <div class="wrap">
    <div class="band-head">
      <h2>From first chat to approval in five steps</h2>
      <p>A clear path, with payments split 50/50 and Council handled by us. <a href="process.html">See the full process</a>.</p>
    </div>
    <div class="steps-wrap"><span class="track" aria-hidden="true"></span><ol class="steps">{steps}</ol></div>
  </div>
</section>

<section class="band on-dark arch-pattern" aria-labelledby="enq-h">
  <div class="wrap enquire-grid">
    <div class="enquire-side">
      <h2 id="enq-h">Start with a free consultation</h2>
      <p>Tell us about your block and what you’d like to build. If you’re not sure of a plan yet, that’s what the first meeting is for.</p>
      <ul class="contact-lines">
        <li><span class="k">Call</span><a class="v" href="tel:{TEL}">{PHONE}</a></li>
        <li><span class="k">Email</span><a class="v" href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span class="k">Based in</span><span class="v">Mortdale, NSW</span></li>
        <li><span class="k">Google</span><a class="v" href="{GBP}" target="_blank" rel="noopener">See us and our reviews</a></li>
      </ul>
    </div>
    {enquiry_form()}
  </div>
</section>
''' + footer()


def page_services():
    arts = "".join(
        f'<article>{icon(k)}<div><h3>{t}</h3><p>{d}</p><a href="contact.html#{k}">Enquire about {t.lower()}</a></div></article>'
        for k, t, d in TYPES)
    return head("Services | Rafla Design",
                "Design and drafting for single and double storey homes, granny flats, duplexes, townhouses, multi-dwelling projects, renovations and extensions. Fixed fees, Council handled.", "services.html") + header("services.html") + page_head(
        "Design and drafting for every kind of home project",
        "New builds and renovations, with budget and buildable design kept at the front. No job is too small.") + f'''
<section class="band band-white">
  <div class="wrap">
    <div class="svc">{arts}</div>
  </div>
</section>
<section class="band on-dark arch-pattern">
  <div class="wrap">
    <div class="band-head"><h2>Included with every project</h2><p>Whatever you’re building, these come as standard.</p></div>
    <ul class="included">
      <li>A fixed fee agreed before we start</li>
      <li>A free initial consultation</li>
      <li>Custom designs drawn for your site</li>
      <li>Council lodgement and liaison through to approval</li>
      <li>No extra charge for minor alterations</li>
      <li>The same people from start to finish</li>
      <li>Surveyor arranged at cost if you need one</li>
      <li>Build oversight available after approval</li>
    </ul>
  </div>
</section>
''' + closer("Not sure where to start?", "If you don’t have a firm plan yet, that’s fine. We’ll work it out together in your free consultation.") + footer()


def page_process():
    items = "".join(f'<li><div><h3>{t}</h3><p>{d}</p><span class="note">{n}</span></div></li>' for t, d, n in STEPS)
    return head("Our Process | Rafla Design",
                "How Rafla Design works: free consultation, survey, design, Council submission and approval, then build. Payments split 50/50 with no surprise costs.", "process.html") + header("process.html") + page_head(
        "Five clear steps from first conversation to ready to build",
        "You always know what happens next and what it costs. Payment is split in two: 50% to start, 50% when you approve the final plan.") + f'''
<section class="band band-white">
  <div class="wrap">
    <div class="timeline-wrap"><span class="track" aria-hidden="true"></span><ol class="timeline">{items}</ol></div>
  </div>
</section>
''' + closer("Ready for step one?", "Your first consultation costs nothing and comes with no obligation.") + footer()


ELEV = {
  "duplex": '<path class="ground" d="M10 120H190"/><path d="M28 120V50h144v70"/><path d="M100 50v70"/><path d="M20 50h160"/><path d="M48 120V96h20v24M132 120V96h20v24"/><path d="M42 62h30v18H42zM128 62h30v18h-30z"/>',
  "granny-flat": '<path class="ground" d="M10 120H190"/><path d="M20 120V62h70v58" stroke-dasharray="5 5"/><path d="M106 120V78h76v42"/><path d="M98 80l46-28 46 28"/><path d="M134 120V98h18v22"/><path d="M116 88h12v10h-12z"/>',
  "townhouses": '<path class="ground" d="M10 120H190"/><path d="M16 120V58h56v62M72 120V44h56v76M128 120V58h56v62"/><path d="M36 120V98h16v22M92 120V98h16v22M148 120V98h16v22"/><path d="M28 68h32v14H28zM84 56h32v14H84zM140 68h32v14h-32z"/>',
  "renovations": '<path class="ground" d="M10 120H190"/><path d="M30 120V64h140v56"/><path d="M20 66l80-44 80 44"/><path d="M90 120V94h20v26"/><path d="M48 76h26v18H48z" stroke-dasharray="4 4"/><path d="M126 76h26v18h-26z"/>',
}

PROJECTS = [
  # slug, suburb, title, filters, blurb, alt-subject, image count
  ("miranda-duplex", "Miranda", "Duplex", "duplex", "A two-storey duplex with glazed balconies, timber-clad feature walls and a single garage to each home.", "two-storey duplex with glass balconies and garages"),
  ("greystanes-duplex", "Greystanes", "Duplex", "duplex", "A contemporary duplex in dark and pale render, with upper-level balconies and a garage to each dwelling.", "contemporary two-storey duplex in dark and pale render"),
  ("peakhurst-two-storey-home", "Peakhurst", "Two-storey home", "houses double-storey", "A two-storey home with glass balustrades, a double garage and a landscaped front garden.", "two-storey home with glass balconies and double garage"),
  ("padstow-duplex-balconies", "Padstow", "Duplex", "duplex", "A two-storey duplex with deep, rounded balconies, tall feature glazing between the homes and a garage to each.", "two-storey duplex with rounded balconies and tall feature windows"),
  ("panania-duplex", "Panania", "Duplex", "duplex", "A pair of two-storey homes with a shared driveway, glazed balconies and generous garages.", "two-storey duplex with glazed balconies and shared driveway"),
  ("padstow-duplex-pool", "Padstow", "Duplex with pool", "duplex", "A duplex with a garage to each home, a rear pool and a covered terrace.", "duplex with double garage and rear swimming pool"),
  ("miranda-corner-duplex", "Miranda", "Corner duplex", "duplex", "A corner-site duplex with a timber-battened fence, glass balconies and street frontage on two sides.", "corner duplex with glass balconies and battened fence"),
  ("sylvania-sloping-site-duplex", "Sylvania", "Duplex on a sloping site", "duplex", "A duplex stepped into a steep block, with basement garages, curved stone retaining walls and glass-balustraded entry stairs.", "duplex on a sloping site with basement garages and stone retaining walls"),
  ("sylvania-duplex", "Sylvania", "Duplex", "duplex", "A duplex with green accents, glass balconies and a sloping driveway to each garage.", "two-storey duplex with green accents and glass balconies"),
  ("padstow-duplex-granny-flat", "Padstow", "Duplex and granny flat", "duplex granny-flat", "A duplex with a garage to each home and a granny flat at the rear.", "duplex with garages and a rear granny flat"),
  ("padstow-duplex", "Padstow", "Duplex", "duplex", "A dark-toned duplex with large glazed openings, balconies over the entry and parking in front.", "dark-toned two-storey duplex with large windows and balconies"),
  ("austral-house", "Austral", "Two-storey house", "houses double-storey", "A narrow-lot two-storey house with a stone feature wall, timber garage door and balcony over the entry.", "two-storey house with stone feature wall and balcony"),
  ("sans-souci-house", "Sans Souci", "Two-storey house", "houses double-storey", "A two-storey house with a tall framed entry, upper balcony, double garage and open-plan living.", "two-storey house with framed entry and double garage"),
  ("bradbury-house-secondary-dwelling", "Bradbury", "House and secondary dwelling", "houses granny-flat", "A two-storey house with a bright open-plan interior and a secondary dwelling with its own entry.", "two-storey house with open-plan interior and secondary dwelling"),
  ("fairfield-heights-car-wash", "Fairfield Heights", "Commercial: hand car wash", "commercial", "A corner-site hand car wash with a curved steel canopy, landscaped planter edge and pedestrian-friendly frontage.", "corner hand car wash with curved canopy and landscaped planter"),
  ("peakhurst-house-model", "Peakhurst", "House, 3D model", "houses", "A 3D model of a brick house stepping down a sloping site, with garage below and balcony above.", "3D model of a brick house on a sloping site"),
  ("sutherland-house-model", "Sutherland", "House, 3D model", "houses double-storey", "A 3D massing model of a two-storey house with skillion roof forms and clerestory windows.", "3D model of a two-storey house with skillion roofs"),
]
IMGDIR = os.path.join(OUT, "images")

def _imgs(slug):
    return sorted(f for f in os.listdir(IMGDIR) if re.fullmatch(re.escape(slug) + r"-\d\d\.webp", f))

def _abs(html):
    """Project pages live one level down, so make asset and nav links root-relative."""
    html = re.sub(r'(href|src)="(?!https?:|/|#|tel:|mailto:|data:)([^"]*)"', lambda m: f'{m.group(1)}="/{m.group(2)}"', html)
    return html.replace('href="/./"', 'href="/"').replace('href="/"', 'href="/"')

def page_portfolio():
    cards = ""
    for i, (slug, suburb, title, types, blurb, alt) in enumerate(PROJECTS):
        n = len(_imgs(slug))
        cls = "work feature" if i == 0 else "work"
        cards += f'''
<article class="{cls}" data-type="{types}">
  <a class="work-link" href="portfolio/{slug}" aria-label="{title} in {suburb}: view {n} images">
    <figure><img src="images/{slug}-thumb.webp" alt="Render of a {alt}, {suburb}" loading="{'eager' if i < 2 else 'lazy'}" width="900" height="600"></figure>
    <div class="work-meta"><h3>{title}</h3><span class="tag">{suburb}</span><span class="count">{n} images</span><p>{blurb}</p></div>
  </a>
</article>'''
    filters = '''<div class="filters" role="group" aria-label="Filter projects">
  <button type="button" data-filter="all" aria-pressed="true">All</button>
  <button type="button" data-filter="houses" aria-pressed="false">Houses</button>
  <button type="button" data-filter="duplex" aria-pressed="false">Duplexes</button>
  <button type="button" data-filter="granny-flat" aria-pressed="false">Granny flats</button>
  <button type="button" data-filter="commercial" aria-pressed="false">Commercial</button>
</div>'''
    items = ",".join(f'{{"@type":"ListItem","position":{i+1},"url":"{SITE}/portfolio/{p[0]}"}}' for i, p in enumerate(PROJECTS))
    ld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{items}]}}</script>'
    return head("Portfolio | Rafla Design",
                "Duplexes, houses and granny flats designed by Rafla Design across Sydney's south and south-west. See the 3D renders.", "portfolio.html").replace("</head>", ld + "\n</head>") + header("portfolio.html") + page_head(
        "Projects since 2000. Here’s a selection.",
        "Every project is drawn for its site, its owners and its Council. Open one to see the full set of renders.") + f'''
<section class="band band-white">
  <div class="wrap">
    {filters}
    <div class="works">{cards}</div>
  </div>
</section>
''' + closer("Have a project in mind?", "Tell us about it and we’ll talk through the options, free of charge.") + footer()


def page_project(slug):
    p = next(x for x in PROJECTS if x[0] == slug)
    _, suburb, title, types, blurb, alt = p
    files = _imgs(slug)
    figs = "".join(
        f'<li><button type="button" class="shot" data-full="/images/{f}" data-alt="Render {k+1} of {len(files)}: {alt}, {suburb}"><img src="/images/{f}" alt="Render {k+1} of {len(files)}: {alt}, {suburb}" loading="{'eager' if k < 2 else 'lazy'}" width="1400" height="788"></button></li>'
        for k, f in enumerate(files))
    others = "".join(
        f'<a class="more-card" href="/portfolio/{o[0]}"><img src="/images/{o[0]}-thumb.webp" alt="" loading="lazy" width="900" height="600"><span><strong>{o[2]}</strong> {o[1]}</span></a>'
        for o in PROJECTS if o[0] != slug)[:6000]
    others = "".join(
        f'<a class="more-card" href="/portfolio/{o[0]}"><img src="/images/{o[0]}-thumb.webp" alt="" loading="lazy" width="900" height="600"><span><strong>{o[2]}</strong> {o[1]}</span></a>'
        for o in [x for x in PROJECTS if x[0] != slug][:3])
    url = f"{SITE}/portfolio/{slug}"
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@graph":['
          f'{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"Portfolio","item":"{SITE}/portfolio"}},{{"@type":"ListItem","position":3,"name":"{title} in {suburb}","item":"{url}"}}]}},'
          f'{{"@type":"ImageGallery","name":"{title} in {suburb}","url":"{url}","image":[' + ",".join(f'{{"@type":"ImageObject","contentUrl":"{SITE}/images/{f}","description":"{alt}, {suburb}"}}' for f in files) + ']}]}</script>')
    h = head(f"{title} in {suburb} | Rafla Design", f"{blurb} Designed by Rafla Design. {len(files)} 3D renders.", f"portfolio/{slug}").replace("</head>", ld + "\n</head>")
    body = header("portfolio.html") + page_head(f"{title}, {suburb}", blurb) + f'''
<section class="band band-white">
  <div class="wrap">
    <p class="crumbs"><a href="portfolio.html">&larr; All projects</a></p>
    <ul class="gallery">{figs}</ul>
    <dl class="facts"><div><dt>Suburb</dt><dd>{suburb}</dd></div><div><dt>Project</dt><dd>{title}</dd></div><div><dt>Images</dt><dd>{len(files)} 3D renders</dd></div></dl>
  </div>
</section>
<section class="band">
  <div class="wrap"><h2>More projects</h2><div class="more">{others}</div></div>
</section>
<dialog class="lightbox" aria-label="Image viewer"><button type="button" class="lb-close" aria-label="Close">Close</button><button type="button" class="lb-prev" aria-label="Previous image">&#8249;</button><img alt=""><button type="button" class="lb-next" aria-label="Next image">&#8250;</button></dialog>
''' + closer("Have a project like this in mind?", "Tell us about it and we’ll talk through the options, free of charge.") + footer()
    return _abs(h + body)


def page_about():
    return head("About | Rafla Design",
                "Rafla Design is a father-and-son design and drafting practice started by civil engineer Joseph Rafla in 2000.", "about.html") + header("about.html") + page_head(
        "A father and son with a love for design",
        "Family owned since 2000, and still small enough that you deal with us directly.") + f'''
<section class="band band-white">
  <div class="wrap about-grid">
    <div class="measure">
      <p>Thank you for visiting Rafla Design. We’d love to get to know you, and we know you’ll decide based on what you know about us. So here it is.</p>
      <p>Rafla Design began in 2000 when Joseph Rafla, a civil engineer, designed the homes of his three brothers. His son, Michael, joined what became a successful family practice.</p>
      <p>Since then we’ve taken on single and double storey houses, duplexes, townhouses, granny flats and more. No job is too small. Whether it’s a new build or a renovation, we keep budget and realistic, buildable design at the front.</p>
      <p>Our tight-knit team means you get our undivided attention and personal service, for a journey that’s as smooth as possible.</p>
      <p style="margin-top:2rem"><a class="btn btn-mint" href="contact.html#enquire">Book a free consultation</a></p>
    </div>
    <aside class="family" aria-label="The people you’ll work with">
      <div><span class="arch" aria-hidden="true"></span><div><h3>Joseph Rafla</h3><p>Founder and civil engineer. Started the practice in 2000.</p></div></div>
      <div><span class="arch" aria-hidden="true"></span><div><h3>Michael Rafla</h3><p>Joined his father to grow the family practice.</p></div></div>
    </aside>
  </div>
</section>
''' + closer() + footer()


def page_contact():
    return head("Contact | Rafla Design",
                "Book a free, no-obligation consultation with Rafla Design for your new home, duplex, granny flat, renovation or extension. Call 0409 701 575.", "contact.html") + header("contact.html") + page_head(
        "Book your free consultation",
        "Tell us about your project and we’ll call to arrange a time. Prefer to talk now? Call us.") + f'''
<section class="band on-dark arch-pattern" aria-labelledby="enq-h">
  <div class="wrap enquire-grid">
    <div class="enquire-side">
      <h2 id="enq-h">Talk to us directly</h2>
      <p>A few lines is plenty: the property suburb, whether it’s a new build, renovation or extension, and roughly what you have in mind.</p>
      <ul class="contact-lines">
        <li><span class="k">Call</span><a class="v" href="tel:{TEL}">{PHONE}</a></li>
        <li><span class="k">Email</span><a class="v" href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span class="k">Based in</span><span class="v">Mortdale, NSW</span></li>
      </ul>
    </div>
    {enquiry_form()}
  </div>
</section>
''' + footer()


def page_404():
    return head("Page not found | Rafla Design", "That page doesn’t exist.", "404.html") + header("") + '''
<section class="band band-white"><div class="wrap"><div class="band-head"><h1>That page isn’t here.</h1><p>It may have moved when we rebuilt the site. Try the links above, or call us on ''' + PHONE + '''.</p></div><p><a class="btn btn-mint" href="./">Back to home</a></p></div></section>
''' + footer()


PAGES = {
  "index.html": page_home, "services.html": page_services, "process.html": page_process,
  "portfolio.html": page_portfolio, "about.html": page_about, "contact.html": page_contact,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(fn())
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><path fill="#3abca3" d="{FRAME}"/><path fill="#0f2e29" d="{" ".join(PANES)}"/></svg>')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        urls = "".join(f"<url><loc>{SITE}/{'' if n == 'index.html' else n.replace('.html', '')}</loc></url>" for n in PAGES) + "".join(f"<url><loc>{SITE}/portfolio/{p[0]}</loc></url>" for p in PROJECTS)
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    os.makedirs(os.path.join(OUT, "portfolio"), exist_ok=True)
    for p in PROJECTS:
        with open(os.path.join(OUT, "portfolio", p[0] + ".html"), "w") as f:
            f.write(page_project(p[0]))
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(page_404())
    with open(os.path.join(OUT, "_headers"), "w") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n\n/images/*\n  Cache-Control: public, max-age=31536000, immutable\n\n/*.css\n  Cache-Control: public, max-age=3600\n\n/*.js\n  Cache-Control: public, max-age=3600\n")
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write("# Old WordPress URLs -> new site\n/project /portfolio 301\n/project/* /portfolio 301\n/dt_team/* /about 301\n/blog / 301\n")
    print("built", ", ".join(PAGES), "+ 404, _headers; form", "posts to /api/enquiry")
