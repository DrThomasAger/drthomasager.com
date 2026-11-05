#!/usr/bin/env bash
# Fetch every PDF, tape and radio recording, scan, photograph, video and
# transcript the archive lists. Resumable; files land in teachers/<t>/downloads/.
cd "$(dirname "$0")" || exit 1
python3 -m pip install --upgrade internetarchive yt-dlp requests pypdf
for t in teachers/*/; do
  [ "$(basename "$t")" = _template ] && continue
  [ -f "$t/fetch.py" ] || continue
  echo "=== $(basename "$t")"
  (cd "$t" && python3 fetch.py && python3 extract-text.py && python3 find-quotes.py)
done
python3 coverage.py
