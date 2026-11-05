"""Download every file the archive lists, on any machine whose network reaches the hosts.

    pip install internetarchive yt-dlp requests pypdf
    python fetch.py                  # everything, resumable; run it again to continue
    python fetch.py --only audio,video --dry-run
    python fetch.py --list           # what would be fetched, by kind

Windows, macOS and Linux alike. ffmpeg on the PATH lets yt-dlp join the best
video and audio; without it the best single file is taken.

What it fetches, from download-manifest.json (written by manifest.py from
items.json):

    archive.org   every file of every item, and every item inside a collection
                  (the tapes, radio and TV recordings, scans, PDFs, images)
    YouTube       every video and every video of a playlist or channel, with
                  its description, thumbnail and every subtitle track, made
                  and automatic, which are the transcripts of the recordings
    SoundCloud    every track
    Wikisource    the book texts, as wikitext and as rendered HTML
    PDFs          as they are
    pages         every other page as HTML, and from pages of images or
                  photographs every image they show

Everything lands in downloads/<kind>/ beside this script. Media files never go
into git. What was fetched is recorded in downloads/fetch-log.jsonl (one line
per attempt) and holdings.json beside this script (item id, files, bytes,
sha256), which is small, goes into git, and lets coverage.py count what the
archive holds. Afterwards, extract-text.py turns the texts into plain text and
find-quotes.py checks every quotation against them.
"""
import argparse
import datetime
import hashlib
import html
import json
import pathlib
import re
import shutil
import sys
import time
from urllib.parse import urljoin, urlparse

HERE = pathlib.Path(__file__).resolve().parent
DL = HERE / "downloads"
LOG = DL / "fetch-log.jsonl"
HOLD = HERE / "holdings.json"
UA = "hanjopurebuddha-archive-fetch/1.0 (open archive of a teacher's words)"
IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff", ".bmp")
KINDS = ("archive_org", "youtube", "soundcloud", "wikisource", "pdf", "well", "other_pages")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def log(rec):
    DL.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": now(), **rec}, ensure_ascii=False) + "\n")


def safe(s, n=120):
    return re.sub(r"[^\w.\- ]+", "_", s, flags=re.UNICODE).strip(" ._")[:n] or "item"


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def session():
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = UA
    return s


def get(s, url, dest, tries=3):
    """One file over HTTP, resumable by skipping what is already whole."""
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    for k in range(tries):
        try:
            with s.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with part.open("wb") as f:
                    for b in r.iter_content(1 << 16):
                        f.write(b)
            part.replace(dest)
            return dest
        except Exception as e:  # noqa
            if k == tries - 1:
                raise
            time.sleep(2 ** (k + 1))


# ---- archive.org
def fetch_archive(rec, args):
    import internetarchive as ia
    ident = rec["identifier"]
    root = DL / "archive_org"
    item = ia.get_item(ident)
    md = item.metadata or {}
    idents = [ident]
    if md.get("mediatype") == "collection":
        idents = [r["identifier"] for r in ia.search_items(f"collection:{ident}")]
    files = []
    for i in idents:
        if args.dry_run:
            files.append(f"{i}/*")
            continue
        it = ia.get_item(i)
        it.download(destdir=str(root), retries=3, ignore_existing=True, verbose=False,
                    glob_pattern=args.ia_glob or None)
        files += [str(p.relative_to(DL)) for p in (root / i).rglob("*") if p.is_file()]
    return files


# ---- YouTube and SoundCloud
def fetch_ytdlp(rec, args, kind):
    import yt_dlp
    url = rec["url"]
    if rec.get("video_id"):
        url = f"https://www.youtube.com/watch?v={rec['video_id']}"
    elif rec.get("playlist_id"):
        url = f"https://www.youtube.com/playlist?list={rec['playlist_id']}"
    root = DL / kind
    root.mkdir(parents=True, exist_ok=True)
    opts = {
        "outtmpl": str(root / "%(uploader,channel|unknown)s" / "%(title).150B [%(id)s].%(ext)s"),
        "format": "bv*+ba/b" if shutil.which("ffmpeg") else "b",
        "download_archive": str(root / ".archive"),
        "writeinfojson": True, "writedescription": True, "writethumbnail": True,
        "writesubtitles": True, "writeautomaticsub": True, "subtitleslangs": ["all", "-live_chat"],
        "subtitlesformat": "vtt/srt/best", "ignoreerrors": True, "retries": 5, "quiet": True,
        "no_warnings": True, "simulate": args.dry_run, "skip_download": args.dry_run,
    }
    before = set(root.rglob("*"))
    with yt_dlp.YoutubeDL(opts) as y:
        y.download([url])
    return [str(p.relative_to(DL)) for p in set(root.rglob("*")) - before if p.is_file()]


