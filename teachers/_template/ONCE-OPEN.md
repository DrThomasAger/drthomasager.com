# When the hosts are reachable — the run order

Everything below is prepared and tested for syntax; none of it has run
here because the gathering environment's network policy refuses the hosts.
On a machine that can reach archive.org, people.well.com, en.wikisource.org,
youtube.com and soundcloud.com (or in this environment once those are
allowed), run in this order from `teachers/ug-krishnamurti/`:

```
pip install internetarchive yt-dlp pypdf

bash enumerate.sh                      # 1. list the collections search could not expose
python3 ingest-enumerations.py scratch # 2. turn the listings into merge-ready JSON
python3 merge.py scratch               # 3. fold them into items.json (dedupes by URL)

bash fetch.sh                          # 4. pull every retrievable item into downloads/ (resumable)
python3 extract-text.py                # 5. Wikisource, WELL and PDF texts -> texts/<book>/<chapter>.txt
python3 find-quotes.py                 # 6. locate every quote in the texts -> local-verification.json
python3 merge.py scratch               # 7. verdicts upgrade where the text itself carries the line

python3 check-links.py                 # 8. status of every cited URL -> link-status.md
python3 integrity.py && python3 readme.py && python3 manifest.py
cd ../.. && python3 build.py           # 9. rebuild the site
```

`downloads/` and `enumerations/` are ignored by git (media is large and
lives at its hosts); `texts/`, `local-verification.json` and
`link-status.*` are committed so the verification is reproducible.

For the new repository: from the drthomasager.com checkout,
`bash hanjopurebuddha.com/publish-to-new-repo.sh <new-repo-url>`.
