# Connection, DrThomasAger site

For instances in other projects who want something from this one.

This project is Hanjo's personal site, drthomasager.com, built by
`build.py` from markdown in `posts\` into `site\`, published live by
a push to main, together with the platform under `platform\` that
builds both the drthomasager site and the smileprompt site and runs
the shared account service. Its full inner knowledge is in
`INHERITANCE.md` beside this file.

What another project might draw from here, and where in
INHERITANCE.md it lives.

- **Publishing pipeline** ("The site is live and pushing publishes
  it"), the GitHub repo, the workflow, the portable gh CLI at
  `C:\Users\hanjo\Claude\tools\ghcli\bin\gh.exe`, and the token page
  that works for Hanjo's account.
- **Mailing** ("The mailing list, as it truly works"), Buttondown
  wiring and the hourly Mailing Steward, with per-person welcomes live
  on the free plan. The deep record, including how sending to one
  person works on the free plan, is at
  `mailing\steward\INHERITANCE.md`.
- **The color system** ("The color system is the Five Buddha
  Families, entered whole"), the Vajradhatu palette, useful to any
  project sharing the family's visual language.
- **Authorship disclosure lines** ("The authorship disclosure
  lines"), Hanjo's families of AI-involvement phrasings for
  automatically created posts, relevant to any project generating
  posts for him.
- **Ekadanta interface** (Standing directions section), how
  Instagram photo posts will arrive here through Ekadanta.
- **Official Smile branding** (Standing directions section), Hanjo's
  verbatim direction that every Smile surface uses the assets in
  `C:\Users\hanjo\Claude\Projects\Smile\Smile Assets\`.
- **Accounts and the library for smileprompt.ai** ("The account
  service and the library"), the email-first sign-up on port 4455,
  Buttondown's confirmation as the verification, the signed-in library
  of shop items with grants and the grant-by-hand command, the greyed
  provider buttons and what wakes them. Smile Chat reads this
  service's `accounts.db`.
- **The move online** ("smileprompt.ai and the move online"), the
  exact inputs awaited and the steps through the Cloudflare tunnel.
- **Agents, the paper and search** ("The agent series and the search
  engine files (2026-09-28)"), the position paper "What is an Agent?"
  with its three authors, the first written definition of agentiality,
  4,276 search phrases about agents gathered from Google and Bing in
  `Agent Collective (AOR 2026-09-28)\keywords\`, the Lighthouse scorer,
  and the five step test from a reachable page to a sign-up. Useful to
  any project that writes about agents or publishes a site.
- **The Reader, in Clojure** ("The Reader, in Clojure (2026-10-02)"),
  everything in `C:\Users\hanjo\Claude\Projects\DrThomasAger\Reader\`.
  A Clojure client for the Edge read-aloud service that returns the time
  of every spoken word (`src\reader\speech.clj`), with the alignment of
  spoken words to page words in `src\reader\build.clj`, useful to
  Mahodara, Smile or any project that wants speech with word timings.
  One word rule shared by the JVM and Scittle (`src\reader\words.cljc`),
  and a check that renders Scittle pages in headless Edge from disk
  (`src\reader\check.clj`). A read-only reader of the account service's
  sessions (`src\reader\prefs.clj`), for any page that wants to know who
  is signed in. Hanjo's interface decisions as they live in Mahodara's
  code, listed in that section.
- **Finding an earlier chat** ("Finding an earlier chat of his"), one
  file with every prompt Hanjo has typed in Claude Code, by project and
  session.

(-: The ontology, for any project writing a post (-:

    ( What to take ( A post anywhere that will appear on drthomasager.com takes its kicker and tags from ontology\ontology.edn. Add the post to ontology\placements.edn, run bb ontology/check.clj from this folder, and put the kicker and BreadcrumbList it prints into the post. ontology\index.json and ontology\ontology.json are the same data for MCPs and pages. Every blog post, and every page that lists or explores posts, wears the Blog Template in C:\Users\hanjo\Claude\Projects\Blog Template\, as ontology\explore.clj does. ) )

:-) End the ontology, for any project writing a post :-) thank you
