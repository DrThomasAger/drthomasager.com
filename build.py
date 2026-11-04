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
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))  # smilecompose sits beside this file, also when another build loads it
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



SONG_PARTS = ("STYLE", "LYRICS", "SOURCES", "COUNT")


def song_html(body):
    """A Suno song's reply (STYLE, LYRICS, SOURCES, COUNT, each on a line of
    its own) with its line breaks kept and the style and lyrics ready to copy.
    Returns None for any other body."""
    import html as _h
    lines = body.splitlines()
    marks = [i for i, l in enumerate(lines) if l.strip() in SONG_PARTS]
    if not any(lines[i].strip() == "LYRICS" for i in marks):
        return None
    head = "\n".join(lines[:marks[0]]).strip()
    out = [md_lite(head)] if head else []
    names = {"STYLE": "Style", "LYRICS": "Lyrics", "SOURCES": "Sources", "COUNT": "Count"}
    for n, i in enumerate(marks):
        part = lines[i].strip()
        text = "\n".join(lines[i + 1:(marks[n + 1] if n + 1 < len(marks) else len(lines))]).strip("\n")
        copy = (f' <button class="btn copy" type="button" data-copy="{part.lower()}">Copy {names[part].lower()} for Suno</button>'
                if part in ("STYLE", "LYRICS") else "")
        size = f' <span class="note">{len(text):,} characters</span>' if part in ("STYLE", "LYRICS") else ""
        out.append(f'<h2>{names[part]}{size}{copy}</h2><pre class="song" id="song-{part.lower()}">{_h.escape(text)}</pre>')
    return "\n".join(out)

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
SITE_CONF = read_json(ROOT / "site.json", {}) if (ROOT / "site.json").exists() else {}
FORMATS = read_json(ROOT / "formats.json", {"formats": []}) if (ROOT / "formats.json").exists() else {"formats": []}


def stable_id(prefix, *parts):
    import hashlib
    return prefix + hashlib.sha1("|".join(str(p or "") for p in parts).encode("utf-8")).hexdigest()[:8]


def give_ids(events, people):
    for e in events:
        e.setdefault("id", stable_id("ev", e.get("date"), e.get("event")))
    for p in people:
        p.setdefault("id", stable_id("p", p.get("name")))


def apply_edits(data, edits):
    """Overlay hand edits (edits.json) on the merged datasets. data is a dict of
    dataset name -> list of records with ids, plus 'meta' -> dict."""
    for ds in ("quotes", "items", "events", "people"):
        e = edits.get(ds) or {}
        recs = data.get(ds, [])
        removed = set(e.get("remove") or [])
        recs = [r for r in recs if r.get("id") not in removed]
        upd = e.get("update") or {}
        for r in recs:
            if r.get("id") in upd:
                r.update(upd[r["id"]])
                r["edited"] = True
        have = {r.get("id") for r in recs}
        for a in e.get("add") or []:
            if a.get("id") and a["id"] not in have:
                a = dict(a); a["added"] = True
                recs.append(a)
        data[ds] = recs
    for k, v in (edits.get("meta") or {}).items():
        data["meta"][k] = v
    return data


