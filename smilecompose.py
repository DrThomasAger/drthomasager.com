"""Compose a teacher's verified quotations into a Smile composition.

One implementation shared by recompose.py (the command line, the C- commands,
Pi) and build.py (which embeds the same texts for the compose page, whose
JavaScript mirrors compose() below line for line).

A composition here is what THE MAP Viewer's composer makes: the modules
chosen, each indented four spaces, then the words given in a face of their
own indented eight, inside the Smile Prompt Language header and footer. The
modules are the rules (smile/rules/), the form (smile/forms/), and what a
form gathers (a Suno style from the Suno lens, Hanjo's /C-blog). The words
are the quotations, each one raw text with its id, source and verification.
"""
import datetime
import json
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
RANK = {"corroborated-primary": 0, "corroborated-secondary": 1, "primary-source": 2, "multi-source": 3,
        "single-source": 4, "disputed": 6, "not-found": 7, "not-ug": 9}
MODEL_NAMES = {"claude-opus-5-5": "Opus 5.5", "claude-fable-5-1": "Fable 5.1",
               "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5"}


def formats():
    return json.loads((ROOT / "formats.json").read_text(encoding="utf-8"))


def _expand(p):
    home = os.environ.get("SMILE_HOME") or str(pathlib.Path.home() / "Claude" / "Projects" / "Smile")
    return pathlib.Path(os.path.expanduser(p.replace("%SMILE_HOME%", home)))


def read_text(rel):
    return (ROOT / rel).read_text(encoding="utf-8") if rel and (ROOT / rel).exists() else ""


def strip_front_matter(t):
    """A Claude Code command's front matter is for Claude Code, not for the prompt."""
    return re.sub(r"(?s)\A---\r?\n.*?\r?\n---\r?\n", "", t).lstrip()


def styles(F=None, live=True):
    """Suno styles by name, the Smile library's Suno lens first when present."""
    F = F or formats()
    out = {}
    d = ROOT / F.get("styles_dir", "smile/styles")
    for f in sorted(d.glob("*.txt")) if d.is_dir() else []:
        out[f.stem] = f.read_text(encoding="utf-8").strip()
    if live:
        for p in (F.get("live") or {}).get("styles", []):
            ld = _expand(p)
            if ld.is_dir():
                for f in sorted(ld.glob("*.txt")):
                    out[f.stem] = f.read_text(encoding="utf-8").strip()
                break
    return out


def c_blog(F=None, live=True):
    F = F or formats()
    if live:
        for p in (F.get("live") or {}).get("C-blog", []):
            f = _expand(p)
            if f.is_file():
                return strip_front_matter(f.read_text(encoding="utf-8"))
    return strip_front_matter(read_text("smile/forms/C-blog, edition 1.md"))


def pick(quotes, topic="", select=None, book="", include_single=False, limit=30):
    """The quotations that go in. Never a line that is not the teacher's, never
    a paraphrase; without a selection, never a disputed or unfound line, never
    a second copy of a passage, and a single-source line only when asked."""
    pool = [q for q in quotes if q.get("verdict") != "not-ug" and q.get("kind") != "paraphrase"]
    if not select:
        pool = [q for q in pool if not q.get("duplicate_of")]
    if select:
        byid = {q["id"]: q for q in pool}
        pool = [byid[i] for i in select if i in byid]
    else:
        pool = [q for q in pool if q.get("verdict") not in ("disputed", "not-found")
                and (include_single or q.get("verdict") != "single-source")]
    if book:
        pool = [q for q in pool if q.get("book") == book]
    words = [w for w in re.split(r"[\s,;]+", (topic or "").lower()) if len(w) > 2]
    if words and not select:
        scored = []
        for q in pool:
            hay = " ".join([q.get("text") or "", q.get("chapter") or ""] + (q.get("tags") or [])).lower()
            n = sum(1 for w in words if w in hay)
            if n:
                scored.append((-n, RANK.get(q.get("verdict"), 5), q))
        pool = [x[2] for x in sorted(scored, key=lambda x: (x[0], x[1]))]
    elif not select:
        pool = sorted(pool, key=lambda q: RANK.get(q.get("verdict"), 5))
    return pool[:max(1, limit)]


def quote_line(q, override=None):
    src = (q.get("book") or "unassigned") + (", " + q["chapter"] if q.get("chapter") else "")
    return f"[{q['id']}] ({src}; {q.get('verdict') or 'unverified'}) {override if override is not None else q['text']}"


def indent(t, n):
    return "\n".join((" " * n + l) if l.strip() else l for l in t.split("\n"))


def face(name, words):
    lower = name[0].lower() + name[1:]
    return f"    (: {name} (:\n{indent(words.strip(), 8)}\n    :) End {lower} :) thank you"


def fill(s, v):
    return re.sub(r"\{(\w+)\}", lambda m: str(v[m.group(1)]) if m.group(1) in v else m.group(0), s or "")


def compose(meta, quotes_in, fmt_id, topic="", extra="", model="claude-opus-5-5", style="", quote_url="",
            overrides=None, F=None, live=True, texts=None):
    """The composed Smile prompt. texts, when given, supplies module texts by
    path (the compose page embeds them this way); otherwise they are read."""
    F = F or formats()
    f = next(x for x in F["formats"] if x["id"] == fmt_id)
    reserved = meta.get("rights") == "reserved"
    get = (lambda rel: (texts or {}).get(rel, "")) if texts is not None else read_text
    v = {"teacher": meta.get("name"), "identity": meta.get("prompt_identity") or meta.get("name"),
         "topic": topic or "the teaching as a whole", "today": datetime.date.today().isoformat(),
         "model": MODEL_NAMES.get(model, model), "instagram": meta.get("instagram") or "",
         "quote_url": quote_url, "quote_budget": f.get("quote_budget", 400),
         "lyrics_max": f.get("lyrics_max", 5000), "style_max": f.get("style_max", 1000),
         "extra": extra or "the piece asked for in the extra asking"}
    mods = [get(r) for r in F.get("rules", [])]
    mods.append(get((F.get("rights") or {}).get("reserved" if reserved else "released", "")))
    mods.append(get(f.get("reserved_module") if reserved and f.get("reserved_module") else f.get("module")))
    if "C-blog" in (f.get("gathers") or []):
        mods.append((texts or {}).get("C-blog") if texts is not None else c_blog(F, live))
    parts = [indent(fill(m, v).strip(), 4) for m in mods if m and m.strip()]
    if "style" in (f.get("gathers") or []):
        st = style or f.get("default_style", "")
        stext = ((texts or {}).get("styles") or {}).get(st) if texts is not None else styles(F, live).get(st)
        if stext:
            parts.append(face("The style chosen", stext))
    if extra and fmt_id != "custom":
        parts.append(face("The extra asking", extra))
    ov = overrides or {}
    parts.append(face(f"The quotations given, {len(quotes_in)} of them", "\n".join(quote_line(q, ov.get(q["id"])) for q in quotes_in)))
    return "(-: Smile Prompt Language! (-:\n\n" + "\n\n".join(parts) + "\n\n:-) End Smile Prompt Language! :-) So much gratitude\n"


def module_texts(F=None):
    """Every text a composition may gather, for embedding in the compose page.
    Copies only, never machine-local paths, since the page is public."""
    F = F or formats()
    rels = list(F.get("rules", [])) + list((F.get("rights") or {}).values())
    for f in F["formats"]:
        rels += [f.get("module"), f.get("reserved_module")]
    out = {r: read_text(r) for r in rels if r}
    out["C-blog"] = c_blog(F, live=False)
    out["styles"] = styles(F, live=False)
    return out