# ---- Wikisource
def fetch_wikisource(rec, args, s):
    u = rec["url"]
    title = u.split("/wiki/")[-1].split("#")[0] if "/wiki/" in u else rec["id"]
    host = urlparse(u).netloc
    root = DL / "wikisource"
    out = []
    for action, ext in (("raw", "wiki"), ("render", "html")):
        dest = root / f"{safe(title)}.{ext}"
        if not args.dry_run:
            get(s, f"https://{host}/w/index.php?title={title}&action={action}", dest)
        out.append(str(dest.relative_to(DL)))
    return out


# ---- PDFs, the WELL, other pages, and the images on image pages
def fetch_page(rec, args, s, kind):
    u = rec["url"]
    p = urlparse(u)
    name = safe(p.netloc + p.path.replace("/", "_") + ("_" + p.query if p.query else ""))
    root = DL / ("pdf" if kind == "pdf" else "well" if kind == "well" else "pages")
    if p.path.lower().endswith(".pdf") or kind == "pdf":
        dest = root / (name if name.lower().endswith(".pdf") else name + ".pdf")
    elif p.path.lower().endswith(IMG_EXT):
        dest = DL / "images" / name
    else:
        dest = root / (name if name.lower().endswith((".html", ".htm")) else name + ".html")
    if args.dry_run:
        return [str(dest.relative_to(DL))]
    get(s, u, dest)
    out = [str(dest.relative_to(DL))]
    if rec.get("medium") == "image" and dest.suffix == ".html":
        out += images_on(dest, u, s, rec)
    return out


def images_on(page, base, s, rec):
    """Every image a page of images shows: <img>, srcset, og:image, and links to image files."""
    t = page.read_text(encoding="utf-8", errors="replace")
    urls = re.findall(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', t)
    urls += re.findall(r'<img[^>]+src=["\']([^"\']+)', t)
    for ss in re.findall(r'srcset=["\']([^"\']+)', t):
        urls += [c.strip().split(" ")[0] for c in ss.split(",") if c.strip()]
    urls += [h for h in re.findall(r'href=["\']([^"\']+)', t) if urlparse(h).path.lower().endswith(IMG_EXT)]
    out, seen = [], set()
    root = DL / "images" / rec["id"]
    for raw in urls:
        u = urljoin(base, html.unescape(raw))
        if u in seen or u.startswith("data:") or not urlparse(u).path.lower().endswith(IMG_EXT):
            continue
        seen.add(u)
        dest = root / safe(urlparse(u).path.split("/")[-1])
        try:
            get(s, u, dest)
            if dest.stat().st_size >= 2048:  # icons and spacers are not the photographs
                out.append(str(dest.relative_to(DL)))
            else:
                dest.unlink()
        except Exception as e:  # noqa
            log({"id": rec["id"], "image": u, "ok": False, "error": str(e)[:300]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="", help="kinds or media, e.g. archive_org,youtube or audio,video,image")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--ia-glob", default="", help="archive.org files to take, e.g. '*.mp3|*.pdf' (default all)")
    args = ap.parse_args()
    man = json.loads((HERE / "download-manifest.json").read_text(encoding="utf-8"))
    if man.get("fetch") is False:
        print("Nothing is fetched for this teacher. " + (man.get("note") or ""))
        return
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    todo = [(k, r) for k in KINDS for r in man.get(k, []) if not only or k in only or r.get("medium") in only]
    if args.list:
        from collections import Counter
        print(dict(Counter(k for k, _ in todo)), dict(Counter(r.get("medium") for _, r in todo)))
        return
    hold = json.loads(HOLD.read_text(encoding="utf-8")) if HOLD.exists() else {}
    s = session()
    ok = fail = 0
    for n, (k, r) in enumerate(todo, 1):
        try:
            if k == "archive_org":
                files = fetch_archive(r, args)
            elif k in ("youtube", "soundcloud"):
                files = fetch_ytdlp(r, args, k)
            elif k == "wikisource":
                files = fetch_wikisource(r, args, s)
            else:
                files = fetch_page(r, args, s, k)
            ok += 1
            log({"id": r["id"], "kind": k, "url": r["url"], "ok": True, "files": len(files), "dry_run": args.dry_run})
            if not args.dry_run:
                h = hold.setdefault(r["id"], {"title": r["title"], "kind": k, "url": r["url"], "files": {}})
                for f in files:
                    p = DL / f
                    if p.is_file() and f not in h["files"]:
                        h["files"][f] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
                h["fetched"] = now()
            print(f"[{n}/{len(todo)}] ok   {k:12} {r['title'][:70]}  ({len(files)} files)")
        except Exception as e:  # noqa
            fail += 1
            log({"id": r["id"], "kind": k, "url": r["url"], "ok": False, "error": str(e)[:500]})
            print(f"[{n}/{len(todo)}] FAIL {k:12} {r['title'][:70]}  {str(e)[:120]}")
        if not args.dry_run and n % 10 == 0:
            HOLD.write_text(json.dumps(hold, ensure_ascii=False, indent=1), encoding="utf-8")
    if not args.dry_run:
        HOLD.write_text(json.dumps(hold, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done: {ok} ok, {fail} failed. Log in {LOG}. Run again to continue what failed.")


if __name__ == "__main__":
    sys.exit(main())
