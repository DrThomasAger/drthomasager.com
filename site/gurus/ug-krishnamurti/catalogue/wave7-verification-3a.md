# Wave 7 — verification pass 3, half A (even-id quotes)

Scope: quotes in `quotes.json` whose `verdict` was still `primary-source`, `multi-source` or `single-source` and whose id ends in an even hex digit (0,2,4,6,8,a,c,e). 101 quotes qualified; prioritised verbatim, then fragment, then paraphrase. 45 WebSearch (extended) queries were run before the shared search budget was exhausted; **48 quotes were checked** (19 of the 20 verbatim — `qbd194c2e` "If you want to call it that" is too generic to search — plus 28 fragments and 1 paraphrase). Jiddu Krishnamurti foundation domains (kfoundation.org, jkrishnamurti.org, kfa.org, krishnamurti.org) were blocked from every query.

Method: exact-phrase search of a distinctive 7–11 word span plus "Krishnamurti". `corroborated-primary` = a primary host (en.wikisource.org, people.well.com, archive.org, ugkrishnamurti.in) carries the wording and at least one further host agrees; `corroborated-secondary` = two or more independent non-primary hosts agree; `single-source` = no host beyond the catalogue's own found; `not-found` = the phrase surfaced nowhere in search.

Machine-readable results: `/tmp/claude-0/-home-user-drthomasager-com/7c7edf2e-a0bd-5288-a28d-2ac0e832645f/scratchpad/json/verification-3a.json` (48 entries).

## Results

