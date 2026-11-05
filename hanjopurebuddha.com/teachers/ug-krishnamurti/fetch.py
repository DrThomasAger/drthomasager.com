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
MEDIA_BIN = (".mp3", ".mp4", ".m4a", ".ogg", ".ogv", ".opus", ".wav", ".flac", ".webm", ".mkv", ".avi", ".mov",
             ".mpg", ".mpeg", ".ra", ".rm", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff", ".bmp", ".jp2", ".zip", ".torrent")
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


def duration(p):
    """Seconds of a recording, through ffprobe when it is on the PATH."""
    if p.suffix.lower() not in MEDIA_BIN[:15] or not shutil.which("ffprobe"):
        return None
    import subprocess
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                           capture_output=True, text=True, timeout=60)
        return round(float(r.stdout.strip()), 1) if r.stdout.strip() else None
    except Exception:  # noqa
        return None


RELEASE = {}  # tag -> [current tag, assets in it]


def release_for(tag):
    """The release that takes the next asset: tag, then tag-2, tag-3 ..., each kept under GitHub's 1000 assets."""
    import subprocess
    cur = RELEASE.get(tag)
    if cur is None:
        n = 1
        while True:
            t = tag if n == 1 else f"{tag}-{n}"
            r = subprocess.run(["gh", "release", "view", t, "--json", "assets", "-q", ".assets | length"], capture_output=True, text=True)
            if r.returncode != 0:
                subprocess.run(["gh", "release", "create", t, "--title", t, "--notes", f"Assets of {tag}, continued."], capture_output=True)
                cur = [t, 0]; break
            if int(r.stdout.strip() or 0) < 990:
                cur = [t, int(r.stdout.strip() or 0)]; break
            n += 1
        RELEASE[tag] = cur
    if cur[1] >= 990:
        base, n = tag, (int(cur[0].rsplit("-", 1)[1]) + 1 if cur[0] != tag else 2)
        t = f"{base}-{n}"
        subprocess.run(["gh", "release", "create", t, "--title", t, "--notes", f"Assets of {tag}, continued."], capture_output=True)
        cur[:] = [t, 0]
    return cur


def upload(tag, p, name):
    """One file to a GitHub release, as an asset under the given name; returns its download address.
    Waits out GitHub's rate limit rather than dropping the file."""
    import os, subprocess
    if p.stat().st_size == 0 or p.stat().st_size >= 2 * 1024 ** 3:
        log({"asset": name, "ok": False, "error": f"size {p.stat().st_size} outside what a release asset takes"})
        return None
    tmp = p.with_name(name)
    if tmp != p:
        p.rename(tmp)
    ok, rel = False, None
    try:
        for attempt in range(40):
            rel = release_for(tag)
            r = subprocess.run(["gh", "release", "upload", rel[0], str(tmp), "--clobber"], capture_output=True, text=True, timeout=3600)
            if r.returncode == 0:
                ok = True; rel[1] += 1; break
            e = r.stderr or ""
            if "rate limit" in e.lower() or "secondary" in e.lower():
                time.sleep(90); continue
            if "422" in e and ("already_exists" in e or "Validation" in e):
                rel[1] = 990; continue  # the release is full or the name is taken there; roll on
            log({"asset": name, "ok": False, "error": e[:300]}); break
    finally:
        if tmp.exists() and tmp != p:
            tmp.rename(p)
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    return f"https://github.com/{repo}/releases/download/{rel[0]}/{name}" if ok else None


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
        skip = ["*_files.xml", "*_meta.xml", "*_reviews.xml", "*_meta.sqlite", "*.sqlite", "*.torrent", "__ia_thumb.jpg", "*_itemimage.jpg"]
        common = dict(destdir=str(root), retries=3, ignore_existing=True, verbose=False, ignore_errors=True, exclude_pattern=skip)
        if args.ia_glob:
            it.download(glob_pattern=args.ia_glob, **common)
        else:
            it.download(source=["original"], **common)  # what was uploaded: tapes, scans, photographs
            if not args.ia_originals:  # and the copies every player opens
                it.download(formats=["VBR MP3", "h.264", "MPEG4", "512Kb MPEG4", "Text PDF", "DjVuTXT"], **common)
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
    errs = YtLog()
    opts = {
        "outtmpl": str(root / "%(uploader,channel|unknown)s" / "%(title).150B [%(id)s].%(ext)s"),
        "format": "bv*+ba/b" if shutil.which("ffmpeg") else "b",
        "download_archive": str(root / ".archive"),
        "writeinfojson": True, "writedescription": True, "writethumbnail": True,
        "writesubtitles": True, "writeautomaticsub": True, "subtitleslangs": ["en", "en-orig", ".*-orig"],
        "extractor_args": {"youtube": {"player_client": ["default", "tv_simply", "web_safari", "mweb"]}},
        "logger": errs,
        "subtitlesformat": "vtt/srt/best", "ignoreerrors": True, "retries": 5, "quiet": True,
        "no_warnings": True, "simulate": args.dry_run, "skip_download": args.dry_run,
    }
    before = set(root.rglob("*"))
    with yt_dlp.YoutubeDL(opts) as y:
        y.download([url])
    files = [str(p.relative_to(DL)) for p in set(root.rglob("*")) - before if p.is_file()]
    if not args.dry_run and not any(f.lower().endswith(MEDIA_BIN[:15]) for f in files) and errs.errors:
        raise RuntimeError("no recording came down: " + " | ".join(errs.errors[:3]))
    return files


