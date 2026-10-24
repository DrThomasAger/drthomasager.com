# Wave 8 — Verification pass 4, half A (even-id paraphrases and fragments)

Scope: every quote in `quotes.json` whose verdict was `primary-source`, `multi-source` or `single-source` (i.e. not yet checked by a verification pass) and whose id ends in an even hex digit (0,2,4,6,8,a,c,e). 71 quotes qualified; 66 were searched (47 extended web searches, several quotes per search). Jiddu Krishnamurti hosts (kfoundation.org, jkrishnamurti.org, kfa.org, krishnamurti.org) were excluded wherever they surfaced. WebFetch was unavailable, so every finding rests on search-result snippets and summaries, not on page reads; a snippet that quotes a sentence is treated as that host carrying it.

Not searched (budget): qbd194c2e, q1a17d2c4, qf9704722, q1c8788f6, q8305f222 — all already on primary hosts (Wikisource / people.well.com / Wikiquote); their prior verdict stands.

## Per-verdict summary

| Verdict | Count |
|---|---|
| corroborated-primary | 22 |
| corroborated-secondary | 25 |
| single-source | 15 |
| disputed | 1 |
| not-ug | 1 |
| not-found | 2 |
| **total searched** | **66** |

Verbatim recovery: 32 quotes now carry the fuller or exact sentence they paraphrase or truncate (listed below); a further 9 carry an adjacent or related line only.

## Table