| id | kind | first words | verdict | confirming hosts | note |
|---|---|---|---|---|---|
| q118b8994 | verbatim | It (thinking) does not put an end … | corroborated-primary | en.wikisource.org, goodreads.com, o-meditation.com, people.well.com, remembering-ug.blogspot.com | Goodreads drops the bracketed '(thinking)' and starts the sentence with 'Thinking'. No Jiddu attribution found. |
| q16c5e496 | fragment | …discovered that there is no such thing … | corroborated-primary | catalign.in, en.wikiquote.org, holybooks.com, ia801804.us.archive.org, people.well.com | WELL and archive.org (On U.G.) are primary hosts confirming. |
| q2384f6fc | fragment | …this is the way you, stripped of … | corroborated-primary | abebooks.com, dokumen.pub, en.wikisource.org, holybooks.com, people.well.com, remembering-ug.blogspot.com | Phrase recurs across several books; the catalogue's Biology of Enlightenment attribution rests on Rao's description quoting U.G. |
| q3b41db6a | fragment | transformation, moksha, and all that stuff are … | corroborated-primary | goodreads.com, inner-quest.org, people.well.com, praveennv.blogspot.com | Line appears in two U.G. books (No Way Out ch. 1 reuses Thought is Your Enemy material); catalogue's Thought is Your Enemy is one valid attribution. |
| q41a1cd4e | fragment | a clinical death will occur, and it … | corroborated-primary | groups.google.com, hindu-blog.com, medium.com, people.well.com, sciforums.com | Wording consistent across repostings; text is as transcribed by Brawley. |
| q5061960a | verbatim | It [thought] is a mechanical thing and … | corroborated-primary | en.wikiquote.org, people.well.com, quotepark.com | ATTRIBUTION CONFLICT: quotepark lists the quote under Jiddu Krishnamurti's name; WELL and Wikiquote attribute to U.G. The words are Chandrasekhar's record of U.G. |
| q5e5b2970 | fragment | Charity is selfishness. | corroborated-primary | dalemusings.wordpress.com, people.well.com | WELL (primary) carries it in Chandrasekhar's record of U.G.'s dialogues; book name per the blog (Thought is Your Enemy) conflicts. |
| q64ae758c | fragment | you keep buying these bogus wares offered … | corroborated-primary | en.wikisource.org, o-meditation.com, people.well.com, scribd.com, zhenhost.net | BOOK CONFLICT: catalogue files this under My Swan Song (people.well.com, medium); every search host places it in Mind is a Myth ch. I. Re-check the Swan Song attribution. |
| q68c996ce | fragment | There is no meaning in and no … | corroborated-primary | inner-quest.org, people.well.com, ugkrishnamurti.in | inner-quest.org is the only new host; other results were unrelated Jiddu material on sorrow. No Jiddu attribution of this sentence found. |
| q8282292e | verbatim | Your beliefs are the result of blind … | corroborated-primary | en.wikisource.org, goodreads.com, harpeony.com | Secondary hosts confirm wording but attach it to compilations (Truth; The Natural State) that reuse Mind is a Myth text. |
| q9cf31b1c | fragment | This state is a state of not … | corroborated-primary | awakeningtoreality.com, en.wikisource.org, jhana8.com, onbeyondzen.com | Original locus is Mystique Part Two; The Natural State compilation (Peter Maverick) reprints it. |
| q9e846fe8 | verbatim | We have invented reality. Otherwise you have … | corroborated-primary | en.wikisource.org, nondualite.free.fr, youtube.com | The Courage to Stand Alone reuses No Way Out material, so the two book names are not a true conflict. |
| qc0edce3e | fragment | the hands and feet become cold, the … | corroborated-primary | dhammawheel.com, en.wikisource.org, kwize.com | Two secondary hosts confirm; original locus is Mystique. |
| qd1cb605c | fragment | The demand to be prepared for all … | corroborated-primary | en.wikisource.org, goodreads.com, quotefancy.com, quotessayings.net | Aggregators agree on wording and book; Wikisource primary already in catalogue. |
| qd70eb646 | fragment | You see, you love fear. The ending … | corroborated-primary | azquotes.com, en.wikisource.org, libquotes.com, quotefancy.com | Same passage as qa52816a8 (which the catalogue files under No Way Out). exploringyourmind.com frames it as Jiddu's. |
| qd829349e | verbatim | There is no moksha, no jivanmukti and … | corroborated-primary | en.wikisource.org, people.well.com, u-g-krishnamurti.blogspot.com | Reported speech recorded by Chandrasekhar; Wikisource primary confirms. |
| q062c2482 | fragment | You can have the courage to climb … | corroborated-secondary | azquotes.com, goodreads.com, libquotes.com, o-meditation.com, quotepark.com | Hosts differ: some end the list at 'Atlantic', some 'Atlantic or Pacific'; kalemati/quotepark continue 'That any fool can do' instead of 'That is not courage'. Full-book PDF on o-meditation corroborates; no listed primary host. |
| q1c893a18 | verbatim | Thinking about and struggling against 'sorrow' is … | corroborated-secondary | goodreads.com, o-meditation.com, quotefancy.com, remembering-ug.blogspot.com | Same passage as q118b8994 (Mind is a Myth ch. I). Full-book PDF copy on o-meditation.com corroborates; no Wikisource hit surfaced in search, though the chapter is on Wikisource. |
| q1fb04988 | fragment | All your experiences, all your meditations, all … | corroborated-secondary | azquotes.com, inner-quest.org, jhana8.com, quotefancy.com | Four hosts agree on wording; no primary host or book named. |
| q3814bcc6 | verbatim | Don't forget that in the name of … | corroborated-secondary | hindu-blog.com | Second host (hindu-blog) confirms wording with British spelling 'neighbour'. No primary host surfaced. |
| q77d45a2c | fragment | …anything you superimpose on that, all the … | corroborated-secondary | azquotes.com, goodreads.com, praveennv.blogspot.com, quotefancy.com, quotepark.com | Catalogue has it unassigned; hosts name No Way Out. No primary host surfaced. |
| q9a924078 | fragment | We are trying to bridge this gap… … | corroborated-secondary | goodreads.com, quotessayings.net | Second host quotessayings.net confirms wording; no primary host. |
| qa52816a8 | fragment | You love fear. The ending of fear … | corroborated-secondary | azquotes.com, libquotes.com, praveennv.blogspot.com, quotefancy.com, quotestats.com | ATTRIBUTION CONFLICT: exploringyourmind.com places the passage in a discussion of Jiddu Krishnamurti. Duplicate of qd70eb646, which is anchored to Mind is a Myth ch. I; the No Way Out attribution here is doubtful. |
| qb1981622 | fragment | The 'you' is born out of fear; … | corroborated-secondary | goodreads.com, libquotes.com | Part of the same Goodreads passage as qbd6fe67c and q08218f4e ('The body cannot be afraid of death...'). Search surfaced only Goodreads; libquotes is the catalogue's second host. |
| qb253e5d0 | fragment | What is morality? It is not the … | corroborated-secondary | beyond5.co.in, goodreads.com, grokipedia.com, infant7sorrow.wordpress.com | Aggregators only; no primary host surfaced. |
| qba6902b4 | fragment | Meditation is evil. | corroborated-secondary | en.wikisource.org, markwhitwell.medium.com, quora.com, soulmind.in | The three-word form is a disciple's recollection; the printed book form differs slightly. Widely repeated (soulmind, Quora). |
| qbb1ee524 | verbatim | Nature is busy creating absolutely unique individuals, … | corroborated-secondary | azquotes.com, goodreads.com, inspiringquotes.us, quotefancy.com, quotepark.com | Book conflict: aggregators cite Mind Is a Myth, catalogue cites The Courage to Stand Alone. steveleasock.com lists it under Jiddu Krishnamurti (misattribution). No primary host surfaced. |
| qbd6fe67c | verbatim | What you are afraid of is not … | corroborated-secondary | goodreads.com, quotessayings.net | Part of the longer Goodreads passage beginning 'The body cannot be afraid of death...' (see q08218f4e). Only aggregators; no primary host surfaced. |
| qd0ca3a02 | paraphrase | You think when you don't want to … | corroborated-secondary | en.wikiquote.org, quotefancy.com, whatsmyquote.com | Catalogue paraphrase omits the sentence 'Your thinking is consuming all your energy.' Words recorded by Bhatt. |
| qd9a45360 | fragment | Thinking is a poor alternative to acting. | corroborated-secondary | azquotes.com, en.wikiquote.org, inner-quest.org, nirvana73.blogspot.com, quotefancy.com | Recorded by editor/biographer Mahesh Bhatt; Wikiquote warns Bhatt's own preceding sentence 'You are what you do, not what you say you want to do' is sometimes misquoted as U.G.'s. Also covers paraphrase qd0ca3a02. |
| qf69919b2 | fragment | the fear of losing what we have … | corroborated-secondary | astitvameditation.com, goodreads.com, libquotes.com, quotlr.com, thequotearchive.com | Book discrepancy: Goodreads credits No Way Out, catalogue Thought is Your Enemy. No primary host surfaced. |
| q03c8d952 | verbatim | There is nothing to understand — that … | single-source | en.wikisource.org, inner-quest.org | Exact clause 'that is the understanding I am talking about' not found on any second host. The theme is heavily attested, the wording only on the catalogue's Wikisource page. |
| q241d3a5e | fragment | as long as you depend upon somebody … | single-source | praveennv.blogspot.com | Exact wording only on praveennv; brooklynaikikai.com has a related but different U.G. sentence. Jiddu's 'you cannot depend upon anybody' (Freedom from the Known) is a distinct, well-attested Jiddu line, not this one. |
| q39067cd0 | verbatim | Love, compassion, ahimsa, understanding, bliss, all these … | single-source | kwize.com | Exact phrase not found beyond kwize; search returned only unrelated Jiddu 'Notebook' material about bodily strain. |
| q76f1764e | verbatim | How I got into this state I … | single-source | realitysandwich.com | Exact sentence not found on any host besides realitysandwich; Wikisource Mystique Part One and The Natural State carry related but different wording. |
| q77b540c6 | verbatim | This can also lead to self-destruction for … | single-source | kwize.com | Only kwize; no primary host surfaced. |
| q8017e676 | fragment | man, who supposedly has achieved so much … | single-source | people.well.com | Exact phrase not indexed by search; results were general seismology pages. Only the catalogue's WELL primary. |
| q93a61f20 | verbatim | I have nothing to say and what … | single-source | ug-k.blogspot.com | Only the ug-k.blogspot transcription of Bhatt's biography; wording is Bhatt's record of U.G. speaking. |
| q9c3dac12 | fragment | is not yours; it is something which … | single-source | en.wikisource.org | Exact phrase not found on any second host; search returned only Jiddu material on inherited conditioning ('two million years of conditioning'), which is a different line. |
| qa2698ac8 | verbatim | It is a business; it has become … | single-source | praveennv.blogspot.com | Only the praveennv blog 'true guru' post; same passage contains q241d3a5e. |
| qb4eaccd2 | verbatim | The basic question which we have to … | single-source | en.wikisource.org | Exact phrase 'model of a perfect being' not found on any second host; only the Wikisource primary. Chapter-number discrepancy (7 vs 8). |
| qbb683516 | verbatim | The body changes from one state into … | single-source | en.wikisource.org | Exact phrase found on no second host; search returned only unrelated science pages. |
| qca29deea | fragment | Can you give me what you have? | single-source | en.wikipedia.org, jhana8.com, people.well.com | Exact wording not found on any host; hosts give a different wording of the same question, addressed to Ramana Maharshi (not J. Krishnamurti). |
| qcc769ade | fragment | By giving money they control you, and … | single-source | inner-quest.org | Only inner-quest.org carries the line. |
| qcf088078 | verbatim | in the 'natural state' the continuity of … | single-source | en.wikisource.org | Exact wording not found on any second host; search returned only Jiddu material on 'continuity'. Primary host only. |
| qf71956be | fragment | "An ashram-like atmosphere can't grow around me," … | single-source | en.wikisource.org, kwize.com | Search surfaced no host beyond the catalogue's kwize/Wikisource pair. Reported speech recorded by Chandrasekhar. |
| qfd63f8c6 | verbatim | Thought has interfered and trying to suppress, … | single-source | goodreads.com | Only Goodreads carries the exact phrase; the Goodreads work page names a different book than the catalogue's 'Thought is Your Enemy'. No primary host found. |
| qdc117690 | fragment | frauds who promise you some goodies that … | not-found | — | Exact phrase not indexed by search; results were only commentary about U.G. calling teachers frauds. Catalogue already lists two primary hosts, which this pass could not independently confirm. |

