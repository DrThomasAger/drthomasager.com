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

PLACE_WORDS = ["gstaad","saanen","bangalore","bengaluru","amsterdam","sydney","yercaud","mysore",
    "kodaikanal","vallecrosia","palm springs","mill valley","carmel","seaside","albuquerque","bombay","mumbai",
    "madras","chennai","hyderabad","delhi","london","paris","geneva","cologne","new york","california",
    "switzerland","india","italy","netherlands","australia","usa","uk","masulipatnam","gudivada","goa"]

def enrich_tags(it, tags):
    """Derive metadata tags from the item's own fields."""
    out = list(tags)
    def add(t):
        t = slug(t)
        if t and t not in out:
            out.append(t)
    y = it.get("year")
    if isinstance(y, int):
        add(f"{y//10*10}s"); add(str(y))
    for p in (it.get("people") or []):
        add("person-" + p.split()[-1]) if p.split() else None
    host = it.get("host") or ""
    if not host and it.get("url"):
        m = re.match(r"https?://(?:www\.)?([^/]+)", it["url"])
        host = m.group(1) if m else ""
    if host: add("host-" + host)
    if it.get("format"): add("format-" + it["format"].split("|")[0].split("(")[0].strip())
    if it.get("language"): add("lang-" + it["language"])
    if it.get("duration"): add("has-duration")
    blob = " ".join(str(it.get(k) or "") for k in ("place","title","description")).lower()
    for w in PLACE_WORDS:
        if w in blob: add("place-" + w)
    if it.get("confidence"): add("confidence-" + it["confidence"])
    return out

BOOKS = {
    "mind is a myth": "Mind is a Myth", "thought is your enemy": "Thought is Your Enemy",
    "the mystique of enlightenment": "The Mystique of Enlightenment", "mystique of enlightenment": "The Mystique of Enlightenment",
    "no way out": "No Way Out", "the courage to stand alone": "The Courage to Stand Alone", "courage to stand alone": "The Courage to Stand Alone",
    "the natural state": "The Natural State", "my swan song": "My Swan Song", "swan song": "My Swan Song",
    "a taste of death": "A Taste of Death", "u.g. krishnamurti: a life": "U.G. Krishnamurti: A Life",
    "stopped in our tracks": "Stopped in Our Tracks", "the biology of enlightenment": "The Biology of Enlightenment",
    "the sage and the housewife": "The Sage and the Housewife",
}
def norm_book(b):
    b = (b or "unassigned").strip()
    return BOOKS.get(b.lower(), b)

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
    if f.name in ("events.json", "people.json") or f.name.startswith("verification"):
        continue
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
                "text": text, "book": norm_book(q.get("book")),
                "chapter": q.get("chapter"), "year": norm_year(q),
                "confidence": conf, "kind": q.get("kind") or "verbatim",
                "tags": norm_tags(q.get("tags")) + [t for t in ["book-" + slug(q.get("book") or "unassigned"), "kind-" + slug(q.get("kind") or "verbatim")] ],
                "note": q.get("note"),
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
                "tags": None,
                "confidence": it.get("confidence") or "lead",
                "sources": [s for s in (it.get("sources") or []) if isinstance(s, str) and s.startswith("http")],
                "origin": f.stem,
            })
            rec = items[-1]
            rec["tags"] = enrich_tags(rec, norm_tags(it.get("tags")) + [medium])
            n += 1
    counts[f.name] = n

