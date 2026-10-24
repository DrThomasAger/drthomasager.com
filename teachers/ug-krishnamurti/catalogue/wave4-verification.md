# Wave 4 — Exact-phrase verification of U.G. Krishnamurti quotes

Date: 2026-10-24. Method: for each quote, an exact-phrase web search (extended mode) of a distinctive 8–12 word span plus "Krishnamurti", with Jiddu Krishnamurti foundation domains (kfoundation.org, jkrishnamurti.org, kfa.org) excluded. A host counts as independent when it is a different domain from the one already in `quotes.json`. Primary hosts: en.wikisource.org, people.well.com, archive.org, ugkrishnamurti.in. Secondary: goodreads, quotepark, azquotes, quotefancy, quotlr, kwize, libquotes, blogs. Full records (confirming URLs, wording variants, book per source) are in the companion JSON `verification.json`.

Quotes checked: 62 (60 searches; priority given to single-host quotes and those attributed to a book). Selection was made from the 134 entries present in `quotes.json` when this wave started; the file grew to 267 entries during the run, so the newer entries are unchecked.

## Summary by verdict

| Verdict | Count | Meaning |
|---|---|---|
| corroborated-primary | 10 | wording confirmed on a primary full-text host (Wikisource / WELL / ugkrishnamurti.in / archive.org) in addition to the dataset source |
| corroborated-secondary | 34 | at least one further independent secondary host (aggregator, blog, publisher page) confirms the wording; no primary full text found |
| single-source | 14 | no independent second host found; only the dataset's own host (or same-domain pages) |
| disputed | 2 | wording or book attribution conflicts between the dataset and the sources found |
| not-ug | 0 | a source attributes the words to someone other than U.G. (Jiddu Krishnamurti, an editor, Mahesh Bhatt) |
| not-found | 2 | the exact span could not be found on any host |
| **total** | **62** | |

No quote was found attributed to Jiddu Krishnamurti. Two quotes (q7f620b02 "Act, don't think" and q45036753 "A real guru...") reach us only through Mahesh Bhatt's writing (A Taste of Death; the WELL biography); they are recorded as UG's words by Bhatt, so they are kept as corroborated rather than not-ug, with a note.

## Results