def front_matter(text):
    """Split '---\nkey: value\n---\nbody' into (dict, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 4:].lstrip("\n")


def edit_url(slug, filename, new=False):
    repo, branch, prefix = SITE_CONF.get("repo", ""), SITE_CONF.get("branch", "main"), SITE_CONF.get("prefix", "")
    if not repo:
        return ""
    kind = "new" if new else "edit"
    return f"https://github.com/{repo}/{kind}/{branch}/{prefix}teachers/{slug}/{filename}"
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
    give_ids(events, people)
    edits = read_json(folder / "edits.json", {})
    edited = apply_edits({"quotes": quotes, "items": items, "events": events, "people": people, "meta": meta}, edits)
    quotes, items, events, people, meta = edited["quotes"], edited["items"], edited["events"], edited["people"], edited["meta"]
    n_edits = sum(len((edits.get(ds) or {}).get(k) or []) for ds in ("quotes", "items", "events", "people") for k in ("update", "add", "remove")) + len(edits.get("meta") or {})
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
        html = (html.replace("__ID__", esc(q["id"])).replace("__SLUG__", esc(slug)).replace("__TEXT__", esc(q["text"])).replace("__TEXT_SHORT__", esc(q["text"][:150]))
                    .replace("__TEXT_JSON__", json.dumps(q["text"]))
                    .replace("__BOOK__", esc(q.get("book") or "unassigned")).replace("__CHAPTER__", (", " + esc(q["chapter"])) if q.get("chapter") else "")
                    .replace("__PILLS__", pills)
                    .replace("__NOTE__", f'<p class="note">{esc(q["note"])}</p>' if q.get("note") else "")
                    .replace("__SOURCES__", "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></li>' for u in q.get("sources") or []) or "<li>No source recorded.</li>")
                    .replace("__INSTAGRAM_BTN__", f'<a class="btn primary" href="{insta_url}" target="_blank" rel="noopener">@{esc(insta)} on Instagram</a>' if insta else "")
                    .replace("__PREV__", f'<a href="../{prev_q["id"]}/">← previous</a>' if prev_q else "")
                    .replace("__NEXT__", f'<a href="../{next_q["id"]}/">next →</a>' if next_q else ""))
        (d / "index.html").write_text(html, encoding="utf-8")

    for n, d in (("items.json", items), ("quotes.json", quotes), ("events.json", events), ("people.json", people), ("meta.json", {k: v for k, v in meta.items() if k != "events"})):
        (out / n).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    for n in ("integrity.json", "download-manifest.json", "fetch.sh", "LICENSE", "edits.json"):
        if (folder / n).exists():
            shutil.copy(folder / n, out / n)
    shutil.copy(ROOT / "formats.json", out / "formats.json") if (ROOT / "formats.json").exists() else None

    # compose and edit pages
    tool_data = embed({"quotes": quotes, "items": items, "events": events, "people": people,
                       "meta": {k: v for k, v in meta.items() if k != "events"}, "edits": edits, "formats": FORMATS,
                       "site": SITE_CONF, "slug": slug,
                       "edit_urls": {"edits": edit_url(slug, "edits.json"), "compositions_new": edit_url(slug, "compositions", new=True),
                                     "formats": (f"https://github.com/{SITE_CONF.get('repo')}/edit/{SITE_CONF.get('branch','main')}/{SITE_CONF.get('prefix','')}formats.json" if SITE_CONF.get("repo") else ""),
                                     "posts_new": (f"https://github.com/{SITE_CONF.get('posts_repo')}/new/{SITE_CONF.get('branch','main')}/{SITE_CONF.get('posts_path','posts')}" if SITE_CONF.get("posts_repo") else "")}})
    import smilecompose
    compose_data = embed({"quotes": quotes, "meta": {k: v for k, v in meta.items() if k != "events"}, "formats": FORMATS, "texts": smilecompose.module_texts(), "edits": edits,
                          "site": SITE_CONF, "slug": slug, "edit_urls": json.loads(tool_data.replace("<\\/", "</"))["edit_urls"]})
    for page, tname, payload in (("compose", "compose.html", compose_data), ("edit", "editor.html", tool_data)):
        tp = TPL / tname
        if tp.exists():
            html = tp.read_text(encoding="utf-8").replace("/*__TOOL_DATA__*/", payload)
            for k, v in common.items():
                html = html.replace(k, v)
            d = out / page; d.mkdir(exist_ok=True)
            (d / "index.html").write_text(html, encoding="utf-8")

    # compositions: teachers/<slug>/compositions/*.md -> compositions/<name>/
    comps = []
    ctpl = (TPL / "composition.html").read_text(encoding="utf-8") if (TPL / "composition.html").exists() else ""
    for f in sorted((folder / "compositions").glob("*.md")) if (folder / "compositions").is_dir() else []:
        fm, body = front_matter(f.read_text(encoding="utf-8"))
        cname = f.stem
        title = fm.get("title") or cname.replace("-", " ")
        first = body.lstrip().splitlines()[0] if body.strip() else ""
        if first.lstrip("# ").strip() == title.strip():
            body = body.lstrip()[len(first):].lstrip("\n")
        comps.append({"name": cname, "title": title, "format": fm.get("format", ""), "topic": fm.get("topic", ""), "date": fm.get("date", ""), "model": fm.get("model", "")})
        if ctpl:
            html = ctpl
            for k, v in common.items():
                html = html.replace(k, v)
            html = (html.replace("__TITLE__", esc(title)).replace("__BODY__", song_html(body) or md_lite(body))
                        .replace("__FMT__", esc(fm.get("format", ""))).replace("__TOPIC__", esc(fm.get("topic", "")))
                        .replace("__DATE__", esc(fm.get("date", ""))).replace("__MODEL__", esc(fm.get("model", "")))
                        .replace("__EDIT__", edit_url(slug, f"compositions/{f.name}")))
            d = out / "compositions" / cname; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(html, encoding="utf-8")
            shutil.copy(f, d / f.name)
    for md in folder.glob("*.md"):
        shutil.copy(md, out / md.name)
    if (folder / "catalogue").is_dir():
        shutil.copytree(folder / "catalogue", out / "catalogue", dirs_exist_ok=True)
    # home
    htpl = (TPL / "home.html").read_text(encoding="utf-8")
    counts = {m: sum(1 for i in items if i.get("medium") == m) for m in ("video", "audio", "text", "image", "archive", "community")}
    doors = [("quotes/", "Quotes", len(quotes), "his words" if meta.get("pronoun", "their") == "his" else "their words, by source"),
             ("archive/", "Archive", len(items), "video, audio, text, image, archive, community"),
             ("timeline/", "Life", len(events) or len(meta["events"]), "dated events with sources"),
             ("people/", "People", len(people), "everyone in the record"),
             ("copyright/", "Copyright", "", "their position on their words"),
             ("sources/", "Sources", "", "every cited URL, by host"),
             ("about/", "About", "", "how this was gathered"),
             ("compose/", "Compose", "", "recompose the words into a song, a book, a post"),
             ("edit/", "Edit", n_edits or "", "change any record; the site applies it")]
    doors_html = "".join(f'<a class="door" href="{h}"><b>{t}</b><span class="n">{n}</span><span>{d}</span></a>' for h, t, n, d in doors)
    def clean_note(q):
        n = (q.get("note") or "").lower()
        return not any(w in n for w in ("bhatt", "editor", "not u.g.", "not ug", "publisher", "narrat", "reported speech", "disputed", "not found", "jiddu", "paraphrase", "foreword", "not roberts", "not her", "interviewer", "reviewer", "preamble"))
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
                .replace("__COMPOSITIONS__", ("<h2>Compositions</h2><div class=\"quotes\">" + "".join(f'<a class="q" href="compositions/{c["name"]}/"><blockquote>{esc(c["title"])}</blockquote><div class="meta"><span>{esc(c["format"])}</span><span>{esc(c["topic"])}</span><span>{esc(c["date"])}</span></div></a>' for c in comps) + "</div>") if comps else "")
                .replace("__INSTAGRAM_FOOT__", f'Daily quotes at <a href="{insta_url}" target="_blank" rel="noopener">@{esc(insta)}</a>.' if insta else ""))
    (out / "index.html").write_text(html, encoding="utf-8")

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