| id | prior verdict | kind | text checked | new verdict | book per sources | hosts confirming | note |
|---|---|---|---|---|---|---|---|
| q5af2e554 | corroborated-secondary | paraphrase | one can do nothing to attain the natural state. In fact, any movement towards it separates one from it. | **corroborated-secondary** | The Mystique of Enlightenment (publisher blurb / introduction) | amazon.com, archive.org, keplers.com, simonandschuster.com | Publisher-blurb/introduction wording (editorial voice describing UG's position), not a verbatim UG utterance; confirmed on Simon & Schuster, Kepler's and Amazon listings; archive.org hosts the book but search did not confirm the sentence there. |
| qc40e7904 | corroborated-secondary | paraphrase | [damn fool passage, paraphrase only] | **corroborated-secondary** | Mind is a Myth, Introduction ('A Note at the Beginning') by Terry Newland | azquotes.com, en.wikiquote.org, people.well.com, quotepark.com | Wikiquote/AZQuotes attribute the line to Terry Newland's Introduction ('Quoted in Introduction by Terry Newland'); quotepark places nearby 'search is at an end' lines in Ch. 4. Editor-mediated quotation: UG's words as reported by the editor. people.well.com hosts the Introduction but the sentence itself was not confirmed there by search. |
| qd124d20c | corroborated-secondary | paraphrase | Tradition is a burden people cling to; it has to fall away on its own. | **corroborated-secondary** | Mind is a Myth | en.wikisource.org, goodreads.com, kwize.com | Paraphrase; verbatim wording uses 'drop away' not 'fall away' and the 'cultural garbage-sack' image. Wikisource Mind is a Myth hosts the passage per search summary (exact chapter not confirmed). |
| q48147bda | single-source | paraphrase | Nobody knows anything about life. | **single-source** | Mind is a Myth (goodreads attribution) | goodreads.com | Exact phrase not found by search outside goodreads; only thematically related passages located. Remains single-source. |
| qdb7053b4 | corroborated-secondary | paraphrase | Society is the human jungle; it would be much easier to survive in nature's jungle. | **corroborated-secondary** | No Way Out (Ch. 1 per people.well.com hit); Wikipedia summary | en.wikipedia.org, people.well.com | Wikipedia paraphrases: 'He refers to society as the "human jungle" and observes that it would be much easier to survive in nature's jungle.' Primary host people.well.com No Way Out Ch.1 surfaced but sentence not confirmed verbatim there. |
| qfd63f8c6 | single-source | verbatim | Thought has interfered and trying to suppress, control, and moralize about desire, to the detriment of mankind. | **corroborated-primary** | Mind is a Myth, Ch. I (Wikisource); goodreads files it under Certainty: Life has no beginning, no end | en.wikisource.org, goodreads.com, the-natural-state.blogspot.com | Book conflict: Wikisource/Mind is a Myth vs goodreads/Certainty (a later compilation). Wikisource reads 'tried to suppress' rather than 'trying to suppress'. |
| q43697aec | corroborated-secondary | paraphrase | There is no such thing as your mind or my mind; a separate individual mind is an illusion; thought is a protective mechanism. | **corroborated-secondary** | Thought is Your Enemy | goodreads.com, holybooks.com | Composite paraphrase of three adjacent claims; the components are quoted on goodreads; holybooks PDF hosts the book. No primary host (wikisource/people.well.com) confirmation found. |
| qbd6fe67c | single-source | verbatim | What you are afraid of is not death. | **corroborated-secondary** | No Way Out | goodreads.com, quotessayings.net | Multiple aggregators agree on wording and book; quotessayings.net is a mixed J./U.G. Krishnamurti topic page (misattribution risk on that host). No primary host confirmed. |
| q08218f4e | corroborated-secondary | fragment | The body cannot be afraid of death. | **corroborated-secondary** | No Way Out | goodreads.com | Full sentence recovered from goodreads quote 8510744 (surfaced during the 'What you are afraid of is not death' search). Still goodreads-only; no second independent host. |
| q92ffcf50 | corroborated-secondary | paraphrase | The fixed "I" as a reference point; the courage needed to drop one's conditioning; rejecting what others offer is the real task. | **corroborated-secondary** | Thought is Your Enemy (passages 6-7, 6-11, 6-12 per remembering-ug) | dalemusings.wordpress.com, holybooks.com, remembering-ug.blogspot.com | Summary paraphrase of several passages; components located on remembering-ug (blog excerpting the book) and holybooks PDF of the book. |
| q9fd58abe | single-source | paraphrase | You cannot look at your thought, because you cannot separate yourself from thought. | **corroborated-secondary** | The Courage to Stand Alone (Amsterdam 'Give Up' tapes, 1982) | en.wikisource.org, nondualite.free.fr, o-meditation.com, praveennv.blogspot.com | Paraphrase; blog wording 'you cannot actually separate yourself from thought and look at it'; a related Amsterdam-dialogue line about watching thoughts found. Wikisource and o-meditation PDF host the book but verbatim match not confirmed there. |
| q1c893a18 | single-source | verbatim | Thinking about and struggling against 'sorrow' is sorrow. Since you can't stop thinking, and thinking is sorrow, you will always suffer. | **corroborated-secondary** | Mind is a Myth | goodreads.com, people.well.com, quotefancy.com, remembering-ug.blogspot.com | Second independent host (quotefancy) gives the longer passage. people.well.com Chandrasekhar excerpts have a related line ('Sadness is not the problem, but thinking about sadness is the problem'), not this sentence. Search also surfaced kfoundation.org (Jiddu) sorrow pages: excluded, different speaker. |
| q373b0000 | single-source | paraphrase | The highest goal is like a horizon that recedes as you approach it, a projection of your own fear. | **corroborated-primary** | Mind is a Myth, Ch. I (Wikisource Q&A); kwize files it under The Natural State | en.wikiquote.org, en.wikisource.org, kwize.com, o-meditation.com | Book conflict: catalogue says The Natural State (after kwize); Wikisource and the Mind is a Myth PDF carry it as Mind is a Myth Ch. I. Verbatim recovered. |
| q241d3a5e | single-source | fragment | as long as you depend upon somebody for solving your problems, so long you remain helpless | **corroborated-secondary** | unassigned (praveennv 'True Guru' post); brooklynaikikai quotes a related line from Louis Brawley's Goner | brooklynaikikai.com, praveennv.blogspot.com | Full sentence recovered from praveennv. Second host (brooklynaikikai) carries only a related line ('as long as you think you are totally helpless, you will depend on some outside agency') attributed to Brawley's Goner, so corroboration is thematic. Search also returned kfoundation/jkrishnamurti.org dependence pages (Jiddu): excluded. |
| q2dd1ea30 | corroborated-secondary | paraphrase | We never look at anything. | **corroborated-secondary** | No Way Out, Ch. 4 You Invent Your Reality (catalogue); hosts give no book | inner-quest.org, praveennv.blogspot.com | Second independent host (inner-quest.org) carries the same passage. Neither host names the book; Wikisource No Way Out Ch. 4 not confirmed by search. |
| q338b17ba | corroborated-primary | paraphrase | If the body lacks the means to survive it goes gracefully. | **corroborated-primary** | My Swan Song (dictated to Louis Brawley, Feb 2007) | hindu-blog.com, medium.com, people.well.com, ugkrishnamurti.in | Passage confirmed on two primary hosts (people.well.com, ugkrishnamurti.in) and two secondary; search summaries paraphrase ('the body knows what it needs to do to survive; if it lacks the means, it lets go') so the exact verbatim sentence was not recovered. |
| qff9ae05a | corroborated-primary | paraphrase | The body knows what it needs to survive; if it lacks the means it goes gracefully. | **corroborated-primary** | My Swan Song (catalogue had it unassigned) | hindu-blog.com, inner-quest.org, people.well.com, ugkrishnamurti.in | Same Swan Song passage as q338b17ba; duplicate pair. Book should be assigned to My Swan Song. |
| qf71956be | corroborated-primary | fragment | "An ashram-like atmosphere can't grow around me," roared U.G. … "Neither my tapes nor books nor letters must be in anyone's control." | **corroborated-primary** | Stopped in Our Tracks: Stories of U.G. in India (K. Chandrasekhar's journal, Book One) | en.wikisource.org, kwize.com, people.well.com | Reported speech in Chandrasekhar's narrative, not a UG-authored text. Wikisource and people.well.com (primary hosts) plus kwize confirm the scene; the ellipsis spans intervening narrative, full sentence not recovered. |
| qcc769ade | corroborated-primary | fragment | By giving money they control you, and by not giving money they control you. | **corroborated-primary** | A Taste of Death (catalogue); inner-quest gives no book; people.well.com Mahesh Bhatt journal (Gstaad diary) | inner-quest.org, people.well.com | Second host is Mahesh Bhatt's diary on people.well.com (primary host, Bhatt reportage). Fragment extended with following sentence. |
| qf7b06ab4 | corroborated-primary | paraphrase | I have wasted seven years listening to you. | **corroborated-primary** | U.G. Krishnamurti: A Life (Mahesh Bhatt), ch. 'Locking of Horns' | en.wikipedia.org, people.well.com, ug-k.blogspot.com | Bhatt biography (Bhatt attribution). Wording varies slightly across hosts; Wikipedia summarises the 1947-1953 listening period. |
| q69a4a09e | corroborated-primary | paraphrase | I wasted seven years listening to him. | **corroborated-primary** | U.G. Krishnamurti: A Life (Mahesh Bhatt), 'Locking of Horns' (catalogue had it unassigned) | people.well.com, ug-k.blogspot.com | Third-person recast of the same Bhatt-reported remark as qf7b06ab4; duplicate pair. Book should be assigned to Bhatt's biography. |
| qca29deea | corroborated-primary | fragment | Can you give me what you have? | **corroborated-primary** | The Mystique of Enlightenment, Part One | en.wikisource.org, holybooks.com, people.well.com | UG's account of asking a teacher (not named in the summary) for what he had; the reply 'I can give it, but can you take it?' is the famous counterpart. Confirmed on two primary hosts. |
| qf83cd77e | corroborated-secondary | paraphrase | Yoga, meditation and prayer are violent techniques. The living body is very peaceful; you don't have to do a thing. | **corroborated-secondary** | unassigned; Whitwell attributes the related 'any doing in any direction is violence' to The Natural State | heartofyoga.com, markwhitwell.medium.com, ugarchive.blogspot.com | All hosts trace to Mark Whitwell (heartofyoga/medium) or reprints of him; ugarchive.blogspot reprints the same post. Verbatim says 'living organism', not 'living body'. No primary-host confirmation. |
| qd39fb8fe | corroborated-primary | fragment | You have to liberate yourself. | **corroborated-primary** | Thought is Your Enemy | en.wikisource.org, goodreads.com, holybooks.com, people.well.com | Full sentence recovered; passage ends with the '--U.G.' attribution on Wikisource (prefatory passage of the book). |
| q3efc45a4 | corroborated-primary | paraphrase | Our basic human problems are neurological, not psychological. Thought has created the problem of desire. | **corroborated-primary** | goodreads: Certainty: Life has no beginning, no end; Wikisource: Mind is a Myth, Ch. I | en.wikisource.org, goodreads.com | Same passage as qfd63f8c6 (desire/neurological). Book conflict: Certainty (goodreads) vs Mind is a Myth (Wikisource). Search also surfaced kfoundation.org/krishnamurti.org pages on desire (Jiddu): excluded. |
| q93a61f20 | single-source | verbatim | I have nothing to say and what I am saying is not born out of my thinking. | **single-source** | U.G. Krishnamurti: A Life (Mahesh Bhatt), 'Conversations following conversations' | ug-k.blogspot.com | Only the ug-k.blogspot serialisation of Bhatt's biography carries it; no second host found. Bhatt attribution (biography based on recorded conversations). |
| q4fc99cde | corroborated-secondary | paraphrase | The peace you seek is already there; the effort to be at peace is what destroys it. | **corroborated-secondary** | The Courage to Stand Alone (Wikiquote, 2001 ed.); catalogue had it unassigned | en.wikiquote.org, en.wikisource.org, goodreads.com, libquotes.com | Wikiquote attributes the passage to The Courage to Stand Alone; a parallel 'search for peace is inner war / disturbing the peace already in the body' dialogue exists in Mind is a Myth Ch. V on Wikisource. Exact verbatim sentence not recovered from summaries. |
| qac537b40 | corroborated-secondary | paraphrase | Human nature is basically violent because thought itself is violent. | **corroborated-secondary** | unassigned; kwize files the thought-is-destructive line under Science and U.G. | hindu-blog.com, inner-quest.org, kwize.com | Thematic corroboration only (kwize/inner-quest give 'whatever is born out of thinking is destructive', not this sentence). Search returned many Jiddu Krishnamurti violence pages (kfoundation.org, jkrishnamurti.org): excluded, misattribution risk high for this generic theme. |
| qcfa88a48 | corroborated-primary | paraphrase | I have never taken any medicine or seen a doctor, except once for typhoid. I would never tell others not to see a doctor, though I say doctors should be shot. | **corroborated-primary** | My Swan Song (Feb 2007, dictated to Louis Brawley) | medium.com, people.well.com, remembering-ug.blogspot.com, ugkrishnamurti.in | Two primary hosts confirm the passage (typhoid in Madras, wife's brother a doctor at General Hospital). Paraphrase compresses several sentences; verbatim not recovered. |
| q27ae73f0 | single-source | paraphrase | You need not worry about nutrition or health foods; the body turns whatever you put into it into energy. | **single-source** | travelswithug 'UG Cookbook' (editorial summary); catalogue says No Way Out Ch. 4 | scribd.com, slideshare.net, travelswithug.com | Only the UG Cookbook (and its slideshare/scribd mirrors) carries this, in the editor's voice ('U.G. does not think we need to concern ourselves with nutrition, vitamins, and health foods'). Wikisource No Way Out Ch. 4/9 surfaced but did not confirm the wording. Not UG verbatim. |
| q9c3dac12 | corroborated-primary | fragment | is not yours; it is something which you and your ancestors have accumulated over a long time | **corroborated-primary** | Mind is a Myth, Ch. III Not Knowing Is Your Natural State | en.wikisource.org, holybooks.com, o-meditation.com | Full sentence recovered from Wikisource Ch. III; PDF copies of the book provide second hosts. |
| qbee19952 | corroborated-primary | fragment | the only test for me is money | **corroborated-primary** | My Swan Song (catalogue); inner-quest passage on money; Bhatt diary on people.well.com | inner-quest.org, people.well.com | Surfaced during the 'By giving money they control you' search: inner-quest ties the control-by-money passage to UG's view that money is the 'only test' of how free someone is; Bhatt's Gstaad diary carries the same passage. Exact fragment wording not independently confirmed. |
| qeb9c85d2 | not-ug | fragment | …a tremendous upheaval… | **not-ug** | The Mystique of Enlightenment, Part One (parenthetical editorial biographical note) | en.wikisource.org, holybooks.com, people.well.com | Full sentence recovered. It is the editor's bracketed biographical note in Part One, written in the third person, not UG's own words. Hosted on primary hosts but should be flagged as editorial voice. |
| q718e3b22 | disputed | paraphrase | A passage that ends with the speaker saying there is no escape. | **disputed** | Aggregators tie the 'no way out, no escape' ending to the sorrow passage of Mind is a Myth, not to No Way Out Ch. 7 | emperyquotes.com, goodreads.com | The only 'no escape' ending found belongs to the Mind is a Myth sorrow passage (= q1c893a18 extended); nothing located for a No Way Out Ch. 7 passage ending this way. Placeholder text; book/chapter attribution disputed. |
| qb4eaccd2 | corroborated-secondary | verbatim | The basic question which we have to ask for ourselves is: what kind of a human being do you want? But unfortunately we have placed before ourselves the model of a perfect being. | **corroborated-secondary** | No Way Out, Ch. 7 What Kind of Human Being Do You Want? | en.wikisource.org, scribd.com, ug-k.blogspot.com | The 'model of a perfect being' half is attested (scribd copy of No Way Out; Bhatt's biography serialised on ug-k.blogspot carries a parallel 'nature does not use anything as a model' interview); the exact question wording was not found by search. Wikisource chapter is the catalogue's original host. |
| q828c848c | single-source | fragment | India will *not* be that country. | **single-source** | The Mystique of Enlightenment, Part Three | en.wikisource.org | Exact wording not surfaced by search; nearest related material is the Part Three answer on India's role in the world crisis (change will come from the West) and a Part Four remark that gurus leaving India changing the world is a fantasy. Remains on Wikisource only. |
| qea9473ac | corroborated-primary | fragment | each individual has now the responsibility; not any particular nation — India or America or Russia | **corroborated-primary** | The Mystique of Enlightenment, Part Three (answer on India's role in the world crisis) | en.wikisource.org, kwize.com, people.well.com | Passage confirmed on Wikisource Part Three (closes an answer about India, naming India, America and Russia); people.well.com hosts the full text. Verbatim sentence not reproduced in search summary. |
| qea825286 | corroborated-primary | fragment | what you call sexual activity, which is biological in its nature, has been turned into a pleasure movement | **corroborated-primary** | No Way Out, Ch. 8 (Wikisource); catalogue had it unassigned | en.wikisource.org, goodreads.com | Wikisource No Way Out Ch. 8 carries the 'pleasure movement' line alongside goodreads; book should be assigned to No Way Out. Search also returned Jiddu pages on pleasure (krishnamurti.org, kfoundation.org): excluded. |
| qcc9c525e | single-source | fragment | the body does not know that it is healthy or unhealthy | **single-source** | No Way Out, Ch. 9 Leave the Body Alone (Conversation with a Physician) | en.wikisource.org | Catalogue host was azquotes; this pass found the Wikisource Ch. 9 opening ('asks whether the body can know if it is healthy') as a primary-host pointer, but the exact fragment wording was not confirmed verbatim. Upgraded host quality, still effectively one confirmed host. |
| q441961c4 | single-source | fragment | nothing of what we consider to be good for the body is actually good for this body | **single-source** | unassigned | inner-quest.org | Exact phrase not found outside inner-quest; related body-knows-best material in Swan Song (people.well.com/medium) and the UG Cookbook only. |
| q1a68f39e | corroborated-primary | fragment | in that sense the body is immortal | **corroborated-primary** | Mind is a Myth, Ch. I (catalogue); people.well.com remembrance and inner-quest biography page quote the same passage | goodreads.com, inner-quest.org, people.well.com | Full sentence recovered with preceding context; two independent hosts incl. primary host people.well.com. |
| qa2698ac8 | corroborated-secondary | verbatim | It is a business; it has become a holy business to people. | **corroborated-secondary** | The Natural State (catalogue); quotlr gives no book | praveennv.blogspot.com, quotlr.com | 'Holy business' phrase attested on quotlr in a different sentence (the 'mystification' passage); the exact catalogue sentence not found. Thematic second host only. |
| q679cf6ae | corroborated-secondary | paraphrase | Man created God out of fear; so the problem is fear, not God. | **corroborated-secondary** | The Mystique of Enlightenment, Part One (catalogue); aggregators give no book | quotepark.com, quotlr.com | Verbatim sequence recovered from quotlr (adjacent to 'no power outside of man'). Aggregator-only; no primary host confirmed by search. Search also surfaced a Jiddu 'On Fear' listing (ebay): excluded. |
| qa1859f82 | corroborated-secondary | fragment | there is no power outside of man | **corroborated-secondary** | The Mystique of Enlightenment, Part One (catalogue); goodreads files fear material under No Way Out | goodreads.com, quotlr.com | Same passage as q679cf6ae; goodreads No Way Out quotes page surfaced for the fear theme but exact sentence confirmed only on quotlr. |
| q670510be | single-source | fragment | man has created religion because it gives him a cover | **single-source** | No Way Out (goodreads) | goodreads.com | Exact phrase not found in search beyond goodreads. |
| q95e9c782 | corroborated-primary | paraphrase | I am neither a jivanmukta nor an evolved being. | **corroborated-primary** | Stopped in Our Tracks, Book One (Chandrasekhar; chapters 'You Will Never Know a Jivanmukta' / 'There Is No Moksha, No Jivanmukti and No Atman') | en.wikisource.org, kwize.com, u-g-krishnamurti.blogspot.com | Verbatim recovered ('not a jivanmukta; nor am I an evolved being'). Reported speech in Chandrasekhar's notebooks (ed. Narayana Moorty). |
| q16ecbc00 | corroborated-primary | paraphrase | What I am saying is outside the field of teachability; it is simply a description of the way I am functioning. | **corroborated-primary** | The Mystique of Enlightenment, Part Two | awakeningtoreality.com, en.wikisource.org, inner-quest.org, people.well.com | Phrase 'outside the field of teachability' attested on several hosts incl. people.well.com; exact full verbatim sentence not reproduced in search summary. |
| q0d1d00a2 | single-source | paraphrase | the idea of selflessness is a protective invention against one's actual selfishness | **single-source** | Mind is a Myth, Ch. IV There Is Nothing to Understand | en.wikisource.org | Search found only the thematically related 'all spiritual effort is self-centred and strengthens the self'; the selflessness/selfishness sentence not surfaced on any second host. |
| q03c8d952 | corroborated-secondary | verbatim | There is nothing to understand — that is the understanding I am talking about. | **corroborated-secondary** | The Mystique of Enlightenment, Part Four | en.wikipedia.org, en.wikisource.org | Wikipedia carries the related famous line 'Tell them that there is nothing to understand' (Mind is a Myth title theme); the exact Part Four sentence not found on a second host. |
| qaa3bf764 | corroborated-primary | paraphrase | The natural state is not a thoughtless state; that is a hoax that has been carried on for thousands of years. You will never be without thought. | **corroborated-primary** | The Natural State | dailygood.org, en.wikisource.org, inner-quest.org, medium.com | Idea confirmed on inner-quest Natural State page and secondary summaries; verbatim wording per summary speaks of 'one of the many hoaxes Hindus have fallen for' rather than 'carried on for thousands of years'. Paraphrase. |
| q85d5f7a2 | corroborated-secondary | paraphrase | It is a physiological state, with no religious or mystical content. | **corroborated-secondary** | The Natural State | goodreads.com, inner-quest.org, jhana8.com | Composite paraphrase; components attested ('pure and simple physical and physiological state of being'; 'devoid of religious or mystical significance' is the jhana8 biography's wording, i.e. editorial). |
| q7969abd0 | corroborated-secondary | fragment | modern day doctors are the modern day witches, and modern day medical technology the modern day witchcraft | **corroborated-secondary** | unassigned; inner-quest talk transcript | actualized.org, inner-quest.org | Second host is inner-quest.org (transcript); catalogue host actualized.org is a forum quoting it. No book attribution found. |
| q55779bfa | single-source | paraphrase | eat what you like because the perfect intelligence of life knows exactly what to do with food | **single-source** | unassigned; Mark Whitwell interview recollection | markwhitwell.medium.com | Whitwell's recollection in his own voice ('He would say...'), not a UG transcript; the UG Cookbook (travelswithug) gives only the related 'I'm not recommending this diet to you'. |
| q07b7ff4c | not-found | paraphrase | Why do you call it green? | **not-found** | Stopped in Our Tracks (catalogue, people.well.com) | — | Phrase not surfaced by search on Wikisource, kwize or the u-g-krishnamurti.blogspot serialisation of Stopped in Our Tracks. Existing people.well.com attribution stands unverified by this pass. |
| q95504a40 | not-found | paraphrase | I am myself a thief. | **not-found** | Stopped in Our Tracks (catalogue, people.well.com) | — | Phrase not surfaced by search on any Stopped in Our Tracks host. Existing people.well.com attribution stands unverified by this pass. |
| q76f1764e | corroborated-secondary | verbatim | How I got into this state I will never be able to tell. | **corroborated-secondary** | The Biology of Enlightenment: Unpublished Conversations 1967-71 (ed. Mukunda Rao, HarperCollins India) | everand.com, realitysandwich.com | Second host is the Everand ebook edition; realitysandwich is Mukunda Rao's excerpt (editor-mediated). Next sentence recovered. |
| q8d5ee424 | single-source | fragment | It is not a change in the structure of your thinking, but a change in the structure of the whole of your physical being. | **single-source** | The Biology of Enlightenment (Mukunda Rao excerpt) | realitysandwich.com | Exact sentence not found on a second host; Everand book description paraphrases ('whatever transformation he has undergone is within the structure of the human body and not in the mind at all'). |
| q77b540c6 | single-source | verbatim | This can also lead to self-destruction for the sake of even a silly idea, as witnessed in wars. | **single-source** | Science and U.G. (ed. from UG's talks by a scientist, hosted as 'reddi.htm' on people.well.com) | en.wikisource.org, kwize.com, people.well.com | Science and U.G. is hosted on Wikisource and people.well.com (primary hosts), but the exact 'silly idea' sentence was not confirmed there by search; only kwize carries it. Treat as single-source pending full-text check. |
| qbb683516 | corroborated-primary | verbatim | The body changes from one state into another as recycling of matter. | **corroborated-primary** | Science and U.G. | en.wikisource.org, kwize.com, people.well.com | 'Recycling of matter' passage confirmed on both Wikisource and people.well.com copies; adjacent sentence recovered. |
| q39067cd0 | single-source | verbatim | Love, compassion, ahimsa, understanding, bliss, all these things which religion and psychology have placed before man, are only adding to the strain of the body. | **single-source** | K. Chandrasekhar audio-tape excerpts, 'Bliss and the Body' (catalogue); kwize gives no book | kwize.com | Verbatim attested on kwize only; the people.well.com chandra.htm excerpts (the likely primary host) did not surface for this sentence. |
| q7960d85e | corroborated-secondary | paraphrase | I don't exercise; I used to walk a great deal. | **corroborated-secondary** | No Way Out, Ch. 9 Leave the Body Alone (Conversation with a Physician) | en.wikisource.org, travelswithug.com | Exact sentence not found by search; the UG Cookbook reporter anecdote corroborates the 'I don't exercise' claim in different wording. Chapter title confirmed via heartofyoga/true-dhamma listings. |
| q8017e676 | single-source | fragment | man, who supposedly has achieved so much progress in the scientific field, cannot even predict precisely when an earthquake is going to occur | **single-source** | Stopped in Our Tracks | en.wikisource.org | Not surfaced by search on any second host. |
| qb3256f66 | corroborated-secondary | paraphrase | Thought is too slow to capture life. | **corroborated-secondary** | Mind is a Myth; Wikiquote: Ch. 1 The Certainty That Blasts Everything; AZQuotes: Ch. 3 Not Knowing Is Your Natural State | azquotes.com, en.wikiquote.org, goodreads.com, libquotes.com, quotefancy.com | Verbatim recovered. Chapter conflict between Wikiquote (Ch. 1) and AZQuotes (Ch. 3). Many aggregators, no primary host surfaced. |
| qcf088078 | single-source | verbatim | in the 'natural state' the continuity of thought is absent. What is present is a disjoined series of independent interactions. | **single-source** | The Natural State | content.e-bookshelf.de, en.wikisource.org | Exact phrase not surfaced by search; e-bookshelf PDF preview of The Natural State is a potential second host but unconfirmed. |
| q585101a0 | single-source | fragment | I had seven years of sadhana. | **single-source** | The Mystique of Enlightenment, Part One | en.wikisource.org, people.well.com | Exact phrase not surfaced by search; people.well.com hosts the same Part One text (likely second primary host) but the sentence was not confirmed there. |
| qb0c876bc | corroborated-primary | fragment | my grandfather knew Blavatsky and Olcott, and then, later on, the second and third generation of Theosophists | **corroborated-primary** | The Mystique of Enlightenment, Part One; Bhatt biography ch. 'Early Years' gives the same background | en.wikisource.org, people.well.com, ug-k.blogspot.com | Full sentence recovered; confirmed on Wikisource and people.well.com (two primary hosts). |

## Recovered verbatim sentences

- **q5af2e554** — catalogue: _one can do nothing to attain the natural state. In fact, any movement towards it separates one from it._
  - > He states emphatically that one can do nothing to attain the natural state. In fact, any movement towards it separates one from it.
  - book per sources: The Mystique of Enlightenment (publisher blurb / introduction)
- **qc40e7904** — catalogue: _[damn fool passage, paraphrase only]_
  - > I have been a damn fool all my life, searching for something which does not exist.
  - book per sources: Mind is a Myth, Introduction ('A Note at the Beginning') by Terry Newland
- **qd124d20c** — catalogue: _Tradition is a burden people cling to; it has to fall away on its own._
  - > You love the burden of the cultural garbage-sack, the dead refuse of the past... it has to drop away naturally.
  - book per sources: Mind is a Myth
- **qfd63f8c6** — catalogue: _Thought has interfered and trying to suppress, control, and moralize about desire, to the detriment of mankind._
  - > Thought has interfered and tried to suppress, control, and moralize about desire, to the detriment of mankind.
  - book per sources: Mind is a Myth, Ch. I (Wikisource); goodreads files it under Certainty: Life has no beginning, no end
- **q43697aec** — catalogue: _There is no such thing as your mind or my mind; a separate individual mind is an illusion; thought is a protective mechanism._
  - > There is no such thing as your mind or my mind.
  - > Thought is a very protective mechanism and is interested in its own survival.
  - book per sources: Thought is Your Enemy
- **qbd6fe67c** — catalogue: _What you are afraid of is not death._
  - > What you are afraid of is not death. It is fear that makes you believe that you are living and that you will be dead.
  - book per sources: No Way Out
- **q08218f4e** — catalogue: _The body cannot be afraid of death._
  - > The body cannot be afraid of death. The movement that is created by society or culture is what does not want to come to an end.
  - book per sources: No Way Out
- **q92ffcf50** — catalogue: _The fixed "I" as a reference point; the courage needed to drop one's conditioning; rejecting what others offer is the real task._
  - > The reference point, the "I", cannot be eliminated through any volition on your part. In the final analysis, it is your genetically predetermined program, your "script".
  - > No amount of cultivation, of either meekness or courage, will be of any help whatsoever.
  - book per sources: Thought is Your Enemy (passages 6-7, 6-11, 6-12 per remembering-ug)
- **q9fd58abe** — catalogue: _You cannot look at your thought, because you cannot separate yourself from thought._
  - > It is not possible for you to watch your thoughts, it is not possible for you to watch every step you take.
  - > You cannot actually separate yourself from thought and look at it.
  - book per sources: The Courage to Stand Alone (Amsterdam 'Give Up' tapes, 1982)
- **q1c893a18** — catalogue: _Thinking about and struggling against 'sorrow' is sorrow. Since you can't stop thinking, and thinking is sorrow, you will always suffer._
  - > Sorrow is there for you as long as you think. There is actually no sorrow there to be free from. Thinking about and struggling against "sorrow" is sorrow.
  - book per sources: Mind is a Myth
- **q373b0000** — catalogue: _The highest goal is like a horizon that recedes as you approach it, a projection of your own fear._
  - > Q: Is there any higher goal at all? U.G.: The so-called "highest goal" is like the horizon. The further you move towards it, the further it recedes. The goal, like the horizon, is not really there. It is a projection of your own fear and it moves away from you as you pursue it.
  - book per sources: Mind is a Myth, Ch. I (Wikisource Q&A); kwize files it under The Natural State
- **q241d3a5e** — catalogue: _as long as you depend upon somebody for solving your problems, so long you remain helpless_
  - > But as long as you depend upon somebody for solving your problems, so long you remain helpless. And this helplessness is exploited by the people who actually do not have the answers to your problems, but they give you some sort of a comforter.
  - book per sources: unassigned (praveennv 'True Guru' post); brooklynaikikai quotes a related line from Louis Brawley's Goner
- **qcc769ade** — catalogue: _By giving money they control you, and by not giving money they control you._
  - > By giving money they control you, and by not giving money they control you... As long as you want something from someone, there will always be someone out there to control you.
  - book per sources: A Taste of Death (catalogue); inner-quest gives no book; people.well.com Mahesh Bhatt journal (Gstaad diary)
- **qf7b06ab4** — catalogue: _I have wasted seven years listening to you._
  - > I have wasted seven years listening to you.
  - > I've wasted seven years.
  - book per sources: U.G. Krishnamurti: A Life (Mahesh Bhatt), ch. 'Locking of Horns'
- **q69a4a09e** — catalogue: _I wasted seven years listening to him._
  - > I have wasted seven years listening to you.
  - book per sources: U.G. Krishnamurti: A Life (Mahesh Bhatt), 'Locking of Horns' (catalogue had it unassigned)
- **qf83cd77e** — catalogue: _Yoga, meditation and prayer are violent techniques. The living body is very peaceful; you don't have to do a thing._
  - > You are trying to enforce peace through violence. Yoga, meditation, prayers, mantras, are all violent techniques. The living organism is very peaceful; you don't have to do a thing.
  - book per sources: unassigned; Whitwell attributes the related 'any doing in any direction is violence' to The Natural State
- **qd39fb8fe** — catalogue: _You have to liberate yourself._
  - > You have to liberate yourself, and you are unable to do that.
  - book per sources: Thought is Your Enemy
- **q3efc45a4** — catalogue: _Our basic human problems are neurological, not psychological. Thought has created the problem of desire._
  - > What I am emphasizing is that we are trying to solve our basic human problems through a psychological framework when the problem is neurological.
  - book per sources: goodreads: Certainty: Life has no beginning, no end; Wikisource: Mind is a Myth, Ch. I
- **q9c3dac12** — catalogue: _is not yours; it is something which you and your ancestors have accumulated over a long time_
  - > And this knowledge is not yours; it is something which you and your ancestors have accumulated over a long time.
  - book per sources: Mind is a Myth, Ch. III Not Knowing Is Your Natural State
- **qeb9c85d2** — catalogue: _…a tremendous upheaval…_
  - > By 1961 his money was finished, and he felt beginning within him a tremendous upheaval which he could not and did not wish to control, and which was to last six years and end with the 'calamity'.
  - book per sources: The Mystique of Enlightenment, Part One (parenthetical editorial biographical note)
- **q718e3b22** — catalogue: _A passage that ends with the speaker saying there is no escape._
  - > Thinking about and struggling against "sorrow" is sorrow. Since you can't stop thinking, and thinking is sorrow, you will always suffer. There is no way out, no escape.
  - book per sources: Aggregators tie the 'no way out, no escape' ending to the sorrow passage of Mind is a Myth, not to No Way Out Ch. 7
- **qb4eaccd2** — catalogue: _The basic question which we have to ask for ourselves is: what kind of a human being do you want? But unfortunately we have placed before ourselves the model of a perfect being._
  - > Unfortunately, the religious thinking of man for centuries has placed before us the model of a perfect being.
  - book per sources: No Way Out, Ch. 7 What Kind of Human Being Do You Want?
- **q1a68f39e** — catalogue: _in that sense the body is immortal_
  - > Life and death cannot be separated. When what you call clinical death takes place, the body breaks itself into its constituent elements and that provides the basis for the continuity of life. In that sense the body is immortal.
  - book per sources: Mind is a Myth, Ch. I (catalogue); people.well.com remembrance and inner-quest biography page quote the same passage
- **q679cf6ae** — catalogue: _Man created God out of fear; so the problem is fear, not God._
  - > There is no power outside of man. Man has created God out of fear. So the problem is fear and not God.
  - book per sources: The Mystique of Enlightenment, Part One (catalogue); aggregators give no book
- **qa1859f82** — catalogue: _there is no power outside of man_
  - > There is no power outside of man. Man has created God out of fear. So the problem is fear and not God.
  - book per sources: The Mystique of Enlightenment, Part One (catalogue); goodreads files fear material under No Way Out
- **q95e9c782** — catalogue: _I am neither a jivanmukta nor an evolved being._
  - > I am not a jivanmukta; nor am I an evolved being.
  - book per sources: Stopped in Our Tracks, Book One (Chandrasekhar; chapters 'You Will Never Know a Jivanmukta' / 'There Is No Moksha, No Jivanmukti and No Atman')
- **qaa3bf764** — catalogue: _The natural state is not a thoughtless state; that is a hoax that has been carried on for thousands of years. You will never be without thought._
  - > ...the ideal of a thoughtless state is one of the many hoaxes Hindus have fallen for.
  - > Thoughts are there and will remain there.
  - book per sources: The Natural State
- **q85d5f7a2** — catalogue: _It is a physiological state, with no religious or mystical content._
  - > ...a pure and simple physical and physiological state of being.
  - > It is not a synonym for enlightenment, freedom or God-realization.
  - book per sources: The Natural State
- **q55779bfa** — catalogue: _eat what you like because the perfect intelligence of life knows exactly what to do with food_
  - > He would say eat what you like because the perfect intelligence of life knows exactly what to do with food.
  - book per sources: unassigned; Mark Whitwell interview recollection
- **q76f1764e** — catalogue: _How I got into this state I will never be able to tell._
  - > How I got into this state I will never be able to tell. I may trace it back to a particular point and beyond that I don't know what happened.
  - book per sources: The Biology of Enlightenment: Unpublished Conversations 1967-71 (ed. Mukunda Rao, HarperCollins India)
- **qb3256f66** — catalogue: _Thought is too slow to capture life._
  - > Thought can never capture the movement of life, it is much too slow. It is like lightning and thunder. They occur simultaneously, but sound, travelling slower than light, arrives later.
  - book per sources: Mind is a Myth; Wikiquote: Ch. 1 The Certainty That Blasts Everything; AZQuotes: Ch. 3 Not Knowing Is Your Natural State
- **qb0c876bc** — catalogue: _my grandfather knew Blavatsky and Olcott, and then, later on, the second and third generation of Theosophists_
  - > He knew Blavatsky (the founder of the Theosophical Society) and Olcott, and then, later on, the second and third generation of Theosophists. They all visited our house.
  - book per sources: The Mystique of Enlightenment, Part One; Bhatt biography ch. 'Early Years' gives the same background

## Conflicts and flags

- **Book attribution conflicts**
  - qfd63f8c6 / q3efc45a4 (desire is neurological; thought has interfered): Wikisource *Mind is a Myth* Ch. I vs goodreads *Certainty: Life has no beginning, no end*. Wikisource also reads "tried to suppress", goodreads "trying to suppress".
  - q373b0000 (highest goal is like the horizon): catalogue/kwize say *The Natural State*; Wikisource and the Mind-is-a-Myth PDF carry it as *Mind is a Myth* Ch. I Q&A. Recommend reassigning to *Mind is a Myth*.
  - qb3256f66 (thought is too slow): Wikiquote places it in *Mind is a Myth* Ch. 1, AZQuotes in Ch. 3.
  - qc40e7904 (damn fool): aggregators attribute it to Terry Newland's Introduction; quotepark puts the neighbouring "search is at an end" lines in Ch. 4.
  - q4fc99cde (peace already there): Wikiquote files it under *The Courage to Stand Alone*; a parallel dialogue exists in *Mind is a Myth* Ch. V. Catalogue has it unassigned.
  - q718e3b22 (passage ending "there is no escape"): the only "no way out, no escape" ending found closes the *Mind is a Myth* sorrow passage (q1c893a18), not a *No Way Out* Ch. 7 passage. Marked disputed.
- **Unassigned quotes that can now be assigned**: qff9ae05a -> *My Swan Song* (duplicate of q338b17ba); q69a4a09e -> Bhatt, *U.G. Krishnamurti: A Life*, "Locking of Horns" (duplicate of qf7b06ab4); qea825286 -> *No Way Out* Ch. 8 (Wikisource); q4fc99cde -> *The Courage to Stand Alone* (Wikiquote).
- **Editor / reporter voice rather than UG's words**
  - qeb9c85d2 "a tremendous upheaval": the editor's bracketed third-person biographical note in *Mystique* Part One. Marked not-ug (UG-adjacent, not UG speech).
  - q5af2e554: publisher/introduction blurb wording ("He states emphatically that one can do nothing...").
  - qc40e7904: Terry Newland (editor) quoting UG in the Introduction.
  - q27ae73f0: travelswithug "UG Cookbook" editorial summary of UG's diet views.
  - q55779bfa: Mark Whitwell's recollection ("He would say eat what you like...").
  - q85d5f7a2: the "no religious or mystical" half is the jhana8 biography's summary.
  - qf71956be, q95e9c782, q07b7ff4c, q95504a40, q8017e676: K. Chandrasekhar's reported speech in *Stopped in Our Tracks* (ed. Narayana Moorty).
  - qf7b06ab4, q69a4a09e, q93a61f20, qcc769ade (second host): Mahesh Bhatt's biography / Gstaad diary.
- **Jiddu Krishnamurti collision risk**: searches for q1c893a18 (sorrow), q241d3a5e (dependence), qac537b40 (violence), q3efc45a4 / qea825286 (desire, pleasure) returned kfoundation.org, jkrishnamurti.org and krishnamurti.org pages for Jiddu; none of those pages carry the UG sentences and all were excluded. quotessayings.net's "Krishnamurti death" topic page (qbd6fe67c) mixes both men. No actual Jiddu misattribution of a UG quote was found; the reverse (generic violence/dependence themes drifting toward Jiddu) is the live risk for qac537b40.
- **Still effectively single-host after search**: q48147bda, q93a61f20, q27ae73f0, q828c848c, qcc9c525e, q441961c4, q670510be, q0d1d00a2, q8d5ee424, q77b540c6, q39067cd0, q8017e676, qcf088078, q585101a0, q55779bfa.
- **Not found at all**: q07b7ff4c ("Why do you call it green?"), q95504a40 ("I am myself a thief.") — neither phrase surfaced on Wikisource, kwize or the blog serialisation of *Stopped in Our Tracks*; the people.well.com attribution is unverified by this pass.

## Sources

- http://nondualite.free.fr/c_ug_courage.htm
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html
- http://praveennv.blogspot.com/2007/10/you-never-see-anything-ug-krishnamurti.html
- http://praveennv.blogspot.com/2008/03/ug-krishnamurti-on-thoughts.html
- http://praveennv.blogspot.com/2016/03/ug-krishnamurtis-quote-on-true-guru.html
- http://remembering-ug.blogspot.com/2012/06/talks-100812.html
- http://remembering-ug.blogspot.com/2012/07/passages-270812.html
- http://remembering-ug.blogspot.com/2012/09/passages-from-thought-is-your-enemy.html
- http://u-g-krishnamurti.blogspot.com/2007/04/there-is-no-moksha-no-jivanmukti-and-no.html
- http://ug-k.blogspot.com/2007/04/conversations-following-conversations.html
- http://ug-k.blogspot.com/2007/04/early-years-real-guru-if-there-is-one.html
- http://ug-k.blogspot.com/2007/04/locking-of-horns-inspiration-is.html
- http://www.travelswithug.com/resources/UGCookbook.pdf
- https://archive.org/details/TheMystiqueOfEnlightenmentU.G.Krishnamurti
- https://content.e-bookshelf.de/media/reading/L-18427162-0b01407361.pdf
- https://dalemusings.wordpress.com/2012/12/25/thought-is-your-enemy-u-g-krishnamurti/
- https://en.wikipedia.org/wiki/U._G._Krishnamurti
- https://en.wikiquote.org/wiki/U._G._Krishnamurti
- https://en.wikisource.org/wiki/Courage_to_Stand_Alone
- https://en.wikisource.org/wiki/Mind_is_a_Myth/I
- https://en.wikisource.org/wiki/Mind_is_a_Myth/III
- https://en.wikisource.org/wiki/Mind_is_a_Myth/IV
- https://en.wikisource.org/wiki/Mind_is_a_Myth/V
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_7
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_8
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_9
- https://en.wikisource.org/wiki/Science_and_U.G.
- https://en.wikisource.org/wiki/Stopped_in_Our_Tracks:_Stories_of_U.G._in_India
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Four
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_One
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Three
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Two
- https://en.wikisource.org/wiki/The_Natural_State
- https://en.wikisource.org/wiki/Thought_is_Your_Enemy
- https://jhana8.com/ug-krishnamurti-biography/
- https://kwize.com/en/authors/U-G-Krishnamurti/
- https://kwize.com/en/texts/U-G-Krishnamurti-Science-and-U-G/
- https://kwize.com/en/texts/U-G-Krishnamurti-Stopped-in-Our-Tracks-Stories-of-U-G-in-India/
- https://kwize.com/en/texts/U-G-Krishnamurti-The-Mystique-of-Enlightenment/
- https://kwize.com/en/texts/U-G-Krishnamurti-The-Natural-State/
- https://libquotes.com/u-g-krishnamurti/quotes/peace
- https://libquotes.com/u-g-krishnamurti/quotes/thought
- https://markwhitwell.medium.com/is-meditation-evil-mark-whitwell-bb32f52c348f
- https://markwhitwell.medium.com/understanding-u-g-krishnamurti-an-interview-with-mark-whitwell-part-4-cab1a90ea0b1
- https://markwhitwell.medium.com/what-u-g-krishnamurti-did-for-yoga-mark-whitwell-4d399223e3c1
- https://medium.com/@alysion42/u-g-krishnamurtis-swan-song-updated-e36a07cc0595
- https://medium.com/@harpeony/book-summary-the-natural-state-in-the-words-of-u-g-krishnamurti-part-1-3-04f7c43a78c4
- https://o-meditation.com/wp-content/uploads/2011/05/krishnamurti-u-g-mind-is-a-myth.pdf
- https://o-meditation.com/wp-content/uploads/2011/05/the-courage-to-stand-alone.pdf
- https://people.well.com/user/jct/Final_Remembering.htm
- https://people.well.com/user/jct/SIT/part_i.htm
- https://people.well.com/user/jct/SWAN_SONG.htm
- https://people.well.com/user/jct/chandra.htm
- https://people.well.com/user/jct/enemy0.htm
- https://people.well.com/user/jct/intro.html
- https://people.well.com/user/jct/mahesh.html
- https://people.well.com/user/jct/mystiq1.htm
- https://people.well.com/user/jct/nwo1.htm
- https://people.well.com/user/jct/reddi.htm
- https://people.well.com/user/jct/ugbio/ugbio2.htm
- https://people.well.com/user/jct/ugbio/ugbio4.htm
- https://quotefancy.com/quote/2210935/U-G-Krishnamurti-Sorrow-is-there-for-you-as-long-as-you-think-There-is-actually-no-sorrow
- https://quotefancy.com/quote/923764/U-G-Krishnamurti-Thought-can-never-capture-the-movement-of-life-it-is-much-too-slow-It-is
- https://quotepark.com/authors/ug-krishnamurti/
- https://quotessayings.net/topics/krishnamurti-death/
- https://quotlr.com/author/ug-krishnamurti
- https://realitysandwich.com/introduction_u_g_krishnamurti/
- https://the-natural-state.blogspot.com/2012/12/3.html
- https://ugarchive.blogspot.com/2021/09/an-introduction-to-ug-krishnamurti.html
- https://www.actualized.org/forum/topic/101055-making-sense-of-ug-krishnamurti-part-2/
- https://www.amazon.com/Mystique-Enlightenment-Radical-Ideas-Krishnamurti/dp/0971078610
- https://www.awakeningtoreality.com/2018/10/ug-krishnamurti-mystique-of.html
- https://www.azquotes.com/author/17848-U_G_Krishnamurti
- https://www.azquotes.com/author/17848-U_G_Krishnamurti?p=2
- https://www.brooklynaikikai.com/post/from-u-g-krishnamurti
- https://www.dailygood.org/pdf/ij.php?tid=118
- https://www.emperyquotes.com/authors/ug-krishnamurti
- https://www.everand.com/book/427470011/Biology-Of-Enlightenment
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=2
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=3
- https://www.goodreads.com/book/show/13438871-the-natural-state
- https://www.goodreads.com/book/show/53527
- https://www.goodreads.com/quotes/7271037-what-i-am-emphasizing-is-that-we-are-trying-to
- https://www.goodreads.com/quotes/8510744-the-body-cannot-be-afraid-of-death-the-movement-that
- https://www.goodreads.com/work/quotes/46398939-u-g-krishnamurti-certainty-life-has-no-beginning-no-end
- https://www.goodreads.com/work/quotes/52202-mind-is-a-myth
- https://www.goodreads.com/work/quotes/6212984
- https://www.goodreads.com/work/quotes/6212984-no-way-out-dialogues-with-krishnamurti
- https://www.goodreads.com/work/quotes/6212994-thought-is-your-enemy-mind-shattering-conversations-with-the-man-called
- https://www.heartofyoga.com/blog/2021/3/12/the-influence-of-ug-krishnamurti-on-yoga
- https://www.hindu-blog.com/2018/09/u-g-krishnamurti-quotes-and-teachings.html
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Mind-is-a-myth.pdf
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-The-Mystique-of-Enlightenment.pdf
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Thought-is-Your-Enemy.pdf
- https://www.inner-quest.org/UG.htm
- https://www.inner-quest.org/UG_Natural_State.htm
- https://www.inner-quest.org/UG_R.htm
- https://www.inner-quest.org/UG_Words.htm
- https://www.keplers.com/book/9780971078611
- https://www.scribd.com/document/107499881/Ug-Cookbook
- https://www.scribd.com/document/111395488/No-Way-Out-UG-Krishnamurti
- https://www.simonandschuster.com/books/The-Mystique-of-Enlightenment/U-G-Krishnamurti/9780971078611
- https://www.slideshare.net/slideshow/ugcookbookpdf/257314660
- https://www.ugkrishnamurti.in/ug-essence/my-swan-song
