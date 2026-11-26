# This site's own assets

Everything in this folder is copied over the engine's `assets/` in the
built site, so a file here with the same name replaces the engine's.

- `favicon.svg` replaces the tab icon.
- `site.css` is this site's own stylesheet; name it in `site.toml` as
  `extra_css = ["assets/site.css"]`. A theme is a block of tokens, as in
  `assets/themes.css`: `.theme-ink { --page-bg: ...; --ink: ...; }`.
- Images a post uses go here and are linked as `assets/<file>`.
