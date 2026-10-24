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
    html = (tpl.replace("/*__DATA__*/", embed({"items": items, "quotes": quotes, "meta": meta, "events": events, "people": people, "integrity": integrity}))
               .replace("__NAME__", meta.get("name", slug))
               .replace("__DATES__", meta.get("dates", ""))
               .replace("__ONELINE__", meta.get("one_line", "")))
    (out / "index.html").write_text(html, encoding="utf-8")
    for name in ("items.json", "quotes.json", "meta.json", "events.json", "people.json", "integrity.json"):
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
    for folder in sorted(p for p in TEACHERS.iterdir() if p.is_dir()):
        card = build_teacher(folder)
        cards.append(card)
        print(f"{card['slug']}: {card['items']} items, {card['quotes']} quotes")
    build_index(cards)
    print(f"-> {SITE}")


if __name__ == "__main__":
    main()
