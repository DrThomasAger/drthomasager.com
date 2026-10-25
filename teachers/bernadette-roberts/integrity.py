"""Integrity check for a teacher folder.

    python3 integrity.py

Reads items.json, quotes.json, events.json, people.json beside this
script and writes integrity-report.md and integrity.json. Checks:
schema (required keys, types), URL well-formedness, duplicate URLs and
near-duplicate titles/quotes, years inside the life span, missing
sources, items whose only source is themselves, Jiddu Krishnamurti
contamination (names and J.K. host names), empty tags, confidence
values, quotes with no book, quotes attributed to editors, and the
per-host distribution of sources.
"""
import json
import pathlib
import re
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
LIFE = (1918, 2026)
JK_MARKERS = ["jiddu", "kfoundation.org", "jkrishnamurti.org", "kfa.org", "kfionline", "krishnamurti foundation"]
URL_RE = re.compile(r"^https?://[^\s/]+\.[^\s/]+(/\S*)?$")
REQUIRED_ITEM = ["id", "medium", "title", "tags", "confidence", "sources"]
REQUIRED_QUOTE = ["id", "text", "book", "confidence", "sources"]


def load(name):
    p = HERE / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def key(s):
    return re.sub(r"\W+", "", (s or "").lower())


issues = defaultdict(list)
items, quotes, events, people = load("items.json"), load("quotes.json"), load("events.json"), load("people.json")

# ---- items
urls = Counter()
titles = Counter()
for it in items:
    for k in REQUIRED_ITEM:
        if k not in it:
            issues["item-missing-key"].append((it.get("id"), k))
    if it.get("url") and not URL_RE.match(it["url"]):
        issues["item-bad-url"].append((it["id"], it["url"]))
    for s in it.get("sources") or []:
        if not URL_RE.match(s):
            issues["item-bad-source-url"].append((it["id"], s))
    if not it.get("sources"):
        issues["item-no-sources"].append((it["id"], it["title"]))
    elif it.get("url") and set(it["sources"]) == {it["url"]}:
        pass  # the item's own page is its source; counted in summary below
    y = it.get("year")
    if isinstance(y, int) and not (LIFE[0] <= y <= LIFE[1]):
        issues["item-year-out-of-range"].append((it["id"], y))
    if it.get("confidence") not in ("S", "T", "lead"):
        issues["item-bad-confidence"].append((it["id"], it.get("confidence")))
    if len(it.get("tags") or []) < 3:
        issues["item-thin-tags"].append((it["id"], it["title"]))
    blob = " ".join(str(it.get(k) or "") for k in ("title", "description", "url")).lower()
    if any(m in blob for m in JK_MARKERS) and "not jiddu" not in blob and "u.g." not in blob and "ug " not in blob:
        issues["item-possible-jk-contamination"].append((it["id"], it["title"]))
    if it.get("url"):
        urls[it["url"]] += 1
    titles[key(it["title"])] += 1
for u, n in urls.items():
    if n > 1:
        issues["item-duplicate-url"].append((u, n))
for t, n in titles.items():
    if n > 1:
        issues["item-duplicate-title"].append((t[:60], n))

# ---- quotes
qkeys = Counter()
for q in quotes:
    for k in REQUIRED_QUOTE:
        if k not in q:
            issues["quote-missing-key"].append((q.get("id"), k))
    if not q.get("sources"):
        issues["quote-no-sources"].append((q["id"], q["text"][:60]))
    for s in q.get("sources") or []:
        if not URL_RE.match(s):
            issues["quote-bad-source-url"].append((q["id"], s))
    if q.get("book") in (None, "", "unassigned"):
        issues["quote-unassigned-book"].append((q["id"], q["text"][:60]))
    if q.get("confidence") not in ("S", "T"):
        issues["quote-bad-confidence"].append((q["id"], q.get("confidence")))
    note = (q.get("note") or "").lower()
    if any(w in note for w in ("editor", "bhatt's own", "not ug", "newland quoting", "misattribut")):
        issues["quote-flagged-not-ug-or-editor"].append((q["id"], q["text"][:60]))
    if "jiddu" in note or any(m in " ".join(q.get("sources") or []).lower() for m in JK_MARKERS):
        issues["quote-possible-jk-contamination"].append((q["id"], q["text"][:60]))
    if len(q.get("text", "")) < 25:
        issues["quote-very-short"].append((q["id"], q["text"]))
    k = key(q["text"])[:80]
    qkeys[k] += 1
for k, n in qkeys.items():
    if n > 1:
        issues["quote-near-duplicate"].append((k[:60], n))

# ---- events / people
for e in events:
    y = e.get("year")
    if isinstance(y, int) and not (LIFE[0] - 1 <= y <= LIFE[1]):
        issues["event-year-out-of-range"].append((e.get("date"), y))
    if not e.get("sources"):
        issues["event-no-sources"].append((e.get("date"), (e.get("event") or "")[:60]))
    if e.get("confidence") == "conflict":
        issues["event-date-conflict"].append((e.get("date"), (e.get("event") or "")[:60]))
for p in people:
    if not p.get("sources"):
        issues["person-no-sources"].append((p.get("name"),))

# ---- source host distribution
hosts = Counter()
for it in items:
    for s in it.get("sources") or []:
        m = re.match(r"https?://(?:www\.)?([^/]+)", s)
        if m: hosts[m.group(1)] += 1
for q in quotes:
    for s in q.get("sources") or []:
        m = re.match(r"https?://(?:www\.)?([^/]+)", s)
        if m: hosts[m.group(1)] += 1

summary = {
    "items": len(items), "quotes": len(quotes), "events": len(events), "people": len(people),
    "items_by_medium": dict(Counter(i.get("medium") for i in items)),
    "items_by_confidence": dict(Counter(i.get("confidence") for i in items)),
    "quotes_by_confidence": dict(Counter(q.get("confidence") for q in quotes)),
    "quotes_by_verdict": dict(Counter(q.get("verdict") for q in quotes)),
    "quotes_by_book": dict(Counter(q.get("book") for q in quotes)),
    "distinct_source_hosts": len(hosts),
    "items_self_sourced_only": sum(1 for i in items if i.get("url") and set(i.get("sources") or []) == {i["url"]}),
    "items_with_second_source": sum(1 for i in items if len(set(i.get("sources") or []) - {i.get("url")}) >= 1),
    "issue_counts": {k: len(v) for k, v in sorted(issues.items())},
}
(HERE / "integrity.json").write_text(json.dumps({"summary": summary, "issues": issues, "hosts": hosts.most_common()}, ensure_ascii=False, indent=1), encoding="utf-8")

lines = ["# Integrity report", "", "Generated by `integrity.py`. Re-run after every merge.", ""]
lines += ["## Summary", ""]
for k, v in summary.items():
    if k == "issue_counts":
        continue
    lines.append(f"- **{k}**: {v}")
lines += ["", "## Issues", ""]
if not issues:
    lines.append("None.")
for k, v in sorted(issues.items()):
    lines.append(f"### {k} ({len(v)})")
    for row in v[:60]:
        lines.append("- " + " · ".join(str(x) for x in row))
    if len(v) > 60:
        lines.append(f"- … and {len(v) - 60} more (see integrity.json)")
    lines.append("")
lines += ["## Sources by host", ""]
for h, n in hosts.most_common(40):
    lines.append(f"- {h}: {n}")
(HERE / "integrity-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=1))
