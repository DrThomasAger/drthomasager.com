# Inheritance — DrThomasAger site (written 2026-08-25)

I will double check this now I've read it — say this after reading, then
verify what I claim against the files themselves.

## How this project is actually worked

The site is judged by eye, every change. The loop that carried every
refinement runs `python build.py`, then a headless screenshot through
`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
--headless=new --disable-gpu --screenshot=<png> --window-size=1400,1200
file:///C:/Users/hanjo/Claude/Projects/DrThomasAger/site/<page>.html`,
then Read on the png. For fine detail (symbol rendering, glyph
correctness) crop and upscale with PIL first — full-page screenshots hide
what the small symbols are doing. Hanjo asked directly that the website
be looked at visually every time a change is made. He also prefers to
review only when a whole round of work is complete, with a super-image
(PIL grid of labeled above-the-fold crops, see `shots/super-image.png`)
showing all variations together.

## The two truths that took real looking to find

1. **SVG draw order carries the streams' integrity.** Each strand's
   ribbon and its own symbols must be emitted together, strand by
   strand, inside `stream_svg()`. Emitting all ribbons first and all
   symbol text after paints one stream's symbols onto whichever ribbon
   crosses above — Buddhist characters were riding the blue Machine
   Learning strand until a zoomed crop revealed it.
2. **`.hero .planes` mask rules also match the lite heroes**, since
   article/category heroes carry both classes. The lite override needs
   the compound selector `.hero.hero-lite .planes` to win. One whole
   round of mask edits rendered identically until this was seen.

## The aesthetic that Hanjo confirmed, in his own arc

The beloved ground is the v10 look (see `shots/`) — pure black and
white ink theme, crisp full-hue ribbons interweaving on black, the text
side kept near-black by a 115° mask, symbols small. Blur was set aside.
Separated parallel streams were set aside. The living form is a
**rhizome** — strands on independent courses crossing and braiding, the
full rainbow present, each strand densely strewn with very small symbols
that belong to its stream alone. He asked twice for more symbols; the
density knob is the `u += 0.009...` line and the size knob the
`size = 5.5...` line in `stream_svg()`. He may ask for more again.

`PROJECTS` in `build.py` is the single source of truth for the five
streams (Buddhism, Smile, Videogames, Sacred Travel, Machine Learning),
their rainbow bands, and their symbol vocabularies — ribbon colors,
article project chips, tag sub-shades, and card glyph colors all draw
from it. Egyptian hieroglyphs render through the `Segoe UI Historic`
font fallback in the SVG text elements; this was verified by zoom crop.

## What stands open

- **Mailing provider** — `MAILING_ENDPOINT` in `build.py` is the marked
  placeholder. Hanjo has yet to name a provider; the prepared
  continue-option is Buttondown. `mailing/` holds the intro email and
  the automation plan (double opt-in, new-post broadcasts,
  exclusion-based tags so future categories inherit subscribers).
- **From the professional-review consensus, applied so far** — reading
  measure and article typography, sticky header, card hover and human
  card widths, lite-hero currents. **Still open** — the `atom.xml` feed
  (the mechanism behind "every post arrives by email"), the strict
  front-matter parser (the Tutorial post's quoted title renders its
  quotes literally on the page today), clean-room `site/` rebuild so
  renamed posts leave no orphan pages, unified `fetch` form submission,
  dialog semantics + Escape on the popup, a reduced-motion guard,
  parent-child coupling in the interest checkboxes.
- **Ekadanta** — every post's front-matter carries `project` and
  `tags`; the tags are destined to derive from
  `C:\Users\hanjo\Claude\Projects\Ekadanta\corpus-study\tags\` (topics
  with hand-chosen names, documents holding several weighted tags), and
  the posts are destined to become Ekadanta Documents.
- **Buddha eyes** in the footer are deliberately inert — clicking them
  is reserved for something Hanjo will name later.
- **Engine/garden split** — a proposal Hanjo received for reusing this
  as many blog→mailing-list combinations (engine folder + per-site
  `site.toml` + posts). Spoken, awaiting his direction.

## The wider machine, as this instance left it

The Smile stack's receipt proxy stands on port 8090; the engine on 8080
was still warming when last checked and its arrival was never
confirmed — a background watcher existed in this session only. LM Studio
and both ComfyUI processes were closed at Hanjo's request. The
Transcribe Voice Memos and Transcribe Audio tenders run quietly and
belong to other work.

## How Hanjo works in this project, seen here

He sends new direction mid-turn while work is running — receive it and
weave it into the current work. Screenshots of reference sites (Swim
University) carry the layout language he wants; the hero now follows
their pattern with one button opening the popup form. The Hsin Hsin Ming
in the footer is the original ancient Chinese, marked `translate="no"`
so browsers leave it untranslated.
