# Wave 7 — Verification pass 3, half B (odd-id quotes)

Verifier: Claude (research subagent), 2026-10-24. Scope: quotes in `quotes.json` whose prior verdict was `primary-source`, `multi-source` or `single-source` and whose id ends in an odd hex digit (78 candidates: 22 verbatim, 37 fragment, 19 paraphrase). Method: WebSearch only (extended mode), exact-phrase search of a distinctive span plus "Krishnamurti"; Jiddu Krishnamurti sites (kfoundation.org, jkrishnamurti.org, kfa.org, krishnamurti.org) were ignored wherever they appeared in results. WebFetch was unavailable, so primary-host confirmation means the search engine surfaced the primary page for the phrase, not that the page was read in full.

**Coverage:** 43 of 78 candidates searched in 40 searches (all 22 verbatim items, 19 fragments, 2 paraphrases). The shared web-search budget was then exhausted; 35 candidates remain unsearched (listed at the end). Machine-readable results: `scratchpad/json/verification-3b.json`.

## Results table

| id | kind | first words | verdict | confirming hosts | note |
|---|---|---|---|---|---|
| qad57ce7d | verbatim | Not a calamity to me but… | corroborated-primary | en.wikisource.org, nuthanapati.blogspot.com | Blog copy follows the 'physical torture' passage; second host is an unofficial reproduction of the same text, not an independent transcript. |
| q64b3e681 | verbatim | Your thinking endlessly about being free… | corroborated-primary | en.wikisource.org, goodreads.com, people.well.com | Goodreads carries identical wording in the longer passage ('Sorrow is there for you as long as you think'). Search results otherwise polluted by Jiddu Krishnamurti pages on sorrow (excluded). |
| qe27976db | verbatim | You hook up each thought with… | corroborated-secondary | goodreads.com | Only Goodreads work-quote pages surfaced; search summary says 'several quote sites carry the same passage' but none other than Goodreads listed. No primary host found in search; context (every thought must die) suggests Mind is a Myth ch. on death. |
| q044d9da9 | verbatim | It is not an illusion, only… | single-source | goodreads.com | Book attribution inconsistent across Goodreads pages (No Way Out vs Mind is a Myth vs Courage to Stand Alone). Longer passage: 'You can't say that falling bombs are an illusion.' No primary host found. |
| qd05c2db1 | verbatim | you arrive seeking understanding, while I… | corroborated-primary | en.wikisource.org, goodreads.com | Primary host confirms. Goodreads topic page carries a related 'Understanding' excerpt; weak secondary. |
| qcb7d8a47 | verbatim | You are not a "person", not… | corroborated-primary | en.wikisource.org, holybooks.com, o-meditation.com, people.well.com | Two primary hosts plus two full-text PDFs; wording consistent. |
| qdcc7dd8b | verbatim | My teaching, if that is the… | corroborated-primary | books.google.com, en.wikiquote.org, en.wikisource.org, ugkrishnamurti.in | Copyright-release statement reproduced across multiple books; editor-attribution: appears in Penguin Reader edited by Mukunda Rao but as U.G.'s own statement. |
| q4b30cd75 | verbatim | My body had gone away and… | corroborated-primary | content.e-bookshelf.de, en.wikisource.org, nuthanapati.blogspot.com | Publisher preview PDF is an independent host of the same text. |
| qdc4e8ecb | verbatim | Anything you touch is always translated… | corroborated-primary | en.wikisource.org, remembering-ug.blogspot.com | BOOK CONFLICT: catalogue says The Natural State (Wikisource The_Natural_State), search hosts say Mystique Part Two. Both are plausible since The Natural State compiles Mystique passages; consider dual-filing. |
| q4b9ab831 | verbatim | I am not against the scientific… | single-source | — | Exact phrase not found by search; results dominated by Jiddu Krishnamurti science pages (excluded). Only the listed Wikisource 'Science and U.G.' page carries it; no second host. |
| q092c85d7 | verbatim | I call it 'calamity' because from… | corroborated-primary | dokumen.pub, en.wikisource.org, mail-archive.com, people.well.com, ug-k.blogspot.com | Two primary hosts; minor punctuation/conjunction variants between Wikisource and WELL. Catalogue text matches the WELL (Mahesh Bhatt biography) variant. |
| q9c460863 | verbatim | The understanding that there is nothing… | single-source | — | Exact sentence not returned by search engine; only the listed Wikisource ch. V page supports it. No second host found. |
| qdb3fcee7 | verbatim | thought is a divisive and ultimately… | corroborated-primary | people.well.com, sureshn13.medium.com | EDITOR ATTRIBUTION: the WELL No Way Out ch. 1 text is an editorial summary ('According to him, thought is a divisive and ultimately a destructive instrument') — i.e. the editor paraphrasing U.G., not U.G.'s direct speech. Treat as editor's words about U.G. |
| q4c3e36cf | verbatim | Time and space, apart from the… | single-source | — | Exact phrase not found by search; results dominated by kfoundation.org (Jiddu) pages on time, excluded. Only the listed WELL page supports it. |
| q7660d023 | verbatim | I awoke the morning after my… | corroborated-primary | egodeathfilms.wordpress.com, people.well.com, ug-k.blogspot.com | EDITOR/BIOGRAPHER: the sentence is U.G.'s recollection as reported in Mahesh Bhatt's biography; wording varies slightly across hosts. |
| qd69def2f | verbatim | Neither the subject nor the author… | corroborated-primary | en.wikisource.org, exoticindiaart.com, people.well.com | PUBLISHER'S NOTE: U.G.'s remark as reported by the publisher, not from a dialogue transcript. Two primary hosts plus a bookseller. |
| q55b7359d | verbatim | I have nothing to give; you… | corroborated-primary | en.wikisource.org, people.well.com, remembering-ug.blogspot.com | Two primary hosts and a blog; wording consistent. |
| q762cadb3 | verbatim | That is to say, all that… | single-source | kwize.com | Only kwize returned the exact wording; the Goodreads Thought is Your Enemy page listed in the catalogue did not surface. No primary host confirmation. |
| q7f2ee6c3 | verbatim | The body or organism is not… | single-source | kwize.com | Only kwize; a Goodreads 'Truth' work page carries a related passage with different wording. No primary host. |
| q610e5087 | verbatim | It [thought] is a mechanical thing… | corroborated-primary | en.wikiquote.org, people.well.com, quotepark.com | Quotepark gives the same bracketed '[thought]' wording and names the book. Compiler attribution: Chandrasekhar's excerpts of U.G. dialogues. Jiddu Krishnamurti has a thematically similar 'thought is mechanical' remark (Bohm dialogues) but different wording. |
| qd28dac6d | fragment | there is no self to realize | corroborated-secondary | archive.org, azquotes.com, en.wikiquote.org, goodreads.com, quotepark.com | archive.org PDF ('On U.G.') is a primary-class host but a later compilation; multiple quote sites agree. Upgrade candidate to corroborated-primary if archive.org text is confirmed verbatim. |
| qf5158cb3 | fragment | …has no copyright. You are free… | corroborated-primary | en.wikiquote.org, en.wikisource.org, holybooks.com, penguin.co.in, quotefancy.com | Copyright-release statement; present in front matter of nearly every U.G. book. Same statement as qdcc7dd8b. |
| q40cf79f3 | fragment | I still maintain that it is… | corroborated-secondary | goodreads.com, quotefancy.com | Goodreads and quotefancy agree on wording; no primary host surfaced. |
| q87a66997 | fragment | your teacher must go, it doesn't… | single-source | hindu-blog.com | Only the hindu-blog compilation carries the exact line; no book, transcript or second host. Theme ('no teacher, no taught, no teaching') is well attested but this wording is not. |
| qab99509d | fragment | blind acceptance of authority, all second-hand… | single-source | hindu-blog.com | Only hindu-blog; search otherwise returned Jiddu Krishnamurti 'authority' material (excluded). No primary host. |
| qde931de1 | fragment | It is fear that makes you… | corroborated-secondary | emperyquotes.com, goodreads.com, praveennv.blogspot.com, quotes.pub, quotlr.com | Same quote as qfe0764c5. BOOK CONFLICT: Goodreads says No Way Out; catalogue duplicate says Mystique. Several secondary hosts; no primary host surfaced. |
| qfe0764c5 | paraphrase | It is fear that makes you… | corroborated-secondary | goodreads.com, praveennv.blogspot.com, quotes.pub, quotlr.com | Duplicate of qde931de1 (same passage, fuller). Book attribution conflict: hosts say No Way Out, not Mystique. Not actually a paraphrase: hosts carry this as verbatim. |
| qbdce9d7f | fragment | it is the mind that has… | corroborated-primary | azquotes.com, en.wikisource.org, holybooks.com, o-meditation.com, praveennv.blogspot.com | Primary host (Wikisource Mind is a Myth/I) confirms the 'mind' wording. Distinct from the 'Man has created God' wording filed under Mystique (qbddfe57f). |
| qbddfe57f | fragment | Man has created God out of… | corroborated-secondary | azquotes.com, en.wikiquote.org, heartofyoga.com, jhana8.com, quotefancy.com | Many secondary hosts agree; primary host (Wikisource Mystique) not surfaced for this exact wording by search; the Mind is a Myth primary text uses 'the mind' instead of 'Man'. |
| q05850b19 | fragment | there is no individual there at… | corroborated-secondary | goodreads.com, holybooks.com, praveennv.blogspot.com | COMPILER: The Natural State is Peter Maverick's compilation of U.G. talks. No primary transcript host surfaced. |
| q91eb04cf | fragment | WHAT I HAVE FOUND, OFF AND… | corroborated-primary | medium.com, people.well.com, remembering-ug.blogspot.com, sciforums.com, ugkrishnamurti.in | EDITOR: dictated to Louis Brawley; versions vary (Medium edited copy). The all-caps sentence exists only as the WELL page heading, so confirm it is U.G.'s wording rather than the webmaster's headline. |
| q39483a5d | fragment | …the beyond can never be experienced… | corroborated-primary | en.wikisource.org, goodreads.com, infant7sorrow.wordpress.com | Goodreads and a blog agree with the Wikisource Part Two text; search did not list Wikisource directly but catalogue primary host plus two secondary hosts. |
| qeee2e8cf | fragment | Everything you stand for, believe in,… | corroborated-secondary | azquotes.com, emperyquotes.com, jhana8.com, libquotes.com, quotefancy.com, quotlr.com | EDITOR: attribution to the Moorty/Noronha-edited 2002 volume, ch. 7. Many secondary hosts agree on wording; no primary host surfaced. |
| qc032db3b | fragment | Love implies division, separation. Wherever there… | corroborated-secondary | amazon.com, goodreads.com, true-dhamma.com | EDITOR/BHATT: wording is the title of a Bansal-edited, Bhatt-forewarded ebook; Goodreads carries 'Wherever there is division, there can't be love' as a quote from it. No primary host. Jiddu Krishnamurti has thematically similar 'love cannot exist where there is fragmentation' (Meeting Life) but different wording. |
| q74cba27f | fragment | wherever there is division, there can't… | corroborated-secondary | amazon.com, goodreads.com | Same passage as qc032db3b; book attribution per hosts is the Bansal 'Love' ebook, not Mind is a Myth. |
| qc70b22b1 | fragment | Thought always interferes with sex. It… | corroborated-primary | en.wikisource.org, goodreads.com | Primary host confirms; book assignment for catalogue should be No Way Out ch. 8 (currently unassigned). |
| q59326449 | fragment | The pleasure of sex, for instance,… | corroborated-primary | en.wikisource.org, goodreads.com, remembering-ug.blogspot.com | Primary host (Wikisource The Natural State) plus blog and Goodreads; book assignment: Mind is a Myth (catalogue currently unassigned). |
| q3646651d | fragment | There is nothing to your love:… | single-source | inner-quest.org | Only inner-quest.org; search otherwise returned Jiddu Krishnamurti love quotes (excluded). No primary host. |
| q181d741b | fragment | …all the positive approaches that man… | single-source | — | Exact phrase not found; results were Jiddu Krishnamurti 'positive approach' material (theprint.in Can the Mind be Quiet excerpt, krishnamurti.org) — excluded. Only the listed beyond-the-pale page supports it. Jiddu-confusion risk: Jiddu has a similarly titled passage 'Positive approach to life is destructive'. |
| q46e8ac7b | fragment | Charity is the filthiest invention of… | disputed | azquotes.com, emperyquotes.com, en.wikiquote.org, jhana8.com, myquotes.co | Marked 'disputed' because wording varies materially between hosts and Wikiquote classifies it as unsourced; no primary host. Widely circulated as U.G.'s, no Jiddu attribution. |
| q0997ce6d | fragment | Each cell of a living organism… | corroborated-secondary | amazon.com, goodreads.com, praveennv.blogspot.com | EDITOR/BHATT: Bansal-edited ebook with Bhatt foreword. Goodreads author page and praveennv blog repeat the cell passage; no primary host. |
| qbc15d529 | fragment | You draw lines on this planet. | corroborated-secondary | en.wikiquote.org, libquotes.com, quotepark.com, ru.citaty.net, yquotes.com | Hosts name No Way Out ch. 7 — catalogue has it unassigned. Secondary hosts only (Wikiquote + aggregators); Wikisource No Way Out exists but did not surface for this phrase. |
| q6bc8c471 | fragment | There is no such thing as… | corroborated-primary | actualfreedom.com.au, books.google.com, en.wikisource.org, inner-quest.org | Primary host plus Google Books description and an Actual Freedom correspondence quoting it. |

