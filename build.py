"""The site engine — markdown posts + one site.toml -> a static site.

    python build.py                      builds the DrThomasAger site from ./site.toml
    python build.py sites/the-new-body   builds that site folder into its own site/
    python build.py --new sites/<name> [--kind blog|signup|blog-with-logins]
                                         copies template/ to start a new site
    python build.py --new-article "Title" [site folder]
                                         a new gold-letterhead article, as a draft
    python build.py --export sites/<name> <folder>
                                         writes that site as a standalone
                                         repository: engine + its files at the root

Everything that belongs to one person (names, colours, categories, the
mailing list, the shop, the home page and footer words) lives in that
site's site.toml. Structure lives here; appearance lives in the theme
tokens of assets/themes.css. TEMPLATE.md tells the whole of it.
"""
import html, itertools, json, math, re, shutil, sys, tomllib
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
ENGINE_ASSETS = ROOT / "assets"
TEMPLATE = ROOT / "template"


def configure(folder=ROOT):
    """Read one site folder's site.toml into the names the engine uses.
    The DrThomasAger site at the repository root is read on import, so
    scripts that `import build` keep working as before."""
    global FOLDER, CONF, POSTS, ASSETS, OVERLAY, SITE, SITE_NAME, SITE_URL
    global AUTHOR, TAGLINE, ROOTS, MAILING_ENDPOINT, CATEGORIES, CHILD_INFO
    global PRODUCTS, PROJECTS, THREAD, HSIN_HSIN_MING
    FOLDER = Path(folder).resolve()
    CONF = tomllib.loads((FOLDER / "site.toml").read_text(encoding="utf-8"))
    POSTS = FOLDER / "posts"
    ASSETS = ENGINE_ASSETS
    # a site's own images, favicon and stylesheets, copied over the
    # engine's assets/ in the built site
    OVERLAY = (FOLDER / "site-assets"
               if (FOLDER / "site-assets").is_dir() else None)
    SITE = FOLDER / "site"
    s = CONF["site"]
    SITE_NAME, SITE_URL, TAGLINE = s["name"], s["url"], s["tagline"]
    AUTHOR = s.get("author", SITE_NAME)   # the person, when the site has its own name
    ROOTS = CONF.get("roots", {})
    MAILING_ENDPOINT = CONF.get("mailing", {}).get("endpoint", "")
    CATEGORIES = CONF.get("categories", {})
    for c in CATEGORIES.values():
        c.setdefault("subs", {})
        for sub in c["subs"].values():
            sub.setdefault("children", [])
    CHILD_INFO = CONF.get("child_info", {})
    PRODUCTS = CONF.get("products", [])
    PROJECTS = CONF.get("projects", {})
    THREAD = CONF.get("weave", {}).get("thread", [])
    HSIN_HSIN_MING = CONF.get("footer", {}).get("scripture", "")


def C(section, key, default=""):
    """One value from site.toml, e.g. C("home", "hero_title")."""
    return CONF.get(section, {}).get(key, default)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def sub_lineage(name):
    """Return (category, subcategory, child-or-None) for a deepest sub name."""
    for cat, c in CATEGORIES.items():
        for sub, s in c["subs"].items():
            if name == sub:
                return cat, sub, None
            if name in s["children"]:
                return cat, sub, name
    raise ValueError(f"Unknown subcategory: {name}")

def inline_signup(idp, tag, heading, button_text):
    """A sign-up form that sits inside a post. It carries the post's
    own mailing list tag, so the list records which post a person
    joined from."""
    return (f'<aside class="post-join"><h2>{heading}</h2>'
            f'<form class="signup" id="{idp}" method="post" '
            f'action="{MAILING_ENDPOINT or "#"}" data-signup>'
            f'<input type="hidden" name="tag" value="{tag}">'
            f'<input type="text" name="metadata-name" placeholder="Name" '
            f'aria-label="Name">'
            f'<input type="email" name="email" placeholder="Email" '
            f'aria-label="Email" required>'
            f'<button type="submit" class="btn">{button_text}</button>'
            f'<p class="reassure">{C("mailing", "reassure")}</p></form></aside>')

def shop_block():
    packs = "".join(
        f'<li><a href="shop.html#{pr["key"]}">{pr["title"]}</a> '
        f'<span class="price">{pr["price"]}</span></li>'
        for pr in PRODUCTS)
    return (f'<aside class="post-shop"><h2>{C("shop", "block_heading")}</h2>'
            f'<p>{C("shop", "block_text")}</p><ul>{packs}</ul>'
            f'<a class="btn" href="shop.html">{C("shop", "block_button")}</a></aside>')

def shortcodes(body, stem):
    """[[join: tag | heading | button]] becomes a sign-up form and
    [[shop]] becomes the shop block."""
    count = itertools.count(1)
    def join(m):
        tag, heading, button = [x.strip() for x in m.group(1).split("|")]
        return inline_signup(f"join-{stem}-{next(count)}", tag, heading,
                             button)
    body = re.sub(r"<p>\[\[join:(.*?)\]\]</p>", join, body)
    body = body.replace("<p>[[shop]]</p>", shop_block())
    return body

