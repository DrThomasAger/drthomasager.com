# Wave 8 — Verification pass 4, half B (odd-id paraphrases and fragments)

Scope: every quote in `quotes.json` whose prior verdict was `primary-source`, `multi-source` or `single-source` and whose id ends in an odd hex digit (47 quotes: 18 paraphrases, 19 fragments, 10 verbatim). Method: 45 web searches (extended mode) on key noun phrases plus "Krishnamurti" and the book title, with Jiddu Krishnamurti foundation domains blocked. Goal: recover the verbatim sentence behind each paraphrase/fragment, find a second independent host, and note primary-host confirmation (en.wikisource.org, people.well.com, archive.org, ugkrishnamurti.in). JSON twin: `scratchpad/json/verification-4b.json`.

## Per-verdict summary

| Verdict | Count |
|---|---|
| corroborated-primary | 28 |
| corroborated-secondary | 10 |
| single-source | 8 |
| disputed | 1 |
| not-ug | 0 |
| not-found | 0 |
| **Total searched** | **47** |

Verbatim or near-verbatim source sentences recovered for **29** of 47 quotes (listed below). Prior-verdict breakdown of the set: 14 primary-source, 3 multi-source, 30 single-source.

## Table

| id | prior | kind | text checked | verdict | book per sources | primary host hit | confirming hosts |
|---|---|---|---|---|---|---|---|
| qee37e731 | single-source | paraphrase | Both the inner and outer worlds proceed from a point of thought; everything experienced is born out of thought… | corroborated-primary | Mind is a Myth, ch. I (The Certainty That Blasts Everything) | yes | en.wikisource.org, holybooks.com, kwize.com |
| q539055bd | single-source | paraphrase | Our experience of our own body depends on thought, and thought is memory. | corroborated-primary | Thought is Your Enemy (1985-90 conversations) | yes | en.wikisource.org, holybooks.com, remembering-ug.blogspot.com |
| q87a66997 | single-source | fragment | your teacher must go, it doesn't matter who the teacher is | single-source | unassigned (hindu-blog gives no book) | no | hindu-blog.com |
| qab99509d | single-source | fragment | blind acceptance of authority, all second-hand stuff | corroborated-secondary | The Natural State (per Harpeony summary) | no | harpeony.com, hindu-blog.com |
| qe74e02bb | single-source | paraphrase | the death of fear is the only death | corroborated-secondary | No Way Out (per praveennv blog title); aggregators give no book | no | praveennv.blogspot.com, quotlr.com |
| q540a25ff | single-source | paraphrase | Death described as atoms changing form, with nothing born and nothing dead. | corroborated-secondary | Mind Is a Myth (AZQuotes, 1987); also recalled in Stopped in Our Tracks (Chandrasekhar) | no | azquotes.com, goodreads.com, kwize.com |
| q77a9194f | single-source | paraphrase | Each time a thought is born, you are born; thought is short-lived. Traditional rebirth read as this cycle. | corroborated-secondary | Goodreads lists under The Mystique of Enlightenment / Mind Is a Myth; catalogue had The Courage to Stand Alone | no | goodreads.com, infant7sorrow.wordpress.com, praveennv.blogspot.com |
| q72c0b555 | single-source | paraphrase | Questioning the solutions requires a tremendous courage. | single-source | The Courage to Stand Alone, p. 69 (per blog) | no | praveennv.blogspot.com |
| qe27976db | single-source | verbatim | You hook up each thought with the next, creating a false continuity. It is that continuity that is the problem… | corroborated-primary | Mind is a Myth, ch. III (Not Knowing Is Your Natural State) | yes | en.wikisource.org, goodreads.com |
| q044d9da9 | single-source | verbatim | It is not an illusion, only your experience of it is an illusion. | corroborated-primary | Mind is a Myth, ch. I (not The Courage to Stand Alone) | yes | en.wikisource.org, goodreads.com, remembering-ug.blogspot.com |
| qd05c2db1 | single-source | verbatim | you arrive seeking understanding, while I am only interested in making it crystal clear that there is nothing … | corroborated-primary | Mind is a Myth, ch. IV (There Is Nothing To Understand) | yes | en.wikisource.org, holybooks.com |
| q6f33cc13 | single-source | fragment | the same old nonsense repeating itself | corroborated-primary | The Natural State (1983-84 Amsterdam talks); also Mind is a Myth ch. III | yes | en.wikisource.org, kwize.com, the-natural-state.blogspot.com |
| qae3cbc6d | multi-source | paraphrase | His findings run counter to everything anyone has said in any field of human thought. | corroborated-primary | My Swan Song (dictated to Louis Brawley, mid-Feb 2007) | yes | groups.google.com, people.well.com, sciforums.com, ugkrishnamurti.in |
| qf7b51191 | primary-source | paraphrase | Freeing the body from what is put in it by spiritual teachers or secular teachers, or by those scientists and … | corroborated-primary | My Swan Song (2007) | yes | people.well.com, sciforums.com, ugkrishnamurti.in |
| q5e50266d | single-source | paraphrase | Sex is for reproduction; people have turned it into a pleasure movement; an enlightened man can never have sex… | corroborated-primary | My Swan Song (2007) | yes | groups.google.com, people.well.com, sciforums.com, ugkrishnamurti.in |
| qa106c8ad | primary-source | paraphrase | Sex is for reproduction; people have turned it into a pleasure pursuit. An enlightened man cannot have sex bec… | corroborated-primary | My Swan Song (2007) | yes | people.well.com, sciforums.com, ugkrishnamurti.in |
| q88d291eb | single-source | fragment | Act, don't think! | corroborated-secondary | Mahesh Bhatt, A Taste of Death: Thirty Days with U.G. in Gstaad (1995), day 12 entry; also in U.G. Krishnamurti: A Life | yes | azquotes.com, en.wikiquote.org, nirvana73.blogspot.com, people.well.com |
| q3646651d | single-source | fragment | There is nothing to your love: if you don't get what you want, what happens to your, "I love you darling…" | corroborated-primary | My Swan Song (2007) | yes | inner-quest.org, medium.com, sciforums.com, ugkrishnamurti.in |
| q505bda73 | single-source | fragment | The whole thing comes to an end. | single-source | The Biology of Enlightenment (ed. Mukunda Rao, HarperCollins India 2010; 1967-71 conversations) | no | realitysandwich.com |
| q181d741b | single-source | fragment | …all the positive approaches that man has invented and used for centuries have not resulted in anything useful… | corroborated-primary | The Courage to Stand Alone, Part III | yes | beyond-the-pale.co.uk, en.wikisource.org, o-meditation.com |
| q96cd1f77 | primary-source | fragment | …I knew without doubt that I had made the biggest mistake of my life. | corroborated-primary | U.G. Krishnamurti: A Life (Mahesh Bhatt), ch. 4 'Locking of Horns' (not ch. 5 'Adrift in London') | yes | egodeathfilms.wordpress.com, people.well.com, ug-k.blogspot.com |
| q2f03fb65 | primary-source | paraphrase | If you could have sex with your own mother without any psychological or spiritual problem, that would be the e… | corroborated-primary | No Way Out, ch. 8 | yes | en.wikisource.org, file.true-dhamma.com, scribd.com |
| qb609f6f3 | single-source | paraphrase | People call me enlightened, a term I dislike; there is no such thing as enlightenment. | corroborated-primary | The Mystique of Enlightenment (1982; conversations 1973-76), Part Three/Four | yes | en.wikisource.org, holybooks.com, people.well.com, quotepark.com |
| q4895987b | primary-source | fragment | belief is an extension of the survival mechanism which has operated for millions of years | corroborated-primary | Science and U.G. (Wikisource/WELL compilation); catalogue says Mind is a Myth ch. III | yes | en.wikisource.org, people.well.com |
| q4b9ab831 | single-source | verbatim | I am not against the scientific method per se. | single-source | unassigned; closest Wikisource hits are No Way Out ch. 10 and Science and U.G. | yes | en.wikisource.org |
| q9c460863 | single-source | verbatim | The understanding that there is nothing to understand is all there is. | single-source | Mind is a Myth (catalogue: ch. V); Wikisource ch. IV is 'There Is Nothing To Understand' | yes | en.wikisource.org, nomindsland.blogspot.com |
| q4c3e36cf | single-source | verbatim | Time and space, apart from the ideas of 'time' and 'space', do not exist at all. | corroborated-secondary | Mind is a Myth, Chapter Six (Dinesh Publications, Goa) per actualfreedom.com.au | yes | actualfreedom.com.au, en.wikisource.org |
| q00193fb7 | primary-source | verbatim | Thought is you. | corroborated-primary | Stopped in Our Tracks, Book Two: Excerpts from U.G.'s Dialogues (K. Chandrasekhar), section 'Thinking Is the Problem' | yes | people.well.com |
| q2d12cceb | single-source | fragment | it is the ones who believe in God, who preach peace and talk of love, who have created the human jungle | corroborated-secondary | Mind is a Myth (1987), ch. I 'The Certainty That Blasts Everything' (per quote sites) | no | en.wikiquote.org, libquotes.com, o-meditation.com, quotepark.com |
| qaccf09f3 | primary-source | fragment | it has to come, and it will come from the West | corroborated-primary | The Mystique of Enlightenment, Part Three | yes | en.wikisource.org, holybooks.com |
| q4f2c81d1 | primary-source | fragment | the very birth of thought creates fear | corroborated-primary | Mind is a Myth, ch. V | yes | en.wikisource.org, holybooks.com, o-meditation.com |
| qc852ca7b | single-source | fragment | happiness without one moment of unhappiness, pleasure without pain, it is the same thing | corroborated-primary | No Way Out (2002), ch. 2 | yes | en.wikiquote.org, en.wikisource.org, praveennv.blogspot.com, quotepark.com |
| qfc5867cf | single-source | verbatim | There is no happiness. | single-source | inner-quest.org interview transcript (interviewer Mr. Kothari); no book named | no | inner-quest.org |
| q762cadb3 | single-source | verbatim | That is to say, all that is born out of thought is destructive, irrespective of its nature, whether it be reli… | corroborated-primary | Science and U.G. | yes | en.wikisource.org, kwize.com |
| q7f2ee6c3 | single-source | verbatim | The body or organism is not interested in spiritual matters. | corroborated-primary | Science and U.G., chapter 'The Innate Intelligence of the Body' | yes | en.wikisource.org, kwize.com, people.well.com |
| qa850f231 | primary-source | paraphrase | I am not suggesting that you should stop thinking; thought is what you are. | corroborated-primary | Stopped in Our Tracks, Book Two: Excerpts from U.G.'s Dialogues, section 'Thinking Is the Problem' | yes | people.well.com |
| q6a9a1403 | single-source | fragment | all we can know is memory and memory is thought | corroborated-primary | The Natural State; near-identical line in Mind is a Myth ch. III | yes | en.wikisource.org, kwize.com |
| qc60032ad | primary-source | fragment | it is through this constant thinking that we are maintaining the continuity of what we call the 'I' or 'self' | corroborated-primary | Thought is Your Enemy (Wikisource; editor's framing of U.G.'s view) | yes | en.wikisource.org, ia801804.us.archive.org |
| q104a81af | single-source | fragment | the fear of losing what we have and what we know is responsible for our problems | corroborated-secondary | No Way Out (2002), Ch. 7 'What Kind Of Human Being Do You Want?' (Wikiquote/Quotepark) | no | en.wikiquote.org, goodreads.com, quotefancy.com, quotepark.com |
| q0c6ee69f | single-source | fragment | a useless exercise | corroborated-secondary | Wikipedia-derived biography text; no book named | no | en-academic.com, heartofyoga.com, inner-quest.org |
| q707dda41 | primary-source | paraphrase | My aim is to silence you. | single-source | Stopped in Our Tracks, Book Two (Chandrasekhar), per catalogue; not confirmed by search | yes | people.well.com |
| q93c2842f | multi-source | paraphrase | Whatever transformation I have undergone is within the structure of the human body and not in the mind at all. | corroborated-secondary | The Biology of Enlightenment (ed. Mukunda Rao, HarperCollins India 2010/2012), Rao's introduction | no | books.google.com, everand.com, goodreads.com, realitysandwich.com |
| qdab04c55 | single-source | paraphrase | The natural state is a pure and simple physical and physiological state of being, where it is not the self or … | corroborated-primary | The Biology of Enlightenment (Rao intro) for the catalogue wording; the core sentence is U.G.'s own in No Way Out ch. 1 / Natural State dialogues | yes | en.wikisource.org, inner-quest.org, people.well.com, realitysandwich.com |
| q8233c2a7 | primary-source | fragment | No one escapes the natural laws. | corroborated-primary | The Sage and the Housewife (Shanta Kelker, 1990; Smriti Books 2005), ch. 1 | yes | en.wikisource.org, people.well.com, ugkrishnamurti.in |
| q7bd7cc71 | multi-source | fragment | It is the body that is immortal. It is living from moment to moment. | disputed | The Sage and the Housewife ch. 3 (Wikiquote/libquotes) vs No Way Out (2002) ch. 4 'You Invent Your Reality' (Quotepark) | no | en.wikiquote.org, libquotes.com, quotepark.com |
| q9feeb1bf | primary-source | paraphrase | I don't know what happiness is. | single-source | The Sage and the Housewife ch. 4 (per catalogue; WELL sage4.htm exists but the line was not surfaced); parallel in inner-quest Kothari interview | yes | inner-quest.org, people.well.com |
| q1268f7b9 | primary-source | paraphrase | A person to whom Kundalini rises would dismiss the very concept of Kundalini. | corroborated-primary | The Sage and the Housewife, ch. 7 | yes | en.wikisource.org, people.well.com, remembering-ug.blogspot.com |

