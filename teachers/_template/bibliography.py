"""Write catalogue/bibliography.md from items.json: everything the archive knows, grouped.

    python3 bibliography.py

Sections: the contents of each book, editions, translations, the teacher's own
writings, recordings, interviews, writings about the teacher, sites and
archives, images. Every entry carries its year, its confirmation (S confirmed
by a source, T likely, lead not yet confirmed) and its link. If
catalogue/bibliography-intro.md exists it opens the page. Run after every
merge so the page and the records agree.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
meta = json.loads((HERE / "meta.json").read_text(encoding="utf-8")) if (HERE / "meta.json").exists() else {}
name = meta.get("name", HERE.name)

OWN = ("essay", "paper", "article", "book chapter", "foreword", "booklet", "manuscript", "letter", "commentary", "pdf paper", "journal article")


def fmt(i):
    return (i.get("format") or "").lower()


def origins(i):
    return set(i.get("origins") or [i.get("origin") or ""])


def about(i):
    return any("about" in o for o in origins(i))


def section(i):
    f, m = fmt(i), i.get("medium")
    if "table of contents" in f:
        return "contents"
    if "interview" in f:
        return "interviews"
    if about(i):
        return "about"
    if m in ("audio", "video"):
        return "recordings"
    if m == "image":
        return "images"
    if m in ("archive", "community"):
        return "sites"
    if "translation" in f or (i.get("language") and i.get("language") not in ("en", "eng", None) and ("edition" in f or "book" in f or "e-book" in f)):
        return "translations"
    if any(k in f for k in ("edition", "e-book", "ebook", "audiobook", "paperback", "hardback", "kindle")):
        return "editions"
    if any(k in f for k in OWN):
        return "writings"
    return "other texts"


TITLES = [("contents", "The contents of each book"), ("editions", "Editions"), ("translations", "Translations"),
          ("writings", f"{name}'s own writings: essays, papers, chapters, letters"), ("recordings", "Recordings: talks, retreats, radio, video"),
          ("interviews", "Interviews"), ("about", f"Written about {name}"), ("other texts", "Other texts, pages and full-text copies"),
          ("sites", "Sites, archives and communities"), ("images", "Images")]
CONF = {"S": "confirmed", "T": "likely", "lead": "lead, not yet confirmed"}

groups = {}
for i in items:
    groups.setdefault(section(i), []).append(i)

L = []
intro = HERE / "catalogue" / "bibliography-intro.md"
L += [intro.read_text(encoding="utf-8").rstrip(), ""] if intro.exists() else [f"# {name}, everything the archive knows", ""]
L += [f"{len(items)} works, written from the archive's records by `bibliography.py`; "
      f"{sum(1 for i in items if i.get('confidence') == 'S')} confirmed by a source, "
      f"{sum(1 for i in items if i.get('confidence') == 'T')} likely, "
      f"{sum(1 for i in items if i.get('confidence') not in ('S', 'T'))} leads not yet confirmed.", ""]
L += ["| Section | Works |", "|---|---|"] + [f"| {t} | {len(groups.get(k, []))} |" for k, t in TITLES if groups.get(k)] + [""]
for key, title in TITLES:
    g = groups.get(key)
    if not g:
        continue
    L += [f"## {title}", ""]
    for i in sorted(g, key=lambda x: (x.get("year") or 9999, x["title"].lower())):
        yr = i.get("year") or "undated"
        link = f" [link]({i['url']})" if i.get("url") else ""
        L.append(f"- **{i['title']}** · {yr} · {CONF.get(i.get('confidence'), 'lead, not yet confirmed')}{link}")
        d = re.sub(r"\s+", " ", (i.get("description") or "")).strip()
        if d:
            L.append(f"  {d if key == 'contents' else d[:400] + ('…' if len(d) > 400 else '')}")
    L.append("")
(HERE / "catalogue").mkdir(exist_ok=True)
(HERE / "catalogue" / "bibliography.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"catalogue/bibliography.md: {len(items)} works in " + ", ".join(f"{k} {len(v)}" for k, v in groups.items()))