def load_posts():
    """Every posts/*.md, newest first. A post whose front-matter says
    `draft: yes` stays out of the site, the feed and the sitemap."""
    posts = []
    for f in sorted(POSTS.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
        if meta.get("draft", "").strip().lower() in ("yes", "true"):
            continue
        if meta.get("style", "").strip() == "article":
            body = render_article(m.group(2), f.stem)
        else:
            body = markdown.markdown(m.group(2), extensions=["extra"])
            body = shortcodes(body, f.stem)
        cat, sub, child = sub_lineage(meta["subcategory"])
        posts.append({
            **meta, "category": cat, "sub": sub, "child": child,
            "pill": child or sub,
            "slug": meta.get("slug") or slugify(meta["title"]),
            "authors": [a.strip() for a in
                        meta.get("authors", AUTHOR).split(",") if a.strip()],
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "body": body,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

# ---- Streams of consciousness ----
# Each project of site.toml pours forth across the dark sections as a
# stream in its own constant colour, carrying its own small symbols all
# along its length. The same colour speaks everywhere the project
# appears: ribbon, project chip, card glyph.

def _hx(c):
    return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))

def _mix(c1, c2, t):
    a, b = _hx(c1), _hx(c2)
    return "#" + "".join(f"{round(a[i] + (b[i]-a[i]) * t):02x}" for i in range(3))

def project_color(name):
    if name in PROJECTS:
        return PROJECTS[name]["color"]
    return "#ffffff"

def shadow_color(name):
    """The solid shadow below project text. White cannot hold a
    shadow on the light ground, so the center wears its silver."""
    c = project_color(name)
    return "#cfcfcf" if c == "#ffffff" else c

def tag_color(project, tag):
    n = sum(map(ord, tag))
    return _mix(project_color(project), "#ffffff", 0.18 + (n % 4) * 0.10)

def deep(color):
    return _mix(color, "#000000", 0.55)

def _sm(u):
    return u * u * (3 - 2 * u)

def stream_svg(h=320):
    """The Great Rope (weaving v9, chosen 2026-08-25): one wandering
    course crosses the whole sky, and every strand — two hues per
    stream — twists around it as a single cable, evenly phased. Large
    scale: the course. Middle: the coiling strands. Small: the glyphs
    riding each strand. Where the rope tightens the hues stack into
    jewels; where it loosens the strands breathe apart to the black."""
    w = 1440
    strands = []
    for k, (name, st) in enumerate(PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k, v))
    n = len(strands)
    pts = 240
    coils = 3.3
    # the thread: the sunwise cycle repeated, so any visible crop of a
    # strand coloured url(#dta-thread) carries all of it
    cycle = THREAD + THREAD
    stops = "".join(
        f'<stop offset="{i / (len(cycle) - 1):.3f}" stop-color="{c}"/>'
        for i, c in enumerate(cycle))
    content = (f'<defs><linearGradient id="dta-thread" '
               f'x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>')
    for name, st, hue, k, v in strands:
        # couples: each project's two strands share adjacent coil
        # phase, so primary and its across-the-center secondary
        # visibly travel together
        phase = 2 * math.pi * k / 5 + v * (math.pi / n)
        idx = k * 2 + v
        thick = 11 if v == 0 else 6.5
        mid = []
        for i in range(pts + 1):
            u = i / pts
            cyu = (h * 0.5
                   + h * 0.24 * math.sin(1.15 * math.pi * u + 0.6)
                   + h * 0.10 * math.sin(2.6 * math.pi * u + 2.2))
            breathe = h * (0.10 + 0.085 * math.sin(2.0 * math.pi * u + 1.1))
            y = cyu + breathe * math.sin(2 * math.pi * coils * u + phase)
            mid.append((u * w, y))
        tops = [(x, y - thick / 2) for x, y in mid]
        bots = [(x, y + thick / 2) for x, y in mid]
        d = ("M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in tops)
             + " L" + " L".join(f"{x:.0f},{y:.1f}" for x, y in reversed(bots))
             + " Z")
        content += f'<path d="{d}" fill="{hue}" fill-opacity="0.75"/>'
        ink = ("#8a8a8a" if hue.startswith("url")
               else _mix(hue, "#000000", 0.6))
        j = 0
        u = 0.03 + (idx % 3) * 0.02
        while u < 0.97:
            i = int(u * pts)
            x, y = mid[i]
            x2, y2 = mid[min(i + 2, pts)]
            ang = math.degrees(math.atan2(y2 - y, x2 - x))
            size = 5.5 + ((j * 7 + idx * 3) % 4) * 1.1
            glyph = st["symbols"][j % len(st["symbols"])]
            content += (f'<text x="{x:.0f}" y="{y:.1f}" '
                        f'font-size="{size:.1f}" fill="{ink}" '
                        f'text-anchor="middle" '
                        f'transform="rotate({ang:.0f} {x:.0f} {y:.1f})" '
                        f'font-family="Cascadia Mono, Segoe UI Historic, Segoe UI Symbol, Leelawadee UI, Consolas, monospace">'
                        f'{glyph}</text>')
            u += 0.02 + ((j * 3) % 3) * 0.004
            j += 1
    return (f'<svg class="planes" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')

WAVE = ('<div class="wave" aria-hidden="true"><svg viewBox="0 0 1440 44" '
        'preserveAspectRatio="none"><path d="M0,22 C120,44 240,0 360,22 '
        'C480,44 600,0 720,22 C840,44 960,0 1080,22 C1200,44 1320,0 1440,22 '
        'L1440,44 L0,44 Z"/></svg></div>')

def dropdown(idp):
    boxes = ""
    for cat, c in CATEGORIES.items():
        boxes += (f'<label><input type="checkbox" name="tag" '
                  f'value="{c["slug"]}" checked> {cat}</label>')
        for sub, s in c["subs"].items():
            boxes += (f'<label class="sub-choice"><input type="checkbox" '
                      f'name="tag" value="{slugify(sub)}" checked> {sub}</label>')
            for ch in s["children"]:
                note = CHILD_INFO.get(ch, {}).get("note", "")
                boxes += (f'<label class="sub-choice child-choice">'
                          f'<input type="checkbox" name="tag" '
                          f'value="{slugify(ch)}" checked> {ch} '
                          + (f'<span class="choice-note">{note}</span>'
                             if note else '')
                          + '</label>')
    return (f'<details class="interests" id="{idp}-interests">'
            f'<summary>{C("mailing", "interests_summary")}</summary>'
            f'<div class="interest-grid">{boxes}</div></details>')

def signup_form(idp, button_text):
    return (f'<form class="signup" id="{idp}" method="post" '
            f'action="{MAILING_ENDPOINT or "#"}" data-signup>'
            f'<input type="text" name="metadata-name" placeholder="Name" '
            f'aria-label="Name">'
            f'<input type="email" name="email" placeholder="Email" aria-label="Email" required>'
            f'{dropdown(idp)}'
            f'<button type="submit" class="btn">{button_text}</button>'
            f'<p class="reassure">{C("mailing", "reassure")}</p></form>')

