"""Locate every quote in the locally extracted texts (after extract-text.py).

    python3 find-quotes.py             # writes local-verification.json

For each quote, searches texts/ for the longest exact run of its words
(case- and punctuation-insensitive). Reports the file, the match length as
a fraction of the quote, and the surrounding sentence. Output is in the
verification schema, so `python3 merge.py <dir-containing-local-verification.json>`
upgrades verdicts to corroborated-primary where the text itself carries the line.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
TXT = HERE / "texts"
norm = lambda s: re.sub(r"[^a-z0-9 ]+", " ", s.lower())
corpus = {}
for f in TXT.rglob("*.txt"):
    corpus[str(f.relative_to(HERE))] = " ".join(norm(f.read_text(encoding="utf-8", errors="replace")).split())
quotes = json.loads((HERE / "quotes.json").read_text(encoding="utf-8"))
out = []
for q in quotes:
    words = norm(q["text"]).split()
    if len(words) < 4:
        continue
    best = (0, None, None)
    for path, text in corpus.items():
        # longest window of the quote present verbatim in this text
        lo, hi = 4, len(words)
        found = None
        while lo <= hi:
            mid = (lo + hi) // 2
            hit = next((i for i in range(0, len(words) - mid + 1) if " ".join(words[i:i + mid]) in text), None)
            if hit is not None:
                found = (mid, hit); lo = mid + 1
            else:
                hi = mid - 1
        if found and found[0] > best[0]:
            best = (found[0], path, " ".join(words[found[1]:found[1] + found[0]]))
    frac = best[0] / len(words) if words else 0
    if best[1]:
        out.append({"id": q["id"], "text_checked": best[2][:200], "verdict": "corroborated-primary" if frac >= 0.6 else "single-source",
                    "confirming_sources": [f"local:{best[1]}"], "book_per_sources": best[1].split("/")[1] if "/" in best[1] else best[1],
                    "wording_variants": [], "note": f"local text match {frac:.0%} of the quote's words", "searched": True})
(HERE / "local-verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(out)} quotes located in {len(corpus)} text files")
