"""Build drthomasager.com — markdown posts -> static site.

Structure lives here; all appearance lives in assets/themes.css tokens.
"""
import itertools, math, re, shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
ASSETS = ROOT / "assets"
SITE = ROOT / "site"

SITE_NAME = "Dr Thomas Ager"
TAGLINE = ("Writing on Buddhism, Smile, Videogames, Sacred Travel, "
           "and Machine Learning.")

# ---------------------------------------------------------------
# MAILING LIST ENDPOINT — the one line that receives the real
# provider URL (form POST target) when a provider is chosen.
MAILING_ENDPOINT = "https://buttondown.com/api/emails/embed-subscribe/drthomasager"
# ---------------------------------------------------------------

CATEGORIES = {
    "Prompt Engineering": {
        "slug": "prompt-engineering",
        "blurb": "The craft of speaking with language models — languages, prompts, and teachings.",
        "subs": {
            "Prompt Language Development": {
                "children": ["Smile"],
                "blurb": "Building languages for speaking with AI."},
            "Free Prompts": {
                "children": [],
                "blurb": "Prompts to take, use, and make your own."},
            "Tutorial": {
                "children": [],
                "blurb": "Step-by-step introductions, from the beginning."},
        },
    },
    "Spirituality": {
        "slug": "spirituality",
        "blurb": "Songs, commentaries, and the living view.",
        "subs": {
            "Songs of Enlightenment": {
                "children": [],
                "blurb": "Songs sung from the living view."},
            "Commentaries": {
                "children": [],
                "blurb": "Commentaries on texts worth resting in."},
            "Sacred Geometry": {
                "children": [],
                "blurb": "The forms beneath the forms — drawn, built, "
                         "and walked into."},
        },
    },
}

# Child pages (deepest level) carry their own words
CHILD_INFO = {
    "Smile": {"blurb": "The Smile Prompt Language and Smile Chat, "
                       "written up as they grow."},
}

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

