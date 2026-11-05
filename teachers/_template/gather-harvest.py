"""Gather the harvest workflow's shards into a teacher folder.

    python gather-harvest.py <shards-dir> <teacher-folder>

Each shard (one per kind of file) carries holdings.json, local-verification.json,
transcripts/ and downloads/fetch-log.jsonl. Holdings are joined item by item and
file by file onto the folder's own holdings.json; quotation checks are joined by
quote id; transcripts are copied in; the fetch logs are appended to
harvest-log.jsonl. Nothing already recorded is lost.
"""
import json
import pathlib
import shutil
import sys

shards, folder = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])


def load(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
    except ValueError:
        return default


hold = load(folder / "holdings.json", {})
checks = {v["id"]: v for v in load(folder / "local-verification.json", [])}
logs = []
n_tr = 0
for s in sorted(p for p in shards.iterdir() if p.is_dir()):
    base = next((p.parent for p in s.rglob("holdings.json")), None) or next((p.parent for p in s.rglob("transcripts")), s)
    for iid, h in load(base / "holdings.json", {}).items():
        cur = hold.setdefault(iid, {"files": {}})
        done = bool(cur.get("complete")) or bool(h.get("complete"))
        cur.update({k: v for k, v in h.items() if k not in ("files", "complete", "fetched")})
        cur["complete"] = done
        for f, v in (h.get("files") or {}).items():
            if f not in cur["files"] or (v.get("asset") and not cur["files"][f].get("asset")):
                cur["files"][f] = v
        if h.get("fetched"):
            cur["fetched"] = max(cur.get("fetched") or "", h["fetched"])
    for v in load(base / "local-verification.json", []):
        checks[v["id"]] = v
    for t in (base / "transcripts").glob("*.txt") if (base / "transcripts").is_dir() else []:
        (folder / "transcripts").mkdir(exist_ok=True)
        shutil.copy(t, folder / "transcripts" / t.name)
        n_tr += 1
    lg = base / "downloads" / "fetch-log.jsonl"
    if lg.exists():
        logs += [l for l in lg.read_text(encoding="utf-8").splitlines() if l.strip()]

(folder / "holdings.json").write_text(json.dumps(hold, ensure_ascii=False, indent=1), encoding="utf-8")
(folder / "local-verification.json").write_text(json.dumps(list(checks.values()), ensure_ascii=False, indent=1), encoding="utf-8")
with (folder / "harvest-log.jsonl").open("a", encoding="utf-8") as f:
    for l in logs:
        f.write(l + "\n")
files = sum(len(h.get("files") or {}) for h in hold.values())
print(f"holdings: {len(hold)} items, {files} files; quotation checks: {len(checks)}; transcripts copied: {n_tr}; log lines: {len(logs)}")