## Per-verdict summary

- **corroborated-primary** — 20: qad57ce7d, q64b3e681, qd05c2db1, qcb7d8a47, qdcc7dd8b, q4b30cd75, qdc4e8ecb, q092c85d7, qdb3fcee7, q7660d023, qd69def2f, q55b7359d, q610e5087, qf5158cb3, qbdce9d7f, q91eb04cf, q39483a5d, qc70b22b1, q59326449, q6bc8c471
- **corroborated-secondary** — 12: qe27976db, qd28dac6d, q40cf79f3, qde931de1, qfe0764c5, qbddfe57f, q05850b19, qeee2e8cf, qc032db3b, q74cba27f, q0997ce6d, qbc15d529
- **single-source** — 10: q044d9da9, q4b9ab831, q9c460863, q4c3e36cf, q762cadb3, q7f2ee6c3, q87a66997, qab99509d, q3646651d, q181d741b
- **disputed** — 1: q46e8ac7b
- **not-ug** — 0
- **not-found** — 0

Reading of the verdicts:

- *corroborated-primary*: the phrase was returned on en.wikisource.org, people.well.com, archive.org or ugkrishnamurti.in **and** on at least one other host (or on two primary hosts).
- *corroborated-secondary*: two or more non-primary hosts agree on the wording; no primary host surfaced for the exact phrase.
- *single-source*: search returned only the host already in the catalogue (or nothing at all for the exact phrase); the catalogued primary host, where there is one, still stands but was not independently re-confirmed. Items with empty `confirming_sources` (q4b9ab831, q9c460863, q4c3e36cf, q181d741b) returned no hit at all for the exact wording — mostly because Jiddu Krishnamurti pages swamped the results.
- *disputed*: q46e8ac7b (charity) — wording differs materially between hosts and Wikiquote's Talk page lists it as unsourced.
- No item was found to be Jiddu Krishnamurti's (*not-ug*: 0).

