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


def build_teacher(folder, out_root=None):
    """Render one teacher into <out_root>/<slug>/ (default: site/gurus/)."""
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
    tpl = (TPL / "teacher.html").read_text(encoding="utf-8")
    cv = folder / "copyright-view.md"
    copyright_html = md_lite(cv.read_text(encoding="utf-8")) if cv.exists() else "<p>No statement recorded yet.</p>"
    html = (tpl.replace("/*__DATA__*/", embed({"items": items, "quotes": quotes, "meta": meta, "events": events, "people": people, "integrity": integrity}))
               .replace("__COPYRIGHT_HTML__", copyright_html)
               .replace("/*__TEACHER_STYLE__*/", teacher_style(meta))
               .replace("__FONT_LINK__", font_link(meta))
               .replace("__NAME__", meta.get("name", slug))
               .replace("__DATES__", meta.get("dates", ""))
               .replace("__ONELINE__", meta.get("one_line", "")))
    (out / "index.html").write_text(html, encoding="utf-8")
    for name in ("items.json", "quotes.json", "meta.json", "events.json", "people.json", "integrity.json", "download-manifest.json", "fetch.sh", "LICENSE"):
        if (folder / name).exists():
            shutil.copy(folder / name, out / name)
    for md in folder.glob("*.md"):
        shutil.copy(md, out / md.name)
    if (folder / "catalogue").is_dir():
        shutil.copytree(folder / "catalogue", out / "catalogue", dirs_exist_ok=True)
    counts = {m: sum(1 for i in items if i.get("medium") == m)
              for m in ("video", "audio", "text", "image", "archive", "community")}
    return {"slug": slug, "meta": meta, "counts": counts, "items": len(items), "quotes": len(quotes), "people": len(people), "events": len(events) or len(meta["events"])}


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
        print(f"{card['slug']}: {card['items']} items, {card['quotes']} quotes")
    build_index(cards)
    print(f"-> {SITE}")


if __name__ == "__main__":
    main()