def header():
    # the roots side by side, each opening onto its own categories
    nav = "".join(
        f'<div class="root"><a class="root-link" href="{CATEGORIES[cats[0]]["slug"]}.html">{root}</a>'
        f'<div class="root-menu">'
        + "".join(f'<a href="{CATEGORIES[c]["slug"]}.html">{c}</a>' for c in cats if c in CATEGORIES)
        + '</div></div>'
        for root, cats in ROOTS.items())
    nav += "".join(f'<a href="{href}">{label}</a>'
                   for label, href in C("header", "nav", []))
    lg = CONF.get("logins", {})
    if C("site", "kind") == "blog-with-logins" and lg.get("url"):
        nav += f'<a href="{lg["url"]}">{lg.get("label", "Sign in")}</a>'
        if lg.get("library_url"):
            nav += f'<a href="{lg["library_url"]}">{lg.get("library_label", "Library")}</a>'

    return (f'<header class="top"><a class="brand" href="index.html">'
            f'<span class="brand-mark">{C("site", "brand_mark")}</span> {SITE_NAME}</a>'
            f'<nav>{nav}</nav>'
            f'<button class="btn btn-small" type="button" data-open-popup>'
            f'{C("header", "join_button", "Join the List")}</button></header>')

def footer():
    cols = ""
    for cat, c in CATEGORIES.items():
        links = ""
        for sub, s in c["subs"].items():
            links += f'<a href="{slugify(sub)}.html">{sub}</a>'
            for ch in s["children"]:
                links += (f'<a class="child-link" '
                          f'href="{slugify(ch)}.html">{ch}</a>')
        cols += f'<div><h3>{cat}</h3>{links}</div>'
    if PROJECTS:
        projects = "".join(
            f'<a class="ptx-shadow" style="--pc:{st["color"]}" '
            f'href="index.html">{name}</a>'
            for name, st in PROJECTS.items())
        cols += f'<div><h3>{C("footer", "projects_heading", "Projects")}</h3>{projects}</div>'
    cols += (f'<div><h3>{C("footer", "site_heading", "Site")}</h3>'
             + "".join(f'<a href="{href}">{label}</a>'
                       for label, href in C("footer", "links", []))
             + '</div>')
    image = (f'<img class="buddha-eyes" src="{C("footer", "image")}" '
             f'width="256" height="256" loading="lazy" decoding="async" '
             f'alt="{C("footer", "image_alt")}">' if C("footer", "image") else '')
    scripture = (f'<div class="hhm notranslate" translate="no" '
                 f'lang="{C("footer", "scripture_lang")}" '
                 f'aria-label="{C("footer", "scripture_label")}">'
                 f'{HSIN_HSIN_MING}</div>' if HSIN_HSIN_MING else '')
    accent = project_color(C("site", "accent_project"))
    return (f'<footer class="deep">{WAVE}<div class="foot-inner">{FOOT_SVG[0]}'
            f'<div class="foot-cta">'
            f'<div><p class="eyebrow" '
            f'style="color:{accent}">{C("footer", "cta_eyebrow")}</p>'
            f'<h2>{C("footer", "cta_heading")}</h2>'
            f'<p>{C("footer", "cta_text")}</p>'
            f'<button class="btn" type="button" data-open-popup>'
            f'{C("footer", "cta_button")}</button></div>'
            f'<div class="foot-cta-art" aria-hidden="true">{C("footer", "cta_art")}</div></div>'
            f'<div class="foot-grid">{cols}</div>'
            f'<div class="foot-close">{image}{scripture}</div></div>'
            f'<div class="foot-legal">&copy; {C("site", "year")} {AUTHOR}. '
            f'{C("footer", "legal")}</div></footer>')

def popup():
    return (f'<div class="popup-veil" id="popup" hidden><div class="popup-card">'
            f'<button class="popup-close" id="popup-close" aria-label="Close">&times;</button>'
            f'<div class="popup-art" aria-hidden="true"><span>{C("popup", "art")}</span></div>'
            f'<div class="popup-body"><h2>{C("popup", "heading")}</h2>'
            f'{signup_form("popup-form", C("popup", "button", "Join"))}'
            f'</div></div></div>')

def page(title, body, desc=None, path="index.html", kind="website",
         data=None):
    """Every page names its own canonical address, carries the preview
    tags social sites read, and carries structured data for search."""
    desc = TAGLINE if desc is None else desc
    url = SITE_URL + ("" if path == "index.html" else path)
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    data = data or {"@context": "https://schema.org", "@type": "WebPage",
                    "name": title, "description": desc, "url": url}
    ld = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    extra_css = "".join(f'<link rel="stylesheet" href="{h}">'
                        for h in C("site", "extra_css", []))
    thanks = C("site", "signup_thanks")
    body_attrs = (f' data-thanks="{html.escape(thanks, quote=True)}"'
                  if thanks else '')
    return (f'<!DOCTYPE html><html lang="{C("site", "lang", "en")}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{t}</title><meta name="description" content="{d}">'
            f'<meta name="google" content="notranslate">'
            f'<meta name="robots" content="index, follow, max-snippet:-1, '
            f'max-image-preview:large">'
            f'<link rel="canonical" href="{url}">'
            f'<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">'
            f'<link rel="alternate" type="application/atom+xml" '
            f'title="{SITE_NAME}" href="{SITE_URL}atom.xml">'
            f'<meta property="og:type" content="{kind}">'
            f'<meta property="og:site_name" content="{SITE_NAME}">'
            f'<meta property="og:title" content="{t}">'
            f'<meta property="og:description" content="{d}">'
            f'<meta property="og:url" content="{url}">'
            f'<meta name="twitter:card" content="summary">'
            f'<meta name="twitter:title" content="{t}">'
            f'<meta name="twitter:description" content="{d}">'
            f'<script type="application/ld+json">{ld}</script>'
            f'<link rel="stylesheet" href="assets/base.css">'
            f'<link rel="stylesheet" href="assets/themes.css">{extra_css}'
            f'</head><body class="{C("site", "body_class", "theme-ink")}"{body_attrs}>'
            f'{header()}{body}{footer()}{popup()}'
            f'<script src="assets/site.js" defer></script></body></html>')

def card(p, level="h3"):
    proj = p.get("project", SITE_NAME)
    return (f'<a class="card" href="{p["slug"]}.html">'
            f'<div class="card-art" aria-hidden="true" style="color:'
            f'{deep(project_color(proj))}">'
            f'<span>{p.get("glyph", C("site", "default_glyph", "☀"))}</span></div>'
            f'<{level} class="ptx-shadow card-title" '
            f'style="--pc:{shadow_color(proj)}">'
            f'{p["title"]}</{level}><p>{p["description"]}</p></a>')

