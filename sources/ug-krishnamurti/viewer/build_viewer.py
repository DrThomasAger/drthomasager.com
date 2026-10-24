"""Build the self-contained U.G. Krishnamurti archive viewer.

Reads ../data/items.json and ../data/quotes.json, embeds them into
template.html, writes index.html beside this script. Run:

    python3 build_viewer.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data"

items = json.loads((DATA / "items.json").read_text(encoding="utf-8"))
quotes = json.loads((DATA / "quotes.json").read_text(encoding="utf-8"))
meta = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))

# Life events come from ../timeline.md (the markdown table).
events = []
for line in (HERE.parent / "timeline.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("|") and not line.startswith("| Date") and not line.startswith("|---"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            events.append({"date": cells[0], "event": cells[1], "place": cells[2]})
meta["events"] = events

payload = json.dumps({"items": items, "quotes": quotes, "meta": meta},
                     ensure_ascii=False)
# Keep the JSON safe inside a <script> element.
payload = payload.replace("</", "<\\/")

template = (HERE / "template.html").read_text(encoding="utf-8")
out = template.replace("/*__DATA__*/", payload)
(HERE / "index.html").write_text(out, encoding="utf-8")
print(f"items={len(items)} quotes={len(quotes)} -> {HERE / 'index.html'} "
      f"({len(out)/1024:.0f} KB)")
