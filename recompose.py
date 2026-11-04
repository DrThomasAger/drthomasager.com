"""Recompose a teacher's verified quotations into a new form with Claude.

    python3 recompose.py <teacher-slug> --format song --topic "fear death"
    python3 recompose.py ug-krishnamurti --format book --topic thought --max 150
    python3 recompose.py bernadette-roberts --format blog --topic silence --to-posts
    python3 recompose.py ug-krishnamurti --format 5000 --select q1a2b3c4d,q5e6f7a8b
    python3 recompose.py ug-krishnamurti --format collection --topic body --prompt-only

The forms, rules and system prompt come from formats.json, the same file the
compose page reads, and the quotation choice follows the same steps, so the
page and this command write the same prompt. Needs ANTHROPIC_API_KEY unless
--prompt-only. Writes teachers/<slug>/compositions/<date>-<form>-<title>.md,
which the build renders as its own page; --to-posts writes a blog-post form
into the drthomasager.com posts/ folder instead.
"""
import argparse, datetime, json, os, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
RANK = {"corroborated-primary": 0, "corroborated-secondary": 1, "primary-source": 2, "multi-source": 3, "single-source": 4, "disputed": 6, "not-found": 7, "not-ug": 9}
MODEL_NAMES = {"claude-opus-5-5": "Opus 5.5", "claude-fable-5-1": "Fable 5.1", "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5"}


def load(p, d):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d


def teacher_data(slug):
    folder = ROOT / "teachers" / slug
    if not folder.is_dir():
        sys.exit(f"no teacher folder {folder}")
    sys.path.insert(0, str(ROOT))
    import build  # reuse the build's edit overlay so the data matches the site
    meta = load(folder / "meta.json", {})
    quotes = load(folder / "quotes.json", [])
    edits = load(folder / "edits.json", {})
    data = build.apply_edits({"quotes": quotes, "items": [], "events": [], "people": [], "meta": meta}, edits)
    return data["meta"], data["quotes"]


def pick(quotes, topic, select, book, include_single, limit):
    pool = [q for q in quotes if q.get("verdict") != "not-ug" and q.get("kind") != "paraphrase"]
    if select:
        byid = {q["id"]: q for q in pool}
        pool = [byid[i] for i in select if i in byid]
    else:
        pool = [q for q in pool if q.get("verdict") not in ("disputed", "not-found") and (include_single or q.get("verdict") != "single-source")]
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


def fill(s, v):
    return re.sub(r"\{(\w+)\}", lambda m: str(v[m.group(1)]) if m.group(1) in v else m.group(0), s or "")


def build_prompt(F, f, meta, qs, topic, extra, model, quote_url):
    reserved = meta.get("rights") == "reserved"
    v = {"teacher": meta.get("name"), "identity": meta.get("prompt_identity") or meta.get("name"), "topic": topic or "the teaching as a whole",
         "today": datetime.date.today().isoformat(), "model": MODEL_NAMES.get(model, model), "instagram": meta.get("instagram") or "",
         "quote_url": quote_url, "quote_budget": f.get("quote_budget", 400), "extra": extra or ""}
    instr = fill(f.get("reserved_instructions") if reserved and f.get("reserved_instructions") else f.get("instructions"), v)
    rules = ["- " + fill(r, v) for r in (F.get("rules") or []) + ((F.get("rights") or {}).get("reserved" if reserved else "released") or [])]
    lines = [f"[{q['id']}] ({q.get('book') or 'unassigned'}{', ' + q['chapter'] if q.get('chapter') else ''}; {q.get('verdict') or 'unverified'}) {q['text']}" for q in qs]
    extra_block = f"\n\n# Extra instructions\n{v['extra']}" if f.get("id") != "custom" and v["extra"] else ""
    return f"# Task\n{instr}\n\n# Rules\n" + "\n".join(rules) + extra_block + f"\n\n# Quotations ({len(qs)})\n" + "\n".join(lines)


def call_claude(system, prompt, model, max_tokens):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set (or use --prompt-only)")
    body = json.dumps({"model": model, "max_tokens": max_tokens, "stream": True, "system": system, "messages": [{"role": "user", "content": prompt}]}).encode()
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
    m = re.search(r"^title:\s*(.+)$", text, re.M) or re.search(r"^#\s+(.+)$", text, re.M) or re.search(r"^\*\*(.+?)\*\*", text, re.M)
    return re.sub(r"[\"#*]", "", m.group(1)).strip() if m else fallback


def main():
    F = load(ROOT / "formats.json", {"formats": []})
    ids = [f["id"] for f in F["formats"]]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug"); ap.add_argument("--format", choices=ids, default="5000")
    ap.add_argument("--topic", default=""); ap.add_argument("--select", default="", help="comma-separated quote ids")
    ap.add_argument("--book", default=""); ap.add_argument("--include-single", action="store_true")
    ap.add_argument("--max", type=int, default=0); ap.add_argument("--extra", default="")
    ap.add_argument("--model", default="claude-opus-5-5"); ap.add_argument("--prompt-only", action="store_true")
    ap.add_argument("--to-posts", action="store_true"); ap.add_argument("--out", default="")
    a = ap.parse_args()
    f = next(x for x in F["formats"] if x["id"] == a.format)
    meta, quotes = teacher_data(a.slug)
    site = load(ROOT / "site.json", {})
    quote_url = (site.get("gurus_url") or "").rstrip("/") + f"/{a.slug}/quotes/ID/"
    qs = pick(quotes, a.topic, [s for s in a.select.split(",") if s.strip()], a.book, a.include_single, a.max or f.get("default_max_quotes", 30))
    if not qs:
        sys.exit("no quotations match; widen the topic or pass --include-single")
    prompt = build_prompt(F, f, meta, qs, a.topic, a.extra, a.model, quote_url)
    if a.prompt_only:
        print("# System\n" + (F.get("system") or "") + "\n\n" + prompt); return
    text = call_claude(F.get("system") or "", prompt, a.model, f.get("max_tokens", 8000))
    today = datetime.date.today().isoformat()
    title = title_of(text, f"{f['name']} on {a.topic or 'the teaching'}")
    slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]
    if a.to_posts and a.format == "blog":
        posts = ROOT.parent / "posts" if (ROOT.parent / "posts").is_dir() else ROOT / "posts"
        posts.mkdir(exist_ok=True)
        m = re.search(r"^slug:\s*(.+)$", text, re.M)
        path = pathlib.Path(a.out) if a.out else posts / ((m.group(1).strip() if m else slugify(title)) + ".md")
        path.write_text(text.strip() + "\n", encoding="utf-8")
    else:
        comp = ROOT / "teachers" / a.slug / "compositions"; comp.mkdir(exist_ok=True)
        path = pathlib.Path(a.out) if a.out else comp / f"{today}-{slugify(a.format + '-' + title)}.md"
        fm = (f"---\ntitle: {title}\nteacher: {a.slug}\nformat: {f['name']}\ntopic: {a.topic}\ndate: {today}\nmodel: {a.model}\n"
              f"authorship: model: {a.model}\nquotes: {', '.join(q['id'] for q in qs)}\n---\n\n")
        path.write_text(fm + (text if a.format != "blog" else text).strip() + "\n", encoding="utf-8")
    sys.stderr.write(f"\nwrote {path}\n")


if __name__ == "__main__":
    main()
