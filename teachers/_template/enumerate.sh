#!/usr/bin/env bash
# Enumerate the collections the search engines could not expose, on a machine
# that can reach the hosts. Output lands in enumerations/ and is turned into
# merge-ready JSON by ingest-enumerations.py.
#   pip install internetarchive yt-dlp
#   bash enumerate.sh && python3 ingest-enumerations.py && python3 merge.py <scratch-with-the-json>
set -u
mkdir -p enumerations
# archive.org: every item whose identifier starts with ug_, plus the two collections
ia search 'identifier:ug_*' --itemlist > enumerations/archive-ug-identifiers.txt
ia search 'collection:ugkrishnamurti-audio' --fields identifier,title,date,description,mediatype,runtime -j > enumerations/archive-audio-collection.jsonl 2>/dev/null || true
ia search 'collection:ugkrishnamurti-video' --fields identifier,title,date,description,mediatype,runtime -j > enumerations/archive-video-collection.jsonl 2>/dev/null || true
ia search 'krishnamurti AND NOT jiddu AND (uppaluri OR "u.g." OR "ug krishnamurti")' --fields identifier,title,date,mediatype -j > enumerations/archive-search.jsonl 2>/dev/null || true
# YouTube: channels and playlists, flat (metadata only, no downloads)
for src in \
  https://www.youtube.com/channel/UCRLQIvQcoF41xZdrtKMXSvg/videos \
  https://www.youtube.com/channel/UCG5ccYuEKBfhGvqGxNwjXdw/videos \
  "https://www.youtube.com/playlist?list=PL0440AC751B2F84E9" \
  "https://www.youtube.com/playlist?list=PLJGnfFmap7N9BTHNv4mIaqgyv-Co1K0Sy" \
  "https://www.youtube.com/playlist?list=PLI3BX4bvdDGoIibgFOUbQL-mSxOFdqW0w" \
  "https://www.youtube.com/playlist?list=PL4D24B9FE63001E98" ; do
  name=$(echo "$src" | sed 's#.*/##; s/[^A-Za-z0-9_=-]/_/g')
  yt-dlp --flat-playlist -J "$src" > "enumerations/youtube-$name.json" 2>/dev/null || echo "failed: $src" >&2
done
# SoundCloud accounts
for acct in krishnamorthy krishnamorthy00 krishnamorthy01 krishnamorthy02 petermaverick; do
  yt-dlp --flat-playlist -J "https://soundcloud.com/$acct" > "enumerations/soundcloud-$acct.json" 2>/dev/null || echo "failed: $acct" >&2
done
# The WELL index pages, for the clip list with durations
mkdir -p enumerations/well
wget -q -nc -P enumerations/well https://people.well.com/user/jct/index_main.html https://people.well.com/user/jct/lists.html https://people.well.com/user/jct/links.htm || true
ls -la enumerations
