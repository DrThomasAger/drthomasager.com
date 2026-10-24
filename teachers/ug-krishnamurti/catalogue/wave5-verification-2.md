# Wave 5 — Quote verification pass 2 (U.G. Krishnamurti)

Second independent verification pass over `quotes.json`. Scope: quotes whose previous verdict was **not** in the skip set (corroborated-primary / corroborated-secondary / disputed / not-found / not-ug). Priority order: verbatim single-source (29), verbatim multi-source (21), then verbatim primary-source and multi-source fragments as budget allowed. **70 quotes searched, 70 exact-phrase WebSearch queries (extended mode).** Jiddu Krishnamurti hosts (kfoundation.org, jkrishnamurti.org, kfa.org) were blocked on every query; krishnamurti.org hits that surfaced were all unrelated JK talks and are not counted as confirmation.

Verdict rules used: *corroborated-primary* = wording confirmed on en.wikisource.org, people.well.com, archive.org or ugkrishnamurti.in; *corroborated-secondary* = at least two independent non-primary domains confirm the wording (or the originating interview transcript); *single-source* = one domain only; *disputed* = exact wording not found but the idea exists in a primary text with different wording; *not-found* = no host carries the wording.

## Results table

| id | first words | verdict | confirming hosts | note |
|---|---|---|---|---|
| qfd63f8c6 | Thought has interfered and trying to suppress,… | single-source | goodreads.com | Only goodreads.com hosts the wording (three Goodreads pages, one domain). Goodreads files it under the Certainty anthology; quotes.json says Thought is Your Enemy. No primary host. Not attributed to JK anywhere. |
| q1c893a18 | Thinking about and struggling against 'sorrow' is… | corroborated-secondary | goodreads.com, quotefancy.com | Second host (quotefancy.com) confirms wording; krishnamurti.org (JK) results are unrelated JK talks on sorrow, not this wording. |
| qe27976db | You hook up each thought with the… | single-source | goodreads.com | Only Goodreads carries the exact sentence; other hits are JK pages on continuity with different wording. Not found on Wikisource Mind is a Myth via search. |
| q044d9da9 | It is not an illusion, only your… | single-source | goodreads.com | ATTRIBUTION CONFLICT: search surfaces it on the Goodreads 'Mind Is a Myth' quotes page, while quotes.json (and an earlier Goodreads listing noted in quotes.json) file it under The Courage to Stand Alone. Only goodreads.com hosts it. |
| qd05c2db1 | you arrive seeking understanding, while I am… | corroborated-primary | **en.wikisource.org** | Primary host en.wikisource.org confirms; chapter title matches the phrase. |
| qacfbd56d | Life has to be described in pure… | corroborated-secondary | azquotes.com, emperyquotes.com, quotlr.com, wisefamousquotes.com | Multiple quote aggregators agree on wording; followed by 'It has to be demystified and depsychologised.' wisefamousquotes.com credits one copy to 'Jiddu Krishnamurti' (misattribution) while crediting the follow-on sentence to UG. No primary host found. |
| q25e43852 | There is nothing there - no soul… | corroborated-secondary | quotefancy.com, quotessayings.net, quotlr.com, remembering-ug.blogspot.com | quotes.json has book 'unassigned'; a UG-community blog places it in The Mystique of Enlightenment. No primary host hit. |
| qec037541 | The only relationship you have with anybody… | disputed | **en.wikisource.org** | Exact sentence 'The only relationship you have with anybody in this world is "What do I get out of it?"' NOT found on any host; the primary text (Wikisource No Way Out ch. 8) carries the idea with different wording. Treat as paraphrase, not verbatim. Other hits are JK quotes on relationship (not this wording). |
| q93a61f20 | I have nothing to say and what… | single-source | ug-k.blogspot.com | Single host (a blog reproducing Mahesh Bhatt's biography). The surrounding text is UG speaking in a recorded conversation reported by Bhatt; wording is UG's reported speech, not Bhatt's narration. |
| q71efd67f | Hope is necessary for tomorrow, not for… | corroborated-primary | **en.wikisource.org**, goodreads.com | Primary host en.wikisource.org confirms; chapter title matches. |
| q1fb36c86 | Not a calamity to me but a… | corroborated-primary | en.wikipedia.org, **en.wikisource.org**, encyclopedia.com, **people.well.com**, ug-k.blogspot.com | Two primary hosts (en.wikisource.org, people.well.com). Duplicate of qad57ce7d with slightly different wording. |
| q80ebe1ef | The pleasure of sex, for instance, is… | corroborated-primary | **en.wikisource.org**, goodreads.com, remembering-ug.blogspot.com | Primary host en.wikisource.org confirms exact sentence. Three different book attributions across hosts (the passage is reused across UG compilations). quotes.json has 'unassigned'. |
| q39067cd0 | Love, compassion, ahimsa, understanding, bliss, all these… | single-source | kwize.com | Only kwize.com carries the wording ('are only adding to the strain of the body'). All other hits are JK pages on love/compassion with unrelated wording; no primary host. |
| q62dd75b6 | All your experiences, all your meditations, all… | corroborated-secondary | azquotes.com, inner-quest.org, jhana8.com, quotefancy.com, quotlr.com | Five secondary hosts agree; inner-quest.org is a UG-community transcript page. No primary host or book named. |
| q08a43a02 | I am only interested in describing this… | corroborated-secondary | amazon.com, awakeningtoreality.com, goodreads.com, simonandschuster.com | Publisher (Simon & Schuster) and multiple hosts confirm; the Wikisource Mystique text did not surface in this search but the awakeningtoreality page reproduces the book text. |
| qa2698ac8 | It is a business; it has become… | single-source | praveennv.blogspot.com | One blog host only. Passage is the 'true guru / shoddy pieces of goods in the market place' talk. No primary host. |
| q1676a73f | It is fear that makes you believe… | corroborated-secondary | emperyquotes.com, goodreads.com, praveennv.blogspot.com, quotes.pub, quotlr.com | Multiple secondary hosts; no primary host found by search. |
| q21e36727 | Because you cannot face the impermanence of… | corroborated-secondary | azquotes.com, jhana8.com, onlygodis.com, quotefancy.com | quotes.json has 'unassigned'; sources name Mind is a Myth ch. 4. No primary host hit. |
| q39d01d99 | Transformation, moksha, liberation, and all that stuff… | corroborated-primary | inner-quest.org, **people.well.com** | ATTRIBUTION CONFLICT: quotes.json says No Way Out; the primary host (people.well.com) files it in Thought is Your Enemy. Minor wording difference (of/on). Cf. q3b41db6a which already carries Thought is Your Enemy. |
| q7f2ee6c3 | The body or organism is not interested… | single-source | kwize.com | Only kwize.com; no second host, no primary host. |
| q77b540c6 | This can also lead to self-destruction for… | single-source | kwize.com | Only kwize.com; krishnamurti.org (JK) hits are unrelated JK talks. No primary host. |
| qd74b2e4b | Political institutions and ideologies are the warty… | corroborated-secondary | elephantjournal.com, en.wikiquote.org, goodreads.com, libquotes.com | ATTRIBUTION CONFLICT: all confirming hosts file it under No Way Out; quotes.json has Thought is Your Enemy. Wording agrees across hosts. No primary host hit. |
| q8d5e7e71 | Yes it is. Because thought is violent.… | corroborated-secondary | hindu-blog.com, inner-quest.org | Two secondary hosts. No primary host; quotes.json's 'Thought is Your Enemy' not named by sources. |
| q3814bcc6 | Don't forget that in the name of… | single-source | hindu-blog.com | Only one host carries the exact passage. No primary host; book unconfirmed. |
| qb4728a46 | The body does not exist except as… | corroborated-secondary | goodreads.com, praveennv.blogspot.com | Two hosts (goodreads.com, praveennv.blogspot.com). quotes.json 'unassigned'; Goodreads files it in Mind Is a Myth. |
| q4e912343 | The knowledge about it, all that he… | corroborated-primary | **en.wikisource.org** | ATTRIBUTION CONFLICT: primary host places the sentence in The Mystique of Enlightenment Part Two; quotes.json has The Natural State (the Natural State compilation reuses Mystique passages, so both may be true). Single host, but primary. |
| qc213105f | Making love is war.… | corroborated-primary | **people.well.com** | EDITOR ATTRIBUTION: the phrase appears in the editor's introduction to Mind is a Myth as a summary of UG positions, not as a transcribed UG sentence. Only people.well.com hosts it (primary host). |
| qac8b2fca | Unquestioned action is morality.… | corroborated-secondary | beyond5.co.in, goodreads.com, infant7sorrow.wordpress.com, thequotearchive.com | Multiple hosts, consistent wording; search now places the Goodreads copy on the Mystique work page (resolving the earlier Mind Is a Myth note). No primary host hit. |
| q5f1205b6 | There is no power outside of man.… | corroborated-secondary | azquotes.com, en.wikiquote.org, inspiringquotes.us, jhana8.com, quotefancy.com, quotlr.com | Widely corroborated; Wikiquote places it in the passage on religious 'exploiters'. No primary host hit. |
| q3148c69a | We don't want to be free from… | corroborated-secondary | emperyquotes.com, o-meditation.com, quotefancy.com, quotlr.com | Four secondary hosts agree; no primary host or book named. |
| q7a1ee58c | Thought can never capture the movement of… | corroborated-primary | azquotes.com, en.wikiquote.org, goodreads.com, **people.well.com**, quotefancy.com, quotepark.com | people.well.com (primary host, 'Excerpts from Dialogues') surfaced; chapter placement disagrees between hosts. |
| qc94ba81d | If you have the courage to touch… | corroborated-secondary | azquotes.com, en.wikiquote.org, goodreads.com, quotefancy.com, quotepark.com | Chapter placement conflict between hosts; no primary host hit. |
| qd8034757 | There is no such thing as truth.… | corroborated-secondary | azquotes.com, jhana8.com, quotefancy.com, quoteslyfe.com, theysaidso.com | Many aggregators; no primary host hit. |
| q69f83f72 | There is no such thing as spiritual… | corroborated-secondary | catalign.in, en.wikiquote.org, jhana8.com, kwize.com | Book attribution differs between Wikiquote (Mind is a Myth) and kwize (Mystique). Wikisource Mystique Part Two surfaced in results but the sentence was not confirmed there. |
| q2c9515a2 | I have had to search and it… | corroborated-secondary | azquotes.com, en.wikiquote.org, jhana8.com, libquotes.com, remembering-ug.blogspot.com | Multiple hosts; no primary host hit. |
| q870d1afa | Nature is busy creating absolutely unique individuals,… | corroborated-secondary | azquotes.com, en.wikiquote.org, goodreads.com, quotefancy.com, quotepark.com | ATTRIBUTION NOTE: Wikiquote traces the wording via Mahesh Bhatt's A Taste of Death; Goodreads (see qbb1ee524) files it under The Courage to Stand Alone. UG's words in all versions. |
| qd42e2a22 | Society or culture or whatever you might… | corroborated-secondary | azquotes.com, en.wikiquote.org, inspiringquotes.us, libquotes.com, quotefancy.com | Three different book attributions across hosts; wording consistent. No primary host hit. |
| q77f34910 | You can have the courage to climb… | corroborated-secondary | azquotes.com, en.wikiquote.org, goodreads.com, libquotes.com, quotepark.com | Consistent across hosts; also covers q062c2482 and qd9402af0 (same passage). No primary host hit. |
| q086ab55c | Fear is the very thing that you… | corroborated-secondary | goodreads.com, praveennv.blogspot.com | Two hosts (goodreads.com + blog). No primary host hit. |
| qc774741b | What you call 'yourself' is fear. The… | corroborated-secondary | goodreads.com, quotessayings.net | Two domains (goodreads.com, quotessayings.net). Also covers qb1981622 (fragment of same sentence). No primary host hit. |
| q6fe326b5 | The body cannot be afraid of death.… | corroborated-secondary | goodreads.com, quotessayings.net | Two domains. quotessayings.net mixes UG and JK death quotes on one page but credits this one to UG. No primary host hit. |
| qb9d58205 | The stopping of doing is courage.… | corroborated-secondary | goodreads.com, kwize.com | Two hosts; three book attributions. No primary host hit. |
| q85310fad | A guru is one who tells you… | corroborated-secondary | azquotes.com, emperyquotes.com, en.wikiquote.org, praveennv.blogspot.com, quotefancy.com, quotepark.com | Widely corroborated; book attribution split between the Natural State compilation and Thought is Your Enemy. No primary host hit. |
| qd9402af0 | That any fool can do, but the… | corroborated-secondary | azquotes.com, en.wikiquote.org, goodreads.com, libquotes.com, o-meditation.com | o-meditation.com hosts a PDF of the book (full text, not a primary archive host). No en.wikisource/people.well.com/archive.org hit. |
| qb5941095 | You are trying to enforce peace through… | corroborated-secondary | heartofyoga.com, inner-quest.org | Two hosts confirm exact wording; krishnamurti.org (JK) hits are unrelated. No primary host or book named. |
| q93823c44 | It would be more interesting to learn… | corroborated-secondary | azquotes.com, emperyquotes.com, peakd.com, picturequotes.com, quotefancy.com | quotes.json 'unassigned'; AZQuotes names Stopped in Our Tracks Book Two. No primary host hit. |
| q01ae8cf2 | I am not anti-rational, just unrational. You… | corroborated-secondary | azquotes.com, en.wikiquote.org, quotefancy.com, quotepark.com, quotlr.com, stillnessspeaks.com | ATTRIBUTION NOTE: No Way Out ch. 1 is an essay by Dr. T.R. Raghunath, so the line may be quoted inside an editor's/commentator's chapter; aggregators also credit Mind Is a Myth. Wording consistent. |
| q762cadb3 | That is to say, all that is… | single-source | kwize.com | Only kwize.com hosts the exact sentence (quotes.json had two sources but search finds one domain). No primary host. |
| q6f67c3f2 | All doctors should be shot.… | corroborated-secondary | inner-quest.org, medium.com, remembering-ug.blogspot.com, sciforums.com, youtube.com | Multiple hosts including a video of UG saying it. quotes.json 'unassigned'; Swan Song is the written source. |
| qf440d043 | You don't have to do a thing.… | corroborated-secondary | en.wikiquote.org, nondualite.free.fr, quotepark.com | Short generic sentence; confirmed as a Part I title/line of The Courage to Stand Alone via a full-text transcription (nondualite.free.fr). Book split with Thought is Your Enemy for the longer form. |
| qc6b6c3b1 | To realize that there is no enlightenment… | corroborated-secondary | goodreads.com, kwize.com | Exact-phrase search returned only kwize; the Wikisource Part Four page already in quotes.json was not re-surfaced by search. Goodreads places the sentence after the No Way Out 'ultimate pleasure' passage, so book attribution is split (Mystique vs No Way Out). |
| q37d40528 | I call these events a calamity because… | corroborated-primary | en.wikipedia.org, **en.wikisource.org**, jhana8.com, **people.well.com**, ug-k.blogspot.com | Two primary hosts confirm. |
| qe646b0ed | This state is a physical condition of… | corroborated-primary | dhammawheel.com, **en.wikisource.org** | Primary host plus an independent forum quotation. |
| q2878603e | The natural state is acausal: it just… | corroborated-primary | awakeningtoreality.com, **en.wikisource.org**, inner-quest.org, simonandschuster.com | Primary host plus three secondary hosts. |
| q64b3e681 | Your thinking endlessly about being free from… | single-source | goodreads.com | Only goodreads.com surfaced for the exact sentence; quotes.json's primary (Wikisource) not re-surfaced. Other hits are JK sorrow talks (different wording). |
| qd2169deb | Sorrow is there for you as long… | corroborated-secondary | goodreads.com, quotefancy.com | Two secondary hosts; primary (Wikisource) not re-surfaced by search. |
| q4fd55d91 | God or Enlightenment is the ultimate pleasure,… | corroborated-primary | **en.wikisource.org**, goodreads.com, inner-quest.org, praveennv.blogspot.com | ATTRIBUTION CONFLICT: primary host places it in No Way Out ch. 1; quotes.json has Mind is a Myth. Wikisource Thought is Your Enemy also surfaced (passage reused). |
| qb324ba7b | Although I assert that all doctors should… | corroborated-secondary | inner-quest.org, remembering-ug.blogspot.com, youtube.com | Fan archives only; no primary host hit. |
| qb2f92764 | We are not created for any grander… | corroborated-secondary | azquotes.com, goodreads.com, praveennv.blogspot.com, quotepark.com | Consistent across hosts; primary (Wikisource) not re-surfaced. |
| qa56a998d | It is not love, compassion, humanism, or… | corroborated-secondary | goodreads.com, quotefancy.com | Also covers q40cf79f3 (same passage). Two domains; primary not re-surfaced. |
| qbe66ba38 | To be yourself requires extraordinary intelligence. You… | corroborated-primary | beyond5.co.in, **en.wikisource.org**, goodreads.com, inner-quest.org, kwize.com | Primary host confirms; many secondary hosts agree. |
| qb7fe3c01 | If anyone thinks he can help you,… | corroborated-secondary | azquotes.com, emperyquotes.com, inner-quest.org, jhana8.com | Four hosts; book attribution split. No primary host hit. |
| qba7b8f15 | It is the ones who believe in… | corroborated-primary | **en.wikisource.org**, libquotes.com, quotepark.com | Primary host (Wikisource The Natural State) plus two aggregators. Book: Mind is a Myth per aggregators, reused in The Natural State. |
| q989dde8c | …everything you stand for, believe in, experience… | corroborated-secondary | azquotes.com, emperyquotes.com, jhana8.com, libquotes.com, quotefancy.com, quotlr.com | Also covers qeee2e8cf (same text, 'unassigned'). Six hosts agree; no primary host hit. |
| q7e344096 | What is there is only the body.… | corroborated-secondary | intuitionnetwork.org | Single host, but it is the interview producer's own transcript (Intuition Network / Thinking Allowed), i.e. the originating source for this interview; treated as corroborated-secondary rather than single-source. Not on the four named primary hosts. |
| q0997ce6d | Each cell of a living organism cooperates… | single-source | goodreads.com | Only goodreads.com. No primary host. |
| qa095f585 | I have one thing against medical technology…… | corroborated-secondary | en.wikiquote.org, kwize.com, quotepark.com, quotewise.io, yquotes.com | quotes.json 'unassigned'; hosts name Mystique. No primary host hit. |
| q3987c101 | It [thought] is a mechanical thing and… | corroborated-primary | en.wikiquote.org, **people.well.com**, quotepark.com | Primary host people.well.com confirms. |
| qf71956be | "An ashram-like atmosphere can't grow around me,"… | single-source | kwize.com | Only kwize.com surfaced; quotes.json's primary source not re-surfaced. Note the sentence is Chandrasekhar's narration quoting UG ('roared U.G.'). |
| q190abbe4 | The belief in reincarnation will only help… | not-found | — | Exact sentence not found on any host. All hits are Jiddu Krishnamurti pages on reincarnation with different wording — risk of JK confusion; keep as fragment/paraphrase pending a check of the Thought is Your Enemy text. |

## Summary per verdict

- corroborated-primary: 15
- corroborated-secondary: 40
- single-source: 13
- disputed: 1
- not-ug: 0
- not-found: 1
- total searched: 70

### Verdict changes versus quotes.json

- multi-source → corroborated-secondary: 25
- single-source → corroborated-secondary: 10
- single-source → single-source: 9
- single-source → corroborated-primary: 7
- primary-source → corroborated-secondary: 5
- primary-source → corroborated-primary: 5
- multi-source → corroborated-primary: 3
- multi-source → single-source: 2
- primary-source → single-source: 2
- single-source → disputed: 1
- primary-source → not-found: 1

## Book attribution conflicts

Cases where the confirming hosts name a different book from `quotes.json`, or disagree among themselves. UG remains the speaker in every case; no source attributes any checked quote to Jiddu Krishnamurti except one stray wisefamousquotes.com listing (qacfbd56d), which is a visible misattribution.

- **q044d9da9** — quotes.json: The Courage to Stand Alone; Goodreads Mind Is a Myth work page also carries it
- **qfd63f8c6** — quotes.json: Thought is Your Enemy; Goodreads files it under the Certainty anthology
- **q39d01d99** — quotes.json: No Way Out; primary host people.well.com files it in Thought is Your Enemy (wording 'variations OF the same theme')
- **qd74b2e4b** — quotes.json: Thought is Your Enemy; Wikiquote, Goodreads, Libquotes all say No Way Out
- **q4e912343** — quotes.json: The Natural State; Wikisource places it in The Mystique of Enlightenment Part Two
- **q4fd55d91** — quotes.json: Mind is a Myth; Wikisource places it in No Way Out ch. 1 (also reused in Thought is Your Enemy)
- **q80ebe1ef** — quotes.json: unassigned; Wikisource The Natural State vs Goodreads No Way Out vs remembering-ug Mind is a Myth
- **qd42e2a22** — quotes.json: Thought is Your Enemy (one host agrees); Wikiquote says No Way Out; another host says Mystique 2002 ed.
- **qb9d58205** — quotes.json: The Courage to Stand Alone; kwize says Science and U.G.; Goodreads says Mind Is a Myth
- **q85310fad** — quotes.json: The Natural State (aggregators agree, p. 141); Wikiquote says Thought is Your Enemy ch. II 'Throw Away Your Crutches'
- **q69f83f72** — quotes.json: Mind is a Myth (Wikiquote agrees); kwize lists it under The Mystique of Enlightenment
- **q870d1afa** — quotes.json: Mind is a Myth (most hosts agree); Wikiquote traces the wording via Mahesh Bhatt's A Taste of Death (1995); Goodreads also files it under The Courage to Stand Alone (qbb1ee524)
- **qb7fe3c01** — quotes.json: The Mystique of Enlightenment; aggregators split between Mystique (2002 ed.) and Stopped in Our Tracks Book Two
- **qc6b6c3b1** — quotes.json: The Mystique of Enlightenment (Wikisource Part Four); Goodreads appends the sentence to a No Way Out passage
- **q01ae8cf2** — quotes.json: No Way Out (Wikiquote agrees: ch. 1, which is Dr T.R. Raghunath's essay, so possibly quoted inside a commentator's chapter); many aggregators say Mind Is a Myth
- **qf440d043** — quotes.json: The Courage to Stand Alone Part I (transcription agrees); Wikiquote files the longer sentence under Thought is Your Enemy
- **q7a1ee58c / qc94ba81d** — Mind is a Myth agreed, but chapter placement differs between Wikiquote and AZQuotes/Quotepark
- **q25e43852, q21e36727, qb4728a46, q93823c44, q6f67c3f2, qa095f585** — quotes.json 'unassigned'; hosts supply a book (Mystique; Mind is a Myth ch. 4; Mind Is a Myth; Stopped in Our Tracks Book Two; My Swan Song; Mystique respectively)

### Editor / biographer attribution notes

- **qc213105f** ("Making love is war") — appears only in Terry Newland's editorial introduction to *Mind is a Myth* (people.well.com/user/jct/intro.html) as a one-line summary of UG positions, not as a transcribed UG sentence.
- **q93a61f20** — reported speech inside Mahesh Bhatt's *U.G. Krishnamurti: A Life*; UG is the speaker, Bhatt the reporter; one blog host only.
- **qf71956be** — Chandrasekhar's narration quoting UG ("roared U.G.") in *Stopped in Our Tracks*.
- **q870d1afa** — Wikiquote sources the wording to Bhatt's *A Taste of Death*.

### Wording issues

- **qec037541** — exact sentence not found anywhere; Wikisource *No Way Out* ch. 8 has the idea as "all relationships are built on the foundation of 'What do I get out of this relationship?'" → downgraded to *disputed* (paraphrase, not verbatim).
- **q190abbe4** — not found; every hit is a Jiddu Krishnamurti reincarnation page, so this fragment is at risk of JK confusion.
- **q39d01d99** — hosts read "variations of the same theme", quotes.json "variations on".
- **q7a1ee58c** — some aggregators read "moment of life" for "movement of life".
- **q1fb36c86 / qad57ce7d** — the same Mystique Part One sentence in two renderings ("but a calamity to those" vs "but to those").

## Not searched

Budget was reserved after 70 queries. Still unchecked from the pool: the remaining verbatim primary-source items (e.g. qbd194c2e "If you want to call it that", q118b8994), all paraphrase items, and most fragments with verdict single-source/primary-source (about 149 quotes).

## Sources

- goodreads.com — 38 confirmations
- azquotes.com — 18 confirmations
- quotefancy.com — 17 confirmations
- en.wikiquote.org — 15 confirmations
- en.wikisource.org (primary) — 12 confirmations
- quotepark.com — 11 confirmations
- kwize.com — 10 confirmations
- inner-quest.org — 10 confirmations
- jhana8.com — 9 confirmations
- quotlr.com — 8 confirmations
- emperyquotes.com — 7 confirmations
- praveennv.blogspot.com — 7 confirmations
- libquotes.com — 7 confirmations
- people.well.com (primary) — 6 confirmations
- remembering-ug.blogspot.com — 5 confirmations
- quotessayings.net — 3 confirmations
- ug-k.blogspot.com — 3 confirmations
- en.wikipedia.org — 2 confirmations
- awakeningtoreality.com — 2 confirmations
- simonandschuster.com — 2 confirmations
- hindu-blog.com — 2 confirmations
- beyond5.co.in — 2 confirmations
- inspiringquotes.us — 2 confirmations
- o-meditation.com — 2 confirmations
- youtube.com — 2 confirmations
- wisefamousquotes.com — 1 confirmations
- encyclopedia.com — 1 confirmations
- amazon.com — 1 confirmations
- quotes.pub — 1 confirmations
- onlygodis.com — 1 confirmations
- elephantjournal.com — 1 confirmations
- thequotearchive.com — 1 confirmations
- infant7sorrow.wordpress.com — 1 confirmations
- theysaidso.com — 1 confirmations
- quoteslyfe.com — 1 confirmations
- catalign.in — 1 confirmations
- heartofyoga.com — 1 confirmations
- peakd.com — 1 confirmations
- picturequotes.com — 1 confirmations
- stillnessspeaks.com — 1 confirmations
- medium.com — 1 confirmations
- sciforums.com — 1 confirmations
- nondualite.free.fr — 1 confirmations
- dhammawheel.com — 1 confirmations
- intuitionnetwork.org — 1 confirmations
- quotewise.io — 1 confirmations
- yquotes.com — 1 confirmations

All URLs are listed per quote in `/tmp/claude-0/-home-user-drthomasager-com/7c7edf2e-a0bd-5288-a28d-2ac0e832645f/scratchpad/json/verification-2.json`. Input: `/home/user/drthomasager.com/hanjopurebuddha.com/teachers/ug-krishnamurti/quotes.json`.