def grid(cards_html, cls="grid"):
    """A card grid. An empty one says so, in the site's own words, when
    site.toml gives home.empty_text."""
    if not cards_html and C("home", "empty_text"):
        return f'<p class="empty-note">{C("home", "empty_text")}</p>'
    return f'<div class="{cls}">{cards_html}</div>'

def hero(title_html, sub_text, form_id, svg=""):
    return (f'<section class="hero">{svg}<div class="hero-inner"><div class="hero-copy">'
            f'<h1>{title_html}</h1><p class="hero-sub">{sub_text}</p>'
            f'<button class="btn btn-hero" type="button" data-open-popup>'
            f'{C("home", "hero_button")}</button></div>'
            f'<div class="hero-art" aria-hidden="true"><span>{C("home", "hero_art")}</span></div>'
            f'</div><div class="ornament" aria-hidden="true">{C("home", "ornament")}</div>'
            f'{WAVE}</section>')

def index_body(posts, svg_fn=None):
    """The Swim University anatomy, worn by this site's own content:
    hero -> trust band -> feature + four cards -> dark mid band ->
    Articles grid. (Footer and popup arrive through page().)"""
    svg_fn = svg_fn or stream_svg
    n_symbols = sum(len(p["symbols"]) for p in PROJECTS.values())
    stats = [(ico, num.format(posts=len(posts), symbols=n_symbols), lab)
             for ico, num, lab in C("home", "stats", [])]
    trust = (f'<section class="trust"><h2>{C("home", "trust_heading")}</h2>'
             '<div class="trust-grid">'
             + "".join(
                 f'<div><div class="stat-num"><span class="stat-ico">{ico}'
                 f'</span>{num}</div><div class="stat-label">{lab}</div></div>'
                 for ico, num, lab in stats)
             + '</div></section>') if stats else ''
    # the feature: one project spoken in its own voice
    feature = ''
    f = CONF.get("home", {}).get("feature")
    if f:
        collage = "".join(
            f'<span style="color:{deep(st["color"])}">{s}</span>'
            for st in PROJECTS.values() for s in st["symbols"][:6])
        first = next((p for p in posts if p.get("project") == f.get("project")),
                     None)
        feature = (
            f'<section class="feature"><div class="feature-art" aria-hidden="true">'
            f'{collage}</div><div class="feature-copy">'
            f'<p class="eyebrow">{f["eyebrow"]}</p>'
            f'<h2>{f["heading"]}</h2>'
            f'<p>{f["text"]}</p>'
            # the button opens f["href"] when given, else the newest
            # post of f["project"]
            + (f'<a class="btn" href="{f.get("href") or first["slug"] + ".html"}">'
               f'{f["button"]}</a>' if f.get("href") or first else '')
            + '</div></section>')
    featured = []
    seen_subs = set()
    for p in posts:
        if p["pill"] not in seen_subs:
            featured.append(p)
            seen_subs.add(p["pill"])
        if len(featured) == 4:
            break
    feature_cards = grid("".join(card(p) for p in featured), "grid grid-4")
    # the dark mid band, a second invitation to the list
    midband = ''
    mb = CONF.get("home", {}).get("midband")
    if mb:
        midband = (
            f'<section class="midband">{WAVE.replace("wave", "wave wave-top", 1)}'
            f'{svg_fn(h=260)}'
            f'<div class="midband-inner"><div class="midband-copy">'
            f'<p class="eyebrow" style="color:{project_color(C("site", "accent_project"))}">'
            f'{mb["eyebrow"]}</p>'
            f'<h2>{mb["heading"]}</h2>'
            f'<p>{mb["text"]}</p>'
            f'<button class="btn" type="button" data-open-popup>'
            f'{mb["button"]}</button></div>'
            f'<div class="midband-art" aria-hidden="true"><span>{mb.get("art", "")}</span></div>'
            f'</div>{WAVE}</section>')
    # Articles — heading left, see-all right, three-column grid
    cat_links = " or ".join(f'<a href="{c["slug"]}.html">{cat}</a>'
                            for cat, c in CATEGORIES.items())
    articles = (f'<section class="band"><div class="band-head">'
                f'<h2>{C("home", "articles_heading", "Articles")}</h2>'
                f'<span class="see-in">See all in '
                f'{cat_links}</span></div>'
                + grid("".join(card(p) for p in posts[:6])) + '</section>')
    return (hero(C("home", "hero_title"), C("home", "hero_sub"), "hero-form",
                 svg_fn(h=320))
            + trust
            + f'<main>{feature}{feature_cards}</main>'
            + midband
            + f'<main>{articles}</main>')

def build_index(posts):
    (SITE / "index.html").write_text(
        page(f"{SITE_NAME} — {TAGLINE}", index_body(posts),
             data={"@context": "https://schema.org", "@type": "WebSite",
                   "name": SITE_NAME, "description": TAGLINE,
                   "url": SITE_URL}), encoding="utf-8")

def build_categories(posts):
    for cat, c in CATEGORIES.items():
        secs = ""
        for sub, s in c["subs"].items():
            groups = [(sub, [p for p in posts if p["sub"] == sub and not p["child"]])]
            groups += [(ch, [p for p in posts if p["child"] == ch])
                       for ch in s["children"]]
            inner = ""
            for name, items in groups:
                if not items:
                    continue
                cards = "".join(card(p) for p in items)
                inner += (f'<div class="band-head" id="{slugify(name)}">'
                          f'<h2>{name}</h2>'
                          f'<a class="see-all" href="{slugify(name)}.html">'
                          f'See all the guides &raquo;</a>'
                          f'</div><div class="grid">{cards}</div>')
            if inner:
                secs += f'<section class="band">{inner}</section>'
        if not secs and C("home", "empty_text"):
            secs = f'<section class="band">{grid("")}</section>'
        body = (f'<section class="hero hero-lite">'
                f'{stream_svg(h=180)}'
                f'<div class="hero-inner">'
                f'<div class="hero-copy"><h1>{cat}</h1>'
                f'<p class="hero-sub">{c["blurb"]}</p></div></div>{WAVE}</section>'
                f'<main>{secs}</main>')
        (SITE / f'{c["slug"]}.html').write_text(
            page(f"{cat} — {SITE_NAME}", body, c["blurb"],
                 path=f'{c["slug"]}.html'), encoding="utf-8")

