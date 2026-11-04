# Editing and recomposing

Every teacher's site carries two working pages beside its archive, and the
same recompositions reach Claude Code, the Pi CLI and THE MAP Viewer's
composer as /C- commands.

## Edit

`gurus/<slug>/edit/` lists every quote, archive item, life event and person,
and the page details (name, dates, lead quote, portrait, Instagram handle,
accent colour, display font, copyright position). Change a field, add a
record, or remove one, and the change collects in the browser as one file,
`edits.json`. Copy it, open `teachers/<slug>/edits.json` on GitHub from the
page's button, paste it over the old text and commit. The site rebuilds and
applies the edits on top of the gathered data.

Edits sit in their own file so a later research merge (`merge.py`, which
rebuilds `quotes.json` and `items.json` from the researchers' files in
`raw/`) never overwrites a hand change. Every other file is text and can be
edited on GitHub directly as well: `meta.json`, `timeline.md`,
`copyright-view.md`, the catalogue reports, `corrections.json`, the
compositions, and every Smile module under `smile/`.

## A recomposition is a Smile composition

The archive is Smile raw text. Each verified quotation is one line,

```
[q4f2c81d1] (Mind is a Myth, Ch. V We Have Created This Jungle Society; corroborated-primary) the very birth of thought creates fear
```

and a recomposition is a composition the way THE MAP Viewer's composer
makes one, inside the Smile Prompt Language header and footer, each module
indented four spaces and the words given in faces of their own.

| Module | File | What it carries |
|---|---|---|
| The rules | `smile/rules/The quotations kept exactly.smile` | every quotation word for word, cuts marked, sources kept, ids listed |
| The rights | `smile/rules/Words released.smile`, `smile/rules/Words under copyright.smile` | full quotation for released words; for reserved words, no quotation over 50 words and a budget per piece |
| The form | `smile/forms/<form>.smile` | what the piece is and how its reply is laid out |
| What the form gathers | `smile/styles/*.txt`, `smile/forms/C-blog, edition 1.md` | a Suno style, Hanjo's /C-blog |
| The words given | the quotations, the extra asking | raw text, in faces |

The forms, all in `formats.json` and each a .smile file to edit.

| Form | id | What it makes |
|---|---|---|
| Suno song | `suno` | lyrics up to 5,000 characters in Suno lens tags, and a style up to 1,000, made from the teacher's lines with every added line declared |
| Collection on a topic | `collection` | an anthology excerpt, quotations in order under a few headings |
| Book with chapters | `book` | title, contents, preface, six to twelve chapters, afterword, sources |
| Blog post | `blog` | a drthomasager.com post through /C-blog, with its front matter, ready for `posts/` |
| Instagram post | `instagram` | one quotation, a caption, the link to the quote's page, hashtags |
| Custom | `custom` | whatever the extra asking says |

When the Smile library is on the machine (`SMILE_HOME`, or
`~/Claude/Projects/Smile`), the Suno styles come live from
`Smile Prompt Language/Lenses/Suno/styles` and /C-blog from
`~/.claude/commands/C-blog.md`, so a change there reaches every
recomposition at once. Without it the copies in `smile/` are used, and
those copies are what the public compose page carries.

## From any project, any CLI

```
python hanjopurebuddha.com/smile/install.py
```

writes `/C-guru`, `/C-guru-suno`, `/C-guru-collection`, `/C-guru-book`,
`/C-guru-blog` and `/C-guru-instagram` into `~/.claude/commands` with this
folder's path written in. From then on, in every project,

```
/C-guru-suno ug fear death
/C-guru-book bernadette silence
/C-guru-blog ug the body
/C-guru ug fear                  the quotations as Smile raw text, for the work at hand
```

Claude Code runs the composition and writes the piece, then keeps it in
`teachers/<slug>/compositions/` (blog posts in `posts/`). install.py then
rebuilds Pi's prompt templates through Pi Integration, so the same commands
run in Pi, and THE MAP Viewer's composer lists every C- command, so they
appear in its module list at its next /modules call, to be composed with
any other module. The repository's own `.claude/commands` carry the same
commands for a session working here. Run install.py again after a command
changes.

The commands call `recompose.py`, which works without any of them.

```
python recompose.py teachers
python recompose.py styles
python recompose.py quotes  ug fear death                  # the quotations as Smile raw text
python recompose.py compose --format suno ug fear death    # the composition, for the instance reading it
python recompose.py write   --format book bernadette silence   # composed and written through the API
python recompose.py save    --format suno ug --topic "fear death" --file song.md
```

Teachers are named loosely (ug, UG Krishnamurti, bernadette, roberts). The
options are `--style`, `--max`, `--select id,id`, `--book "<title>"`,
`--include-single`, `--extra "<asking>"`, `--model`, `--to-posts`. compose
needs nothing; write needs `ANTHROPIC_API_KEY`.

## On the site

`gurus/<slug>/compose/` makes the same composition word for word, from
`smilecompose.py` on the command line and its JavaScript mirror on the page.
Choose a form, a style for a song, a topic, or quotes picked one by one on
the quotes page (each quote has a select button). The quotations gathered
leave out anything disputed, not found, not the teacher's words, or a
paraphrase, and by default anything that rests on a single source.

The composition appears rendered and writable. Change a quotation's words
inside the render and the page notices it: keep the change in this
composition only (it travels in the composition's front matter as
`overrides`), or write it into the quote itself through the editor's
`edits.json`, so every composition and the site carry it.

Then copy the composition into any Claude or Pi, or paste an Anthropic API
key and press Compose with Claude: the key goes only from the browser to
api.anthropic.com and can be remembered on that device. A Suno song shows
its lyrics and style counts against 5,000 and 1,000, with a copy button for
each. The result can be kept in the browser, downloaded as markdown, or
added to the site: the button opens GitHub with the file named (and filled
in, when it is short enough) under `teachers/<slug>/compositions/`. Commit
it and it becomes its own page, listed on the teacher's home. Blog posts get
a second button that opens a new file in `posts/` instead.

`teachers/ug-krishnamurti/compositions/2026-11-04-collection-born-of-fear.md`
is a first example.