## Per-verdict summary

| verdict | count |
|---|---|
| corroborated-primary | 16 |
| corroborated-secondary | 15 |
| single-source | 16 |
| not-found | 1 |
| **total checked** | **48** |

By kind checked: verbatim 19, fragment 28, paraphrase 1.  
Previous catalogue verdict of the checked quotes: corroborated-primary 16, single-source 18, corroborated-secondary 13, not-found 1.

Observations:

- Every quote that resolved to a book resolved to a U.G. book; no quote was found to be Jiddu's (`not-ug` = 0).
- 16 of the 41 `primary-source` quotes checked gained a second host; the other `primary-source` ones (`qb4eaccd2`, `qcf088078`, `q03c8d952`, `qbb683516`, `q9c3dac12`, `q8017e676`, `qf71956be`) sit only on Wikisource/WELL and are not indexed by search engines under their exact wording.
- Aggregator-only quotes (Goodreads, quotefancy, azquotes, libquotes, quotepark) copy one another; their agreement raises confidence in wording but not in the book attribution, which they often supply from the Goodreads work page.
- Several Swan Song / Stopped in Our Tracks / Bhatt lines are editor-recorded speech (Louis Brawley, K. Chandrasekhar, Mahesh Bhatt) rather than U.G.'s own prose; this is noted per row.