def build_subcategories(posts):
    """The middle level of the tree: one page per subcategory (and per
    child), holding its name, its blurb, and every one of its cards."""
    pages = []
    for cat, c in CATEGORIES.items():
        for sub, s in c["subs"].items():
            items = [p for p in posts if p["sub"] == sub]
            pages.append((sub, s.get("blurb", c["blurb"]), items))
            for ch in s["children"]:
                child_items = [p for p in posts if p["child"] == ch]
                blurb = CHILD_INFO.get(ch, {}).get("blurb", "")
                pages.append((ch, blurb, child_items))
    for name, blurb, items in pages:
        cards = "".join(card(p, "h2") for p in items)
        body = (f'<section class="hero hero-lite">'
                f'{stream_svg(h=180)}'
                f'<div class="hero-inner">'
                f'<div class="hero-copy"><h1>{name}</h1>'
                f'<p class="hero-sub">{blurb}</p></div></div>{WAVE}</section>'
                f'<main><section class="band">'
                f'{grid(cards)}</section></main>')
        (SITE / f'{slugify(name)}.html').write_text(
            page(f"{name} — {SITE_NAME}", body, blurb or TAGLINE,
                 path=f"{slugify(name)}.html"),
            encoding="utf-8")
    return len(pages)

def build_posts(posts):
    initials = C("site", "author_initials")
    for p in posts:
        if p.get("style") == "article":
            (SITE / f'{p["slug"]}.html').write_text(article_page(p, posts),
                                                    encoding="utf-8")
            continue
        more = [q for q in posts if q["category"] == p["category"]
                and q is not p][:3]
        more_html = "".join(card(q) for q in more)
        body = (
            f'<section class="hero hero-lite">'
            f'{stream_svg(h=140)}'
            f'<div class="hero-inner"></div>{WAVE}</section>'
            f'<main class="article"><h1 class="post-title ptx-shadow" '
            f'style="--pc:{shadow_color(p.get("project", SITE_NAME))}">'
            f'{p["title"]}</h1>'
            f'<div class="byline"><span class="avatar" aria-hidden="true">{initials}</span>'
            f'<strong>{", ".join(p["authors"])}</strong>'
            f'<span class="dot">|</span>'
            f'<span>Updated {p["date"]}</span><span class="dot">|</span>'
            f'<span>{p["readtime"]} min read</span>'
            f'<a class="pill" href="{slugify(p["pill"])}.html">'
            f'{p["pill"]}</a></div>'
            f'<div class="post-body">{p["body"]}</div>'
            f'<div class="tag-row"><span class="tag tag-project ptx-shadow" '
            f'style="--pc:{shadow_color(p.get("project", SITE_NAME))}">'
            f'Project &mdash; {p.get("project", SITE_NAME)}</span>'
            + "".join(
                f'<span class="tag" style="border-color:'
                f'{deep(tag_color(p.get("project", SITE_NAME), t))};color:'
                f'{deep(tag_color(p.get("project", SITE_NAME), t))}">{t}</span>'
                for t in p["tags"]) +
            f'<div class="author-card"><span class="avatar avatar-big" '
            f'aria-hidden="true">{initials}</span><div><h2>{AUTHOR}</h2>'
            f'<p>{C("site", "author_bio")}</p></div></div>'
            f'<section class="band"><div class="band-head"><h2>More Reading</h2>'
            f'<span class="see-in">See more in '
            f'<a href="{slugify(p["pill"])}.html">{p["pill"]}</a></span></div>'
            f'<div class="grid">{more_html}</div></section></main>')
        (SITE / f'{p["slug"]}.html').write_text(
            page(f'{p["title"]} — {SITE_NAME}', body, p["description"],
                 path=f'{p["slug"]}.html', kind="article",
                 data=article_data(p)),
            encoding="utf-8")

def article_data(p):
    url = f'{SITE_URL}{p["slug"]}.html'
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": p["title"], "description": p["description"],
        "datePublished": p["date"],
        "dateModified": p.get("updated", p["date"]),
        "author": [{"@type": "Person", "name": a} for a in p["authors"]],
        "publisher": {"@type": "Person", "name": AUTHOR, "url": SITE_URL},
        "mainEntityOfPage": url, "url": url,
        "articleSection": p["pill"], "keywords": ", ".join(p["tags"]),
        "inLanguage": "en",
    }

FOOT_SVG = [""]

# ---- Articles in the Blog Template, with the gold letterhead ----
# A post whose front-matter says `style: article` is written as a reading
# page in assets/blog/ (the Blog Template of the Smile Portal post), its
# widgets written in plain words. template/posts/every-widget.md shows
# every one of them.

CALLOUTS = {"key": "Key idea", "learn": "Learn more", "caveat": "Caveat",
            "vision": "Vision", "aside": "Aside"}

def _blocks(md):
    """The ::: blocks. `:::key Label` ... `:::` and its kin."""
    def one(m):
        kind, label, body = m.group(1), m.group(2).strip(), m.group(3)
        if kind in CALLOUTS:
            return (f'<div class="callout {kind}" markdown="1">\n'
                    f'<div class="label">{label or CALLOUTS[kind]}</div>\n\n'
                    f'{body}\n\n</div>')
        if kind == "more":
            return (f'<details class="more" markdown="1">\n'
                    f'<summary>{label or "Read more"}</summary>\n'
                    f'<div class="body" markdown="1">\n\n{body}\n\n</div>\n</details>')
        if kind == "quote":
            cite = f'<cite>{label}</cite>' if label else ''
            return (f'<blockquote class="pull" markdown="1">\n\n{body}\n\n'
                    f'{cite}</blockquote>')
        if kind == "math":
            return f'<div class="math">{body.strip()}</div>'
        if kind == "terms":
            rows = "".join(
                f'<div class="term">{t.strip()}</div><div>{d.strip()}</div>'
                for t, d in (line.split(":", 1) for line in body.splitlines()
                             if ":" in line))
            head = f'<div class="label">{label}</div>' if label else ''
            return f'<div class="callout aside">{head}<div class="terms">{rows}</div></div>'
        return m.group(0)
    return re.sub(r"^:::(\w+)[ \t]*(.*?)\n(.*?)\n:::[ \t]*$", one, md,
                  flags=re.M | re.S)