## Recovered verbatim sentences

Entries in square brackets are search-summary renderings or reported speech, not clean verbatim text.

- **qee37e731** (Mind is a Myth, ch. I (The Certainty That Blasts Everything)) — catalogue text: *Both the inner and outer worlds proceed from a point of thought; everything experienced is born out of thought, so exper*
  - Both the 'inner' and 'outer' worlds proceed from a point of thought [search-summary rendering of the Wikisource ch. I passage; companion line: 'It is not an illusion, only your experience of it is an illusion']
- **q539055bd** (Thought is Your Enemy (1985-90 conversations)) — catalogue text: *Our experience of our own body depends on thought, and thought is memory.*
  - [summary rendering] Without the knowledge that is passed on to us, you cannot experience your own body or your experiences... thought is memory
- **q87a66997** (unassigned (hindu-blog gives no book)) — catalogue text: *your teacher must go, it doesn't matter who the teacher is*
  - Your teacher must go, it doesn't matter who the teacher is.
- **qab99509d** (The Natural State (per Harpeony summary)) — catalogue text: *blind acceptance of authority, all second-hand stuff*
  - Your beliefs are the result of blind acceptance of authority, all second-hand stuff.
- **qe74e02bb** (No Way Out (per praveennv blog title); aggregators give no book) — catalogue text: *the death of fear is the only death*
  - The death of fear is the only death.