## Attribution and book conflicts

**Attribution to Jiddu Krishnamurti (misattributions on third-party hosts, not supported by any primary text):**

- `qbb1ee524` "Nature is busy creating absolutely unique individuals…" — listed under Jiddu on steveleasock.com; all other hosts and the book (Mind Is a Myth) say U.G.
- `q5061960a` "It [thought] is a mechanical thing…" — quotepark files it under Jiddu Krishnamurti; WELL (Chandrasekhar's Stopped in Our Tracks, Book Two) and Wikiquote give U.G.
- `qa52816a8` / `qd70eb646` "You love fear. The ending of fear is death…" — exploringyourmind.com frames the passage as Jiddu's; Wikisource Mind is a Myth ch. I confirms U.G.
- `q241d3a5e` "as long as you depend upon somebody…" — not a misattribution, but search surfaces Jiddu's genuinely distinct line "You cannot depend upon anybody" (Freedom from the Known); do not conflate.

**Editor / recorder attributions (words recorded by someone other than U.G.):**

- Mahesh Bhatt: `q93a61f20` (A Life), `qd9a45360` / `qd0ca3a02` (A Taste of Death — Wikiquote warns Bhatt's own sentence "You are what you do…" is sometimes merged into the quote).
- K. Chandrasekhar / Narayana Moorty: `q5061960a`, `qd829349e`, `qf71956be`, `q5e5b2970`, `q8017e676` (Stopped in Our Tracks).
- Louis Brawley (dictation, Feb 2007): `q41a1cd4e`, `q68c996ce`, `qdc117690` (My Swan Song).
- Mukunda Rao: `q2384f6fc` is quoted inside Rao's blurb for The Biology of Enlightenment; the line itself is also printed in Thought is Your Enemy and The Natural State.
- Mark Whitwell: `qba6902b4` "Meditation is evil." is Whitwell's recollection; the printed form (Mind is a Myth ch. I) is "meditation is itself an evil".

**Book / chapter discrepancies between catalogue and hosts:**

- `q64ae758c` "bogus wares offered up by the experts" — catalogue: My Swan Song; Wikisource, WELL, Scribd all: Mind is a Myth ch. I. Re-check.
- `qbb1ee524` — catalogue: The Courage to Stand Alone; aggregators: Mind Is a Myth (1987).
- `qfd63f8c6` — catalogue: Thought is Your Enemy; Goodreads work page: 'Certainty: Life has no beginning, no end'.
- `qf69919b2` — catalogue: Thought is Your Enemy; Goodreads: No Way Out.
- `qa52816a8` — catalogue: No Way Out; the passage is in Mind is a Myth ch. I (duplicate of `qd70eb646`).
- `qb4eaccd2` — catalogue: No Way Out ch. 8; hosts give the chapter title 'What Kind Of Human Being Do You Want?' as ch. 7.
- `q77d45a2c` — catalogue unassigned; hosts: No Way Out, but split between ch. 4 and ch. 7.
- `q9cf31b1c`, `qc0edce3e` — catalogue: The Natural State; hosts: The Mystique of Enlightenment (the Natural State compilation reprints Mystique). Not a true conflict.
- `q9e846fe8`, `q3b41db6a` — printed in two U.G. books each (No Way Out / The Courage to Stand Alone; No Way Out ch. 1 / Thought is Your Enemy). Not a true conflict.
- `q5e5b2970` — catalogue blog titles it Thought is Your Enemy; WELL places it in Chandrasekhar's Stopped in Our Tracks, Book Two.
- `qca29deea` "Can you give me what you have?" — hosts give the question in different words ("This thing called moksha, can you give it to me?") and addressed to Ramana Maharshi (1939), not J. Krishnamurti.

**Wording variants worth normalising:**

- `q118b8994`: "Thinking does not put an end to sorrow."
- `qbb1ee524`: "...to which all must conform. It is grotesque!"
- `q1c893a18`: "Sorrow is there for you as long as you think. There is actually no sorrow there to be free from. Thinking about and struggling against sorrow is sorrow."
- `q9e846fe8`: "you will find that you have no way of experiencing the reality of anything"
- `qb4eaccd2`: "Society has put before you the ideal of a 'perfect man'... (related Goodreads quote)"
- `q03c8d952`: "In that sense, there is nothing to understand."
- `q3814bcc6`: "Love thy neighbour as thyself"
- `q76f1764e`: "I wish I knew how I got into... what state? (Mystique Part One)" / "I somehow stumbled into this natural state on my own (The Natural State)"
- `q16c5e496`: "Is there such a thing as enlightenment at all? (catalign, from a 1980s interview)"
- `qf69919b2`: "What is responsible for our problems is the fear of losing what we have and what we know."
- `qa52816a8`: "You see, you love fear. The ending of fear is death, and you don't want THAT to happen. ... The death of fear is the only death."
- `qd70eb646`: "You love fear. The ending of fear is death, and you don't want that to happen."
- `q062c2482`: "...the other side of the Atlantic or Pacific. That any fool can do, but the courage to be on your own, to stand on your two solid feet, is something which cannot be given by somebody." / "...the other side of the Atlantic. That is not courage."
- `q241d3a5e`: "as long as you think you are totally helpless, you will depend on some outside agency (brooklynaikikai.com, different sentence)"
- `qb1981622`: "What you call 'yourself' is fear. The 'you' is born out of fear..."
- `qd9a45360`: "You think when you don't want to do anything. Thinking is a poor alternative to acting. Your thinking is consuming all your energy. Act, don't think!"
- `qd0ca3a02`: "...Thinking is a poor alternative to acting. Your thinking is consuming all your energy. Act, don't think!"
- `q1fb04988`: "Whatever you do to be free from the "self" also is a self-centred activity." / "By searching, you want to be free from the self, but whatever you are doing to free yourself from the self is the self."
- `q9a924078`: "We are trying to bridge this gap, which is horrible for us, which has no meaning, which is demanding something from us, with this fancy idea that there must be love between these two individuals."
- `qcc769ade`: "By giving money they control you, and by not giving money they control you... As long as you want something from someone, there will always be someone out there to control you."
- `q2384f6fc`: "That is the way you, stripped of the machinations of thought, are also functioning."
- `qca29deea`: "This thing called moksha, can you give it to me? — I can give it, but can you take it?"
- `q77d45a2c`: "Nature is interested in only two things—to survive and to reproduce one like itself. Anything you superimpose on that, all the cultural input, is responsible for the boredom of man."
- `q5e5b2970`: "'Be selfish and stay selfish,' that is my message. ... Wanting enlightenment is selfishness."
- `qba6902b4`: "meditation is itself an evil (Mind is a Myth ch. I)" / "Meditation is evil. It is a hoax pulled on humanity in the idea that there is something they have not yet realised. (Whitwell)"

## Not checked (budget)

53 even-id quotes remain unchecked, mostly paraphrases: `q07b7ff4c`, `q08218f4e`, `q0d1d00a2`, `q16ecbc00`, `q1a17d2c4`, `q1a68f39e`, `q1c8788f6`, `q27ae73f0`, `q2dd1ea30`, `q338b17ba`, `q373b0000`, `q3efc45a4`, `q43697aec`, `q441961c4`, `q48147bda`, `q4fc99cde`, `q55779bfa`, `q585101a0`, `q5af2e554`, `q670510be`, `q679cf6ae`, `q69a4a09e`, `q718e3b22`, `q7960d85e`, `q7969abd0`, `q828c848c`, `q8305f222`, `q85d5f7a2`, `q8d5ee424`, `q92ffcf50`, `q95504a40`, `q95e9c782`, `q9fd58abe`, `qa1859f82`, `qaa3bf764`, `qac537b40`, `qb0c876bc`, `qb3256f66`, `qbd194c2e`, `qbee19952`, `qc40e7904`, `qcc9c525e`, `qcfa88a48`, `qd124d20c`, `qd39fb8fe`, `qdb7053b4`, `qea825286`, `qea9473ac`, `qeb9c85d2`, `qf7b06ab4`, `qf83cd77e`, `qf9704722`, `qff9ae05a`.

## Sources

- https://en.wikisource.org/wiki/Mind_is_a_Myth/I — q118b8994, q8282292e, qd70eb646, q64ae758c, qba6902b4
- https://people.well.com/user/jct/chapter1.html — q118b8994, q64ae758c
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti — q118b8994, q1c893a18, qd1cb605c, qf69919b2
- http://remembering-ug.blogspot.com/2012/07/passages-270812.html — q118b8994, q1c893a18
- https://o-meditation.com/wp-content/uploads/2011/05/krishnamurti-u-g-mind-is-a-myth.pdf — q118b8994, q1c893a18, q64ae758c
- https://www.goodreads.com/work/quotes/46398939-u-g-krishnamurti-certainty-life-has-no-beginning-no-end — qfd63f8c6
- https://www.goodreads.com/quotes/8510744-the-body-cannot-be-afraid-of-death-the-movement-that — qbd6fe67c, qb1981622
- https://www.goodreads.com/work/quotes/6212984-no-way-out-dialogues-with-krishnamurti — qbd6fe67c
- https://quotessayings.net/topics/krishnamurti-death/ — qbd6fe67c
- https://www.goodreads.com/quotes/73098-nature-is-busy-creating-absolutely-unique-individuals-whereas-culture-has — qbb1ee524
- https://quotefancy.com/quote/923745/U-G-Krishnamurti-Nature-is-busy-creating-absolutely-unique-individuals-whereas-culture — qbb1ee524
- https://www.azquotes.com/quote/363380 — qbb1ee524
- https://www.inspiringquotes.us/quotes/qFLR_q1QjlTph — qbb1ee524
- https://quotepark.com/authors/ug-krishnamurti/ — qbb1ee524
- https://quotefancy.com/quote/2210935/U-G-Krishnamurti-Sorrow-is-there-for-you-as-long-as-you-think-There-is-actually-no-sorrow — q1c893a18
- http://ug-k.blogspot.com/2007/04/conversations-following-conversations.html — q93a61f20
- https://www.goodreads.com/book/show/25601775-truth — q8282292e
- https://www.harpeony.com/articles/book-summary-the-natural-state-in-the-words-of-ug-krishnamurti-part-23 — q8282292e
- https://en.wikisource.org/wiki/No_Way_Out — q9e846fe8, qb4eaccd2
- http://nondualite.free.fr/c_ug_courage.htm — q9e846fe8
- https://www.youtube.com/watch?v=kDgOKc-YRnI — q9e846fe8
- https://en.wikisource.org/wiki/The_Natural_State — qcf088078, q9cf31b1c, q2384f6fc, qc0edce3e
- https://kwize.com/en/texts/U-G-Krishnamurti-Science-and-U-G/ — q39067cd0, q77b540c6
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Four — q03c8d952
- https://en.wikisource.org/wiki/Mind_is_a_Myth/IV — q03c8d952
- https://www.inner-quest.org/UG_Nothing.htm — q03c8d952
- https://people.well.com/user/jct/chandra.htm — q5061960a, q5e5b2970
- https://en.wikiquote.org/wiki/U._G._Krishnamurti — q5061960a, q16c5e496, qd9a45360, qd0ca3a02
- https://quotepark.com/quotes/1733648-ug-krishnamurti-it-thought-is-a-mechanical-thing-and-can-solve-o/ — q5061960a
- http://praveennv.blogspot.com/2016/03/ug-krishnamurtis-quote-on-true-guru.html — qa2698ac8, q241d3a5e
- https://en.wikisource.org/wiki/Science_and_U.G. — qbb683516
- https://www.hindu-blog.com/2018/09/u-g-krishnamurti-quotes-and-teachings.html — q3814bcc6, q41a1cd4e
- https://en.wikisource.org/wiki/Stopped_in_Our_Tracks:_Stories_of_U.G._in_India — qd829349e, qf71956be
- http://u-g-krishnamurti.blogspot.com/2007/04/there-is-no-moksha-no-jivanmukti-and-no.html — qd829349e
- https://people.well.com/user/jct/ — qd829349e, q8017e676
- https://www.realitysandwich.com/ — q76f1764e
- https://people.well.com/user/jct/mystiq1.htm — q16c5e496
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-The-Mystique-of-Enlightenment.pdf — q16c5e496
- https://ia801804.us.archive.org/12/items/UGKrishnamurtiOnU.G185p/UG%20Krishnamurti%20-%20On%20U.G%20(185p).pdf — q16c5e496
- https://www.catalign.in/2020/06/why-does-u-g-krishnamurti-ask-is-there.html — q16c5e496
- https://en.wikisource.org/wiki/Thought_is_Your_Enemy — qd1cb605c
- https://quotefancy.com/u-g-krishnamurti-quotes — qd1cb605c, q1fb04988
- https://quotessayings.net/topics/being-prepared-for-the-future/ — qd1cb605c
- https://people.well.com/user/jct/nwo1.htm — q3b41db6a
- https://people.well.com/user/jct/enemy0.htm — q3b41db6a
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=3 — q3b41db6a
- https://www.inner-quest.org/UG_Words.htm — q3b41db6a, qd9a45360, q1fb04988, q68c996ce, qcc769ade
- http://praveennv.blogspot.com/2016/03/ug-krishnamurthi-on-god-or-enlightenment.html — q3b41db6a
- https://astitvameditation.com/2020/11/20/fear-of-losing-u-g-krishnamurti/ — qf69919b2
- https://quotlr.com/author/ug-krishnamurti — qf69919b2
- https://libquotes.com/u-g-krishnamurti/quotes/fear — qf69919b2, qa52816a8, qd70eb646, qb1981622
- https://thequotearchive.com/quotes/U.G.%20Krishnamurti — qf69919b2
- https://quotefancy.com/quote/923772/U-G-Krishnamurti-You-love-fear-The-ending-of-fear-is-death-and-you-don-t-want-that-to — qa52816a8, qd70eb646
- https://www.azquotes.com/quote/755135 — qa52816a8, qd70eb646
- https://quotestats.com/topic/quotes-about-krishnamurti-death/ — qa52816a8
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html — qa52816a8
- https://www.goodreads.com/quotes/590899-you-can-have-the-courage-to-climb-the-mountain-swim — q062c2482
- https://quotepark.com/quotes/1922951-ug-krishnamurti-you-can-have-the-courage-to-climb-the-mountain-sw/ — q062c2482
- https://www.azquotes.com/quote/487305 — q062c2482
- https://libquotes.com/u-g-krishnamurti/quote/lbc3l4a — q062c2482
- https://o-meditation.com/wp-content/uploads/2011/05/the-courage-to-stand-alone.pdf — q062c2482
- https://people.well.com/user/jct/SWAN_SONG.htm — q41a1cd4e, q68c996ce
- https://medium.com/@alysion42/u-g-krishnamurtis-swan-song-updated-e36a07cc0595 — q41a1cd4e
- https://www.sciforums.com/threads/the-last-message-of-u-g-krishnamurti.95095/ — q41a1cd4e
- https://groups.google.com/g/noshonuts/c/fGiwo09RzyI — q41a1cd4e
- https://www.scribd.com/book/487774373/Mind-is-a-Myth — q64ae758c
- https://www.zhenhost.net/Mind_is_a_Myth_1.html — q64ae758c
- https://www.goodreads.com/quotes/984886-what-is-morality-it-is-not-the-following-of-enjoined — qb253e5d0
- https://www.goodreads.com/work/quotes/52201-the-mystique-of-enlightenment-the-radical-ideas-of-u-g-krishnamurti — qb253e5d0
- https://infant7sorrow.wordpress.com/ug/ — qb253e5d0
- https://www.beyond5.co.in/post/quotes-u-g-krishnamurti — qb253e5d0
- https://grokipedia.com/page/U._G._Krishnamurti — qb253e5d0
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=2 — qb1981622, q9a924078, q77d45a2c
- https://quotefancy.com/quote/923753/U-G-Krishnamurti-You-think-when-you-don-t-want-to-do-anything-Thinking-is-a-poor — qd9a45360, qd0ca3a02
- https://www.azquotes.com/author/17848-U_G_Krishnamurti — qd9a45360
- http://nirvana73.blogspot.com/2013/03/from-ug-krishnamurti-life-by-mahesh.html — qd9a45360
- https://whatsmyquote.com/quote/you-think-when-you-don-t-want-to-do-anything-thinking-is-a-poor-alternative-to-acting-your-thinking-is — qd0ca3a02
- https://www.azquotes.com/quote/765776 — q1fb04988
- https://jhana8.com/ug-krishnamurti-quotes/ — q1fb04988
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Two — q9cf31b1c
- https://jhana8.com/ug-krishnamurtis-natural-state/ — q9cf31b1c
- https://onbeyondzen.com/ug-krishnamurti/ — q9cf31b1c
- https://www.awakeningtoreality.com/2018/10/ug-krishnamurti-mystique-of.html — q9cf31b1c
- https://www.ugkrishnamurti.in/ug-essence/my-swan-song — q68c996ce
- https://kwize.com/en/texts/U-G-Krishnamurti-Stopped-in-Our-Tracks-Stories-of-U-G-in-India/ — qf71956be
- https://www.goodreads.com/work/quotes/43411143-u-g-krishnamurti-love-love-implies-division-separation — q9a924078
- https://quotessayings.net/topics/love-krishnamurti/ — q9a924078
- https://people.well.com/user/jct/note.htm — q2384f6fc
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Thought-is-Your-Enemy.pdf — q2384f6fc
- https://dokumen.pub/the-penguin-ug-krishnamurti-reader-0143101021-9780143101024.html — q2384f6fc
- http://remembering-ug.blogspot.com/2012/09/passages-from-thought-is-your-enemy.html — q2384f6fc
- https://www.abebooks.com/9789350290095/BIOLOGY-ENLIGHTENMENT-Rao-Mukunda-935029009X/plp — q2384f6fc
- https://en.wikipedia.org/wiki/U._G._Krishnamurti — qca29deea
- https://jhana8.com/ug-krishnamurti-biography/ — qca29deea
- https://people.well.com/user/jct/ugbio/ugbio4.htm — qca29deea
- https://www.azquotes.com/quote/949641 — q77d45a2c
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html?m=1 — q77d45a2c
- https://quotepark.com/authors/ug-krishnamurti/man/ — q77d45a2c
- https://quotefancy.com/quote/923749/U-G-Krishnamurti-Nature-is-interested-in-only-two-things-to-survive-and-to-reproduce-one — q77d45a2c
- https://dalemusings.wordpress.com/2012/12/25/thought-is-your-enemy-u-g-krishnamurti/ — q5e5b2970
- https://markwhitwell.medium.com/my-life-with-u-g-krishnamurti-mark-whitwell-f596037e9fbf — qba6902b4
- https://soulmind.in/ug-krishnmurti-meditation-is-evil — qba6902b4
- https://www.quora.com/Why-do-some-teachers-recommend-meditation-J-Krishnamurti-said-a-method-based-meditation-dulls-the-mind-U-G-Krishnamurti-called-meditation-evil-There-are-others-who-meditate-for-many-years-without-any-spiritual — qba6902b4
- https://en.wikisource.org/wiki/Mind_is_a_Myth/III — q9c3dac12
- https://kwize.com/en/texts/U-G-Krishnamurti-The-Mystique-of-Enlightenment/ — qc0edce3e
- https://www.dhammawheel.com/viewtopic.php?t=30425&start=120 — qc0edce3e
