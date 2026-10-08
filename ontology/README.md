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

`bb ontology/explore.clj` writes `site\explore.html` in the Blog Template,
`C:\Users\hanjo\Claude\Projects\Blog Template\`, the blog aesthetic made with
Hanjo, like Medium with a rose madder palette. It copies the template's
`blog.css` and `blog.js` into `site\assets\blog\` and writes `index.json` and
`ontology.json` beside the page.

The page is the interface itself. The roots All, AI and Buddhism sit under
the title, then a search, four sorts (newest, measured first, shortest, most
specific) and the count. Places opens the tree with a count at every place,
and Tags opens a chip for every tag in use with the count it would leave. The
posts follow as a reading list, each with its kicker, title, description and
byline. Every view is kept in the address, e.g.
`explore.html#place=ai/agents&evidence=measured`, so a reader can share a view
and an MCP can name one.

`node ontology/shots.mjs` screenshots the page and the template's `sample.html`
at 1440 and 390, light and night, into `shots\`, and reports any sideways
scroll or page error.

Hanjo's words that brought the page to the Blog Template:

> This also is NOT the blog post aesthetic determined with Rose, impersonating Medium. Please identify it and ensure all models know it and it is referred to in /C-explain#

> also dont assert obvious things. show dont tell, the medium is the message

> So none of thisW" Every post lives at one place under AI or Buddhism, and carries its tags. Choose a place, any tags, a sort, or search." just provide the GUI/visualization/interface directly