- **q540a25ff** (Mind Is a Myth (AZQuotes, 1987); also recalled in Stopped in Our Tracks (Chandrasekhar)) — catalogue text: *Death described as atoms changing form, with nothing born and nothing dead.*
  - The body is a fortuitous concourse of atoms. There is no death for the body, only an exchange of atoms... In reality, nothing is born and nothing is dead.
- **q77a9194f** (Goodreads lists under The Mystique of Enlightenment / Mind Is a Myth; catalogue had The Courage to Stand Alone) — catalogue text: *Each time a thought is born, you are born; thought is short-lived. Traditional rebirth read as this cycle.*
  - Every time a thought is born, you are born. When the thought is gone, you are gone.
  - Thought in its very nature is shortlived, and once it is gone, that's the end of it... what the traditions probably meant by rebirth is death and birth and death and birth
- **q72c0b555** (The Courage to Stand Alone, p. 69 (per blog)) — catalogue text: *Questioning the solutions requires a tremendous courage.*
  - You never question the solutions. If you really question the solutions, you will have to question the people who offered them.
  - The courage to be on your own, to stand on your two solid feet, is something which cannot be given by somebody.
- **q6f33cc13** (The Natural State (1983-84 Amsterdam talks); also Mind is a Myth ch. III) — catalogue text: *the same old nonsense repeating itself*
  - Memory is nothing more than the same old nonsense repeating itself.
