"""Name every set the archive holds, its count, and what is not yet reached.

    python3 coverage.py

Counted from the files themselves at each run, for every teacher folder,
and written to COVERAGE.md beside this script. check.py runs it after the
integrity checks.
"""
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import smilecompose as sc  # noqa: E402

USABLE = ("corroborated-primary", "corroborated-secondary", "primary-source", "multi-source")


def load(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
    except ValueError:
        return default


def front(p):
    m = re.match(r"(?s)---\r?\n(.*?)\r?\n---", p.read_text(encoding="utf-8"))
    return dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M)) if m else {}


def table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def teacher(d, F):
    meta = load(d / "meta.json", {})
    items, quotes = load(d / "items.json", []), load(d / "quotes.json", [])
    events, people = load(d / "events.json", []), load(d / "people.json", [])
    integ = load(d / "integrity.json", {})
    manifest = load(d / "download-manifest.json", {})
    L = [f"## {meta.get('name', d.name)}", ""]

    L += ["### Archive items", ""]
    by_m = Counter(i.get("medium") for i in items)
    rows = []
    for m in sorted(by_m):
        g = [i for i in items if i.get("medium") == m]
        rows.append((m, len(g), sum(1 for i in g if i.get("confidence") == "S"), sum(1 for i in g if i.get("confidence") != "S"),
                     sum(1 for i in g if i.get("year")), sum(1 for i in g if not i.get("sources"))))
    rows.append(("all", len(items), sum(r[2] for r in rows), sum(r[3] for r in rows), sum(r[4] for r in rows), sum(r[5] for r in rows)))
    L += table(rows, ["medium", "items", "confirmed", "lead or likely", "dated", "no source"]) + [""]

    L += ["### Quotations", ""]
    v = Counter(q.get("verdict") for q in quotes)
    L += table(sorted(v.items(), key=lambda kv: sc.RANK.get(kv[0], 5)), ["verification", "quotations"]) + [""]
    k = Counter(q.get("kind") for q in quotes)
    pool = sc.pick(quotes, limit=10 ** 6)
    pool_single = sc.pick(quotes, include_single=True, limit=10 ** 6)
    L += [f"- Kinds: " + ", ".join(f"{n} {kk}" for kk, n in k.most_common()) + ".",
          f"- Books: {len(set(q.get('book') for q in quotes))}, with {sum(1 for q in quotes if q.get('book') in (None, '', 'unassigned'))} quotations not yet placed in a book.",
          f"- Marked as a second copy of a passage: {sum(1 for q in quotes if q.get('duplicate_of'))}.",
          f"- Given to a composition by default: {len(pool)}; with single-source lines allowed: {len(pool_single)}.",
          ""]

    L += ["### Life and people", "",
          f"- Life events: {len(events)}, {sum(1 for e in events if e.get('sources'))} with sources, "
          f"{integ.get('summary', {}).get('events_with_recorded_date_conflict', 0)} where sources give different dates (both shown).",
          f"- People: {len(people)}, {sum(1 for p in people if p.get('sources'))} with sources.", ""]

    L += ["### Compositions", ""]
    comps = [front(p) | {"file": p.name} for p in sorted((d / "compositions").glob("*.md"))] if (d / "compositions").is_dir() else []
    rows = []
    for f in F["formats"]:
        made = [c for c in comps if c.get("format") == f["name"]]
        rows.append((f["name"], len(made), "; ".join(c.get("title", c["file"]) for c in made) or "not yet made"))
    L += table(rows, ["form", "made", "titles"]) + [""]
    bad = [r for k2, rs in (integ.get("issues") or {}).items() if k2.startswith("composition") for r in rs]
    L += [f"- Compositions whose every quoted line is checked against their quotations: {integ.get('summary', {}).get('compositions_checked', 0)}. "
          f"Lines not found: {len(bad)}.", ""]

    L += ["### Media files", ""]
    if isinstance(manifest, dict) and manifest.get("fetch") is False:
        L += [f"- Not fetched by design: {manifest.get('note', 'her words are under copyright')}", ""]
    else:
        n = {kk: len(vv) for kk, vv in manifest.items() if isinstance(vv, list)}
        hold = load(d / "holdings.json", {})
        held = {kk: sum(1 for r in manifest.get(kk, []) if hold.get(r["id"], {}).get("complete")) for kk in n}
        secs = sum(f.get("seconds", 0) for h in hold.values() for f in (h.get("files") or {}).values())
        assets = sum(1 for h in hold.values() for f in (h.get("files") or {}).values() if f.get("asset"))
        nfiles = sum(len(h.get("files") or {}) for h in hold.values())
        nbytes = sum(f.get("bytes", 0) for h in hold.values() for f in (h.get("files") or {}).values())
        L += [f"- Listed for download by fetch.py: {sum(n.values())} addresses, items and the media among their sources.", ""]
        L += table([(kk, vv, held[kk]) for kk, vv in n.items()], ["kind", "listed", "held"]) + [""]
        L += [f"- Held: {nfiles} files, {nbytes / 1e9:.2f} GB, {secs / 3600:.1f} hours of recordings, each with its sha256 in holdings.json;"
              f" {assets} of them are public release assets of this repository (media-<kind> releases), each with its download address.",
              "- Not yet held, with the last answer each host gave: catalogue/not-yet-held.md. The harvest workflow (harvest.yml, then gather.yml) or `python fetch.py` on any machine continues.", ""]

    L += ["### Integrity", ""]
    ic = (integ.get("summary") or {}).get("issue_counts") or {}
    L += [("- Open: " + ", ".join(f"{n} {kk}" for kk, n in sorted(ic.items())) + ".") if ic else "- Open: none.", ""]

    L += ["### Not yet reached", ""]
    gaps = []
    if v.get("single-source"):
        gaps.append(f"{v['single-source']} quotations rest on one source and wait for a second.")
    if v.get("disputed") or v.get("not-found"):
        gaps.append(f"{v.get('disputed', 0)} disputed and {v.get('not-found', 0)} not found, never quoted.")
    leads = sum(1 for i in items if i.get("confidence") != "S")
    if leads:
        gaps.append(f"{leads} archive items are leads or likely, not yet confirmed by a source.")
    und = sum(1 for i in items if not i.get("year"))
    if und:
        gaps.append(f"{und} archive items have no year (websites and accounts among them, which take none).")
    for f in F["formats"]:
        if not any(c.get("format") == f["name"] for c in comps):
            gaps.append(f"No {f['name']} composition yet.")
    nw = d / "catalogue" / "NEXT-WAVE.md"
    if nw.exists():
        gaps.append("The hosts the gathering network could not reach, and the briefs waiting for them, are in catalogue/NEXT-WAVE.md.")
    L += [f"- {g}" for g in gaps] or ["- Nothing."]
    return L + [""]


