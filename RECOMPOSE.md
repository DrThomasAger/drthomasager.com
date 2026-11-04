# Editing and recomposing

Every teacher's site carries two working pages beside its archive.

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
`raw/`) never overwrites a hand change. Every other file is plain text and
can be edited on GitHub directly as well: `meta.json`, `timeline.md`,
`copyright-view.md`, the catalogue reports, `corrections.json`, and the
compositions.

## Compose

`gurus/<slug>/compose/` turns the verified quotations into a new piece. The
forms come from `formats.json` at the site root and can be edited there.

| Form | What it makes |
|---|---|
| 5,000 characters | one continuous reading of about 5,000 characters on a topic |
| Song | verses and a chorus made from the teacher's lines, with every added line declared |
| Collection on a topic | an anthology excerpt, quotations in order under a few headings |
| Book with chapters | title, contents, preface, six to twelve chapters, afterword, sources |
| Blog post | a drthomasager.com post with its front matter, ready for `posts/` |
| Instagram post | one quotation, a caption, the link to the quote's page, hashtags |
| Custom | whatever you write in Extra instructions |

Choose a form, a topic, or quotes picked one by one on the quotes page (each
quote has a select button). The page gathers the matching quotations,
leaving out anything disputed, not found, not the teacher's words, or a
paraphrase, and by default anything that rests on a single source. It
writes the whole prompt with the rules that keep every quotation exact,
attributed and listed by id at the end.

Then either copy the prompt into any Claude chat, or paste an Anthropic API
key and press Compose with Claude: the key goes only from the browser to
api.anthropic.com and can be remembered on that device. The result appears
in an editable box. Keep it in the browser, download it as markdown, or add
it to the site: the button opens GitHub with the file named (and filled in,
when it is short enough) under `teachers/<slug>/compositions/`. Commit it and
it becomes its own page, listed on the teacher's home. Blog posts get a
second button that opens a new file in `posts/` instead.

Teachers whose words are under ordinary copyright (`"rights": "reserved"` in
`meta.json`, as for Bernadette Roberts) get the brief-quotation forms: no
quotation over 50 words, a word budget per piece, and the writing mostly in
Claude's own words as commentary or study.

## From the command line

```
python3 recompose.py ug-krishnamurti --format song --topic "fear death"
python3 recompose.py ug-krishnamurti --format book --topic thought --max 150
python3 recompose.py bernadette-roberts --format blog --topic silence --to-posts
python3 recompose.py ug-krishnamurti --format collection --topic body --prompt-only
```

The same forms, the same quotation choice and the same prompt as the page.
It needs `ANTHROPIC_API_KEY` unless `--prompt-only`, streams the piece as it
is written, and saves it into `compositions/` (or `posts/` with
`--to-posts`). `teachers/ug-krishnamurti/compositions/2026-11-04-collection-born-of-fear.md`
is a first example.
