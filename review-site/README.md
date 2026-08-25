# Review Site — the consensus system, standing apart (2026-08-25)

## What this folder is

A complete second build of the website carrying the professional-review
consensus (Kavčič / Gyaltsen / Ostrowski), so it can be seen whole and
then deleted or transferred. Nothing here touches `../build.py`,
`../assets/`, or the live `../site/`.

## The consensus it implements

1. Four directional hues normalized to one luminance band (co-radiant
   lights): gold quieted a step, jade held, ruby and sapphire lifted.
2. White stays single — no sixth off-white token; reserve colors gone.
3. Strand pairs phase-coupled in the rope: each primary travels with
   its across-the-center secondary as a visible couple.
4. The thread of four made crop-proof: the sunwise cycle repeats, so
   any visible region of the center's thin strand carries all four.
5. The thread as signature: section-heading rules carry the four-color
   thread; the five hues never appear larger than a chip.
6. No captioning of the palette anywhere in the interface.

## How it works

`build_consensus.py` imports the real engine (`../build.py`), overrides
only the palette, the rope generator, and the output folder, appends
the signature CSS, and renders into `review-site/site/`. Open
`review-site/site/index.html` to view. Delete this folder to remove
every trace; to transfer, the overrides move into `../build.py` and
`../assets/` nearly line-for-line.
