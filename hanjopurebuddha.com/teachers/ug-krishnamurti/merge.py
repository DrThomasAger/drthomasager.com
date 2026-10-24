"""Merge researcher JSON files into items.json and quotes.json.

Usage: python3 merge.py <dir-with-json-files>
Reads every *.json in the directory. Files named quotes*.json are quote
lists; everything else is an item list. Normalises keys, drops exact
duplicates (same url + title, or same quote text), assigns stable ids,
and writes items.json / quotes.json beside this script.
"""
import json
import pathlib
import re
import sys
import hashlib

HERE = pathlib.Path(__file__).resolve().parent
src = pathlib.Path(sys.argv[1])

MEDIA = {"video", "audio", "text", "image", "archive", "community"}

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")

def norm_tags(tags):
    out = []
    for t in tags or []:
        t = slug(str(t))
        if t and t not in out:
            out.append(t)
    return out

def norm_year(it):
    y = it.get("year")
    if isinstance(y, str) and y.strip().isdigit():
        y = int(y)
    if not isinstance(y, int):
        m = re.search(r"(18|19|20)\d\d", str(it.get("date") or ""))
        y = int(m.group(0)) if m else None
    return y

items, quotes = [], []
seen_items, seen_quotes = set(), set()
counts = {}
for f in sorted(src.glob("*.json")):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:  # noqa
        print(f"skip {f.name}: {e}")
        continue
    if not isinstance(data, list):
        print(f"skip {f.name}: not a list"); continue
    n = 0
    if f.name.startswith("quotes"):
        for q in data:
            text = (q.get("text") or "").strip()
            if not text:
                continue
            key = re.sub(r"\W+", "", text.lower())[:120]
            if key in seen_quotes:
                continue
            seen_quotes.add(key)
            conf = q.get("confidence") or ("T" if q.get("kind") == "paraphrase" else "S")
            quotes.append({
                "id": "q" + hashlib.sha1(key.encode()).hexdigest()[:8],
                "text": text, "book": q.get("book") or "unassigned",
                "chapter": q.get("chapter"), "year": norm_year(q),
                "confidence": conf, "kind": q.get("kind") or "verbatim",
                "tags": norm_tags(q.get("tags")), "note": q.get("note"),
                "sources": [s for s in (q.get("sources") or []) if isinstance(s, str) and s.startswith("http")],
                "origin": f.stem,
            })
            n += 1
    else:
        for it in data:
            title = (it.get("title") or "").strip()
            url = (it.get("url") or "").strip() or None
            if not title:
                continue
            key = (url or "") + "|" + title.lower()
            if key in seen_items:
                continue
            seen_items.add(key)
            medium = (it.get("medium") or f.stem).lower()
            if medium not in MEDIA:
                medium = {"images": "image", "texts": "text", "archives": "archive"}.get(medium, "archive")
            items.append({
                "id": "i" + hashlib.sha1(key.encode()).hexdigest()[:8],
                "medium": medium, "title": title, "date": it.get("date"),
                "year": norm_year(it), "place": it.get("place"),
                "people": [p for p in (it.get("people") or []) if p],
                "format": it.get("format"), "language": it.get("language"),
                "duration": it.get("duration"), "host": it.get("host"),
                "url": url, "description": it.get("description"),
                "tags": norm_tags(it.get("tags")) + [medium],
                "confidence": it.get("confidence") or "lead",
                "sources": [s for s in (it.get("sources") or []) if isinstance(s, str) and s.startswith("http")],
                "origin": f.stem,
            })
            n += 1
    counts[f.name] = n

(HERE / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "quotes.json").write_text(json.dumps(quotes, ensure_ascii=False, indent=1), encoding="utf-8")
print(counts)
print(f"items={len(items)} quotes={len(quotes)}")
