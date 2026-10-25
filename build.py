"""Build hanjopurebuddha.com into site/.

    python3 build.py

Reads every teacher folder under teachers/<slug>/ and renders:
  site/index.html                 the guru browsing grid
  site/gurus/<slug>/index.html    that teacher's archive viewer, data embedded
  site/gurus/<slug>/items.json    the raw data, for anyone who wants it
  site/gurus/<slug>/quotes.json
  site/gurus/<slug>/meta.json

A teacher folder holds:
  meta.json       name, dates, places, one-line, portrait, copyright statement,
                  confidence legend; see teachers/ug-krishnamurti/meta.json
  items.json      the media catalogue (video, audio, text, image, archive, community)
  quotes.json     the quotes, each with book, chapter, confidence, sources
  timeline.md     a markdown table | Date | Event | Place | of life events
  *.md            any prose files, copied through as-is
  catalogue/      the researchers' full reports, copied through as-is
"""
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
TEACHERS = ROOT / "teachers"
SITE = ROOT / "site"
TPL = ROOT / "templates"


def read_json(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def read_events(p):
    events = []
    if not p.exists():
        return events
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and not line.startswith("| Date") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3:
                events.append({"date": cells[0], "event": cells[1], "place": cells[2]})
    return events


def md_lite(text):
    """A small markdown-to-HTML for the prose files: headings, paragraphs,
    lists, blockquotes, tables, links, emphasis, code."""
    import html as _h
    out, para, lst, quote, table = [], [], None, [], []
    def inline(s):
        s = _h.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"(?<![\"'>=])(https?://[^\s<)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
        return s
    def flush():
        nonlocal para, lst, quote, table
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in lst) + "</ul>"); lst = None
        if quote: out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>"); quote = []
        if table:
            rows = [r for r in table if not re.match(r"^\|?\s*-", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if cells:
                head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
                body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
                out.append(f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            table = []
    for line in text.splitlines():
        if line.startswith("#"):
            flush(); level = min(len(line) - len(line.lstrip("#")), 3); out.append(f"<h{max(level,2)}>{inline(line.lstrip('#').strip())}</h{max(level,2)}>")
        elif line.startswith("|"):
            if para or lst or quote: flush()
            table.append(line)
        elif line.startswith(">"):
            if para or lst or table: flush()
            quote.append(line.lstrip(">").strip())
        elif re.match(r"^\s*[-*] ", line):
            if para or quote or table: flush()
            lst = (lst or []) + [re.sub(r"^\s*[-*] ", "", line)]
        elif not line.strip():
            flush()
        else:
            if lst is not None and line.startswith("  "):
                lst[-1] += " " + line.strip()
            elif quote and not para:
                quote.append(line.strip())
            else:
                if lst or quote or table: flush()
                para.append(line.strip())
    flush()
    return "\n".join(out)


def teacher_style(meta):
    acc = meta.get("accent"); acc_dark = meta.get("accent_dark") or acc
    css = ""
    if acc:
        css += f":root {{ --accent: {acc_dark}; }} @media (prefers-color-scheme: dark) {{ :root:not([data-theme=\"light\"]) {{ --accent: {acc}; }} }} :root[data-theme=\"dark\"] {{ --accent: {acc}; }}"
    if meta.get("display_font"):
        css += f" :root {{ --display: \"{meta['display_font']}\", Georgia, serif; }}"
    return css


def font_link(meta):
    f = meta.get("display_font")
    if not f:
        return ""
    fam = f.replace(" ", "+")
    return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}:ital,wght@0,400;0,500;0,600;1,400&display=swap">'


def embed(payload):
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


SECTIONS = ["archive", "quotes", "timeline", "people", "copyright", "sources", "about"]
VERDICT_RANK = {"corroborated-primary": 0, "corroborated-secondary": 1, "primary-source": 2, "multi-source": 3, "single-source": 4, "disputed": 6, "not-found": 7, "not-ug": 9}


def esc(s):
    import html as _h
    return _h.escape(str(s if s is not None else ""))


def build_teacher(folder, out_root=None):
    """Render one teacher as a small site under <out_root>/<slug>/:
    index.html (home), <section>/index.html for each section of the browser,
    quotes/<id>/index.html for every quote, plus the data files."""
    out_root = out_root or (SITE / "gurus")
    slug = folder.name
    meta = read_json(folder / "meta.json", {})
    items = read_json(folder / "items.json", [])
    quotes = read_json(folder / "quotes.json", [])
    meta["events"] = read_events(folder / "timeline.md")
    events = read_json(folder / "events.json", [])
    people = read_json(folder / "people.json", [])
    integrity = read_json(folder / "integrity.json", {})
    if integrity:
        integrity = {"summary": integrity.get("summary", {})}
    meta["slug"] = slug
    out = out_root / slug
    out.mkdir(parents=True, exist_ok=True)
    name, dates, one = meta.get("name", slug), meta.get("dates", ""), meta.get("one_line", "")
    insta = (meta.get("instagram") or "").strip().lstrip("@")
    insta_url = f"https://www.instagram.com/{insta}/" if insta else ""
    cv = folder / "copyright-view.md"
    copyright_html = md_lite(cv.read_text(encoding="utf-8")) if cv.exists() else "<p>No statement recorded yet.</p>"
    common = {"__NAME__": name, "__DATES__": dates, "__ONELINE__": one, "__FONT_LINK__": font_link(meta), "/*__TEACHER_STYLE__*/": teacher_style(meta)}

    # section pages
    tpl = (TPL / "teacher.html").read_text(encoding="utf-8")
    data = embed({"items": items, "quotes": quotes, "meta": meta, "events": events, "people": people, "integrity": integrity})
    for sec in SECTIONS:
        html = tpl.replace("/*__DATA__*/", data).replace("__COPYRIGHT_HTML__", copyright_html).replace("__INITIAL_TAB__", sec)
        for k, v in common.items():
            html = html.replace(k, v)
        d = out / sec; d.mkdir(exist_ok=True)
        (d / "index.html").write_text(html, encoding="utf-8")

    # quote pages
    qtpl = (TPL / "quote.html").read_text(encoding="utf-8")
    ordered = sorted(quotes, key=lambda q: (VERDICT_RANK.get(q.get("verdict"), 5), q.get("book") or "", q.get("id")))
    for i, q in enumerate(ordered):
        d = out / "quotes" / q["id"]; d.mkdir(parents=True, exist_ok=True)
        v = q.get("verdict") or ""
        cls = "good" if v.startswith("corroborated-primary") else "ok" if v in ("corroborated-secondary", "primary-source") else "warn" if v in ("multi-source", "single-source") else "bad"
        pills = f'<span class="pill {cls}">{esc(v)}</span><span class="pill">{esc(q.get("kind") or "verbatim")}</span><span class="pill">confidence {esc(q.get("confidence"))}</span>' + (f'<span>{esc(q.get("year"))}</span>' if q.get("year") else "")
        prev_q = ordered[i - 1] if i > 0 else None
        next_q = ordered[i + 1] if i + 1 < len(ordered) else None
        html = qtpl
        for k, v2 in common.items():
            html = html.replace(k, v2)
        html = (html.replace("__TEXT__", esc(q["text"])).replace("__TEXT_SHORT__", esc(q["text"][:150]))
                    .replace("__TEXT_JSON__", json.dumps(q["text"]))
                    .replace("__BOOK__", esc(q.get("book") or "unassigned")).replace("__CHAPTER__", (", " + esc(q["chapter"])) if q.get("chapter") else "")
                    .replace("__PILLS__", pills)
                    .replace("__NOTE__", f'<p class="note">{esc(q["note"])}</p>' if q.get("note") else "")
                    .replace("__SOURCES__", "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></li>' for u in q.get("sources") or []) or "<li>No source recorded.</li>")
                    .replace("__INSTAGRAM_BTN__", f'<a class="btn primary" href="{insta_url}" target="_blank" rel="noopener">@{esc(insta)} on Instagram</a>' if insta else "")
                    .replace("__PREV__", f'<a href="../{prev_q["id"]}/">← previous</a>' if prev_q else "")
                    .replace("__NEXT__", f'<a href="../{next_q["id"]}/">next →</a>' if next_q else ""))
        (d / "index.html").write_text(html, encoding="utf-8")

    # home
    htpl = (TPL / "home.html").read_text(encoding="utf-8")
    counts = {m: sum(1 for i in items if i.get("medium") == m) for m in ("video", "audio", "text", "image", "archive", "community")}
    doors = [("quotes/", "Quotes", len(quotes), "his words" if meta.get("pronoun", "their") == "his" else "their words, by source"),
             ("archive/", "Archive", len(items), "video, audio, text, image, archive, community"),
             ("timeline/", "Life", len(events) or len(meta["events"]), "dated events with sources"),
             ("people/", "People", len(people), "everyone in the record"),
             ("copyright/", "Copyright", "", "their position on their words"),
             ("sources/", "Sources", "", "every cited URL, by host"),
             ("about/", "About", "", "how this was gathered")]
    doors_html = "".join(f'<a class="door" href="{h}"><b>{t}</b><span class="n">{n}</span><span>{d}</span></a>' for h, t, n, d in doors)
    def clean_note(q):
        n = (q.get("note") or "").lower()
        return not any(w in n for w in ("bhatt", "editor", "not u.g.", "not ug", "publisher", "narrat", "reported speech", "disputed", "not found", "jiddu", "paraphrase"))
    featured = [q for q in ordered if 60 <= len(q["text"]) <= 260 and q.get("kind", "verbatim") == "verbatim" and clean_note(q)][:6] or ordered[:6]
    feat_html = "".join(f'<a class="q" href="quotes/{q["id"]}/"><blockquote>{esc(q["text"])}</blockquote><div class="meta"><span>{esc(q.get("book") or "")}</span><span class="pill">{esc(q.get("verdict") or "")}</span></div></a>' for q in featured)
    evs = [{"date": e.get("date"), "event": e.get("event"), "place": e.get("place")} for e in (events or meta["events"])][:10]
    ev_html = "".join(f'<div class="event"><div class="when">{esc(e["date"])}</div><p>{esc(e["event"])}</p><div class="when">{esc(e["place"])}</div></div>' for e in evs)
    lead_q = meta.get("lead_quote") or (featured[0]["text"] if featured else "")
    lead_src = meta.get("lead_quote_source") or (featured[0].get("book") if (not meta.get("lead_quote") and featured) else "")
    statement = f'<blockquote class="statement">{esc(lead_q)}<span class="src">{esc(lead_src)}</span></blockquote>' if lead_q else ""
    portrait = f'<figure class="portrait"><img src="{esc(meta["portrait"])}" alt="{esc(name)}" loading="lazy"><figcaption class="credit">{esc(meta.get("portrait_credit") or "")}</figcaption></figure>' if meta.get("portrait") else ""
    html = htpl
    for k, v in common.items():
        html = html.replace(k, v)
    html = (html.replace("__BORN__", esc(meta.get("born") or "")).replace("__DIED__", esc(meta.get("died") or ""))
                .replace("__STATEMENT__", statement).replace("__PORTRAIT__", portrait).replace("__DOORS__", doors_html)
                .replace("__FEATURED__", feat_html or "<p>Quotes are being gathered.</p>").replace("__EVENTS__", ev_html or "<p>The chronology is being gathered.</p>")
                .replace("__INSTAGRAM_BTN__", f'<a class="btn primary" href="{insta_url}" target="_blank" rel="noopener">@{esc(insta)} on Instagram</a>' if insta else "")
                .replace("__INSTAGRAM_FOOT__", f'Daily quotes at <a href="{insta_url}" target="_blank" rel="noopener">@{esc(insta)}</a>.' if insta else ""))
    (out / "index.html").write_text(html, encoding="utf-8")

    for n in ("items.json", "quotes.json", "meta.json", "events.json", "people.json", "integrity.json", "download-manifest.json", "fetch.sh", "LICENSE"):
        if (folder / n).exists():
            shutil.copy(folder / n, out / n)
    for md in folder.glob("*.md"):
        shutil.copy(md, out / md.name)
    if (folder / "catalogue").is_dir():
        shutil.copytree(folder / "catalogue", out / "catalogue", dirs_exist_ok=True)
    return {"slug": slug, "meta": {k: v for k, v in meta.items() if k != "events"}, "counts": counts, "items": len(items), "quotes": len(quotes), "people": len(people), "events": len(events) or len(meta["events"]), "pages": 1 + len(SECTIONS) + len(quotes)}


def build_index(cards, out_path=None, prefix="gurus/"):
    """Render the guru grid. prefix is the path from the index to the teacher
    folders ("gurus/" when the index sits at the site root, "" when the index
    sits inside the gurus folder itself)."""
    out_path = out_path or (SITE / "index.html")
    tpl = (TPL / "index.html").read_text(encoding="utf-8")
    html = tpl.replace("/*__CARDS__*/", embed(cards)).replace("__PREFIX__", prefix)
    out_path.write_text(html, encoding="utf-8")


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / ".nojekyll").write_text("")
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", SITE / "CNAME")
    cards = []
    for folder in sorted(p for p in TEACHERS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        card = build_teacher(folder)
        cards.append(card)
        print(f"{card['slug']}: {card['items']} items, {card['quotes']} quotes, {card['pages']} pages")
    build_index(cards)
    base = "https://hanjopurebuddha.com"
    urls = [f"{base}/"]
    for f in sorted(SITE.rglob("index.html")):
        rel = f.parent.relative_to(SITE).as_posix()
        if rel != ".":
            urls.append(f"{base}/{rel}/")
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    print(f"-> {SITE} ({len(urls)} urls)")


if __name__ == "__main__":
    main()
