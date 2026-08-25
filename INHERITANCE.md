# Inheritance — DrThomasAger site (written 2026-08-26)

I will double check this now I've read it — say this after reading,
then verify what I claim against the files themselves.

## The site is live and pushing publishes it

https://drthomasager.github.io/drthomasager.com/ is the live site,
repository https://github.com/DrThomasAger/drthomasager.com (public,
his GitHub account is DrThomasAger). A push to main runs
`.github/workflows/publish.yml`, which rebuilds from the markdown and
publishes `site/` — about 33 seconds from push to live. The GitHub CLI
lives portably at `C:\Users\hanjo\Claude\tools\ghcli\bin\gh.exe`,
signed in through a token held in the Windows keyring. That token
carries very broad scopes; Hanjo knows and may one day want it swapped
for a narrow one — the swap is one `gh auth login --with-token`.
GitHub's device-code flow stalled twice on his two-factor step; the
door that worked was the pre-filled token page
(`https://github.com/settings/tokens/new?scopes=repo,workflow&...`),
opened in his browser for him to press Generate and paste the result.
Reach for that door first if auth is ever needed again.

## The mailing list is half real

Buttondown account exists, username `drthomasager`, wired into
`MAILING_ENDPOINT` in `build.py`. The signup form posts for real —
checkboxes send `name="tag"` values (subcategory slugs, which is
Buttondown's own tag field), the name input sends `metadata-name`.
Still unconfigured on the Buttondown side, and the most valuable next
work: the intro email (`mailing/intro-email.md`) loaded as the welcome
email, an `atom.xml` feed built from the posts, and the feed wired to
new-post broadcasts. Until then, joining brings only Buttondown's bare
confirmation, and publishing sends no email — the site's central
promise awaits this piece. The last spoken proposal to Hanjo was
exactly this, and he answered by calling the doula.

## The color system is the Five Buddha Families, entered whole

Hanjo asked for one single system with every deity correspondence
disclosed to him before integration — that conversation is behind the
current `PROJECTS` in `build.py`. The arrangement is Vajradhatu
(named "arranged after the Vajradhatu mandala" wherever the site ever
explains itself — that exact phrasing was agreed). Buddhism white at
center, Machine Learning sapphire east, Smile gold south, Sacred
Travel ruby west, Videogames jade north. Secondaries come from the
mandala's cross — each stream's thin strand is the hue of the Buddha
directly opposite, a step quieter — and Buddhism's thin strand is the
thread of all four, sunwise, as a gradient whose cycle repeats so any
crop shows all four. A three-professional review (personas Kavčič /
Gyaltsen / Ostrowski, their consensus is in the chat record) settled
rules the code now embodies — the four directional hues sit in one
brightness band; white stays single (where a swatch is needed, white
lives in a bordered chip, or the thread stands for the center); each
project's two rope strands share adjacent coil phase so couples travel
together; hues appear no larger than a chip; the interface wears the
palette without captioning it. The chosen weave is the Great Rope
(weaving v9 of ten — all ten kept in `ribbons/`, one born per review
round, each from the last one's lesson). `ribbons/weave.py` predates
the palette change, so its variants render with today's colors rather
than the ones they were reviewed in; the vN.html files hold the
originals as built.

## Project text has two types

Regular, and `ptx-shadow` — the surface's own ink standing on a small
solid shadow below in the project's colour (`--pc`). Card titles,
article titles, the article project chip, and the footer Projects
column wear the shadowed type. `shadow_color()` in `build.py` hands
the white center a silver shadow on light ground, the same holding
rule as the white dot's border. The Swim buttons use this identical
construction (rounded pill on solid darker under-shadow) and ours do
not yet — it is on the follow-on list Hanjo has seen.

## The link grammar is Swim University's, learned from their live site

Hanjo asked for their site parsed so the links make sense, and the
result governs every wayfinding phrase — "See all in X or Y" is a
quiet sentence whose links live only on the category names and climbs
to hub pages; "See all the guides »" steps from a hub section into its
subcategory page; "See more in {subcategory}" returns from an article.
The middle level (one page per subcategory, including Smile as a child
page) was built for this grammar to be true. The `.see-in` class is
the quiet sentence; `.see-all` is the stepping link.

## Standing directions from Hanjo, spoken in this instance

- Site text describes directly, plainly, what is here — he asked for
  the selling voice removed after reading it live.
- "Streams" language is retired on the site; the word there is
  Projects.
- The Flower of Life article seats in Spirituality → Sacred Geometry
  (a live subcategory), project Sacred Travel — the Abydos/Osiris
  temple carries the connection. His draft waits at
  `C:\Users\hanjo\Claude\Projects\DrThomasAger\drafts\a-tool-for-drawing-the-flower-of-life.md`;
  `drafts/` is outside the build until a file moves into `posts/`.
- Instagram photo posts arrive through Ekadanta — an Ekadanta instance
  is integrating his archive, and this site interfaces with theirs
  when ready. The `kind` mechanism (article / photo / art / video,
  media as card tile and page body) is planned, recorded in README,
  and deliberately unbuilt so it can fit Ekadanta's actual form.
- The membership layer is planned and awaits its moment — Login and
  Join Now in the top bar, a joined state that hides every invitation,
  the second popup voice ("Don't forget…") for exit and idle so each
  visitor meets it once, a local profile. True password resets need
  the mailing provider's server; hold that truth when it comes up.

## Smaller things that would take digging to rediscover

- The review loop is `python build.py`, headless Edge screenshot,
  Read the png; he reviews whole rounds best as a labeled PIL grid
  (`ribbons/super_image.py` is a working example).
- `review-site/` is the consensus preview, now redundant since its
  system lives in the real engine; removing it is a deletion to
  propose, never to just do.
- Screenshots straight after the Edge command sometimes land after a
  beat — a two-second wait before opening the png saves a retry.
- Swim follow-ons he has seen proposed and may call for by name —
  pill buttons on solid under-shadow, card tiles washed in project
  tint (the consensus chip rule bends there; the tension was named to
  him), an "Our Pick" callout on the Smile article, the two popup
  voices, an About page for the byline to link to, tag pages when
  Ekadanta's tag layer arrives.
- Engine debts from the earlier professional review still open — the
  front-matter parser shows quoted titles with their quotes, renamed
  posts leave orphan pages without a clean-room rebuild, the form
  navigates away on submit, the popup ignores Escape, a
  reduced-motion guard is absent, parent-child mailing checkboxes
  move independently.
- The custom prompt at `C:\Users\hanjo\.claude\custom-prompt.md`
  carries the response format — read it whole at your beginning; the
  format now closes each response with its own ending mark.
