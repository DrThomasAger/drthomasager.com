"""Turn enumerate.sh output into merge-ready JSON (the shared item schema).

    python3 ingest-enumerations.py [out-dir]

Writes <out-dir>/enum-archive.json, enum-youtube.json, enum-soundcloud.json
(default out-dir: enumerations/json). Then: python3 merge.py <out-dir>
together with the researchers' scratch folder, or copy these files into it.
"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
ENUM = HERE / "enumerations"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ENUM / "json"
OUT.mkdir(parents=True, exist_ok=True)

def year_of(s):
    m = re.search(r"(18|19|20)\d\d", str(s or ""))
    return int(m.group(0)) if m else None

archive = []
for f in ENUM.glob("archive-*.jsonl"):
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        ident = d.get("identifier")
        if not ident:
            continue
        medium = {"movies": "video", "audio": "audio", "texts": "text", "image": "image"}.get(d.get("mediatype"), "audio")
        archive.append({"medium": medium, "title": d.get("title") or ident, "date": d.get("date"), "year": year_of(d.get("date")),
                        "place": None, "people": [], "format": f"archive.org {d.get('mediatype') or 'item'}", "language": None,
                        "duration": d.get("runtime"), "host": "archive.org", "url": f"https://archive.org/details/{ident}",
                        "description": f"identifier {ident}; {d.get('description') or ''}"[:600], "tags": ["archive-org", "enumerated"],
                        "confidence": "S", "sources": [f"https://archive.org/details/{ident}"]})
ids_file = ENUM / "archive-ug-identifiers.txt"
if ids_file.exists():
    known = {a["url"] for a in archive}
    for ident in ids_file.read_text().split():
        u = f"https://archive.org/details/{ident}"
        if u not in known:
            archive.append({"medium": "audio", "title": ident, "date": None, "year": None, "place": None, "people": [],
                            "format": "archive.org item", "language": None, "duration": None, "host": "archive.org", "url": u,
                            "description": f"identifier {ident}", "tags": ["archive-org", "enumerated"], "confidence": "S", "sources": [u]})

def flat_entries(path):
    try:
        d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except Exception:
        return [], None
    return d.get("entries") or [], d.get("title") or d.get("uploader")

youtube, soundcloud = [], []
for f in ENUM.glob("youtube-*.json"):
    entries, src = flat_entries(f)
    for e in entries:
        vid = e.get("id")
        if not vid:
            continue
        youtube.append({"medium": "video", "title": e.get("title") or vid, "date": e.get("upload_date"), "year": year_of(e.get("upload_date")),
                        "place": None, "people": [e.get("uploader") or e.get("channel") or ""], "format": "YouTube video", "language": None,
                        "duration": (f"{int(e['duration'])//60} min" if e.get("duration") else None), "host": "youtube.com",
                        "url": f"https://www.youtube.com/watch?v={vid}", "description": f"id {vid}; from {src}", "tags": ["youtube", "enumerated"],
                        "confidence": "S", "sources": [f"https://www.youtube.com/watch?v={vid}"]})
for f in ENUM.glob("soundcloud-*.json"):
    entries, src = flat_entries(f)
    for e in entries:
        u = e.get("url") or e.get("webpage_url")
        if not u:
            continue
        soundcloud.append({"medium": "audio", "title": e.get("title") or u, "date": e.get("upload_date"), "year": year_of(e.get("upload_date") or e.get("title")),
                           "place": None, "people": [e.get("uploader") or ""], "format": "SoundCloud track", "language": None,
                           "duration": (f"{int(e['duration'])//60} min" if e.get("duration") else None), "host": "soundcloud.com", "url": u,
                           "description": f"from {src}", "tags": ["soundcloud", "enumerated"], "confidence": "S", "sources": [u]})
for name, data in (("enum-archive.json", archive), ("enum-youtube.json", youtube), ("enum-soundcloud.json", soundcloud)):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print({"archive": len(archive), "youtube": len(youtube), "soundcloud": len(soundcloud), "out": str(OUT)})
