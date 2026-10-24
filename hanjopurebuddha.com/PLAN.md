# Plan — the guru browsing section

## What it is

A place to browse enlightened people and see what they said and what
remains of them. Not commentary. The person's own words, the recordings
of their voice, the footage, the photographs, the books that carry their
conversations, and the places where all of that is kept, with the source
of every item beside it.

## One teacher, one folder

```
teachers/<slug>/
  meta.json          name, full_name, dates, born, died, places, one_line,
                     lead_quote, portrait, portrait_credit,
                     copyright_statement, media list, confidence legend
  items.json         the media catalogue, one object per located item
  quotes.json        the quotes, one object per quote
  timeline.md        | Date | Event | Place | table of the life
  copyright-view.md  the teacher's own position on ownership of their words
  README.md          what is in the folder and how it was gathered
  sources.md         where the complete texts live
  catalogue/         the researchers' full reports, one per medium and wave
  merge.py           turns the researchers' JSON into items.json/quotes.json
```

### items.json, one object per item

```
{ "id", "medium": video|audio|text|image|archive|community,
  "title", "date", "year", "place", "people": [], "format", "language",
  "duration", "host", "url", "description", "tags": [],
  "confidence": S|T|lead, "sources": [urls], "origin": which report }
```

### quotes.json, one object per quote

```
{ "id", "text", "book", "chapter", "year", "confidence": S|T,
  "kind": verbatim|fragment|paraphrase, "tags": [], "note", "sources": [] }
```

### Confidence marks

- **S** the wording or the item's existence was confirmed against a quoted
  copy or a direct description during gathering.
- **T** from memory of the published text or a secondary account. Wants
  checking against the full text.
- **lead** an unverified lead. Location given, content unseen.

## How a teacher is gathered

Seven parallel researchers, one per medium, each sweeping web search
exhaustively for that teacher. Video (channels, playlists, films, TV by
country, conversations by place and year, tape provenance). Audio
(cassettes and who recorded them, archive collections, radio, podcasts,
audiobooks, other languages). Texts (every edition with ISBN, every free
full text, every transcript site, press, papers, translations, letters).
Images (photographers, galleries, Commons, covers, drawings, documents,
places). Archives and communities (sites, blogs, wiki pages, forums, social
accounts, holders of material, memorials). Two quote harvesters, by book.
Each writes JSON in the shared schema and a full markdown report. A second
wave runs on the gaps the first wave names. `merge.py` dedupes and unifies.

## Who comes next

The section is for enlightened people whose own words survive. Candidates
for the next folders, in no order: Ramana Maharshi, Nisargadatta Maharaj,
Jiddu Krishnamurti (a separate person from U.G.), Anandamayi Ma, Hui-neng,
Longchenpa, Dōgen, Bankei, Milarepa, Machig Labdrön, Rumi, Meister Eckhart,
Hakuin, Ajahn Chah, Dipa Ma, Lalleshwari, Akka Mahadevi, Kabir.

## What the site does not do

It does not rank, compare or explain. It does not host files it has no
right to. It links to where each item lives and says who holds it. Where a
teacher released their words from copyright, as U.G. did, the site says so
in that teacher's Copyright tab.