# Items that share a URL are one item: keep the richest, union the rest.
by_url = {}
merged = []
for it in items:
    u = it.get("url")
    if not u:
        merged.append(it); continue
    if u in by_url:
        keep = by_url[u]
        if len(it.get("description") or "") > len(keep.get("description") or ""):
            keep["description"], it["description"] = it["description"], keep["description"]
        if it["title"].lower() != keep["title"].lower():
            keep.setdefault("also_titled", [])
            if it["title"] not in keep["also_titled"]:
                keep["also_titled"].append(it["title"])
        for k in ("tags", "sources", "people"):
            for v in it.get(k) or []:
                if v not in keep[k]:
                    keep[k].append(v)
        for k in ("date", "year", "place", "format", "language", "duration", "host"):
            if not keep.get(k) and it.get(k):
                keep[k] = it[k]
        if keep.get("confidence") != "S" and it.get("confidence") == "S":
            keep["confidence"] = "S"
        keep.setdefault("origins", [keep["origin"]])
        if it["origin"] not in keep["origins"]:
            keep["origins"].append(it["origin"])
    else:
        by_url[u] = it
        merged.append(it)
print(f"url-merge: {len(items)} -> {len(merged)}")
items = merged

# Extra datasets: events, people, verification
def load_list(name):
    f = src / name
    if not f.exists():
        return []
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception as e:  # noqa
        print(f"skip {name}: {e}"); return []

events = load_list("events.json")
people = load_list("people.json")
verification = {}
for vf in sorted(src.glob("verification*.json")):
    for v in load_list(vf.name):
        if v.get("id") and v.get("searched", True) and v.get("verdict"):
            verification[v["id"]] = v
for q in quotes:
    hosts = set()
    for u in q["sources"]:
        m = re.match(r"https?://(?:www\.)?([^/]+)", u)
        if m: hosts.add(m.group(1))
    q["source_hosts"] = sorted(hosts)
    primary = {"en.wikisource.org", "people.well.com", "archive.org", "ugkrishnamurti.in", "well.com"}
    v = verification.get(q["id"])
    if v:
        q["verdict"] = v.get("verdict")
        q["confirming_sources"] = v.get("confirming_sources") or []
        q["wording_variants"] = v.get("wording_variants") or []
    elif hosts & primary:
        q["verdict"] = "primary-source"
    elif len(hosts) >= 2:
        q["verdict"] = "multi-source"
    else:
        q["verdict"] = "single-source"
# Hand corrections (corrections.json beside this script), applied last.
corr_path = HERE / "corrections.json"
if corr_path.exists():
    corr = json.loads(corr_path.read_text(encoding="utf-8"))
    # researcher-produced attribution corrections (same shape), applied first so hand corrections win
    for extra in sorted(src.glob("attribution-corrections*.json")):
        try:
            ext = json.loads(extra.read_text(encoding="utf-8"))
            if isinstance(ext, dict):
                for k, v in ext.items():
                    if k.startswith("_"):
                        continue
                    fields = {kk: vv for kk, vv in v.items() if kk in ("book", "chapter", "note", "kind", "confidence")}
                    if k not in corr:
                        corr[k] = fields
                    else:  # hand correction wins field by field; researcher fills what it lacks
                        for kk, vv in fields.items():
                            if kk == "note":
                                corr[k]["note"] = ((corr[k].get("note") or "") + " " + vv).strip()
                            elif kk not in corr[k]:
                                corr[k][kk] = vv
        except Exception as e:  # noqa
            print(f"skip {extra.name}: {e}")
    byid = {q["id"]: q for q in quotes}
    applied = 0
    for qid, fix in corr.items():
        if qid.startswith("_") or qid not in byid:
            continue
        q = byid[qid]
        for k, v in fix.items():
            if k == "note":
                q["note"] = ((q.get("note") or "") + " " + v).strip()
            elif k == "book":
                q["book"] = norm_book(v)
            else:
                q[k] = v
        q["corrected"] = True
        applied += 1
    print(f"corrections applied: {applied}")
if events:
    (HERE / "events.json").write_text(json.dumps(events, ensure_ascii=False, indent=1), encoding="utf-8")
if people:
    (HERE / "people.json").write_text(json.dumps(people, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"events={len(events)} people={len(people)} verified={len(verification)}")

(HERE / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / "quotes.json").write_text(json.dumps(quotes, ensure_ascii=False, indent=1), encoding="utf-8")
print(counts)
print(f"items={len(items)} quotes={len(quotes)}")