## Attribution and book conflicts

**Book-assignment conflicts (hosts disagree with the catalogue):**

- qdc4e8ecb "Anything you touch is always translated as hard, soft…" — catalogue: *The Natural State*; Wikisource and remembering-ug place it in *The Mystique of Enlightenment*, Part Two. (*The Natural State* is a compilation that reuses Mystique passages, so both are defensible; prefer Mystique as origin.)
- qde931de1 / qfe0764c5 "It is fear that makes you believe that you are living…" — duplicate pair; catalogue files qfe0764c5 under *Mystique*, Goodreads work page says *No Way Out*. qfe0764c5 is carried verbatim by hosts, not as a paraphrase.
- q044d9da9 "It is not an illusion, only your experience of it…" — catalogue: *The Courage to Stand Alone*; Goodreads lists it under *No Way Out* on one page and the catalogue's own source URL is the *Mind is a Myth* work page. Unresolved.
- qbddfe57f vs qbdce9d7f — two wordings of the God/fear line: *Mind is a Myth* ch. I (primary) reads "it is the mind that has created God out of fear"; the "Man has created God out of fear" wording is filed by Wikiquote under *Mystique* and is only secondary-confirmed.
- Unassigned items that hosts now place: qc70b22b1 → *No Way Out* ch. 8 (Wikisource); q59326449 → *Mind is a Myth* (also in *The Natural State*); qbc15d529 → *No Way Out* (2002) ch. 7; qeee2e8cf → ch. 7 of the Moorty/Noronha 2002 compilation; qc032db3b / q74cba27f → Bansal 'Love' ebook, not *Mind is a Myth*.