| id | first words | verdict | confirming hosts | note |
|---|---|---|---|---|
| q0e92d293 | The native intelligence of the human body is… | corroborated-primary | groups.google.com, people.well.com, sciforums.com, ugkrishnamurti.in | Two primary hosts confirm; dataset marked paraphrase; minor word difference 'that is' vs 'it is'. |
| q6ae4e93f | My teaching, if that is the word you… | corroborated-primary | en.wikiquote.org, en.wikisource.org, penguin.co.in, quotefancy.com, ugkrishnamurti.in | Wikisource full text of Thought is Your Enemy confirms wording as opening disclaimer; Wikiquote notes copyright restrictions nonetheless apply to the editions. |
| q7f620b02 | You think when you don't want to do… | corroborated-primary | azquotes.com, en.wikiquote.org, jhana8.com, nirvana73.blogspot.com, people.well.com, quotefancy.com | WELL (primary host) Mahesh Bhatt journal confirms; words are UG's as recorded by Bhatt. Bhatt's framing sentence is not UG's. |
| q86ac0c5a | The human being is more despicable than all… | corroborated-primary | medium.com, people.well.com, sciforums.com, ugkrishnamurti.in | Dataset text is a paraphrase; primary hosts confirm the underlying sentence. |
| q9bf6e642 | The only way to find your own path… | corroborated-primary | azquotes.com, goodreads.com, people.well.com | Paraphrase; underlying verbatim line is well attested (see qe6277a45). |
| qc45e9d64 | The term natural state is not a synonym… | corroborated-primary | en.wikisource.org, medium.com | Primary text confirms the sense; 'freedom' and 'synonym' are the Medium summariser's wording. Also confirms the sentence 'Enlightenment, if there is any such thing, is not an experience at all' (relevant to q36edddbf). |
| qc97ac3cc | His experience has nothing to do with the… | corroborated-primary | groups.google.com, medium.com, people.well.com, sciforums.com, ugkrishnamurti.in | Two primary hosts (WELL, ugkrishnamurti.in) carry the full text. |
| qcd6ff1c7 | We are not created for any grander purpose… | corroborated-primary | en.wikisource.org, goodreads.com, praveennv.blogspot.com, quotepark.com | Primary Wikisource text confirms, but in No Way Out ch.4, not Mystique; pronoun differs. |
| qe6277a45 | Only if you reject all the other paths… | corroborated-primary | astitvawellbeing.com, azquotes.com, goodreads.com, people.well.com, praveennv.blogspot.com, quotlr.com | WELL (primary host) carries the dialogue context; book attribution split between Mind is a Myth and Chandrasekhar's excerpts. Also covers paraphrase q9bf6e642. |
| qfc6d0e49 | The search ends with the realization that there… | corroborated-primary | azquotes.com, en.wikiquote.org, en.wikisource.org, jhana8.com, kwize.com, people.well.com | Primary Wikisource Part Four confirms; conversations dated 1973-76. |
| q02c3e502 | is like a nuclear explosion… | corroborated-secondary | amazon.com, en.wikisource.org, keplers.com, kwize.com, simonandschuster.com | The exact 'is like a nuclear explosion' phrase is publisher-blurb wording repeated on retailer pages; Wikisource has the explosion metaphor but not this exact clause confirmed. |
| q07528773 | whatever you do to be free from the… | corroborated-secondary | emperyquotes.com, inner-quest.org, jhana8.com | Three independent secondary hosts beyond azquotes; no primary full text. UG attribution consistent. |
| q1985d54c | basically violent, because thought is violent… | corroborated-secondary | inner-quest.org | inner-quest.org is a second independent host to hindu-blog; no book. |
| q1bec15ca | Your traditions are choking you.… | corroborated-secondary | kwize.com, praveennv.blogspot.com, remembering-ug.blogspot.com | Two blog hosts confirm wording and book; no Wikisource hit in results. |
| q1e9233a1 | Courage is not an instrument or quality you… | corroborated-secondary | beyond-the-pale.co.uk, goodreads.com, libquotes.com | Book disputed between Mind is a Myth (Goodreads) and Courage to Stand Alone (beyond-the-pale transcript, dataset). The passage continues 'ending of tradition within you is courage'. |
| q2959c7d4 | There is no such thing as spiritual or… | corroborated-secondary | azquotes.com, catalign.in, en.wikiquote.org, jhana8.com | Wikisource Mystique Part Two surfaced but for a related, not identical, passage; no primary full-text hit for this exact line. 'at all' variant exists. |
| q3173b5b8 | it has to dawn on you that it… | corroborated-secondary | en.wikiquote.org, libquotes.com, nondualite.free.fr, quotepark.com, yquotes.com | Multiple hosts incl. a full transcript page (nondualite.free.fr) agree on book. |
| q3bdfe3cb | I am not anti-rational, just unrational. You may… | corroborated-secondary | azquotes.com, en.wikiquote.org, onlygodis.com, quotefancy.com, quotepark.com, quotlr.com | Wording widely confirmed; book attribution disputed across three titles. Wikiquote places it in No Way Out, not Mind is a Myth. |
| q406d4a93 | Don't follow me, I'm lost.… | corroborated-secondary | azquotes.com, goodreads.com, quotefancy.com, quotepark.com, quotlr.com | Widely repeated on aggregators; no primary full-text confirmation found. |
| q41e40f21 | There is no such thing as truth. The… | corroborated-secondary | en.wikisource.org, praveennv.blogspot.com, quotefancy.com, quotepark.com, quoteslyfe.com, theysaidso.com | Dataset leaves book unassigned; multiple aggregators give Mind is a Myth ch.1. Primary (Wikisource) has only a cognate line in No Way Out. |
| q42bd7292 | Nature is interested in only two things--to survive… | corroborated-secondary | goodreads.com, praveennv.blogspot.com, quotefancy.com, quotepark.com | Wording confirmed by several hosts; book attribution in dataset (Mystique) conflicts with majority (No Way Out). |
| q45036753 | A real guru, if there is one, frees… | corroborated-secondary | academickids.com, en.wikiquote.org, people.well.com, ug-k.blogspot.com, yquotes.com | The WELL (primary host) carries it in Mahesh Bhatt's biography, so the line is mediated by Bhatt's narrative; Wikiquote keeps it unsourced. |
| q64ffef08 | Tell them that there is nothing to understand.… | corroborated-secondary | en.wikipedia.org, quotepark.com | Second host (quotepark) confirms and names a book/chapter; dataset leaves it unassigned. |
| q66516e8f | The plain fact is that if you don't… | corroborated-secondary | azquotes.com, emperyquotes.com, en.wikiquote.org, goodreads.com, praveennv.blogspot.com, quotefancy.com | Book disputed: No Way Out vs A Taste of Death (recorded by Bhatt). Attributed to UG in all. |
| q68aa6bb3 | all gurus are welfare organizations providing petty experiences… | corroborated-secondary | grokipedia.com, praveennv.blogspot.com, sulochanosho.wordpress.com | Two blogs plus Grokipedia; no book citation anywhere. Several JK pages surfaced but none carry the line. |
| q6fe42d31 | Charity is a way for the comfortable to… | corroborated-secondary | azquotes.com, emperyquotes.com, en.wikiquote.org, inspiringquotes.us, jhana8.com | Dataset text is a paraphrase; verbatim form is the 'filthiest invention' passage, widely repeated but with two endings. |
| q7fad3985 | everything you are doing to be at peace… | corroborated-secondary | libquotes.com, nondualite.free.fr, yquotes.com | Confirming transcript places it in Courage to Stand Alone, not Thought is Your Enemy. |
| q95f072f5 | …the constant use of thought to give continuity… | corroborated-secondary | awakin.org, azquotes.com, forum.aypsite.org, inner-quest.org, jhana8.com, libquotes.com | Dataset wording ('constant use') is a variant of the sourced 'constant utilization'; libquotes books it under Mind is a Myth. |
| q9aa9e10b | The things that had astonished me that week… | corroborated-secondary | nuthanapati.blogspot.com | Second host is a blog reproducing the same calamity narrative (Natural State compilation reuses Mystique text). |
| q9fcae79f | All your experiences, all your meditations, all your… | corroborated-secondary | azquotes.com, inner-quest.org, jhana8.com, quotefancy.com, quotlr.com | Several hosts, consistent wording, no book. |
| qa86cd51d | the demand for permanence-permanent relationships, permanent happiness, and… | corroborated-secondary | hindu-blog.com, inner-quest.org, medium.com | Two further hosts; Medium associates it with My Swan Song. |
| qa8d80bc5 | Food, clothing and shelter — these are the… | corroborated-secondary | azquotes.com, jhana8.com, quotefancy.com, quotessayings.net | Book attribution in dataset (Mind is a Myth) not supported; sources cite Stopped in Our Tracks Book Two. |
| qa96fd115 | no qualitative change in man's thinking… | corroborated-secondary | en.wikiquote.org, quotepark.com | Wikiquote (second host) confirms wording and chapter; no Wikisource hit. Covers qcbb3c5aa too. |
| qb87a576d | I don't know what I will do if… | corroborated-secondary | inner-quest.org | inner-quest.org is a second independent host to the Medium source; context: never taken medicine nor seen a doctor. No primary text hit. |
| qc3857d6f | There is no need to change this world… | corroborated-secondary | azquotes.com, emperyquotes.com, en.wikisource.org, jhana8.com, quotefancy.com, quotlr.com | Dataset marks paraphrase; sentiment widely attested, exact sentence not in a primary host. A JK transcript with similar phrasing surfaced but is a different speaker. |
| qc80ccd13 | What is morality? It is not the following… | corroborated-secondary | beyond5.co.in, goodreads.com, quotessayings.net | Two further hosts (beyond5.co.in, quotessayings) beyond Goodreads; no Wikisource hit. |
| qcb9a4286 | All I can guarantee you is that as… | corroborated-secondary | emperyquotes.com, praveennv.blogspot.com, quotefancy.com, quotlr.com | Wording stable across aggregators; no book, talk or primary host. |
| qcbb3c5aa | our ability to destroy our neighbor and his… | corroborated-secondary | en.wikiquote.org, quotepark.com | Same passage as qa96fd115; confirmed by Wikiquote in addition to quotepark. |
| qd1a6079f | There is no death for the body; there… | corroborated-secondary | azquotes.com, emperyquotes.com, jhana8.com, kwize.com, quotlr.com | Book attribution Mind Is a Myth unsupported; kwize places it in Stopped in Our Tracks (a memoir, so wording is Chandrasekhar's recollection). Covers q540a25ff theme too. |
| qde44a012 | …nature had been allowed to go on in… | corroborated-secondary | en.wikiquote.org, kwize.com, quotepark.com, yquotes.com | Book disputed Mystique vs No Way Out. yquotes also lists the line on a Gautama Buddha page (misattribution). |
| qe06bf8ca | The fact is that we don't want to… | corroborated-secondary | goodreads.com, inner-quest.org, quotefancy.com, quotlr.com, thequotearchive.com | Multiple hosts; JK 'fear of the known coming to an end' is a distinct line that surfaced alongside, not a conflict. |
| qf1800473 | a bunch of exploiters, thriving on the gullibility… | corroborated-secondary | books.google.com, en.wikiquote.org, gururating.org, inner-quest.org, quotepark.com | Google Books listing of Mystique carries the phrase; archive.org 'On U.G.' PDF also surfaced. |
| qf42bae73 | nothing more than a protective mechanism, programmed to… | corroborated-secondary | azquotes.com, emperyquotes.com, jhana8.com, quotefancy.com | Aggregators agree on wording; no book or primary text found for this exact phrasing. |
| qfb105fa5 | There is no such thing as experience here.… | corroborated-secondary | azquotes.com, emperyquotes.com | Second host is a minor aggregator; book disputed (No Way Out vs Mystique). |
| q044d9da9 | It is not an illusion, only your experience… | single-source | goodreads.com | Only Goodreads hit. Book attribution conflicts: Goodreads files it under Courage to Stand Alone, not Mind is a Myth. Attributed to UG, not JK. |
| q1c893a18 | Thinking about and struggling against 'sorrow' is sorrow.… | single-source | goodreads.com | Only Goodreads carries this wording; many JK (Jiddu) sorrow transcripts surfaced but none contain this line. Attributed to UG. |
| q241d3a5e | as long as you depend upon somebody for… | single-source | praveennv.blogspot.com | Only praveennv blog; continuation: 'this helplessness is exploited by the people who actually do not have the answers'. |
| q373b0000 | The highest goal is like a horizon that… | single-source | en.wikisource.org, kwize.com | Horizon passage only on kwize; Wikisource supports context ('ultimate goal society has set before us ... has to go') but exact wording unconfirmed. Dataset marks paraphrase. |
| q5e50266d | Sex is for reproduction; people have turned it… | single-source | actualized.org | Only a forum repost found beyond ugkrishnamurti.in; dataset marks it a paraphrase. Context is the story about his own birth/mother. |
| q6f33cc13 | the same old nonsense repeating itself… | single-source | kwize.com | Only kwize; inner-quest Natural State page surfaced but exact phrase not confirmed there. JK memory transcripts are unrelated. |
| q72c0b555 | Questioning the solutions requires a tremendous courage.… | single-source | praveennv.blogspot.com | Only one host (two posts on praveennv); the heading may be the blogger's summary rather than UG's sentence. |
| q87a66997 | your teacher must go, it doesn't matter who… | single-source | hindu-blog.com | Only hindu-blog. |
| q9fd58abe | You cannot look at your thought, because you… | single-source | praveennv.blogspot.com | Only praveennv (two overlapping posts); dataset wording is a compression of the blog text. |
| qab99509d | blind acceptance of authority, all second-hand stuff… | single-source | hindu-blog.com | Only hindu-blog. |
| qbd6fe67c | What you are afraid of is not death.… | single-source | goodreads.com, quotessayings.net | Goodreads plus a quotessayings topic page (which mixes JK and UG death quotes); weak second host. Same passage as q6fe326b5. |
| qd05c2db1 | you arrive seeking understanding, while I am only… | single-source | en.wikisource.org | Exact match on the primary Wikisource page (already the dataset's source); no second host found. |
| qe27976db | You hook up each thought with the next,… | single-source | goodreads.com | Only Goodreads. |
| qfd63f8c6 | Thought has interfered and trying to suppress, control,… | single-source | goodreads.com | Only Goodreads (same host); Goodreads books it under 'Certainty', not Thought is Your Enemy. |
| q36edddbf | Enlightenment (if there is any such thing as… | disputed | en.wikisource.org | Primary (Wikisource) has 'is not an experience at all' but NOT the parenthetical 'if there is any such thing as enlightenment' in that sentence; the dataset wording appears to be a conflation/paraphrase. Only one host. |
| q8891a8e5 | There seems to be no way out.… | disputed | en.wikiquote.org, praveennv.blogspot.com | Wikiquote places the line under No Way Out, not Courage to Stand Alone as the dataset has it. |
| q6518586c | By 1961 my money was finished…… | not-found | en.wikipedia.org, ug-k.blogspot.com | Exact phrase not retrievable by search on any second host; biographical context corroborated. Remains single-source (Wikisource). |
| qf0b3cb2e | The basic method of maintaining the continuity is… | not-found | en.wikisource.org | Exact Goodreads wording not found on any other host; only JK transcripts and a related UG passage in Mystique Pt.4 surfaced. Wording unverified. |

## Book attribution conflicts found

- **q044d9da9** (dataset: Mind is a Myth): Goodreads: The Courage to Stand Alone (dataset says Mind is a Myth)
- **q1e9233a1** (dataset: The Courage to Stand Alone): Goodreads: Mind is a Myth; beyond-the-pale.co.uk: Courage to Stand Alone Pt. III
- **q3bdfe3cb** (dataset: Mind is a Myth): Wikiquote: No Way Out (2002) Ch.1 'The Unrational Philosophy of U.G. Krishnamurti'; aggregators: Mind is a Myth Ch.1; one site: Mystique p.57
- **q42bd7292** (dataset: The Mystique of Enlightenment): No Way Out (2002): azquotes Ch.4 'You Invent Your Reality'; quotepark Ch.7 'What Kind of Human Being Do You Want?' (dataset: Mystique of Enlightenment)
- **q5e50266d** (dataset: My Swan Song): none given (forum repost); dataset: My Swan Song
- **q66516e8f** (dataset: No Way Out): No Way Out (Goodreads et al.); Wikiquote cites it to A Taste of Death (1995) by Mahesh Bhatt
- **q7fad3985** (dataset: Thought is Your Enemy): The Courage to Stand Alone (nondualite.free.fr transcript) (dataset: Thought is Your Enemy)
- **q95f072f5** (dataset: Thought is Your Enemy): Mind is a Myth (libquotes, Sentient 2007 ed.) (dataset: Thought is Your Enemy)
- **q9aa9e10b** (dataset: The Mystique of Enlightenment): nuthanapati blog: The Natural State ch.1.2 (dataset: Mystique of Enlightenment via Wikisource)
- **qa8d80bc5** (dataset: Mind is a Myth): Stopped in Our Tracks, Book Two: Excerpts from U.G.'s Dialogues (K. Chandrasekhar, 2005) per azquotes/quotessayings (dataset: Mind is a Myth)
- **qb87a576d** (dataset: My Swan Song): none given (dataset: My Swan Song; inner-quest talk collection)
- **qcd6ff1c7** (dataset: The Mystique of Enlightenment): No Way Out (2002, ed. Moorty & Naronha) Ch.4 'You Invent Your Reality' (dataset: Mystique of Enlightenment)
- **qd1a6079f** (dataset: Mind is a Myth): kwize: Stopped in Our Tracks: Stories of U.G. in India (K. Chandrasekhar) — recalled beside a dead friend's body; aggregators give none (dataset: Mind Is a Myth)
- **qde44a012** (dataset: The Mystique of Enlightenment): Wikiquote/kwize: The Mystique of Enlightenment (1982); quotepark: No Way Out (2002) Ch.7
- **qe06bf8ca** (dataset: No Way Out): No Way Out (Goodreads)
- **qf42bae73** (dataset: Thought is Your Enemy): none given by aggregators (dataset: Thought is Your Enemy)
- **qfb105fa5** (dataset: The Mystique of Enlightenment): azquotes: No Way Out; another listing: The Mystique of Enlightenment p.121 (Sentient)
- **qfd63f8c6** (dataset: Thought is Your Enemy): Goodreads: Certainty: Life Has No Beginning, No End (dataset: Thought is Your Enemy)

## Wording variants recorded

- **q02c3e502**: Publisher blurb phrasing; transcripts speak of an explosion that 'shatters the body' and alters its chemistry
- **q07528773**: 'self' in quotation marks on inner-quest.org
- **q0e92d293**: '...is amazing, and that is all it needs to survive in any dangerous situation in life' (dataset has 'it is all it needs')
- **q1985d54c**: Full: 'Human nature is basically violent, because thought is violent.'
- **q2959c7d4**: ...no such thing as spirit or psyche at all.
- **q3173b5b8**: Full sentence: 'Whatever pursuit you are indulging in, somewhere along the line it has to dawn on you that it is not leading you anywhere.'
- **q36edddbf**: Wikisource: 'this is not an experience which can be shared with somebody else; this is not an experience at all.'
- **q41e40f21**: single vs double quotation marks around 'logically'/'truth'
- **q41e40f21**: Wikisource No Way Out ch.2: 'you can only say that there is a logically ascertained premise called truth'
- **q42bd7292**: Full: 'Nature is interested in only two things – to survive and to reproduce one like itself. Anything you superimpose on that, all the cultural input, is responsible for the boredom of man.'
- **q5e50266d**: Forum: enlightened man 'cannot reproduce another one like him, so he cannot have sex'; sexual function 'only for reproduction'
- **q6518586c**: Biographical accounts: 'down to his last five pence', 'his last 150 francs', 'I am finished'
- **q66516e8f**: Continuation: '...if you don't have a problem you don't feel alive'
- **q68aa6bb3**: Follow-up line: 'The guru game is a profitable industry; try and make two million dollars a year any other way.'
- **q6fe42d31**: 'Charity is the filthiest invention of the human mind: first you take away what belongs to others by the law and various other means, then you give a little back to keep the have-nots from rebelling against you; it also makes you feel less guilty.'
- **q6fe42d31**: Wikiquote Talk variant ends with 'a policeman and an atom bomb'
- **q72c0b555**: Blog heading adds '!!!'; body text: 'you never question the solutions'
- **q7f620b02**: Often wrongly merged with Bhatt's own sentence 'You are what you do, not what you say you want to do.'
- **q7fad3985**: Full: 'That is an impossible goal for you because everything you are doing to be at peace with yourself is what is destroying the peace that is already there.'
- **q86ac0c5a**: Verbatim: 'The human being is a more despicable thing than all the other forms of life on this planet.'
- **q86ac0c5a**: Medium copy inserts '[modern]' editorially
- **q8891a8e5**: 'But there seems to be no way out.'
- **q95f072f5**: 'Your constant utilization of thought to give continuity to your separate self is you.'
- **q95f072f5**: 'utilisation' / 'you' in quotes in some copies
- **q9bf6e642**: Dataset paraphrase 'The only way to find your own path is to reject the others' not found verbatim anywhere
- **q9fd58abe**: Blog: 'So you cannot actually separate yourself from thought and look at it.'
- **qa86cd51d**: Followed by 'There is nothing to permanence.'
- **qa8d80bc5**: Continuation: 'Beyond that, if you want anything, it is the beginning of self-deception.'
- **qc3857d6f**: Aggregator form: 'there is no need to change the world at all, and no need to change yourself either'
- **qc45e9d64**: Wikisource: 'It is not a synonymous term for enlightenment or God-realization or self-realization.' (dataset/Medium: 'is not a synonym for enlightenment, freedom or God-realization')
- **qc80ccd13**: Full: '...enjoined rules of conduct... Unquestioned action is morality. Questioning your actions is destroying the expression of life.'
- **qc97ac3cc**: Punctuation/capitalisation differs between copies; Medium copy marked 'Updated'
- **qcd6ff1c7**: Wikisource addresses 'you' rather than 'we/us'; quote sites: '...than the ants that are there or the flies that are hovering around us'
- **qd1a6079f**: Longer form: body is 'a fortuitous concourse of atoms'... 'nothing is born and nothing is dead'
- **qde44a012**: Nearby: 'if it had not been for the culture, Nature would have thrown up many more flowers'
- **qe6277a45**: Goodreads/azquotes prefix an asterisk: '*Only if you reject...'
- **qf0b3cb2e**: Mystique Pt.4 (Wikisource): the 'How?' question lets the structure establish itself and get its continuity
- **qf42bae73**: Related primary-style line: 'a protective mechanism. It draws frontiers around itself, and it wants to protect itself.'
- **qfb105fa5**: Continuation: imagination has to end; absence of will, effort and movement 'cannot be experienced at all. It is not an experience.'

## Sources


**academickids.com**
- <https://academickids.com/encyclopedia/index.php/U._G._Krishnamurti>

**actualized.org**
- <https://www.actualized.org/forum/topic/101055-making-sense-of-ug-krishnamurti-part-2/>

**amazon.com**
- <https://www.amazon.com/Mystique-Enlightenment-Radical-Ideas-Krishnamurti/dp/0971078610>

**astitvawellbeing.com**
- <https://astitvawellbeing.com/2020/11/20/discover-your-own-path-u-g-krishnamurti/>

**awakin.org**
- <https://www.awakin.org/v2/read/view.php?tid=118>

**azquotes.com**
- <https://www.azquotes.com/author/17848-U_G_Krishnamurti>
- <https://www.azquotes.com/author/17848-U_G_Krishnamurti?p=2>
- <https://www.azquotes.com/quote/456918>
- <https://www.azquotes.com/quote/504919>
- <https://www.azquotes.com/quote/610426>
- <https://www.azquotes.com/quote/765776>
- <https://www.azquotes.com/quote/818215>
- <https://www.azquotes.com/quote/934218>
- <https://www.azquotes.com/quote/943427>

**beyond-the-pale.co.uk**
- <https://beyond-the-pale.co.uk/ugk3.htm>

**beyond5.co.in**
- <https://www.beyond5.co.in/post/quotes-u-g-krishnamurti>

**books.google.com**
- <https://books.google.com/books/about/The_Mystique_of_Enlightenment.html?id=zt1hEAAAQBAJ>

**catalign.in**
- <https://www.catalign.in/2020/06/why-does-u-g-krishnamurti-ask-is-there.html>

**emperyquotes.com**
- <https://www.emperyquotes.com/authors/ug-krishnamurti>

**en.wikipedia.org**
- <https://en.wikipedia.org/wiki/U._G._Krishnamurti>

**en.wikiquote.org**
- <https://en.wikiquote.org/wiki/Talk:U._G._Krishnamurti>
- <https://en.wikiquote.org/wiki/U._G._Krishnamurti>

**en.wikisource.org**
- <https://en.wikisource.org/wiki/Mind_is_a_Myth/IV>
- <https://en.wikisource.org/wiki/No_Way_Out/Chapter_2>
- <https://en.wikisource.org/wiki/No_Way_Out/Chapter_4>
- <https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Four>
- <https://en.wikisource.org/wiki/The_Natural_State>
- <https://en.wikisource.org/wiki/Thought_is_Your_Enemy>

**forum.aypsite.org**
- <https://forum.aypsite.org/t/u-g-krishnamurti-quotes/7543>

**goodreads.com**
- <https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti>
- <https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=2>
- <https://www.goodreads.com/quotes/591002-we-are-not-created-for-any-grander-purpose-than-the>
- <https://www.goodreads.com/quotes/729309-only-if-you-reject-all-the-other-paths-can-you>
- <https://www.goodreads.com/quotes/8510738-nature-is-interested-in-only-two-things-to-survive-and-to>
- <https://www.goodreads.com/quotes/8510744-the-body-cannot-be-afraid-of-death-the-movement-that>
- <https://www.goodreads.com/quotes/984886-what-is-morality-it-is-not-the-following-of-enjoined>
- <https://www.goodreads.com/work/quotes/46398939-u-g-krishnamurti-certainty-life-has-no-beginning-no-end>
- <https://www.goodreads.com/work/quotes/52201-the-mystique-of-enlightenment-the-radical-ideas-of-u-g-krishnamurti>
- <https://www.goodreads.com/work/quotes/52202-mind-is-a-myth>
- <https://www.goodreads.com/work/quotes/6212984-no-way-out-dialogues-with-krishnamurti>

**grokipedia.com**
- <https://grokipedia.com/page/U._G._Krishnamurti>

**groups.google.com**
- <https://groups.google.com/g/noshonuts/c/fGiwo09RzyI>

**gururating.org**
- <https://gururating.org/u-g-krishnamurti/>

**hindu-blog.com**
- <https://www.hindu-blog.com/2018/09/u-g-krishnamurti-quotes-and-teachings.html>

**inner-quest.org**
- <https://www.inner-quest.org/UG_Words.htm>

**inspiringquotes.us**
- <https://www.inspiringquotes.us/author/3700-u-g-krishnamurti>

**jhana8.com**
- <https://jhana8.com/ug-krishnamurti-quotes/>

**keplers.com**
- <https://www.keplers.com/book/9780971078611>

**kwize.com**
- <https://kwize.com/en/authors/U-G-Krishnamurti/>
- <https://kwize.com/en/texts/U-G-Krishnamurti-Stopped-in-Our-Tracks-Stories-of-U-G-in-India/>
- <https://kwize.com/en/texts/U-G-Krishnamurti-The-Mystique-of-Enlightenment/>
- <https://kwize.com/en/texts/U-G-Krishnamurti-The-Natural-State/>

**libquotes.com**
- <https://libquotes.com/u-g-krishnamurti>
- <https://libquotes.com/u-g-krishnamurti/quote/lbz3k3b>
- <https://libquotes.com/u-g-krishnamurti/quotes/courage>
- <https://libquotes.com/u-g-krishnamurti/quotes/peace>

**medium.com**
- <https://medium.com/@alysion42/u-g-krishnamurtis-swan-song-updated-e36a07cc0595>
- <https://medium.com/@harpeony/book-summary-the-natural-state-in-the-words-of-u-g-krishnamurti-part-1-3-04f7c43a78c4>

**nirvana73.blogspot.com**
- <http://nirvana73.blogspot.com/2013/03/from-ug-krishnamurti-life-by-mahesh.html>

**nondualite.free.fr**
- <http://nondualite.free.fr/c_ug_courage.htm>

**nuthanapati.blogspot.com**
- <http://nuthanapati.blogspot.com/2011/11/natural-state-miracles-experienced-by.html>

**onlygodis.com**
- <https://onlygodis.com/teachings/ug_krishnamurti.html>

**penguin.co.in**
- <https://www.penguin.co.in/book/the-penguin-u-g-krishnamurti-reader/>

**people.well.com**
- <https://people.well.com/user/jct/SWAN_SONG.htm>
- <https://people.well.com/user/jct/chandra.htm>
- <https://people.well.com/user/jct/mahesh.html>
- <https://people.well.com/user/jct/mystiq1.htm>
- <https://people.well.com/user/jct/ugbio/ugbio2.htm>

**praveennv.blogspot.com**
- <http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html>
- <http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html?m=1>
- <http://praveennv.blogspot.com/2008/03/ug-krishnamurti-on-thoughts.html>
- <http://praveennv.blogspot.com/2016/03/do-you-have-any-question-which-you-can.html>
- <http://praveennv.blogspot.com/2016/03/questioning-solutions-requires.html>
- <http://praveennv.blogspot.com/2016/03/ug-krishnamurtis-quote-on-true-guru.html>
- <http://praveennv.blogspot.com/2016/03/you-have-no-answer-of-your-own.html>
- <http://praveennv.blogspot.com/2016/04/spirituality-is-invention-of-mind-and.html>

**quotefancy.com**
- <https://quotefancy.com/quote/923747/U-G-Krishnamurti-Everything-you-stand-for-believe-in-experience-and-aspire-to-is-the>
- <https://quotefancy.com/quote/923749/U-G-Krishnamurti-Nature-is-interested-in-only-two-things-to-survive-and-to-reproduce-one>
- <https://quotefancy.com/quote/923750/U-G-Krishnamurti-Don-t-follow-me-I-m-lost>
- <https://quotefancy.com/quote/923753/U-G-Krishnamurti-You-think-when-you-don-t-want-to-do-anything-Thinking-is-a-poor>
- <https://quotefancy.com/quote/923756/U-G-Krishnamurti-All-I-can-guarantee-you-is-that-as-long-as-you-are-searching-for>
- <https://quotefancy.com/quote/923757/U-G-Krishnamurti-Food-clothing-and-shelter-these-are-the-basic-needs-Beyond-that-if-you>
- <https://quotefancy.com/quote/923758/U-G-Krishnamurti-I-am-not-anti-rational-just-unrational-You-may-infer-a-rational-meaning>
- <https://quotefancy.com/quote/923763/U-G-Krishnamurti-My-teaching-if-that-is-the-word-you-want-to-use-has-no-copyright-You-are>
- <https://quotefancy.com/quote/923781/U-G-Krishnamurti-There-is-no-such-thing-as-truth-The-only-thing-that-is-actually-there-is>
- <https://quotefancy.com/u-g-krishnamurti-quotes>

**quotepark.com**
- <https://quotepark.com/authors/ug-krishnamurti/>
- <https://quotepark.com/authors/ug-krishnamurti/man/>
- <https://quotepark.com/quotes/1271340-ug-krishnamurti-dont-follow-me-im-lost/>
- <https://quotepark.com/quotes/1787020-ug-krishnamurti-there-is-no-such-thing-as-truth-the-only-thing-th/>
- <https://quotepark.com/quotes/1928276-ug-krishnamurti-our-mind-and-there-are-no-individual-minds-only/>
- <https://quotepark.com/quotes/949961-ug-krishnamurti-we-are-not-created-for-any-grander-purpose-than-th/>

**quoteslyfe.com**
- <https://www.quoteslyfe.com/quote/There-is-no-such-thing-as-truth-1127802>

**quotessayings.net**
- <https://quotessayings.net/quotes/food-clothing-and-shelter-these-are-the-basic-needs-1684795.html>
- <https://quotessayings.net/topics/krishnamurti-death/>
- <https://quotessayings.net/topics/not-following-rules/>

**quotlr.com**
- <https://quotlr.com/author/ug-krishnamurti>

**remembering-ug.blogspot.com**
- <http://remembering-ug.blogspot.com/2012/07/passages-270812.html>

**sciforums.com**
- <https://www.sciforums.com/threads/the-last-message-of-u-g-krishnamurti.95095/>

**simonandschuster.com**
- <https://www.simonandschuster.com/books/The-Mystique-of-Enlightenment/U-G-Krishnamurti/9780971078611>

**sulochanosho.wordpress.com**
- <https://sulochanosho.wordpress.com/tag/ug-quotes/>

**thequotearchive.com**
- <https://thequotearchive.com/quotes/U.G.%20Krishnamurti>

**theysaidso.com**
- <https://theysaidso.com/quote/u-g-krishnamurti-there-is-no-such-thing-as-truth-the-only-thing-that-is-actually>

**ug-k.blogspot.com**
- <http://ug-k.blogspot.com/2007/04/adrift-in-london-experiences-of-others.html>
- <http://ug-k.blogspot.com/2007/04/early-years-real-guru-if-there-is-one.html>

**ugkrishnamurti.in**
- <https://www.ugkrishnamurti.in/>
- <https://www.ugkrishnamurti.in/ug-essence/my-swan-song>

**yquotes.com**
- <https://yquotes.com/quotes/u-g-krishnamurti/>
- <https://yquotes.com/u-g-krishnamurti/83670/>