def main():
    F = sc.formats()
    teachers = sorted(p for p in (ROOT / "teachers").iterdir() if p.is_dir() and not p.name.startswith("_"))
    L = ["# Coverage", "",
         "Every set the archive holds, its count, and what is not yet reached, counted from the files by `coverage.py`. "
         "Run it again after any merge, edit or composition.", ""]
    L += ["## The sets across the archive", ""]
    cmds = sorted(p.name for p in (ROOT / "smile" / "commands").glob("C-*.md"))
    L += [f"- Teachers: {len(teachers)} ({', '.join(t.name for t in teachers)}).",
          f"- Forms: {len(F['formats'])} ({', '.join(f['name'] for f in F['formats'])}), each a .smile module in smile/forms, "
          f"with {sum(1 for f in F['formats'] if f.get('reserved_module'))} carrying a variant for words under copyright.",
          f"- Suno styles held as copies: {len(sc.styles(F, live=False))}.",
          f"- Commands: {len(cmds)} ({', '.join(c[:-3] for c in cmds)}), for Claude Code, Pi and THE MAP Viewer's composer through smile/install.py."]
    sm = ROOT / "site" / "sitemap.xml"
    if sm.exists():
        L += [f"- Pages in the built site: {sm.read_text(encoding='utf-8').count('<loc>')}."]
    L += [""]
    for t in teachers:
        L += teacher(t, F)
    (ROOT / "COVERAGE.md").write_text("\n".join(L), encoding="utf-8")
    print(f"COVERAGE.md written, {len(teachers)} teachers")


if __name__ == "__main__":
    main()
