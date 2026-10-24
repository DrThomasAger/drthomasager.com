"""Regenerate the dataset table in README.md from integrity.json.

    python3 readme.py

Replaces everything between <!-- counts --> and <!-- /counts --> in
README.md with the current counts. Add those two markers to a README once.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
s = json.loads((HERE / "integrity.json").read_text(encoding="utf-8"))["summary"]
block = f"""<!-- counts -->
| File | What | Count |
|---|---|---|
| `items.json` | located media items across video, audio, text, image, archive, community | {s['items']} |
| `quotes.json` | words of the teacher, each with book, chapter, confidence, kind, verdict, sources | {s['quotes']} |
| `events.json` | dated life events with sources | {s['events']} |
| `people.json` | everyone connected to the record, with role and what they hold | {s['people']} |

Items by medium: {", ".join(f"{k} {v}" for k, v in s['items_by_medium'].items())}.
Items by confidence: {", ".join(f"{k} {v}" for k, v in s['items_by_confidence'].items())}.
Quotes by verdict: {", ".join(f"{k} {v}" for k, v in s['quotes_by_verdict'].items())}.
Distinct source hosts cited: {s['distinct_source_hosts']}.
<!-- /counts -->"""
p = HERE / "README.md"
t = p.read_text(encoding="utf-8")
if "<!-- counts -->" in t:
    t = re.sub(r"<!-- counts -->[\s\S]*?<!-- /counts -->", block, t)
else:
    t = t + "\n\n" + block + "\n"
p.write_text(t, encoding="utf-8")
print("README counts updated")