def _video(url):
    m = re.search(r"(?:youtu\.be/|v=|embed/)([\w-]{6,})", url)
    if m:
        return f"https://www.youtube-nocookie.com/embed/{m.group(1)}"
    m = re.search(r"vimeo\.com/(\d+)", url)
    return f"https://player.vimeo.com/video/{m.group(1)}" if m else url

def render_article(md, stem):
    """Markdown with the article widgets -> the article's HTML."""
    md = _blocks(md)
    body = markdown.markdown(md, extensions=["extra", "toc"])
    body = shortcodes(body, stem)
    # [[video: address | caption]]
    def video(m):
        url, _, cap = m.group(1).partition("|")
        cap = f'<figcaption>{cap.strip()}</figcaption>' if cap.strip() else ''
        return (f'<figure class="video"><iframe src="{_video(url.strip())}" '
                f'title="{html.escape(cap and cap or "Video", quote=True)}" loading="lazy" '
                f'allow="accelerometer; encrypted-media; picture-in-picture; fullscreen" '
                f'allowfullscreen></iframe>{cap}</figure>')
    body = re.sub(r"<p>\[\[video:(.*?)\]\]</p>", video, body)
    # [[button: words | address]]
    body = re.sub(r"<p>\[\[button:(.*?)\|(.*?)\]\]</p>",
                  lambda m: f'<p class="btn-row"><a class="btn-link" href="{m.group(2).strip()}">'
                            f'{m.group(1).strip()}</a></p>', body)
    # a picture alone in its paragraph becomes a figure, its words the caption
    body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)" ?/?></p>',
                  lambda m: f'<figure><img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">'
                            + (f'<figcaption>{m.group(1)}</figcaption>' if m.group(1) else '')
                            + '</figure>', body)
    # - [ ] a checklist a reader ticks, remembered in their browser
    body = re.sub(r"<li>\[( |x|X)\] ?",
                  lambda m: '<li class="check"><label><input type="checkbox"'
                            + (' checked' if m.group(1) != ' ' else '') + '> ', body)
    body = re.sub(r'(<li class="check"><label>.*?)</li>', r"\1</label></li>", body,
                  flags=re.S)
    # a list right after a Sources or Notes heading is set as sources
    body = re.sub(r'(<h2 id="[^"]*">(?:Sources|Notes|References)</h2>\s*)<(ol|ul)>',
                  r'\1<\2 class="sources">', body)
    # --- is the ornament
    body = body.replace("<hr />", '<hr class="ornament">')
    # the first paragraph opens with a drop capital
    body = body.replace("<p>", '<p class="drop">', 1)
    # [[note: words]] beside its line on a wide screen, opened in place on a phone
    n = itertools.count(1)
    def para(m):
        notes = []
        def note(k):
            i = next(n)
            notes.append(f'<p class="sn" id="n-{stem}-{i}"><span class="n">{i}</span>'
                         f'{k.group(1).strip()}</p>')
            return f'<sup class="fn"><a href="#n-{stem}-{i}">{i}</a></sup>'
        inner = re.sub(r"\[\[note:((?:(?!\[\[|<code>).)*?)\]\]", note, m.group(0))
        return inner + "".join(notes)
    body = re.sub(r"<(p|li)[^>]*>.*?</\1>", para, body, flags=re.S)
    return body

def _fonts():
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">')

def _reading_head(title, desc, path, kind="article", data=None):
    url = SITE_URL + ("" if path == "index.html" else path)
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    data = data or {"@context": "https://schema.org", "@type": "WebPage",
                    "name": title, "description": desc, "url": url}
    ld = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    extra_css = "".join(f'<link rel="stylesheet" href="{h}">'
                        for h in C("site", "extra_css", []))
    return (f'<!DOCTYPE html><html lang="{C("site", "lang", "en")}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{t}</title><meta name="description" content="{d}">'
            f'<link rel="canonical" href="{url}">'
            f'<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">'
            f'<link rel="alternate" type="application/atom+xml" title="{SITE_NAME}" href="{SITE_URL}atom.xml">'
            f'<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE_NAME}">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            f'<meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">'
            f'<script type="application/ld+json">{ld}</script>{_fonts()}'
            f'<link rel="stylesheet" href="assets/blog/blog.css">'
            f'<link rel="stylesheet" href="assets/blog/letterhead-gold.css">'
            f'<link rel="stylesheet" href="assets/blog/widgets.css">{extra_css}</head>')

def _reading_tail():
    eyes = (f'<a class="buddha-eyes" href="index.html" aria-label="{SITE_NAME}">'
            f'<img src="{C("footer", "image")}" width="256" height="256" '
            f'loading="lazy" decoding="async" alt="{C("footer", "image_alt")}"></a>'
            if C("footer", "image") else '')
    thanks = C("site", "signup_thanks")
    return (f'<div class="toolbar"><button id="restore" type="button" hidden>Restore removed</button>'
            f'<button id="theme" type="button">☾ Night</button></div>{eyes}'
            f'<script src="assets/blog/blog.js"></script>'
            f'<script src="assets/blog/letterhead-gold.js"></script>'
            f'<script src="assets/blog/widgets.js"></script>'
            f'<script src="assets/site.js" defer></script>'
            + (f'<script>document.body.dataset.thanks={json.dumps(thanks)}</script>' if thanks else '')
            + '</body></html>')

def _top_links():
    links = [(f'&larr; {SITE_NAME}', "index.html")]
    lg = CONF.get("logins", {})
    if C("site", "kind") == "blog-with-logins" and lg.get("url"):
        links.append((lg.get("label", "Sign in"), lg["url"]))
    return ('<nav class="home-link">'
            + "".join(f'<a href="{h}">{l}</a>' for l, h in links) + '</nav>')