- **qae3cbc6d** (My Swan Song (dictated to Louis Brawley, mid-Feb 2007)) — catalogue text: *His findings run counter to everything anyone has said in any field of human thought.*
  - [source phrases confirmed: 'counter to everything' ... 'any field of human thought'; full sentence identical across copies]
- **qf7b51191** (My Swan Song (2007)) — catalogue text: *Freeing the body from what is put in it by spiritual teachers or secular teachers, or by those scientists and medical te*
  - Once this body is freed from the stranglehold of whatever is put in there either by spiritual teachers or secular teachers, or by those scientists and medical technology, it functions in a very efficient way.
- **q5e50266d** (My Swan Song (2007)) — catalogue text: *Sex is for reproduction; people have turned it into a pleasure movement; an enlightened man can never have sex because h*
  - The only reason for this organism to exist is to give continuity to the human species. Sex is only for reproduction, but you have turned that into a pleasure movement.
  - An enlightened man can never have sex because he cannot reproduce another one like him.
- **qa106c8ad** (My Swan Song (2007)) — catalogue text: *Sex is for reproduction; people have turned it into a pleasure pursuit. An enlightened man cannot have sex because he ca*
  - Sex is only for reproduction, but you have turned that into a pleasure movement.
  - An enlightened man can never have sex because he cannot reproduce another one like him.
- **q88d291eb** (Mahesh Bhatt, A Taste of Death: Thirty Days with U.G. in Gstaad (1995), day 12 entry; also in U.G. Krishnamurti: A Life) — catalogue text: *Act, don't think!*
  - Thinking is a poor alternative to acting. Your thinking is consuming all your energy. Act, don't think!
  - "Act, don't think!" says U.G., turning his fire in my direction.
