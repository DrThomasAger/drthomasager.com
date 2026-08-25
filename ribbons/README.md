# Ribbons — ten weavings (begun 2026-08-25)

## What this folder is

Ten extremely different rainbow ribbon weavings for the drthomasager.com
hero and dark bands, made one at a time, each reviewed by eye before the
next is conceived. Each version seeks what Christopher Alexander called
**local symmetries** — small centers of mirrored beauty that strengthen
each other — with ribbons weaving in and out of one another, opacity
where they overlap forming larger structures and symmetries.

## Assumptions and thoughts that went into this

- The five streams and their colors/symbols come from `PROJECTS` in
  `../build.py` — that stays the single source of truth.
- Each version is a full-page preview (`vN.html`) rendered through the
  real site page shell, so what is reviewed is what the site would be.
- Screenshots land in `../shots/ribbon-vN.png`.
- All ten versions are kept; Hanjo decides when the ten are done and
  which weaving (or weavings) the site itself wears.
- `weave.py` holds one generator function per version, grown one at a
  time — each new version born from what the last one's review taught.
- Nothing here changes the live `site/` output until chosen.
