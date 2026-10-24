# Wave 8 — archive.org identifier sweep and Reddit threads (U.G. Krishnamurti)

Scope: U.G. (Uppaluri Gopala) Krishnamurti only; Jiddu Krishnamurti excluded. 54 extended web searches, 2026-10-24. Tool limits: only WebSearch; `reddit.com`, `old.reddit.com`, `redd.it`, `redditmedia.com`, `teddit.net` and `rareddit.com` are refused by the search tool; archive.org could not be fetched directly, so the collection listing (80 items) could not be enumerated. Redlib/libreddit mirrors returned nothing. **SocialGrep (socialgrep.com) is indexed and turned out to be the only working Reddit index** — all thread rows below come from its snippets.

JSON: `scratchpad/json/wave8-archive-reddit.json` (17 rows, validated).

## 1. archive.org — new identifiers (not in download-manifest.json)

| Identifier | Title (archive.org) | Date | Notes | Conf. |
|---|---|---|---|---|
| `ug_01_anger_is_energy_dec1587` | Anger is Energy | 1987-12-15 | Numbered item 01 of the Kaplan `ugkrishnamurti-audio` series (known: 04, 06, 10, 11). Title matches a passage in *Stopped in Our Tracks* Book Two. | S |
| `ug_08_journalists_i-experss_week_kannada-prabha_jan1988` | The India Express Journalists, Kannada Prabha | 1988-01 | Numbered item 08; U.G. with Indian Express / The Week / Kannada Prabha journalists; RealAudio source. Bangalore inferred. | S |
| `ug_w_donnald_ingram` | U.G. with Donald Ingram | undated | "Krishnamurti conversing with Donald Ingram"; third Donald Ingram Smith item, distinct from the 1990-03-07 interview and the ABC Sept 1990 item. | S |
| `ug_amsterdam_19820901` | Conversation in Amsterdam | 1982-09-01 | Added 2012-08-29; the September 1982 Amsterdam sessions (Henk Schonewille tapes) that became *The Courage to Stand Alone*. | S |
| `elpensamientoest0000ugkr` | El Pensamiento es Tu Enemigo | — | Scanned library text (Spanish *Thought Is Your Enemy*), not audio; new identifier nonetheless. | S |

Numbered series status: 01 ✔ new, 02 ?, 03 ?, 04 known, 05 ?, 06 known, 07 ?, 08 ✔ new, 09 ?, 10 known, 11 known, 12 ?. Pattern of identifiers is `ug_NN_<slug>_<monYY>`; the missing six did not surface under any single-word or year probe (sorrow, con, spiritual, mill valley, whitewater, seaside, carmel, palm springs, kodaikanal, mysore, bombay, delhi, saanen, sydney, soiree, friends, khushwant, patriot, chandrasekhar, brahmachari, moorty, newland, thayer, radio, talk, 1968–2006).

Collection facts confirmed: `ugkrishnamurti-audio` metadata lists collectionSize 80 and creator Jeff Kaplan; items were bulk-added 2012-08-29; original sources were `.rm` files at `mindgazer.org/ug/ug_audio_2002212/…` (the ugkrishnamurti.org audio section). Manifest + this wave now account for 49 audio-collection identifiers (45 known + 4 new audio); ~31 remain unlisted.

thisrobotdreaming (Nicolas C. Grey, *This Dog Barking*) cassette uploads: blog post "U. G. Krishnamurti tapes" says all tapes (1967–1990s) were put on the Internet Archive, and the store offers "U. G. Krishnamurti IN Bangalore 1982 FREE MP3", but no archive.org identifier or uploader name surfaced; `ug_bangalore_bramchari_chants` (metadata year 1982/1984) is the only Bangalore-1982 item found and belongs to the Kaplan collection, so it is probably not his. Still a lead.

## 2. Reddit threads (via SocialGrep index; permalinks not captured)