def load_posts():
    posts = []
    for f in sorted(POSTS.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
        body = markdown.markdown(m.group(2), extensions=["extra"])
        cat, sub, child = sub_lineage(meta["subcategory"])
        posts.append({
            **meta, "category": cat, "sub": sub, "child": child,
            "pill": child or sub, "slug": slugify(meta["title"]),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "body": body,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

# ---- Streams of consciousness ----
# Four streams pour forth across the black sections: each a project of
# the one hand, in its own constant color, carrying its own small
# symbols all along its length. The same color speaks everywhere the
# project appears: ribbon, project chip, card glyph.
PROJECTS = {
    # The rainbow, in order across its arc — each project one band of it,
    # each with its own symbols and no symbol shared between streams.
    "Buddhism": {
        # Vairocana, center, Buddha family. Space; dharmadhatu wisdom;
        # transforms ignorance. White light in black space — the
        # source the other four emanate from, barest of the five.
        "color": "#ffffff",   # Vairocana white
        # thin strand: the thread of all four directions, sunwise
        # (sapphire, gold, ruby, jade) — the center contains them
        "hues": ["#ffffff", "url(#dta-thread)"],
        "symbols": ["☸", "◯", "無", "空", "禪", "心", "佛", "法", "慈",
                    "悲", "定", "慧", "ॐ", "戒"],
    },
    "Smile": {
        # Ratnasambhava, south, Jewel family. Earth; wisdom of
        # equanimity; transforms pride. Gold — the open giving hand,
        # generosity and dignity; second tone gold toward the light.
        "color": "#f5c542",   # Ratnasambhava gold, quieted into the band
        # secondary: the Buddha across the center — Amoghasiddhi's
        # jade, a step quieter (the giving hand met by the fearless)
        "hues": ["#f5c542", "#4ca373"],
        "symbols": ["(-:", ":-)", "(:", ":)", ";-)", ":o)", "{ }",
                    "[= =]", "‹ ›", "(^:", "=)", "(-;", ":-P", "8-)"],
    },
    "Videogames": {
        # Amoghasiddhi, north, Karma family. Wind; all-accomplishing
        # wisdom; transforms jealousy into mastery held lightly —
        # play. Jade green (also the phosphor of the first screens);
        # second tone jade toward the light.
        "color": "#62d194",   # Amoghasiddhi jade, held in the band
        # secondary: Ratnasambhava's gold across the center, a step
        # quieter (accomplishment met by equanimity)
        "hues": ["#62d194", "#bf9a33"],
        "symbols": ["▲", "●", "✕", "■", "►", "▌▌", "★", "♥", "⬆",
                    "⬇", "⬅", "➡", "1UP", "XP"],
    },
    "Sacred Travel": {
        # Amitabha, west, Lotus family. Fire; discriminating wisdom —
        # seeing each place as this place; transforms craving. The
        # western Pure Land, destination of pilgrimage; luminous ruby
        # on the black ground; second tone ruby toward the light.
        "color": "#ff7f8d",   # Amitabha ruby, lifted into the band
        # secondary: Akshobhya's sapphire across the center, a step
        # quieter (the pilgrim's longing met by the mirror)
        "hues": ["#ff7f8d", "#577ab2"],
        "symbols": ["☥", "𓂀", "𓆣", "𓉴", "𓋹", "𓅓", "✈", "✦", "៙",
                    "៚", "𓊽", "𓁹"],
    },
    "Machine Learning": {
        # Akshobhya, east, Vajra family. Water; mirror-like wisdom —
        # a trained model reflects without holding; transforms
        # aversion. Sapphire lifted to be read on black; second tone
        # sapphire toward the light.
        "color": "#6f9ce4",   # Akshobhya sapphire, lifted into the band
        # secondary: Amitabha's ruby across the center, a step
        # quieter (clarity met by warmth and the particular)
        "hues": ["#6f9ce4", "#c7636e"],
        "symbols": ["∇", "Σ", "λ", "⊗", "∂", "θ", "ε", "σ", "π",
                    "≈", "∞", "⊕", "01", "110"],
    },
}
# No sixth seat exists to be reserved: an unknown project wears the
# center's white until it is truly seated.
THREAD = ["#6f9ce4", "#f5c542", "#ff7f8d", "#62d194"]  # sunwise

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
    course crosses the whole sky, and all ten strands — two hues per
    stream — twist around it as a single cable, evenly phased. Large
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
    # the thread of four: the sunwise cycle repeated, so any visible
    # crop of the center's thin strand carries all four directions
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

HSIN_HSIN_MING = (
    "信心銘 "
    "至道無難 唯嫌揀擇 但莫憎愛 洞然明白 毫釐有差 天地懸隔 欲得現前 莫存順逆 "
    "違順相爭 是為心病 不識玄旨 徒勞念靜 圓同太虛 無欠無餘 良由取捨 所以不如 "
    "莫逐有緣 勿住空忍 一種平懷 泯然自盡 止動歸止 止更彌動 唯滯兩邊 寧知一種 "
    "一種不通 兩處失功 遣有沒有 從空背空 多言多慮 轉不相應 絕言絕慮 無處不通 "
    "歸根得旨 隨照失宗 須臾返照 勝卻前空 前空轉變 皆由妄見 不用求真 唯須息見 "
    "二見不住 慎莫追尋 纔有是非 紛然失心 二由一有 一亦莫守 一心不生 萬法無咎 "
    "無咎無法 不生不心 能隨境滅 境逐能沈 境由能境 能由境能 欲知兩段 元是一空 "
    "一空同兩 齊含萬象 不見精麁 寧有偏黨 大道體寬 無易無難 小見狐疑 轉急轉遲 "
    "執之失度 必入邪路 放之自然 體無去住 任性合道 逍遙絕惱 繫念乖真 昏沈不好 "
    "不好勞神 何用疏親 欲取一乘 勿惡六塵 六塵不惡 還同正覺 智者無為 愚人自縛 "
    "法無異法 妄自愛著 將心用心 豈非大錯 迷生寂亂 悟無好惡 一切二邊 良由斟酌 "
    "夢幻空華 何勞把捉 得失是非 一時放卻 眼若不睡 諸夢自除 心若不異 萬法一如 "
    "一如體玄 兀爾忘緣 萬法齊觀 歸復自然 泯其所以 不可方比 止動無動 動止無止 "
    "兩既不成 一何有爾 究竟窮極 不存軌則 契心平等 所作俱息 狐疑盡淨 正信調直 "
    "一切不留 無可記憶 虛明自照 不勞心力 非思量處 識情難測 真如法界 無他無自 "
    "要急相應 唯言不二 不二皆同 無不包容 十方智者 皆入此宗 宗非促延 一念萬年 "
    "無在不在 十方目前 極小同大 忘絕境界 極大同小 不見邊表 有即是無 無即是有 "
    "若不如是 必不須守 一即一切 一切即一 但能如是 何慮不畢 信心不二 不二信心 "
    "言語道斷 非去來今")

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
                boxes += (f'<label class="sub-choice child-choice">'
                          f'<input type="checkbox" name="tag" '
                          f'value="{slugify(ch)}" checked> {ch} '
                          f'<span class="choice-note">the Smile Prompt '
                          f'Language and Smile Chat</span></label>')
    return (f'<details class="interests" id="{idp}-interests">'
            f'<summary>Choose which projects you receive</summary>'
            f'<div class="interest-grid">{boxes}</div></details>')

def signup_form(idp, button_text):
    return (f'<form class="signup" id="{idp}" method="post" '
            f'action="{MAILING_ENDPOINT or "#"}" data-signup>'
            f'<input type="text" name="metadata-name" placeholder="Name" '
            f'aria-label="Name">'
            f'<input type="email" name="email" placeholder="Email" aria-label="Email" required>'
            f'{dropdown(idp)}'
            f'<button type="submit" class="btn">{button_text}</button>'
            f'<p class="reassure">We\'ll never share your info with anyone.</p></form>')

def header():
    nav = "".join(f'<a href="{c["slug"]}.html">{cat}</a>'
                  for cat, c in CATEGORIES.items())
    return (f'<header class="top"><a class="brand" href="index.html">'
            f'<span class="brand-mark">(-:</span> {SITE_NAME}</a>'
            f'<nav>{nav}</nav>'
            f'<button class="btn btn-small" type="button" data-open-popup>'
            f'Join the List</button></header>')

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
    projects = "".join(
        f'<a class="ptx-shadow" style="--pc:{st["color"]}" '
        f'href="index.html">{name}</a>'
        for name, st in PROJECTS.items())
    cols += f'<div><h3>Projects</h3>{projects}</div>'
    cols += ('<div><h3>Site</h3><a href="index.html">Home</a>'
             '<a href="https://crystallizationculture.com">'
             'Crystallization Culture</a></div>')
    return (f'<footer class="deep">{WAVE}<div class="foot-inner">{FOOT_SVG[0]}'
            f'<div class="foot-cta">'
            f'<div><p class="eyebrow" '
            f'style="color:{PROJECTS["Smile"]["color"]}">The mailing list</p>'
            f'<h2>New posts arrive by email.</h2>'
            f'<p>Join once, choose your projects, and each new piece is sent '
            f'when it is published.</p>'
            f'<button class="btn" type="button" data-open-popup>'
            f'Join the Mailing List</button></div>'
            f'<div class="foot-cta-art" aria-hidden="true">(-:</div></div>'
            f'<div class="foot-grid">{cols}</div>'
            f'<div class="foot-close">'
            f'<img class="buddha-eyes" src="assets/buddha_eyes.png" '
            f'alt="Buddha eyes">'
            f'<div class="hhm notranslate" translate="no" lang="zh" '
            f'aria-label="Hsin Hsin Ming, '
            f'the original Chinese">{HSIN_HSIN_MING}</div>'
            f'</div></div>'
            f'<div class="foot-legal">&copy; 2026 {SITE_NAME}. May this '
            f'writing benefit all beings.</div></footer>')

def popup():
    return (f'<div class="popup-veil" id="popup" hidden><div class="popup-card">'
            f'<button class="popup-close" id="popup-close" aria-label="Close">&times;</button>'
            f'<div class="popup-art" aria-hidden="true"><span>(-:</span></div>'
            f'<div class="popup-body"><h2>Join the mailing list.</h2>'
            f'{signup_form("popup-form", "Join")}'
            f'</div></div></div>')

def page(title, body, desc=TAGLINE):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{title}</title><meta name="description" content="{desc}">'
            f'<meta name="google" content="notranslate">'
            f'<link rel="stylesheet" href="assets/base.css">'
            f'<link rel="stylesheet" href="assets/themes.css">'
            f'</head><body class="theme-ink">{header()}{body}{footer()}{popup()}'
            f'<script src="assets/site.js"></script></body></html>')

def card(p):
    proj = p.get("project", SITE_NAME)
    return (f'<a class="card" href="{p["slug"]}.html">'
            f'<div class="card-art" aria-hidden="true" style="color:'
            f'{deep(project_color(proj))}">'
            f'<span>{p.get("glyph","☀")}</span></div>'
            f'<h3 class="ptx-shadow" style="--pc:{shadow_color(proj)}">'
            f'{p["title"]}</h3><p>{p["description"]}</p></a>')

def hero(title_html, sub_text, form_id, svg=""):
    return (f'<section class="hero">{svg}<div class="hero-inner"><div class="hero-copy">'
            f'<h1>{title_html}</h1><p class="hero-sub">{sub_text}</p>'
            f'<button class="btn btn-hero" type="button" data-open-popup>'
            f'Join the Mailing List</button></div>'
            f'<div class="hero-art" aria-hidden="true"><span>(-:</span></div>'
            f'</div><div class="ornament" aria-hidden="true">(:☸:)</div>'
            f'{WAVE}</section>')

def index_body(posts, svg_fn=None):
    """The Swim University anatomy, worn by this site's own content:
    hero -> trust band -> feature + four cards -> dark mid band ->
    Articles grid. (Footer and popup arrive through page().)"""
    svg_fn = svg_fn or stream_svg
    n_symbols = sum(len(p["symbols"]) for p in PROJECTS.values())
    stats = [
        ("☸", "5", "Writing Projects"),
        ("✎", str(len(posts)), "Pieces of Writing"),
        ("✳", str(n_symbols), "Symbols in the Weave"),
        ("(-:", "1", "Author"),
    ]
    trust = ('<section class="trust"><h2>What Is Here</h2>'
             '<div class="trust-grid">'
             + "".join(
                 f'<div><div class="stat-num"><span class="stat-ico">{ico}'
                 f'</span>{num}</div><div class="stat-label">{lab}</div></div>'
                 for ico, num, lab in stats)
             + '</div></section>')
    # feature — the Smile Prompt Language, spoken as Smile speaks
    collage = "".join(
        f'<span style="color:{deep(st["color"])}">{s}</span>'
        for st in PROJECTS.values() for s in st["symbols"][:6])
    smile_post = next((p for p in posts if p.get("project") == "Smile"), None)
    feature = (
        f'<section class="feature"><div class="feature-art" aria-hidden="true">'
        f'{collage}</div><div class="feature-copy">'
        f'<p class="eyebrow">The Smile Prompt Language</p>'
        f'<h2>A prompt language written in emoticons.</h2>'
        f'<p>Smile is a prompt language for speaking with language models. '
        f'It is developed here, alongside Smile Chat, the local '
        f'conversation rig it runs in. Posts document the language as it '
        f'develops.</p>'
        + (f'<a class="btn" href="{smile_post["slug"]}.html">'
           f'Read About Smile</a>' if smile_post else '')
        + '</div></section>')
    featured = []
    seen_subs = set()
    for p in posts:
        if p["pill"] not in seen_subs:
            featured.append(p)
            seen_subs.add(p["pill"])
        if len(featured) == 4:
            break
    feature_cards = ('<div class="grid grid-4">'
                     + "".join(card(p) for p in featured) + '</div>')
    # dark mid band — Smile's own list, on this same engine
    midband = (
        f'<section class="midband">{WAVE.replace("wave", "wave wave-top", 1)}'
        f'{svg_fn(h=260)}'
        f'<div class="midband-inner"><div class="midband-copy">'
        f'<p class="eyebrow" style="color:{PROJECTS["Smile"]["color"]}">'
        f'The Smile mailing list</p>'
        f'<h2>Smile has its own sub-mailing-list.</h2>'
        f'<p>It runs on this same mailing engine. Choose Smile when you '
        f'join and Smile posts arrive on their own.</p>'
        f'<button class="btn" type="button" data-open-popup>'
        f'Join the Smile List</button></div>'
        f'<div class="midband-art" aria-hidden="true"><span>(-:</span></div>'
        f'</div>{WAVE}</section>')
    # Articles — heading left, see-all right, three-column grid
    cat_links = " or ".join(f'<a href="{c["slug"]}.html">{cat}</a>'
                            for cat, c in CATEGORIES.items())
    articles = (f'<section class="band"><div class="band-head">'
                f'<h2>Articles</h2><span class="see-in">See all in '
                f'{cat_links}</span></div>'
                f'<div class="grid">'
                + "".join(card(p) for p in posts[:6]) + '</div></section>')
    return (hero("The Writing of<br>Dr Thomas Ager",
                 "Buddhism, Smile, Videogames, Sacred Travel, and Machine "
                 "Learning. New posts go out by email when they are "
                 "written.", "hero-form",
                 svg_fn(h=320))
            + trust
            + f'<main>{feature}{feature_cards}</main>'
            + midband
            + f'<main>{articles}</main>')

def build_index(posts):
    (SITE / "index.html").write_text(
        page(f"{SITE_NAME} — {TAGLINE}", index_body(posts)), encoding="utf-8")

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
        body = (f'<section class="hero hero-lite">'
                f'{stream_svg(h=180)}'
                f'<div class="hero-inner">'
                f'<div class="hero-copy"><h1>{cat}</h1>'
                f'<p class="hero-sub">{c["blurb"]}</p></div></div>{WAVE}</section>'
                f'<main>{secs}</main>')
        (SITE / f'{c["slug"]}.html').write_text(
            page(f"{cat} — {SITE_NAME}", body, c["blurb"]), encoding="utf-8")

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
        cards = "".join(card(p) for p in items)
        body = (f'<section class="hero hero-lite">'
                f'{stream_svg(h=180)}'
                f'<div class="hero-inner">'
                f'<div class="hero-copy"><h1>{name}</h1>'
                f'<p class="hero-sub">{blurb}</p></div></div>{WAVE}</section>'
                f'<main><section class="band">'
                f'<div class="grid">{cards}</div></section></main>')
        (SITE / f'{slugify(name)}.html').write_text(
            page(f"{name} — {SITE_NAME}", body, blurb or TAGLINE),
            encoding="utf-8")
    return len(pages)

def build_posts(posts):
    for p in posts:
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
            f'<div class="byline"><span class="avatar" aria-hidden="true">TA</span>'
            f'<strong>{SITE_NAME}</strong><span class="dot">|</span>'
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
            f'aria-hidden="true">TA</span><div><h2>{SITE_NAME}</h2>'
            f'<p>Dr Thomas Ager holds a Ph.D in Artificial Intelligence and '
            f'writes on prompt engineering and spirituality. His current '
            f'research is the Smile Prompt Language.</p></div></div>'
            f'<section class="band"><div class="band-head"><h2>More Reading</h2>'
            f'<span class="see-in">See more in '
            f'<a href="{slugify(p["pill"])}.html">{p["pill"]}</a></span></div>'
            f'<div class="grid">{more_html}</div></section></main>')
        (SITE / f'{p["slug"]}.html').write_text(
            page(f'{p["title"]} — {SITE_NAME}', body, p["description"]),
            encoding="utf-8")

FOOT_SVG = [""]

def main():
    SITE.mkdir(exist_ok=True)
    out_assets = SITE / "assets"
    if out_assets.exists():
        shutil.rmtree(out_assets)
    shutil.copytree(ASSETS, out_assets)
    posts = load_posts()
    FOOT_SVG[0] = stream_svg(h=280)
    build_index(posts)
    build_categories(posts)
    n_subs = build_subcategories(posts)
    build_posts(posts)
    print(f"Built {1 + len(CATEGORIES) + n_subs + len(posts)} "
          f"pages into {SITE}")

if __name__ == "__main__":
    main()
