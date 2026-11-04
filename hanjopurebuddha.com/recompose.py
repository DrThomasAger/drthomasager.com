"""Recompose a teacher's verified quotations, from any CLI or project.

    python recompose.py teachers
    python recompose.py quotes  ug fear death                 # the quotations as Smile raw text
    python recompose.py compose --format suno ug fear death   # the composed Smile prompt, to follow
    python recompose.py write   --format book bernadette silence   # composed and written by Claude
    python recompose.py save    --format suno ug --file song.md     # keep a written piece as a composition

The /C-guru commands (smile/commands/) call compose and save, so a song, a
collection, a book or a post can be made from Claude Code, from the Pi CLI,
or from THE MAP Viewer's composer, which lists every C- command. The page at
gurus/<slug>/compose/ makes the same composition. write needs
ANTHROPIC_API_KEY; compose needs nothing, since the instance reading it
writes the piece itself.

Teachers are named loosely: ug, UG Krishnamurti, bernadette, roberts.
Options: --format suno|collection|book|blog|instagram|custom  --style <name>
--max N  --select id,id  --book "<title>"  --include-single  --extra "<asking>"
--model claude-opus-5-5  --to-posts (blog form, writes into posts/).
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import smilecompose as sc  # noqa: E402


def teachers():
    return sorted(p.name for p in (ROOT / "teachers").iterdir() if p.is_dir() and not p.name.startswith("_"))


def resolve(name):
    n = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    ts = teachers()
    for t in ts:
        if t == n:
            return t
    hits = [t for t in ts if n and (t.startswith(n) or n in t or any(part == n for part in t.split("-")))]
    if len(hits) == 1:
        return hits[0]
    sys.exit(f"no single teacher matches {name!r}; teachers are {', '.join(ts)}")


def teacher_data(slug):
    import build  # the build's edit overlay, so the words match the site
    folder = ROOT / "teachers" / slug
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    quotes = json.loads((folder / "quotes.json").read_text(encoding="utf-8"))
    edits = json.loads((folder / "edits.json").read_text(encoding="utf-8")) if (folder / "edits.json").exists() else {}
    data = build.apply_edits({"quotes": quotes, "items": [], "events": [], "people": [], "meta": meta}, edits)
    return data["meta"], data["quotes"]


def quote_url(slug):
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8")) if (ROOT / "site.json").exists() else {}
    return (site.get("gurus_url") or "").rstrip("/") + f"/{slug}/quotes/ID/"


def split_args(rest):
    """The first word or two name the teacher, the rest is the topic."""
    if not rest:
        sys.exit("name a teacher, e.g. ug or bernadette")
    for k in (2, 1):
        if len(rest) >= k:
            try:
                return resolve(" ".join(rest[:k])), " ".join(rest[k:])
            except SystemExit:
                if k == 1:
                    raise
    return resolve(rest[0]), " ".join(rest[1:])


def call_claude(system, prompt, model, max_tokens):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set; use compose to print the prompt instead")
    body = json.dumps({"model": model, "max_tokens": max_tokens, "stream": True, "system": system,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    out, stop = [], ""
    with urllib.request.urlopen(req, timeout=900) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            try:
                ev = json.loads(line[5:])
            except ValueError:
                continue
            if ev.get("type") == "content_block_delta" and ev.get("delta", {}).get("type") == "text_delta":
                t = ev["delta"]["text"]; out.append(t); sys.stderr.write(t); sys.stderr.flush()
            elif ev.get("type") == "message_delta":
                stop = ev.get("delta", {}).get("stop_reason") or stop
            elif ev.get("type") == "error":
                sys.exit(f"\nClaude error: {ev.get('error')}")
    if stop == "max_tokens":
        sys.stderr.write("\n[stopped at this form's max_tokens; raise it in formats.json to go longer]\n")
    return "".join(out)


def title_of(text, fallback):
    m = (re.search(r"^title:\s*(.+)$", text, re.M) or re.search(r"^#\s+(.+)$", text, re.M)
         or re.search(r"^\*\*(.+?)\*\*", text, re.M))
    return re.sub(r"[\"#*]", "", m.group(1)).strip() if m else fallback


def save(slug, f, text, topic, model, qs, out="", to_posts=False):
    today = datetime.date.today().isoformat()
    title = title_of(text, f"{f['name']} on {topic or 'the teaching'}")
    slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]
    if to_posts and f["id"] == "blog":
        posts = ROOT.parent / "posts" if (ROOT.parent / "posts").is_dir() else ROOT / "posts"
        posts.mkdir(exist_ok=True)
        m = re.search(r"^slug:\s*(.+)$", text, re.M)
        path = pathlib.Path(out) if out else posts / ((m.group(1).strip() if m else slugify(title)) + ".md")
        path.write_text(text.strip() + "\n", encoding="utf-8")
        return path
    comp = ROOT / "teachers" / slug / "compositions"
    comp.mkdir(exist_ok=True)
    path = pathlib.Path(out) if out else comp / f"{today}-{slugify(f['id'] + '-' + title)}.md"
    fm = (f"---\ntitle: {title}\nteacher: {slug}\nformat: {f['name']}\ntopic: {topic}\ndate: {today}\nmodel: {model}\n"
          f"authorship: model: {model}\nquotes: {', '.join(q['id'] for q in qs)}\n---\n\n")
    path.write_text(fm + text.strip() + "\n", encoding="utf-8")
    return path


def main():
    F = sc.formats()
    ids = [f["id"] for f in F["formats"]]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["teachers", "quotes", "compose", "write", "save", "styles"])
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--format", choices=ids, default="suno")
    ap.add_argument("--style", default="")
    ap.add_argument("--select", default="")
    ap.add_argument("--book", default="")
    ap.add_argument("--include-single", action="store_true")
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--extra", default="")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--file", default="", help="save: the written piece")
    ap.add_argument("--topic", default="", help="save: the topic it was written on")
    ap.add_argument("--to-posts", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if a.action == "teachers":
        for t in teachers():
            m = json.loads((ROOT / "teachers" / t / "meta.json").read_text(encoding="utf-8"))
            print(f"{t}\t{m.get('name')}\t{m.get('dates', '')}\t{m.get('rights', '')}")
        return
    if a.action == "styles":
        for k, v in sc.styles(F).items():
            print(f"{k}\t{v[:90]}")
        return
    f = next(x for x in F["formats"] if x["id"] == a.format)
    slug, topic = split_args(a.rest)
    topic = topic or a.topic
    meta, quotes = teacher_data(slug)
    qs = sc.pick(quotes, topic, [s for s in a.select.split(",") if s.strip()], a.book, a.include_single,
                 a.max or f.get("default_max_quotes", 30))
    if a.action == "quotes":
        print(sc.face(f"{meta.get('name')}, the quotations given, {len(qs)} of them", "\n".join(sc.quote_line(q) for q in qs)))
        return
    if not qs:
        sys.exit("no quotations match; widen the topic or pass --include-single")
    prompt = sc.compose(meta, qs, a.format, topic, a.extra, a.model, a.style, quote_url(slug), F=F)
    if a.action == "compose":
        print(prompt)
        print(f"\n(When the piece is written, keep it with: python \"{ROOT / 'recompose.py'}\" save --format {a.format} {slug} --topic \"{topic}\" --select {','.join(q['id'] for q in qs)} --file <the file written>)")
        return
    if a.action == "save":
        if not a.file:
            sys.exit("save needs --file")
        path = save(slug, f, pathlib.Path(a.file).read_text(encoding="utf-8"), topic, a.model, qs, a.out, a.to_posts)
        print(f"kept {path}")
        return
    text = call_claude(F.get("system", ""), prompt, a.model, f.get("max_tokens", 8000))
    path = save(slug, f, text, topic, a.model, qs, a.out, a.to_posts)
    sys.stderr.write(f"\nkept {path}\n")


if __name__ == "__main__":
    main()