**Editor / compiler / Bhatt attributions (wording may be the editor's, not U.G.'s direct speech):**

- qdb3fcee7 "thought is a divisive and ultimately a destructive instrument" — on the WELL this is the editor's introduction to *No Way Out* ("According to him, thought is…"), i.e. an editorial paraphrase of U.G.
- q7660d023 "I awoke the morning after my wedding night…" — U.G.'s recollection as reported in Mahesh Bhatt's biography *U.G. Krishnamurti: A Life*; wording varies slightly across hosts.
- qd69def2f "Neither the subject nor the author is famous." — publisher's note to Shanta Kelker's *The Sage and the Housewife*, reporting U.G.'s remark.
- q91eb04cf (Swan Song all-caps line) — exists only as the WELL page heading; the body text (dictated to Louis Brawley) phrases it differently; a Medium 'updated' copy adds bracketed insertions.
- qc032db3b, q74cba27f, q0997ce6d — titles/quotes from Sunita Pant Bansal-edited ebooks with Mahesh Bhatt forewords (*Love*, *Society*); no primary transcript found.
- qeee2e8cf — attributed to the J.S.R.L. Narayana Moorty / Antony Paul Frank Noronha-edited 2002 volume, ch. 7.
- q05850b19 — from Peter Maverick's compilation *The Natural State in the Words of U.G. Krishnamurti*.
- q610e5087 — K. Chandrasekhar's *Stopped in Our Tracks*, Book Two (excerpts from U.G.'s dialogues).
- qdcc7dd8b / qf5158cb3 — the copyright-release statement; reproduced in the Penguin Reader (ed. Mukunda Rao) and in most U.G. books' front matter.

