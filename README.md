# hanjopurebuddha.com

A guru browsing section. Enlightened people, each with their own words,
their recordings, their films and television, their photographs, their
books and transcripts, the archives and communities around them, and
their life in dates. Every line traced to where it was found.

The first teacher is U.G. Krishnamurti. The structure is made so the
next teacher is added by adding a folder.

## How it is built

```
python3 build.py        # renders site/ from teachers/
```

- `teachers/<slug>/` is one teacher. See `PLAN.md` for what a folder holds
  and how a new teacher is gathered.
- `templates/teacher.html` is the archive viewer every teacher page is
  rendered from, with that teacher's data embedded. It has an Archive tab
  (search, medium, year, language, place, person, host, confidence and tag
  filters, cards or table), a Quotes tab (by book, by confidence, search),
  a Timeline tab (items per year stacked by medium, and the life events),
  a Copyright tab, a Sources tab (every cited URL grouped by host) and an
  About tab.
- `templates/index.html` is the guru grid.
- `site/` is the output. `.github/workflows/publish.yml` builds it on every
  push to `main` and deploys it to GitHub Pages. `CNAME` names the domain.

## Deploying to hanjopurebuddha.com

1. Create the repository (this folder is its whole content) and push.
2. In the repository settings, Pages → Source → GitHub Actions.
3. At the domain's DNS, point `hanjopurebuddha.com` at GitHub Pages
   (A records 185.199.108.153, 185.199.109.153, 185.199.110.153,
   185.199.111.153, and `www` as a CNAME to the GitHub Pages host).
4. Pages → Custom domain → `hanjopurebuddha.com`, then Enforce HTTPS once
   the certificate is issued.

## This folder inside drthomasager.com

It was born inside the drthomasager.com repository because the session
that built it could not create a new repository. It is self-contained.
To lift it out with its history:

```
git subtree split --prefix=hanjopurebuddha.com -b hanjopurebuddha-site
git push <new-remote> hanjopurebuddha-site:main
```