class YtLog:
    """yt-dlp's messages, so a refused video is reported instead of passing as done."""
    def __init__(self):
        self.errors = []
    def debug(self, m): pass
    def info(self, m): pass
    def warning(self, m): pass
    def error(self, m):
        self.errors.append(re.sub(r"\s+", " ", str(m))[:200])


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
    ap.add_argument("--ia-originals", action="store_true", help="archive.org: only the files as uploaded, not the derived copies")
    ap.add_argument("--shard", default="", help="i/n: take only every n-th address, starting at i (for parallel runners)")
    ap.add_argument("--give-up-after", type=int, default=0, help="stop a kind after this many refusals in a row")
    ap.add_argument("--skip-held", action="store_true", help="leave out items holdings.json already holds files for")
    ap.add_argument("--release", default="", help="a GitHub release tag: each file is uploaded to it as an asset "
                    "with the gh CLI as soon as it comes down (needs GH_TOKEN), then removed from disk")
    ap.add_argument("--discard-media", action="store_true",
                    help="after hashing and measuring, delete recordings and images and keep only texts, subtitles and "
                         "metadata (for a machine that verifies and transcribes but keeps nothing)")
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
    if args.skip_held:
        todo = [(k, r) for k, r in todo if not hold.get(r["id"], {}).get("complete")]
    if args.shard:
        i, n = (int(x) for x in args.shard.split("/"))
        todo = [x for j, x in enumerate(todo) if j % n == i]
    s = session()
    ok = fail = 0
    streak, given_up = {}, set()
    for n, (k, r) in enumerate(todo, 1):
        if k in given_up:
            continue
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
            streak[k] = 0
            log({"id": r["id"], "kind": k, "url": r["url"], "ok": True, "files": len(files), "dry_run": args.dry_run})
            if not args.dry_run:
                h = hold.setdefault(r["id"], {"title": r["title"], "kind": k, "url": r["url"], "files": {}})
                for f in files:
                    p = DL / f
                    if p.is_file() and f not in h["files"]:
                        h["files"][f] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
                        d = duration(p)
                        if d:
                            h["files"][f]["seconds"] = d
                    if args.release and p.is_file() and not h["files"][f].get("asset"):
                        name = safe(f"{r['id']}__{f.replace('/', '__')}", 240).replace(' ', '_')
                        u = upload(args.release, p, name)
                        if u:
                            h["files"][f]["asset"] = u
                            h["files"][f]["kept"] = "release"
                            if p.suffix.lower() in MEDIA_BIN:  # texts stay for extract-text.py and find-quotes.py
                                p.unlink()
                    if args.discard_media and p.is_file() and p.suffix.lower() in MEDIA_BIN:
                        p.unlink()
                        h["files"][f]["kept"] = False
                h["fetched"] = now()
                h["complete"] = bool(h["files"]) and (not args.release or all(v.get("asset") for v in h["files"].values())) and (
                    k not in ("youtube", "soundcloud") or any(x.lower().endswith(MEDIA_BIN[:15]) for x in h["files"]))
            print(f"[{n}/{len(todo)}] ok   {k:12} {r['title'][:70]}  ({len(files)} files)")
        except Exception as e:  # noqa
            fail += 1
            streak[k] = streak.get(k, 0) + 1
            log({"id": r["id"], "kind": k, "url": r["url"], "ok": False, "error": str(e)[:500]})
            if args.give_up_after and streak[k] >= args.give_up_after:
                print(f"{k}: {streak[k]} refusals in a row; leaving the rest of this kind for another route")
                given_up.add(k)
            print(f"[{n}/{len(todo)}] FAIL {k:12} {r['title'][:70]}  {str(e)[:120]}")
        if not args.dry_run and n % 10 == 0:
            HOLD.write_text(json.dumps(hold, ensure_ascii=False, indent=1), encoding="utf-8")
    if not args.dry_run:
        HOLD.write_text(json.dumps(hold, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done: {ok} ok, {fail} failed. Log in {LOG}. Run again to continue what failed.")


if __name__ == "__main__":
    sys.exit(main())