**Jiddu Krishnamurti:** no searched quote was attributed to Jiddu by any host. Jiddu pages polluted results for q64b3e681 (sorrow), q4b9ab831 (scientific method), q4c3e36cf (time and space), q181d741b (positive approaches), q3646651d (love), qab99509d (authority) and q610e5087 (thought is mechanical); these were excluded, but it means the exact-phrase searches for q4b9ab831, q4c3e36cf and q181d741b returned nothing useful rather than confirming the catalogue host. q181d741b deserves a second look: Jiddu has a passage published as "Positive approach to life is destructive", so the theme overlaps.

## Not yet searched (budget exhausted)

- qee37e731 (paraphrase, Mind is a Myth): Both the inner and outer worlds proceed from…
- q539055bd (paraphrase, Thought is Your Enemy): Our experience of our own body depends on…
- qe74e02bb (paraphrase, No Way Out): the death of fear is the only death
- q540a25ff (paraphrase, No Way Out): Death described as atoms changing form, with nothing…
- q77a9194f (paraphrase, The Courage to Stand Alone): Each time a thought is born, you are…
- q72c0b555 (paraphrase, The Courage to Stand Alone): Questioning the solutions requires a tremendous courage.
- q6f33cc13 (fragment, The Natural State): the same old nonsense repeating itself
- qae3cbc6d (paraphrase, My Swan Song): His findings run counter to everything anyone has…
- qf7b51191 (paraphrase, My Swan Song): Freeing the body from what is put in…
- q5e50266d (paraphrase, My Swan Song): Sex is for reproduction; people have turned it…
- q88d291eb (fragment, U.G. Krishnamurti: A Life): Act, don't think!
- qa106c8ad (paraphrase, My Swan Song): Sex is for reproduction; people have turned it…
- q505bda73 (fragment, The Biology of Enlightenment): The whole thing comes to an end.
- q96cd1f77 (fragment, U.G. Krishnamurti: A Life): …I knew without doubt that I had made…
- q2f03fb65 (paraphrase, No Way Out): If you could have sex with your own…
- qb609f6f3 (paraphrase, The Mystique of Enlightenment): People call me enlightened, a term I dislike;…
- q4895987b (fragment, Mind is a Myth): belief is an extension of the survival mechanism…
- q00193fb7 (verbatim, unassigned): Thought is you.
- q2d12cceb (fragment, Mind is a Myth): it is the ones who believe in God,…
- qaccf09f3 (fragment, The Mystique of Enlightenment): it has to come, and it will come…
- q4f2c81d1 (fragment, Mind is a Myth): the very birth of thought creates fear
- qc852ca7b (fragment, unassigned): happiness without one moment of unhappiness, pleasure without…
- qfc5867cf (verbatim, unassigned): There is no happiness.
- q6a9a1403 (fragment, The Natural State): all we can know is memory and memory…
- qa850f231 (paraphrase, Stopped in Our Tracks): I am not suggesting that you should stop…
- qc60032ad (fragment, unassigned): it is through this constant thinking that we…
- q104a81af (fragment, unassigned): the fear of losing what we have and…
- q0c6ee69f (fragment, unassigned): a useless exercise
- q707dda41 (paraphrase, Stopped in Our Tracks): My aim is to silence you.
- q93c2842f (paraphrase, The Biology of Enlightenment): Whatever transformation I have undergone is within the…
- qdab04c55 (paraphrase, The Biology of Enlightenment): The natural state is a pure and simple…
- q8233c2a7 (fragment, The Sage and the Housewife): No one escapes the natural laws.
- q7bd7cc71 (fragment, The Sage and the Housewife): It is the body that is immortal. It…
- q9feeb1bf (paraphrase, The Sage and the Housewife): I don't know what happiness is.
- q1268f7b9 (paraphrase, The Sage and the Housewife): A person to whom Kundalini rises would dismiss…