def article_page(p, posts):
    lineage = " › ".join(x for x in (p["category"], p["sub"], p["child"]) if x)
    toc_items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])
    toc = ('<nav class="toc" aria-label="Contents"><div class="label">Contents</div><ol>'
           + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc_items)
           + '</ol></nav>') if len(toc_items) >= 3 else ''
    more = [q for q in posts if q["category"] == p["category"] and q is not p][:3]
    more_html = ('<section class="more-reading"><h2>More reading</h2><ul>'
                 + "".join(f'<li><a href="{q["slug"]}.html">{q["title"]}</a>'
                           f'<span>{q["description"]}</span></li>' for q in more)
                 + '</ul></section>') if more else ''
    tags = ('<p class="tag-row">' + "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
            + '</p>') if p["tags"] else ''
    join = ''
    if MAILING_ENDPOINT is not None and C("mailing", "reassure"):
        join = inline_signup(f'join-{p["slug"]}-end', p["slug"],
                             C("footer", "cta_heading", "New posts arrive by email."),
                             C("footer", "cta_button", "Join the Mailing List"))
    body = (f'<body><div class="progress"></div><div class="page"><article>'
            f'{_top_links()}'
            f'<header class="letterhead"><p class="kicker">{lineage}</p>'
            f'<h1>{p["title"]}</h1><p class="lede">{p["description"]}</p>'
            f'<div class="byline"><span class="who">{", ".join(p["authors"])}</span>'
            f'<span class="dot"></span><span>{p["date"]}</span><span class="dot"></span>'
            f'<span>{p["readtime"]} min read</span></div></header>'
            f'{toc}<div class="article-body">{p["body"]}</div>{tags}'
            f'<div class="author"><span class="avatar">{C("site", "author_initials")}</span>'
            f'<div><div class="name">{AUTHOR}</div>{C("site", "author_bio")}</div></div>'
            f'{join}{more_html}</article></div>')
    return (_reading_head(f'{p["title"]} — {SITE_NAME}', p["description"],
                          f'{p["slug"]}.html', data=article_data(p))
            + body + _reading_tail())

def build_signup():
    """A mailing-list-only site: one short page, its words from the
    [signup] table of site.toml."""
    su = CONF.get("signup", {})
    fb = next((pr for pr in PRODUCTS
               if pr["key"] == C("freebie", "product")), None)
    gift = (f'<div class="callout key"><div class="label">Free for joining</div>'
            f'<p><strong>{fb["title"]}</strong>. {fb["text"]}</p></div>') if fb else ''
    form = inline_signup("signup-join", su.get("tag", "signup"),
                         su.get("form_heading", ""),
                         su.get("button", C("home", "hero_button", "Join")))
    body = (f'<body class="signup-only"><div class="page"><article>'
            f'<header class="letterhead"><p class="kicker">{su.get("kicker", SITE_NAME)}</p>'
            f'<h1>{su.get("heading", SITE_NAME)}</h1>'
            f'<p class="lede">{su.get("text", TAGLINE)}</p></header>'
            f'{gift}{form}'
            f'<p class="legal">&copy; {C("site", "year")} {AUTHOR}. {C("footer", "legal")}</p>'
            f'</article></div>')
    (SITE / "index.html").write_text(
        _reading_head(f"{SITE_NAME} — {TAGLINE}", TAGLINE, "index.html",
                      kind="website") + body + _reading_tail(),
        encoding="utf-8")

def build_feed(posts):
    """atom.xml — the door the mailing list's RSS-to-email automation
    (or the Mailing Steward) watches. Each entry carries its category
    lineage as atom categories so per-tag sending stays possible."""
    def esc(t):
        return (t.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;"))
    entries = ""
    for p in posts[:22]:
        url = f"{SITE_URL}{p['slug']}.html"
        cats = "".join(
            f'<category term="{slugify(c)}" label="{esc(c)}"/>'
            for c in [p["category"], p["sub"]] + ([p["child"]] if p["child"] else []))
        entries += (
            f'<entry><title>{esc(p["title"])}</title>'
            f'<link href="{url}"/><id>{url}</id>'
            f'<updated>{p["date"]}T00:00:00Z</updated>'
            f'<summary>{esc(p["description"])}</summary>{cats}</entry>')
    updated = (posts[0]["date"] if posts else "2026-08-30") + "T00:00:00Z"
    feed = (f'<?xml version="1.0" encoding="utf-8"?>'
            f'<feed xmlns="http://www.w3.org/2005/Atom">'
            f'<title>{SITE_NAME}</title><subtitle>{TAGLINE}</subtitle>'
            f'<link href="{SITE_URL}"/>'
            f'<link rel="self" href="{SITE_URL}atom.xml"/>'
            f'<id>{SITE_URL}</id><updated>{updated}</updated>'
            f'<author><name>{AUTHOR}</name></author>{entries}</feed>')
    (SITE / "atom.xml").write_text(feed, encoding="utf-8")

def build_shop():
    """The shop page, when site.toml lists products. Returns whether
    one was built."""
    if not PRODUCTS:
        return False
    gp = C("shop", "glyph_project", C("site", "accent_project"))
    items = "".join(
        f'<div class="card shop-item" id="{pr["key"]}">'
        f'<div class="card-art" aria-hidden="true" style="color:'
        f'{deep(project_color(gp))}"><span>{pr["glyph"]}</span></div>'
        f'<h2 class="ptx-shadow card-title" '
        f'style="--pc:{shadow_color(gp)}">{pr["title"]}</h2>'
        f'<p class="price">{pr["price"]}</p><p>{pr["text"]}</p></div>'
        for pr in PRODUCTS)
    blurb = C("shop", "blurb")
    body = (f'<section class="hero hero-lite">{stream_svg(h=180)}'
            f'<div class="hero-inner"><div class="hero-copy"><h1>{C("shop", "title", "Shop")}</h1>'
            f'<p class="hero-sub">{blurb}</p></div></div>{WAVE}</section>'
            f'<main><section class="band"><div class="grid">{items}</div>'
            f'</section><section class="band">'
            + inline_signup("shop-join", C("shop", "signup_tag"),
                            C("shop", "signup_heading"),
                            C("shop", "signup_button"))
            + '</section></main>')
    (SITE / "shop.html").write_text(
        page(f"{C('shop', 'title', 'Shop')} — {SITE_NAME}", body, blurb,
             path="shop.html"),
        encoding="utf-8")
    return True

def build_sitemap(posts, names):
    """sitemap.xml lists every page with its last change, and
    robots.txt invites every crawler and names the sitemap."""
    latest = posts[0]["date"] if posts else "2026-08-30"
    rows = [("", latest)] + [(f"{n}.html", latest) for n in names]
    rows += [(f'{p["slug"]}.html', p.get("updated", p["date"])) for p in posts]
    # HTML posts published outside posts/, one folder each under site/,
    # named in site.toml's sections.sitemap_folders
    for folder in C("sections", "sitemap_folders", []):
        here = SITE / folder
        if here.exists():
            rows += [(f.parent.relative_to(SITE).as_posix() + "/", latest)
                     for f in sorted(here.glob("**/index.html"))]
    urls = "".join(f"<url><loc>{SITE_URL}{path}</loc>"
                   f"<lastmod>{day}</lastmod></url>" for path, day in rows)
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>", encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n",
        encoding="utf-8")

