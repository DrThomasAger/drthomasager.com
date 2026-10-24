"""Turn downloaded texts into chapter-split plain text for local quote checks.

    python3 extract-text.py            # reads downloads/, writes texts/<book>/<chapter>.txt

Handles Wikisource wikitext (downloads/wikisource/*.wiki), WELL HTML pages
(downloads/well/*.htm*), and PDFs (downloads/pdf/*.pdf, needs `pip install
pypdf`). Then `python3 find-quotes.py` locates every quote in those texts.
"""
import pathlib, re, html
HERE = pathlib.Path(__file__).resolve().parent
DL, OUT = HERE / "downloads", HERE / "texts"
OUT.mkdir(exist_ok=True)

def clean_wiki(s):
    s = re.sub(r"\{\{[^}]*\}\}", " ", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"'{2,}", "", s)
    return html.unescape(re.sub(r"[ \t]+", " ", s)).strip()

def clean_html(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"[ \t]+", " ", s)).strip()

def split_chapters(text, name):
    parts = re.split(r"\n(?==+ ?[^=\n]{3,80} ?=+\n)|\n(?=(?:Chapter|CHAPTER|Part|PART) [\dIVX]+)", text)
    if len(parts) < 2:
        return {name: text}
    out, i = {}, 0
    for p in parts:
        head = p.strip().splitlines()[0][:60] if p.strip() else f"part-{i}"
        i += 1
        out[re.sub(r"[^A-Za-z0-9]+", "-", head).strip("-").lower() or f"part-{i}"] = p
    return out

n = 0
for f in (DL / "wikisource").glob("*.wiki") if (DL / "wikisource").exists() else []:
    book = f.stem.split("_")[0].lower()
    for ch, body in split_chapters(clean_wiki(f.read_text(encoding="utf-8", errors="replace")), f.stem).items():
        d = OUT / book; d.mkdir(exist_ok=True); (d / f"{ch}.txt").write_text(body, encoding="utf-8"); n += 1
for f in (DL / "well").glob("*.htm*") if (DL / "well").exists() else []:
    d = OUT / "well"; d.mkdir(exist_ok=True)
    (d / f"{f.stem}.txt").write_text(clean_html(f.read_text(encoding="utf-8", errors="replace")), encoding="utf-8"); n += 1
try:
    from pypdf import PdfReader
    for f in (DL / "pdf").glob("*.pdf") if (DL / "pdf").exists() else []:
        d = OUT / "pdf"; d.mkdir(exist_ok=True)
        (d / f"{f.stem}.txt").write_text("\n".join((pg.extract_text() or "") for pg in PdfReader(str(f)).pages), encoding="utf-8"); n += 1
except ImportError:
    print("pypdf not installed; PDFs skipped")
print(f"{n} text files written under {OUT}")
