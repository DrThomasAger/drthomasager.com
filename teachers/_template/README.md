# _template — how to add a teacher

Copy this folder to `teachers/<slug>/` (lowercase, hyphenated, e.g.
`ramana-maharshi`). Folders starting with `_` are skipped by the build.

1. Fill `meta.json`. Name, dates, places, a one-line description, a lead
   quote, a portrait URL with its credit, and the teacher's own position on
   the copyright of their words (or a note that none is recorded).
2. Gather. Run seven researchers, one per medium, with the briefs in
   `GATHERING.md`. Each writes a JSON file in the shared schema into a
   scratch folder, and a full markdown report into `catalogue/`.
3. Merge. `python3 merge.py <scratch-folder>` writes `items.json`,
   `quotes.json`, and `events.json` / `people.json` when present.
4. Check. `python3 integrity.py` writes `integrity-report.md` and
   `integrity.json`. Read the report. Fix what it names, re-merge.
5. Write `timeline.md` as a `| Date | Event | Place |` table (used when
   `events.json` is absent), `copyright-view.md`, and `sources.md`.
6. Build. From the site root, `python3 build.py`. The teacher appears in
   the grid and at `gurus/<slug>/`.

`merge.py` and `integrity.py` are copied here from the first teacher's
folder so each teacher's data step is self-contained and can be adjusted
for that teacher without touching the others.
