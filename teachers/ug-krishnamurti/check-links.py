"""Check every URL cited by items, quotes, events and people. Run where the
hosts are reachable.

    python3 check-links.py            # writes link-status.json and link-status.md

Uses HEAD then GET on failure, 15 s timeout, 8 workers. Records status code,
final URL after redirects, and content type. A 404/410 is a dead link; a
403/429 is "blocked here"; connection errors are "unreachable".
"""
import json, pathlib, concurrent.futures, urllib.request, urllib.error, ssl, time
HERE = pathlib.Path(__file__).resolve().parent
urls = set()
for name in ("items.json", "quotes.json", "events.json", "people.json"):
    p = HERE / name
    if p.exists():
        for rec in json.loads(p.read_text(encoding="utf-8")):
            if rec.get("url"): urls.add(rec["url"])
            for s in rec.get("sources") or []: urls.add(s)
urls = sorted(u for u in urls if u.startswith("http"))
ctx = ssl.create_default_context()
UA = "Mozilla/5.0 (hanjopurebuddha.com link check)"

def check(u):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return {"url": u, "status": r.status, "final": r.geturl(), "type": r.headers.get("Content-Type", "")[:60], "verdict": "ok"}
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (405, 403, 400):
                continue
            v = "dead" if e.code in (404, 410) else ("blocked" if e.code in (401, 403, 429, 451) else "error")
            return {"url": u, "status": e.code, "final": None, "type": "", "verdict": v}
        except Exception as e:  # noqa
            if method == "HEAD":
                continue
            return {"url": u, "status": None, "final": None, "type": "", "verdict": "unreachable", "error": str(e)[:120]}
    return {"url": u, "status": None, "final": None, "type": "", "verdict": "unreachable"}

t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    results = list(ex.map(check, urls))
summary = {}
for r in results:
    summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
(HERE / "link-status.json").write_text(json.dumps({"checked": len(results), "summary": summary, "seconds": round(time.time() - t0), "results": results}, ensure_ascii=False, indent=1), encoding="utf-8")
lines = ["# Link status", "", f"{len(results)} URLs checked. " + ", ".join(f"{k} {v}" for k, v in sorted(summary.items())), ""]
for v in ("dead", "unreachable", "blocked", "error"):
    rows = [r for r in results if r["verdict"] == v]
    if rows:
        lines += [f"## {v} ({len(rows)})", ""] + [f"- {r['url']} ({r.get('status')})" for r in rows] + [""]
(HERE / "link-status.md").write_text("\n".join(lines), encoding="utf-8")
print(summary)
