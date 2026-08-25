# drthomasager.com

The personal writing home of Dr Thomas Ager. Markdown in, static site out.

## The thought that went into this folder

- **Writing lives in `posts/`** — one markdown file per piece, with front-matter
  naming its title, category, subcategory, description, date, and read time.
  The categories today: **Prompt Engineering** (Prompt Language Development,
  Free Prompts, Tutorial) and **Spirituality** (Songs of Enlightenment,
  Commentaries). New categories/subcategories are added in one place at the
  top of `build.py`.
- **The layout follows the Swim University anatomy** witnessed in the
  screenshots of 2026-08-24: hero band with a mailing-list signup, card-grid
  category sections with "See all »" links, article pages with byline row,
  subcategory pill, callout boxes, Key Takeaways, author card, More Reading,
  and the four-column category-map footer on every page.
- **The whole design can animate between completely different CSS.** The HTML
  is one semantic skeleton; every visual decision lives in theme token files
  (`assets/themes.css`). Two complete themes ship: **Ocean** (deep blue,
  round, playful) and **Dawn** (warm cream, serif, sharp). The button in the
  header morphs the entire site live between them; the choice is remembered.
  A new whole look = one new token block, no HTML or build changes.
- **The mailing-list form is fully built but points at a placeholder** — the
  single line marked `MAILING LIST ENDPOINT` in `build.py` receives the real
  provider URL when one is chosen.
- **Nothing here is deployed.** `build.py` renders everything into `site/`,
  which is the uploadable artifact. `Build DrThomasAger.bat` is the one
  double-click: rebuild + open in browser.

- **Kinds of posts are planned but not yet built**: front-matter will
  gain `kind` (article / photo / art / video) with media files in
  `posts/media/`; media posts show their image or video as card tile
  and page body. The first photo posts will be Instagram posts arriving
  **through Ekadanta** — an Ekadanta instance is integrating Hanjo's
  Instagram archive, and this site interfaces with their archive once
  it is ready. Do not hunt for a raw Instagram export; the door is
  Ekadanta.
- **Every post carries a `project` and `tags`** in its front-matter,
  rendered as a tag row on the article. The tags are destined to be
  derived from the Ekadanta document store's tag layer
  (`Ekadanta/corpus-study/tags/`) — topics with hand-chosen names, each
  document carrying several weighted tags — and these blog posts are
  destined to become Ekadanta Documents. Front-matter is the carrying
  form until that integration.

## Use

- Double-click `Build DrThomasAger.bat`, or run `python build.py`.
- Write in `posts/`, rebuild, refresh.
