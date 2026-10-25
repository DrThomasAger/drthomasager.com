# Gathering briefs

Seven researchers in parallel, each exhaustive for one medium, each told:
the teacher's full name and dates; who to EXCLUDE (namesakes); that only
web search may work in a locked-down environment; to write output files
incrementally; the JSON schema below; and to list every URL used.

## Shared item schema (items.json)

```
{"medium":"video|audio|text|image|archive|community","title":"","date":"YYYY-MM-DD|YYYY|null",
 "year":int|null,"place":"City, Country|null","people":[],"format":"","language":"",
 "duration":"|null","host":"domain","url":"https://...","description":"",
 "tags":["lowercase-hyphenated"],"confidence":"S|T|lead","sources":["https://..."]}
```

## Shared quote schema (quotes.json)

```
{"text":"verbatim","book":"canonical title|unassigned","chapter":"|null","year":int|null,
 "confidence":"S|T","kind":"verbatim|fragment|paraphrase","tags":[],"note":"|null","sources":[]}
```

## The seven briefs

1. **Video**: channels, playlists, documentaries, TV by country and
   programme, conversations by place and year, subtitled versions, tape
   formats and who holds masters.
2. **Audio**: original tapes and recordists, archive collections, radio,
   podcasts, audiobooks, other languages, extracted audio, masters.
3. **Texts**: every edition with editor/publisher/year/ISBN, every free
   full-text URL, transcript sites, press, papers, translations, letters.
4. **Images**: photographers, galleries, Commons files with licences,
   covers, drawings, documents, stills, places and memorials.
5. **Archives and communities**: sites past and present with operators,
   blogs, wiki pages, forums, groups, social accounts, holders of material,
   institutional archives.
6. **Quotes A** and 7. **Quotes B**: verbatim lines by book, with chapter,
   source URL, and attribution conflicts.

Then a second wave on the gaps each one names, a chronology researcher
(events.json), a people researcher (people.json), a verification pass that
re-finds each quote on a second independent host (verification.json), and
an Indian-language or other-language pass where relevant.
