# The template — making another site like DrThomasAger

Everything that makes drthomasager.com one person's site lives in one
file, `site.toml`. `build.py` is the engine and holds none of it. Any
person's site is the engine and their own `site.toml`, posts, freebie
and mailing texts. The first copy is Ananda's, **The New Body: EDS
Insight with Ananda Purebuddha**, in `sites/the-new-body/`, whose freebie
is **The Ultimate Supplement Stack**.

Proof the split holds: after the change, `python build.py` writes every
file of the DrThomasAger `site/` byte for byte as before, except one line
of `assets/site.js` that lets a site give its own thank-you text.

## The three commands

```
python build.py                                   the DrThomasAger site, as always
python build.py --new sites/<name>                copy template/ to start a new site
python build.py sites/<name>                      build that site into sites/<name>/site/
python build.py --export sites/<name> <folder>    write that site as its own repository
```

On the PC, `Build a Site.bat` builds and opens a site: drag the site's
folder onto it, or double-click it for the DrThomasAger site.

## What a site folder holds

| Path | What it is |
|---|---|
| `site.toml` | The whole site. Name, author, address, tagline, header, categories, project colours and symbols, home page words, popup, footer, shop, freebie, Ghost author. Every key is explained in `template/site.toml`. |
| `posts/` | One markdown file per post. `template/posts/start-here.md` shows every front-matter line. A post with `draft: yes` stays out of the site. |
| `freebie/` | The free thing for joining. The welcome email delivers it, and the engine never publishes it on the site. |
| `mailing/` | The welcome email and how to connect the mailing list, in `mailing/README.md`. |
| `site-assets/` | The site's own favicon, stylesheet and images, copied over the engine's `assets/`. |
| `site/` | The built site. Not committed for sites under `sites/`. |

## Making a new site, start to finish

1. `python build.py --new sites/<name>`.
2. Fill in `sites/<name>/site.toml`. The categories decide the posts'
   `subcategory:` lines, so name them first.
3. Write the freebie in `freebie/` and the welcome in `mailing/intro-email.md`.
4. `python build.py sites/<name>` and open `sites/<name>/site/index.html`.
5. Mailing list: a Buttondown account of the site's own, its form address
   in `mailing.endpoint`, and the Mailing Steward as `mailing/README.md`
   says.
6. Publishing: `python build.py --export sites/<name> <folder>` writes a
   folder that is a whole repository on its own, the engine with the
   site's files at its root. Make it a new GitHub repository, push it,
   and turn on GitHub Pages with source "GitHub Actions". The
   `.github/workflows/publish.yml` it carries builds and publishes on
   every push to main, as drthomasager.com does. Then put the published
   address in `site.url` and push again.

## What the template carries from DrThomasAger

The Swim University anatomy of every page (hero, trust band, feature,
dark mid band with the woven rope, card grids, category and subcategory
pages, articles with byline, tags, author card and More Reading), the
popup at 33 seconds, 55% scroll or exit intent, the signup forms with
interests, the shop and the `[[shop]]` and `[[join: …]]` post blocks, the
Atom feed the Mailing Steward reads, the sitemap and robots.txt,
structured data on every page, the Buddha eyes in the footer, the Blog
Template with the gold letterhead in `assets/blog/`, and the Ghost export
in `tools/ghost_one.py`, which reads its author from the site's
`[ghost]` table: `python tools/ghost_one.py sites/<name>/posts/<post>.md sites/<name>`.

## What stays on the PC

These were never in the repository, so a new site's copy of them is
made there.

- **The Mailing Steward**, `mailing\steward\steward.py`, its `key.txt`
  and its scheduled task. Its welcome texts are written inside
  `steward.py`. A second site needs a copy of the steward folder with
  its own Buttondown key, its own feed address, its own welcome with
  the freebie, and a second scheduled task. `mailing/README.md` in the
  template says the same.
- **The account service and library** in `platform\accounts\`, if the
  site is to have sign-in and a library of what a person has unlocked.
- **The ontology and explore page** (`ontology/`) are DrThomasAger's own
  tree. A new site starts without them.