def page_names():
    names = []
    for cat, c in CATEGORIES.items():
        names.append(c["slug"])
        for sub, s in c["subs"].items():
            names.append(slugify(sub))
            names += [slugify(ch) for ch in s["children"]]
    return names

def build_gurus():
    """The guru browsing section, built by hanjopurebuddha.com/build.py into
    site/gurus/, when site.toml names it in sections.gurus. That folder is
    a self-contained site of its own (one teacher per folder under its
    teachers/); here it renders as a section."""
    import importlib.util
    name = C("sections", "gurus")
    if not name:
        return 0
    src = ROOT / name / "build.py"
    if not src.exists():
        return 0
    spec = importlib.util.spec_from_file_location("gurus_build", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.SITE = SITE / "gurus"
    if mod.SITE.exists():
        shutil.rmtree(mod.SITE)
    mod.SITE.mkdir(parents=True)
    cards = [mod.build_teacher(f, mod.SITE) for f in sorted(p for p in mod.TEACHERS.iterdir() if p.is_dir() and not p.name.startswith("_"))]
    mod.build_index(cards, mod.SITE / "index.html", prefix="")
    return len(cards)

KINDS = ("blog", "signup", "blog-with-logins")

def new_site(target, kind="blog"):
    """Copy template/ to start a new site of one kind: blog (a blog with
    a mailing list), signup (one signup page), or blog-with-logins.
    Refuses to touch a folder that already exists."""
    target = Path(target)
    if kind not in KINDS:
        sys.exit(f"The kind is one of {', '.join(KINDS)}.")
    if target.exists():
        sys.exit(f"{target} already exists; nothing was copied.")
    shutil.copytree(TEMPLATE, target)
    toml = target / "site.toml"
    toml.write_text(toml.read_text(encoding="utf-8").replace(
        'kind = "blog"', f'kind = "{kind}"', 1), encoding="utf-8")
    print(f"New site at {target}. Fill in {target / 'site.toml'}, then "
          f"run: python build.py {target}")

def new_article(title, folder="."):
    """A new article in posts/, in the gold-letterhead style with every
    widget shown, held back as a draft until `draft: yes` is deleted."""
    configure(folder)
    import datetime
    slug = slugify(title)
    dest = POSTS / f"{slug}.md"
    if dest.exists():
        sys.exit(f"{dest} already exists; nothing was written.")
    first_sub = next((sub for c in CATEGORIES.values() for sub in c["subs"]), "")
    text = (TEMPLATE / "posts" / "every-widget.md").read_text(encoding="utf-8")
    text = re.sub(r"^title: .*$", f"title: {title}", text, count=1, flags=re.M)
    text = re.sub(r"^subcategory: .*$", f"subcategory: {first_sub}", text, count=1, flags=re.M)
    text = re.sub(r"^date: .*$", f"date: {datetime.date.today()}", text, count=1, flags=re.M)
    text = re.sub(r"^project: .*$", f"project: {next(iter(PROJECTS), '')}", text, count=1, flags=re.M)
    POSTS.mkdir(exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print(f"New article at {dest}. Write it, delete the line `draft: yes`, and build.")

ENGINE_FILES = ["build.py", "assets", "template", "TEMPLATE.md", "HOW-TO.md", "docs/how-to",
                "tools/ghost_one.py", ".github/workflows/publish.yml",
                ".github/workflows/new-article.yml", ".github/workflows/new-site.yml",
                ".github/workflows/export-site.yml", ".github/workflows/ghost-export.yml",
                "New Article.bat", "New Site.bat", "Build a Site.bat"]

def export_site(folder, dest):
    """Write one site as a standalone repository: the engine files, and
    the site folder's own files at the root, where build.py reads them.
    The new folder builds with `python build.py` and publishes with the
    GitHub Pages workflow it carries."""
    folder, dest = Path(folder), Path(dest)
    if dest.exists():
        sys.exit(f"{dest} already exists; nothing was written.")
    dest.mkdir(parents=True)
    for name in ENGINE_FILES:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dest / name)
        elif src.exists():
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / name)
    for item in folder.iterdir():
        if item.name in ("site", "__pycache__"):
            continue
        if item.is_dir():
            shutil.copytree(item, dest / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest / item.name)
    (dest / ".gitignore").write_text(
        "__pycache__/\n*.pyc\nmailing/steward/key.txt\n"
        "mailing/steward/state.json\n", encoding="utf-8")
    print(f"Standalone repository written to {dest}. Inside it: python build.py")

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--new"]:
        return new_site(argv[1], argv[3] if argv[2:3] == ["--kind"] else "blog")
    if argv[:1] == ["--new-article"]:
        return new_article(argv[1], argv[2] if len(argv) > 2 else ".")
    if argv[:1] == ["--export"]:
        return export_site(argv[1], argv[2])
    if argv:
        configure(argv[0])
    SITE.mkdir(exist_ok=True)
    out_assets = SITE / "assets"
    if out_assets.exists():
        shutil.rmtree(out_assets)
    shutil.copytree(ASSETS, out_assets)
    if OVERLAY:
        shutil.copytree(OVERLAY, out_assets, dirs_exist_ok=True)
    if C("site", "kind") == "signup":
        build_signup()
        build_sitemap([], [])
        print(f"Built the signup page into {SITE}")
        return
    posts = load_posts()
    FOOT_SVG[0] = stream_svg(h=280)
    build_index(posts)
    build_categories(posts)
    n_subs = build_subcategories(posts)
    build_posts(posts)
    build_feed(posts)
    shop = build_shop()
    n_gurus = build_gurus()
    build_sitemap(posts, page_names() + (["shop"] if shop else []))
    if C("sections", "gurus"):
        print(f"Guru section: {n_gurus} teacher page(s) in {SITE / 'gurus'}")
    print(f"Built {1 + len(CATEGORIES) + n_subs + len(posts)} "
          f"pages into {SITE}")

configure(ROOT)

if __name__ == "__main__":
    main()