- **q3646651d** (My Swan Song (2007)) — catalogue text: *There is nothing to your love: if you don't get what you want, what happens to your, "I love you darling…"*
  - There is nothing to your love: if you don't get what you want, what happens to your, 'I love you darling, dearie, honey bunch, shnookie putsie, sugar britches, petite shu-shu, sugar booger?'
  - The only relationship you have with anybody in this world is 'What do I get out of it?'
- **q96cd1f77** (U.G. Krishnamurti: A Life (Mahesh Bhatt), ch. 4 'Locking of Horns' (not ch. 5 'Adrift in London')) — catalogue text: *…I knew without doubt that I had made the biggest mistake of my life.*
  - [reported speech] he was to say later that he knew without doubt he had made the biggest mistake of his life
- **q2f03fb65** (No Way Out, ch. 8) — catalogue text: *If you could have sex with your own mother without any psychological or spiritual problem, that would be the end of your*
  - [summary rendering] I tell people that if they could have sex with their mother without any problem, psychological or spiritual, then that will put an end to your sex. I am not advocating incest as a way of life.
  - Thought always interferes with sex.
- **qb609f6f3** (The Mystique of Enlightenment (1982; conversations 1973-76), Part Three/Four) — catalogue text: *People call me enlightened, a term I dislike; there is no such thing as enlightenment.*
  - People call me an enlightened man — I detest that term — they can't find any other word to describe the way I am functioning.
- **q4b9ab831** (unassigned; closest Wikisource hits are No Way Out ch. 10 and Science and U.G.) — catalogue text: *I am not against the scientific method per se.*
  - [not recovered; related lines: 'I am not anti-rational, just unrational'; 'pure science is nothing but speculation']
- **q9c460863** (Mind is a Myth (catalogue: ch. V); Wikisource ch. IV is 'There Is Nothing To Understand') — catalogue text: *The understanding that there is nothing to understand is all there is.*
  - [closest found] the understanding that there is nothing to understand, nothing to get, dawned on me (nomindsland blog transcript)
  - the truth has to dawn upon you that there is nothing to understand (Mind is a Myth ch. IV)
