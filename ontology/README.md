# The DrThomasAger ontology

Where every post lives, and the tags it is found by. Readers use it to search,
sort and filter, and MCPs parse it from `index.json` and `ontology.json`.

## Hanjo's words, as he typed them

> "AI Friends · a trial with every number" this is a bad ontology. update all blog making commands, advice, prompts etc so that yu write these as avalid hierarchjy with an agent reviewer LLM

> "Ganapati · the Dharma Wheel" is also horrible. there are 2 main blog categories, spirituality/buddhism and technology/AI. that is always the first category, then we need extremely meaningful, granular, specific tagging system, sorting system, filtering system, as well as intensely accurate to the DrThomasAger lens and magnification on all of the sub hierarchy categories as people will be using this as UX to search and use MCPs/parse the website.

## The files

- `ontology.edn` is the tree, two roots, AI (Technology) and Buddhism
  (Spirituality), then field, subject and project, each node with a
  definition. Beside the tree are eight facet vocabularies (format, model,
  tool, method, project, practice, level, evidence) and the sort orders.
- `placements.edn` gives every post its one place and its facets.
- `check.clj` checks the tree and every placement and writes `index.json`
  and `ontology.json`. `bb ontology/check.clj <slug>` prints a post's kicker,
  its BreadcrumbList JSON-LD and its tags.
- `reviewer.smile` is the agent reviewer LLM's prompt. It reads a post
  against the ontology and says what is right and what is to change. It runs
  only once Hanjo has read it and written `approved.txt` beside it.

## How a post gets its place

1. Choose the root the whole post is about, AI or Buddhism.
2. Walk down to the most specific node whose definition the whole post fits.
3. The kicker is the route, written with `›` between the steps, e.g.
   `AI › Agents › AI Companions › AI Friends`. It names places and never
   describes the post.
4. Add every true facet value from the vocabularies.
5. Run `bb ontology/check.clj`, then the reviewer.
6. A post that fits no node gets a new node proposed by the reviewer, with its
   parent and a one sentence definition, added to `ontology.edn` by hand.

## Assumptions made while building

- The roots are labelled AI and Buddhism, with Technology and Spirituality as
  their other names, since the site's existing categories already say AI and
  Buddhism.
- The project tier is kept for named bodies of his own work with posts of
  their own, e.g. Smile, Ganapati, AI Friends.
- A post wholly about AI that is built in a Buddhist form lives under AI and
  carries the practice facet, e.g. the Dharma Wheel of Ganapati.
- The site's `build.py` still reads its own `CATEGORIES`. Moving it to read
  `ontology.edn` and drawing the filters from `index.json` is the next step.

## The explore page

`bb ontology/explore.clj` writes `explore.html` here and into `site\`, with
`index.json` and `ontology.json` beside it. It has the tree with a count at
every place, a chip for every tag value in use with the count it would leave,
four sorts (newest, measured first, shortest first, most specific first), and
a search over titles and places. Every view is kept in the address, e.g.
`explore.html#place=ai/agents&evidence=measured`, so a reader can share a
view and an MCP can name one. On a phone the places and tags fold shut, so
the posts come first. It was seen at 1440 and 390 pixels in light and dark,
with no sideways scroll and no page errors.