| Subreddit | Thread title (as indexed) | Approx. date | Score / notes | Conf. |
|---|---|---|---|---|
| r/atheism | Extreme Atheist and Anti-Guru UG Krishnamurti interview. Fascinating. Highly recommended. | 2021-05-19 | link post | lead |
| r/askphilosophy (also r/spirituality) | Western philosophies/"religions" akin to zen, Advaita, Taoism, and whatever the hell UG Krishnamurti was on about? | 2021-08-18 | question | lead |
| r/ugkrishnamurti | UG Krishnamurti - Real Cause of Man's Tragedy | 2022-01-30 | 6 points, self-post | lead |
| r/awakened | UG Krishnamurti interview from "Thinking Allowed" (Mishlove) | 2022-03-07 | score 2; "a very unusual type of awakening" | lead |
| r/krishnamurti | UG Krishnamurti Answers Big Questions From Dr. Mishlove in « Thinking Allowed » (praise post) | 2022-03-14 | | lead |
| r/psychonaut | (title not shown) | 2023-02-18 | score 1 | lead |
| r/nonduality | U.G. Krishnamurti - Garden Conversation Bits | 2023-02-20 | video clip | lead |
| r/krishnamurti | UG Krishnamurti and Genetics | 2023-02-20 | | lead |
| r/krishnamurti | Long UG Krishnamurti quote on thinking that I think (ironically enough) applies to this sub | 2023-02-21 | quote | lead |
| (unknown) | UG on past, present and future (Thinking Allowed excerpt) | — | | lead |

Subreddit-level facts (SocialGrep snapshot 2021–2023): r/UGKrishnamurti exists (self.ugkrishnamurti = 2.2% of source domains for the query) [S]; query "ug krishnamurti" = 93 posts / 629 comments; comment share r/zen 14.5%, r/awakened 10.3%, r/krishnamurti 8.9%, r/nonduality 3.2%, then r/meditation, r/psychonaut, r/buddhism. r/streamentry, r/Buddhism, r/philosophy, r/Jung, r/occult, r/Soulnexus, r/RationalPsychonaut: no titled threads surfaced. Thread count: 10 (9 with subreddit).

## Still open

1. Six numbered items (`ug_02/03/05/07/09/12`) and ~25 further `ugkrishnamurti-audio` identifiers — need a direct fetch of `archive.org/advancedsearch.php?q=collection:ugkrishnamurti-audio&fl[]=identifier&rows=100&output=json`.
2. thisrobotdreaming cassette uploads: identifier(s) and uploader account.
3. Reddit permalinks, scores and comment counts for the 10 threads; r/UGKrishnamurti subscriber count and creation date; threads on r/streamentry, r/Buddhism, r/philosophy, r/Jung, r/occult. SocialGrep pages themselves (`socialgrep.com/search?query=ug+krishnamurti`, `?query=/r/ugkrishnamurti`) would list them if fetched in a browser.
4. Whether `ug_w_donnald_ingram` duplicates either dated Donald Ingram Smith item.

## Sources

- https://archive.org/details/ugkrishnamurti-audio (collection; size 80; creator Jeff Kaplan)
- https://archive.org/details/ug_01_anger_is_energy_dec1587
- https://archive.org/details/ug_08_journalists_i-experss_week_kannada-prabha_jan1988
- https://archive.org/details/ug_w_donnald_ingram
- https://archive.org/details/ug_amsterdam_19820901
- https://archive.org/details/elpensamientoest0000ugkr
- https://archive.org/details/ug_dr_kbr_sastrii_bramchari_babu (mindgazer.org `.rm` source path)
- https://archive.org/details/ug_bangalore_bramchari_chants
- https://www.thisrobotdreaming.com/blog/u-g-krishnamurti-tapes
- https://www.thisrobotdreaming.com/store/p/u-g-krishnamurti-in-bangalore-1982-free-mp3
- https://www.socialgrep.com/search?query=ug+krishnamurti
- https://socialgrep.com/search?query=krishnamurti
- https://socialgrep.com/search?query=/r/krishnamurti
- https://people.well.com/user/jct/index_main.html (WELL streaming list, "UG in Mill Valley", not on archive.org)
