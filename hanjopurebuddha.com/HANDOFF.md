# Handoff — brief for a Claude on a machine that can reach GitHub and the hosts

Paste the block below to a Claude Code session running where `gh` is
authenticated and archive.org, people.well.com, en.wikisource.org,
youtube.com and soundcloud.com are reachable.

```
You are finishing the hanjopurebuddha.com guru browsing section and its first
teacher archive, U.G. Krishnamurti. All the work so far is in the GitHub
repository DrThomasAger/drthomasager.com. Do every step yourself, in order,
without stopping to ask. Report at the end what you did and what remains.

CONTEXT
- The site lives in the folder hanjopurebuddha.com/ inside that repository and
  also exists as its own branch, hanjopurebuddha-site, with its own history.
- The teacher folder is hanjopurebuddha.com/teachers/ug-krishnamurti/. Read its
  README.md, ONCE-OPEN.md and catalogue/NEXT-WAVE.md first. They explain the
  data files, the pipeline, the run order, and exactly what is still open.
- Only U.G. Krishnamurti (Uppaluri Gopala Krishnamurti, 1918–2007). Never
  Jiddu Krishnamurti; discard anything from kfoundation.org, jkrishnamurti.org,
  kfa.org, krishnamurti.org.
- Every item and quote keeps the URLs it was found at. Never invent a source.

STEP 1 — the new repository
  git clone https://github.com/DrThomasAger/drthomasager.com && cd drthomasager.com
  gh repo create DrThomasAger/hanjopurebuddha.com --public --description \
    "A guru browsing section: enlightened people, their words, their media, every line cited."
  bash hanjopurebuddha.com/publish-to-new-repo.sh https://github.com/DrThomasAger/hanjopurebuddha.com.git
  gh api -X POST repos/DrThomasAger/hanjopurebuddha.com/pages -f build_type=workflow
  Wait for the first "Build and publish hanjopurebuddha.com" workflow run to succeed
  (gh run list --repo DrThomasAger/hanjopurebuddha.com --watch).

STEP 2 — the domain
  If a Cloudflare or registrar API token is available, create A records for
  hanjopurebuddha.com → 185.199.108.153, 185.199.109.153, 185.199.110.153,
  185.199.111.153 and CNAME www → drthomasager.github.io. Then
  gh api -X PUT repos/DrThomasAger/hanjopurebuddha.com/pages -f cname=hanjopurebuddha.com
  and enable HTTPS once the certificate is issued. If no DNS access exists,
  write the exact records needed into the final report.

STEP 3 — the files and the local verification (from the new repository's clone)
  cd teachers/ug-krishnamurti
  pip install internetarchive yt-dlp pypdf
  bash enumerate.sh
  python3 ingest-enumerations.py scratch
  python3 merge.py scratch
  bash fetch.sh            # resumable; re-run until downloads/fetch.log shows no "fail"
  python3 extract-text.py
  python3 find-quotes.py
  python3 merge.py scratch
  python3 check-links.py
  python3 integrity.py && python3 readme.py && python3 manifest.py
  cd ../.. && python3 build.py
  Commit everything except downloads/ and enumerations/ (already ignored) and push.

STEP 4 — close the items a browser can reach (catalogue/NEXT-WAVE.md)
  - Pull the full archive.org collection listings and compare against items.json.
  - List every video of YouTube channels UCRLQIvQcoF41xZdrtKMXSvg and
    UCG5ccYuEKBfhGvqGxNwjXdw and playlists PL0440AC751B2F84E9,
    PLJGnfFmap7N9BTHNv4mIaqgyv-Co1K0Sy, PLI3BX4bvdDGoIibgFOUbQL-mSxOFdqW0w,
    PL4D24B9FE63001E98 (enumerate.sh does this; confirm the counts).
  - Wayback Machine: capture range and operator of ugkrishnamurti.org.
  - Who holds the WELL account people.well.com/user/jct (a WELL member lookup).
  - Reddit permalinks for the ten threads in catalogue/wave8-archive-reddit.md
    and the size of r/UGKrishnamurti.
  - Photographs of Chalet Sunbeam (Gstaad), Poornakutee and Hridaya Vihar
    (Bangalore), the Vallecrosia villa, the Yercaud house.
  Add each finding as a record in the shared schema (see
  teachers/_template/GATHERING.md), with URL and sources, merge, rebuild, push.

STEP 5 — repair what the checks reveal
  - For every quote whose verdict is single-source, disputed, not-found or
    not-ug after find-quotes.py, read the primary text and set the correct
    book, chapter and wording in corrections.json; re-merge.
  - Fix or replace dead links from link-status.md; keep the original URL in
    sources with a note, add the live one.
  - Resolve the 7 event date conflicts where a primary source settles them.

STEP 6 — the second teacher (only if asked)
  Copy teachers/_template to teachers/<slug>, fill meta.json, run the seven
  gathering briefs in GATHERING.md with parallel researchers, then the merge,
  integrity, readme, manifest and build steps. The index grid picks it up.

RULES
  - Commit and push after each step. Keep the attribution footer lines the
    repository's commits already carry.
  - Never bypass a network policy or a site's terms; if a host is refused,
    record it in NEXT-WAVE.md and move on.
  - Media files never go into git; texts, verification and link status do.
  - The response format and word preferences in the user's instructions apply
    to everything you write to them.
```