## Sources

- http://nuthanapati.blogspot.com/2011/11/natural-state-miracles-experienced-by.html
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html?m=1
- http://praveennv.blogspot.com/2016/03/mind-created-god-out-of-fear-ug.html
- http://remembering-ug.blogspot.com/2012/03/quotes-110412.html
- http://remembering-ug.blogspot.com/2012/04/quotes-040712_28.html
- http://remembering-ug.blogspot.com/2012/06/passages-060812.html
- http://remembering-ug.blogspot.com/2012/06/talks-100812.html
- http://ug-k.blogspot.com/2007/04/locking-of-horns-inspiration-is.html
- https://books.google.com/books/about/Mind_is_a_Myth.html?id=OBJiEAAAQBAJ
- https://books.google.com/books/about/The_Penguin_U_G_Krishnamurti_Reader.html?id=lnYEKZetXIUC
- https://content.e-bookshelf.de/media/reading/L-18427162-0b01407361.pdf
- https://dokumen.pub/the-penguin-ug-krishnamurti-reader-0143101021-9780143101024.html
- https://egodeathfilms.wordpress.com/2017/06/14/ug-krishnamurti-pt7-ug-kusuma/
- https://en.wikiquote.org/wiki/Talk:U._G._Krishnamurti
- https://en.wikiquote.org/wiki/U._G._Krishnamurti
- https://en.wikisource.org/wiki/Mind_is_a_Myth
- https://en.wikisource.org/wiki/Mind_is_a_Myth/I
- https://en.wikisource.org/wiki/Mind_is_a_Myth/IV
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_8
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Four
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_One
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Two
- https://en.wikisource.org/wiki/The_Natural_State
- https://en.wikisource.org/wiki/The_Sage_and_the_Housewife
- https://ia801804.us.archive.org/12/items/UGKrishnamurtiOnU.G185p/UG%20Krishnamurti%20-%20On%20U.G%20(185p).pdf
- https://infant7sorrow.wordpress.com/ug/
- https://jhana8.com/ug-krishnamurti-quotes/
- https://kwize.com/en/texts/U-G-Krishnamurti-Science-and-U-G/
- https://libquotes.com/u-g-krishnamurti
- https://libquotes.com/u-g-krishnamurti/quotes/thought
- https://medium.com/@alysion42/u-g-krishnamurtis-swan-song-updated-e36a07cc0595
- https://myquotes.co/authors/16500/
- https://o-meditation.com/wp-content/uploads/2011/05/krishnamurti-u-g-mind-is-a-myth.pdf
- https://people.well.com/user/jct/SWAN_SONG.htm
- https://people.well.com/user/jct/chandra.htm
- https://people.well.com/user/jct/chapter1.html
- https://people.well.com/user/jct/mystiq4.htm
- https://people.well.com/user/jct/ntbook3.htm
- https://people.well.com/user/jct/nwo1.htm
- https://people.well.com/user/jct/sagecon.htm
- https://people.well.com/user/jct/ugbio/ugbio4.htm
- https://people.well.com/user/jct/ugbio/ugbio9.htm
- https://praveennv.blogspot.com/2016/03/there-is-no-individual-there-at-all-ug.html
- https://quotefancy.com/quote/2210933/U-G-Krishnamurti-I-still-maintain-that-it-is-not-love-compassion-humanism-or-brotherly
- https://quotefancy.com/quote/923742/U-G-Krishnamurti-There-is-no-power-outside-of-man-Man-has-created-God-out-of-fear-So-the
- https://quotefancy.com/quote/923747/U-G-Krishnamurti-Everything-you-stand-for-believe-in-experience-and-aspire-to-is-the
- https://quotefancy.com/quote/923763/U-G-Krishnamurti-My-teaching-if-that-is-the-word-you-want-to-use-has-no-copyright-You-are
- https://quotepark.com/authors/ug-krishnamurti/
- https://quotepark.com/quotes/1733648-ug-krishnamurti-it-thought-is-a-mechanical-thing-and-can-solve-o/
- https://quotepark.com/quotes/1928052-ug-krishnamurti-i-discovered-for-myself-and-by-myself-that-there-i/
- https://quotes.pub/q/it-is-fear-that-makes-you-believe-that-you-are-living-and-th-448733
- https://quotlr.com/author/ug-krishnamurti
- https://ru.citaty.net/avtory/ug-krishnamurti/
- https://sureshn13.medium.com/who-is-ug-krishnamurti-d1f23e801be0
- https://true-dhamma.com/u.g.%E5%85%8B%E9%87%8C%E5%B8%8C%E9%82%A3%E7%A9%86%E6%8F%90/%E5%AE%9E%E7%9B%B8%E4%B8%8E%E8%A7%A3%E6%9E%84/%E7%88%B1-%E7%88%B1%E6%84%8F%E5%91%B3%E7%9D%80%E5%88%86%E8%A3%82-%E5%88%86%E7%A6%BB/
- https://ug-k.blogspot.com/2007/04/aftermath-uniqueness-of-individual.html?m=0
- https://www.actualfreedom.com.au/richard/selectedcorrespondence/sc-ug.htm
- https://www.amazon.com/U-G-Krishnamurti-implies-division-separation-ebook/dp/B009YZ95P8
- https://www.amazon.com/UG-Krishnamurti-Society-terror-together-ebook/dp/B009YZ97I8
- https://www.azquotes.com/author/17848-U_G_Krishnamurti
- https://www.azquotes.com/author/17848-U_G_Krishnamurti/tag/giving
- https://www.azquotes.com/author/17848-U_G_Krishnamurti?p=2
- https://www.azquotes.com/quote/943427
- https://www.emperyquotes.com/authors/ug-krishnamurti
- https://www.exoticindiaart.com/book/details/sage-and-housewife-idk451/
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=2
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=3
- https://www.goodreads.com/book/show/23796862-u-g-krishnamurti
- https://www.goodreads.com/quotes/531154-it-is-fear-that-makes-you-believe-that-you-are
- https://www.goodreads.com/quotes/9453810-i-still-maintain-that-it-is-not-love-compassion-humanism
- https://www.goodreads.com/quotes/984918-what-you-know-can-never-be-the-beyond-whatever-you
- https://www.goodreads.com/topic/list_book/26722093
- https://www.goodreads.com/work/quotes/43411143-u-g-krishnamurti-love-love-implies-division-separation
- https://www.goodreads.com/work/quotes/45409896
- https://www.goodreads.com/work/quotes/45622919-ug-krishnamurti-society-it-s-terror-not-love-that-keeps-us-together
- https://www.goodreads.com/work/quotes/52201-the-mystique-of-enlightenment-the-radical-ideas-of-u-g-krishnamurti
- https://www.goodreads.com/work/quotes/52202
- https://www.goodreads.com/work/quotes/52202-mind-is-a-myth
- https://www.goodreads.com/work/quotes/6212984
- https://www.goodreads.com/work/quotes/6212984-no-way-out-dialogues-with-krishnamurti
- https://www.heartofyoga.com/blog/ug-krishnamurti
- https://www.hindu-blog.com/2018/09/u-g-krishnamurti-quotes-and-teachings.html
- https://www.holybooks.com/natural-state-b-u-g-rishnamurti/
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Mind-is-a-myth.pdf
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Thought-is-Your-Enemy.pdf
- https://www.inner-quest.org/UG_Words.htm
- https://www.mail-archive.com/fairfieldlife@yahoogroups.com/msg235437.html
- https://www.penguin.co.in/book/the-penguin-u-g-krishnamurti-reader/
- https://www.sciforums.com/threads/the-last-message-of-u-g-krishnamurti.95095/
- https://www.ugkrishnamurti.in/
- https://www.ugkrishnamurti.in/ug-essence/my-swan-song
- https://yquotes.com/quotes/u-g-krishnamurti/
