# U.G. Krishnamurti — source archive

The first teacher folder of hanjopurebuddha.com. Uppaluri Gopala
Krishnamurti (9 July 1918 – 22 March 2007). Not Jiddu Krishnamurti.

Rendered at `gurus/ug-krishnamurti/` on hanjopurebuddha.com and inside
drthomasager.com. Data files beside this README are the source of truth and
are published next to the page as JSON.

## The dataset now

<!-- counts -->
| File | What | Count |
|---|---|---|
| `items.json` | located media items across video, audio, text, image, archive, community | 524 |
| `quotes.json` | words of the teacher, each with book, chapter, confidence, kind, verdict, sources | 267 |
| `events.json` | dated life events with sources | 84 |
| `people.json` | everyone connected to the record, with role and what they hold | 87 |

Items by medium: archive 95, community 22, audio 79, image 93, text 143, video 92.
Items by confidence: S 483, T 2, lead 39.
Quotes by verdict: multi-source 53, primary-source 75, disputed 2, corroborated-secondary 34, single-source 91, not-found 2, corroborated-primary 10.
Distinct source hosts cited: 285.
<!-- /counts -->

## The one-line answer on copyright

> My teaching, if that is the word you want to use, has no copyright. You
> are free to reproduce, distribute, interpret, misinterpret, distort,
> garble, do what you like, even claim authorship, without my consent or
> the permission of anybody.

Printed in place of a copyright line in every book of his conversations.
`copyright-view.md` has where it appears and how archives treat it.

## Pipeline

```
python3 merge.py <scratch-folder-of-researcher-json>   # -> items.json quotes.json events.json people.json
python3 integrity.py                                   # -> integrity-report.md integrity.json
cd ../.. && python3 build.py                           # -> site/
```

`merge.py` canonicalises book names, merges items that share a URL (keeping
every title under `also_titled`, unioning tags, sources, people and origins),
derives metadata tags (decade, year, person, host, format, language, place,
confidence) on top of the researchers' own, and gives each quote a verdict:
`corroborated-primary` / `corroborated-secondary` from the verification pass,
else `primary-source` when a Wikisource, WELL, archive.org or
ugkrishnamurti.in URL is among its sources, else `multi-source` when two or
more hosts cite it, else `single-source`.

## How it was gathered (2026-10-24)

The gathering session's network policy refused direct connections to every
hosting site (the WELL, Wikisource, Wikiquote, the Internet Archive,
YouTube, SoundCloud, the quote aggregators), so no file was downloaded.
Researchers swept web search in waves, one per medium, each writing JSON in
the shared schema and a full markdown report into `catalogue/`. Wave one:
video, audio, texts, images, archives and communities, two quote harvests.
Wave two: the gaps each named. Wave three: Wikisource chapter mining and an
archive.org / YouTube / SoundCloud identifier sweep. Wave four: a dated
chronology, a people registry, a quote verification pass on second
independent hosts, and Indian-language material. Every quote and item keeps
the URLs it was found at. Opening those hosts in the environment's network
settings lets the full texts, audio and photographs be pulled in beside
these files.

`sources.md` lists where the complete texts live. `quotes-hand-gathered.md`
is the first hand-gathered list, kept for its confidence marks.

Licences: `LICENSE` (MIT for code, CC0 for the catalogue, his own release
for his words).