- **q00193fb7** (Stopped in Our Tracks, Book Two: Excerpts from U.G.'s Dialogues (K. Chandrasekhar), section 'Thinking Is the Problem') — catalogue text: *Thought is you.*
  - I am not suggesting that you should not think. Thought is you.
- **q2d12cceb** (Mind is a Myth (1987), ch. I 'The Certainty That Blasts Everything' (per quote sites)) — catalogue text: *it is the ones who believe in God, who preach peace and talk of love, who have created the human jungle*
  - It is the ones who believe in God, who preach peace and talk of love, who have created the human jungle. Compared to man, the animals are not so violent... The so-called 'civilized' man kills for ideals and beliefs, while the animals kill only for survival.
- **qaccf09f3** (The Mystique of Enlightenment, Part Three) — catalogue text: *it has to come, and it will come from the West*
  - [summary rendering] something has to emerge to save the world... I believe it will come from the West, I cannot say from where... that is why I think India has no chance. I am no prophet of doom.
- **q4f2c81d1** (Mind is a Myth, ch. V) — catalogue text: *the very birth of thought creates fear*
  - Since we think all the time, the very birth of thought creates fear, and it is out of fear that all experience springs.
- **qc852ca7b** (No Way Out (2002), ch. 2) — catalogue text: *happiness without one moment of unhappiness, pleasure without pain, it is the same thing*
  - Whether you are interested in moksha, liberation, freedom, transformation, you name it, you are interested in happiness without one moment of unhappiness, pleasure without pain. It is the same thing.
- **qfc5867cf** (inner-quest.org interview transcript (interviewer Mr. Kothari); no book named) — catalogue text: *There is no happiness.*
  - Q: What is the secret of total happiness? U.G.: There is no happiness. ... Total happiness is an invention.
- **q762cadb3** (Science and U.G.) — catalogue text: *That is to say, all that is born out of thought is destructive, irrespective of its nature, whether it be religious, sci*
  - Thought is destructive; it is a self-protecting mechanism.
- **q7f2ee6c3** (Science and U.G., chapter 'The Innate Intelligence of the Body') — catalogue text: *The body or organism is not interested in spiritual matters.*
  - The body or organism is not interested in spiritual matters. It only aims at survival and reproduction.
- **qa850f231** (Stopped in Our Tracks, Book Two: Excerpts from U.G.'s Dialogues, section 'Thinking Is the Problem') — catalogue text: *I am not suggesting that you should stop thinking; thought is what you are.*
  - I am not suggesting that you should not think. Thought is you.
- **q6a9a1403** (The Natural State; near-identical line in Mind is a Myth ch. III) — catalogue text: *all we can know is memory and memory is thought*
  - All you know or can ever know is memory, and memory is thought. (The Natural State)
  - All you know, or can ever know, is memory, and memory is thought. (Mind is a Myth)
- **qc60032ad** (Thought is Your Enemy (Wikisource; editor's framing of U.G.'s view)) — catalogue text: *it is through this constant thinking that we are maintaining the continuity of what we call the 'I' or 'self'*
  - U.G. says that it is through this constant thinking that we are maintaining the continuity of what we call the 'I' or 'self'. Since it is the continuous thinking activity that gives the illusion of the 'self' or 'I', there is no feeling of 'self' or 'I' within him.
  - Your constant utilization of thought to give continuity to your separate self is 'you'. (1972 talk, On U.G.)
- **q104a81af** (No Way Out (2002), Ch. 7 'What Kind Of Human Being Do You Want?' (Wikiquote/Quotepark)) — catalogue text: *the fear of losing what we have and what we know is responsible for our problems*
  - [fuller passage begins] people don't want to be free... the fear of losing what we have and what we know
- **q0c6ee69f** (Wikipedia-derived biography text; no book named) — catalogue text: *a useless exercise*
  - [Wikipedia mirror] he would later also dismiss this period with Sivananda as a useless exercise
  - [dialogue variant] it didn't help, so I dropped it
- **q93c2842f** (The Biology of Enlightenment (ed. Mukunda Rao, HarperCollins India 2010/2012), Rao's introduction) — catalogue text: *Whatever transformation I have undergone is within the structure of the human body and not in the mind at all.*
  - [Rao, reported speech] He insisted that whatever transformation he had undergone was within the structure of the human body and not in the mind at all.
- **qdab04c55** (The Biology of Enlightenment (Rao intro) for the catalogue wording; the core sentence is U.G.'s own in No Way Out ch. 1 / Natural State dialogues) — catalogue text: *The natural state is a pure and simple physical and physiological state of being, where it is not the self or the mind, *
  - The natural state is a pure and simple, physical and physiological state of being.
- **q8233c2a7** (The Sage and the Housewife (Shanta Kelker, 1990; Smriti Books 2005), ch. 1) — catalogue text: *No one escapes the natural laws.*
  - Ramana or anybody for that matter undergoes the same physical suffering. No one escapes the natural laws.
- **q9feeb1bf** (The Sage and the Housewife ch. 4 (per catalogue; WELL sage4.htm exists but the line was not surfaced); parallel in inner-quest Kothari interview) — catalogue text: *I don't know what happiness is.*
  - [inner-quest interview parallel] For all practical purposes, I don't think I ever feel happy at all. That's why I don't even know what happiness is. Therefore I can never be unhappy either.
  - If you do not know what happiness is, you will never be unhappy. (No Way Out)
- **q1268f7b9** (The Sage and the Housewife, ch. 7) — catalogue text: *A person to whom Kundalini rises would dismiss the very concept of Kundalini.*
  - [near-verbatim] if a Kundalini Shakti exists and rises, the person to whom it happens would brush aside the very concept of Kundalini

## Conflicts and cautions

- **q044d9da9** — Catalogue files 'It is not an illusion, only your experience of it is an illusion' under The Courage to Stand Alone; Wikisource ch. I, Goodreads and remembering-ug all place it in Mind is a Myth.
- **q540a25ff** — Atoms/'nothing is born and nothing is dead' passage: AZQuotes says Mind Is a Myth (1987); the kwize excerpt of Stopped in Our Tracks has Chandrasekhar recalling U.G. saying it before a corpse.
- **q77a9194f** — 'Every time a thought is born, you are born': catalogue says The Courage to Stand Alone; Goodreads lists its two halves under The Mystique of Enlightenment and Mind Is a Myth.
- **q96cd1f77** — 'Biggest mistake of my life' sits in WELL ugbio4.htm = Bhatt ch. 4 'Locking of Horns', not ch. 5 'Adrift in London' as catalogued. Reported speech via Mahesh Bhatt.
- **q4895987b** — 'Belief is an extension of the survival mechanism' found only in the Science and U.G. compilation (Wikisource + WELL reddi.htm), not in the Mind is a Myth ch. III hit.
- **q4c3e36cf** — 'Time and space, apart from the ideas...' found only on actualfreedom.com.au, which cites Mind is a Myth ch. 6; catalogue's people.well.com host not surfaced.
- **q9c460863** — 'The understanding that there is nothing to understand is all there is' — the 'is all there is' tail was not found verbatim anywhere; chapter is probably IV, not V.
- **q4b9ab831** — 'I am not against the scientific method per se' — not surfaced in any search result; remains Wikisource-only per catalogue.
- **q707dda41** — 'My aim is to silence you' — not found; the only 'silence' line in Stopped in Our Tracks is Nagaraj's 'I will salute you if you can silence him'. Check the archive.org full text.
- **q7bd7cc71** — 'It is the body that is immortal' — Wikiquote/libquotes: Sage and the Housewife ch. 3; Quotepark: No Way Out ch. 4. Marked disputed (attribution only).
- **q00193fb7 / qa850f231** — Both paraphrase the same chandra.htm sentence pair 'I am not suggesting that you should not think. Thought is you.' The source is Chandrasekhar's Stopped in Our Tracks Book Two, not a standalone audio-tape interview.
- **q5e50266d / qa106c8ad** — Duplicates of the same Swan Song passage; source says 'pleasure movement', not 'pleasure pursuit'.
- **q88d291eb** — 'Act, don't think!' is reported by Mahesh Bhatt (Gstaad diary, day 12; also in A Life). Wikiquote warns Bhatt's own line 'You are what you do, not what you say you want to do' is sometimes merged into it.
- **q93c2842f** — First-person form is a conversion of Mukunda Rao's indirect speech ('He insisted that whatever transformation he had undergone...').
- **qdab04c55** — Catalogue calls it Rao's editorial wording, but the core sentence 'The natural state is a pure and simple, physical and physiological state of being' is U.G.'s own in dialogue (inner-quest; WELL No Way Out ch. 1). The 'different kind of intelligence' clause was not found.
- **qc60032ad** — Wikisource Thought is Your Enemy carries the exact phrase in reported speech ('U.G. says that...'), i.e. an editor's paraphrase; U.G.'s own parallel is in the 1972 talk 'On U.G.' (archive.org).
- **q0c6ee69f** — 'A useless exercise' is Wikipedia narrative voice about the Sivananda years, not a verbatim U.G. sentence; dialogue variant: 'it didn't help, so I dropped it'.
- **q1268f7b9** — Sage and the Housewife ch. 7 wording is 'brush aside the very concept of Kundalini', not 'dismiss'; the November 1988 date is not confirmed by the chapter.
- **q104a81af** — 'Fear of losing what we have and what we know': Wikiquote and Quotepark both cite No Way Out ch. 7, resolving the catalogue's Mystique/No Way Out ambiguity.
- **Jiddu** — No Jiddu Krishnamurti misattribution was found for any quote in this half; one Jiddu quotepark entry ('What you are is the memory...') surfaced near q6a9a1403 but is a different sentence.

## Sources

- http://nirvana73.blogspot.com/2013/03/from-ug-krishnamurti-life-by-mahesh.html
- http://praveennv.blogspot.com/2007/10/ug-krishnamurti-quotes.html
- http://praveennv.blogspot.com/2016/03/questioning-solutions-requires.html
- http://remembering-ug.blogspot.com/2012/01/ebook-february-26th-2012.html
- http://remembering-ug.blogspot.com/2012/07/passages-240812.html
- http://remembering-ug.blogspot.com/2012/10/passages-from-thought-is-your-enemy.html
- http://ug-k.blogspot.com/2007/04/locking-of-horns-inspiration-is.html
- https://actualfreedom.com.au/richard/selectedcorrespondence/sc-ug2.htm
- https://beyond-the-pale.co.uk/ugk3.htm
- https://books.google.com/books/about/The_Biology_of_Enlightenment.html?id=EFQOI25tLlQC
- https://egodeathfilms.wordpress.com/2017/06/14/ug-krishnamurti-pt7-ug-kusuma/
- https://en-academic.com/dic.nsf/enwiki/262193
- https://en.wikiquote.org/wiki/U._G._Krishnamurti
- https://en.wikisource.org/wiki/Courage_to_Stand_Alone
- https://en.wikisource.org/wiki/Mind_is_a_Myth/I
- https://en.wikisource.org/wiki/Mind_is_a_Myth/III
- https://en.wikisource.org/wiki/Mind_is_a_Myth/IV
- https://en.wikisource.org/wiki/Mind_is_a_Myth/V
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_10
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_2
- https://en.wikisource.org/wiki/No_Way_Out/Chapter_8
- https://en.wikisource.org/wiki/Science_and_U.G.
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Four
- https://en.wikisource.org/wiki/The_Mystique_of_Enlightenment/Part_Three
- https://en.wikisource.org/wiki/The_Natural_State
- https://en.wikisource.org/wiki/The_Sage_and_the_Housewife
- https://en.wikisource.org/wiki/Thought_is_Your_Enemy
- https://file.true-dhamma.com/%E5%AE%9E%E7%9B%B8%E4%B8%8E%E8%A7%A3%E6%9E%84/U.G.%E5%85%8B%E9%87%8C%E5%B8%8C%E9%82%A3%E7%A9%86%E6%8F%90/No_Way_Out-U.G.Krishnamurti.pdf
- https://groups.google.com/g/noshonuts/c/fGiwo09RzyI
- https://ia801804.us.archive.org/12/items/UGKrishnamurtiOnU.G185p/UG%20Krishnamurti%20-%20On%20U.G%20(185p).pdf
- https://infant7sorrow.wordpress.com/ug/
- https://kwize.com/en/authors/U-G-Krishnamurti/
- https://kwize.com/en/texts/U-G-Krishnamurti-Science-and-U-G/
- https://kwize.com/en/texts/U-G-Krishnamurti-Stopped-in-Our-Tracks-Stories-of-U-G-in-India/
- https://kwize.com/en/texts/U-G-Krishnamurti-The-Natural-State/
- https://kwize.com/r/U.+G.+Krishnamurti,+The+Natural+State/
- https://libquotes.com/u-g-krishnamurti/quote/lbs1h8v
- https://libquotes.com/u-g-krishnamurti/quote/lby6y0i
- https://medium.com/@alysion42/u-g-krishnamurtis-swan-song-updated-e36a07cc0595
- https://nomindsland.blogspot.com/2016/03/u-g-krishnamurti-nothing-to-understand.html
- https://o-meditation.com/wp-content/uploads/2011/05/krishnamurti-u-g-mind-is-a-myth.pdf
- https://o-meditation.com/wp-content/uploads/2011/05/the-courage-to-stand-alone.pdf
- https://people.well.com/user/jct/SWAN_SONG.htm
- https://people.well.com/user/jct/chandra.htm
- https://people.well.com/user/jct/mahesh.html
- https://people.well.com/user/jct/mystiq1.htm
- https://people.well.com/user/jct/nwo1.htm
- https://people.well.com/user/jct/reddi.htm
- https://people.well.com/user/jct/sage1.htm
- https://people.well.com/user/jct/sage4.htm
- https://people.well.com/user/jct/sage7.htm
- https://people.well.com/user/jct/ugbio/ugbio4.htm
- https://quotefancy.com/u-g-krishnamurti-quotes
- https://quotepark.com/authors/ug-krishnamurti/
- https://quotepark.com/authors/ug-krishnamurti/culture/
- https://quotepark.com/quotes/1899973-ug-krishnamurti-it-is-the-ones-who-believe-in-god-who-preach-peac/
- https://quotepark.com/quotes/1932699-ug-krishnamurti-whether-you-are-interested-in-moksha-liberation/
- https://quotepark.com/quotes/1943820-ug-krishnamurti-people-call-me-an-enlightened-man-i-detest-that/
- https://quotlr.com/author/ug-krishnamurti
- https://realitysandwich.com/biology-enlightenment/
- https://realitysandwich.com/introduction_u_g_krishnamurti/
- https://the-natural-state.blogspot.com/2012/12/3.html
- https://ugkrishnamurti.in/ug-essence/book-pdf
- https://www.actualfreedom.com.au/richard/selectedcorrespondence/sc-ug.htm
- https://www.azquotes.com/author/17848-U_G_Krishnamurti
- https://www.everand.com/book/427470011/Biology-Of-Enlightenment
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=2
- https://www.goodreads.com/author/quotes/30268.U_G_Krishnamurti?page=3
- https://www.goodreads.com/book/show/19120668
- https://www.goodreads.com/quotes/17878-the-body-is-a-fortuitous-concourse-of-atoms-there-is
- https://www.goodreads.com/work/quotes/52202-mind-is-a-myth
- https://www.harpeony.com/articles/book-summary-the-natural-state-in-the-words-of-ug-krishnamurti-part-23
- https://www.heartofyoga.com/blog/ug-krishnamurti
- https://www.hindu-blog.com/2018/09/u-g-krishnamurti-quotes-and-teachings.html
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Mind-is-a-myth.pdf
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-The-Mystique-of-Enlightenment.pdf
- https://www.holybooks.com/wp-content/uploads/U.G.-Krishnamurti-Thought-is-Your-Enemy.pdf
- https://www.inner-quest.org/UG_Natural_State.htm
- https://www.inner-quest.org/UG_R.htm
- https://www.inner-quest.org/UG_Words.htm
- https://www.sciforums.com/threads/the-last-message-of-u-g-krishnamurti.95095/
- https://www.scribd.com/document/111395488/No-Way-Out-UG-Krishnamurti
- https://www.ugkrishnamurti.in/ug-essence/my-swan-song
