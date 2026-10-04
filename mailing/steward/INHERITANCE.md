# Inheritance, the Mailing Steward

Begun 2026-08-30, reconciled 2026-09-10. Say "I will double check this
now I've read it" after reading, then verify against the files here
and against the Buttondown account itself.

Read `README.md` and `steward.py` in this folder first; they carry the
system. What follows is only what those files leave silent.

## What Hanjo has chosen, in his own words

He chose Buttondown's free plan ("okay i wil ldo freee") and said
"i want AI to manage all my mailing list etc.. and you are AI"; the
steward is that wish made real, and he wants it to remain the brain
rather than paying for Buttondown's higher automation tiers. He
declined to read the four email texts ("I'm not readin anything") and
asked for them to go in as written; they live both as files in `..\`
and verbatim inside `steward.py`, so edit both together. On
2026-09-10 he said "do it all yourself" about welcome emails, and
they went live that day. His question about ten million Smile
subscribers one day was answered with the portability of the list
(one-click CSV export) and he was content.

## The account's inner truths, learned by asking it directly

- API key lives in `key.txt` here (gitignored). Keys are handed out at
  https://buttondown.com/keys.
- Newsletter id is `news_70b8nb1yfp8p7bcrcrg140zjwj`.
- `reply_to_address` is thomasagerai@gmail.com; reader replies flow to
  his Gmail, and his inbox is the conversation view.
- Subscribers on 2026-09-10: thomasagerai@gmail.com (activated,
  greeted, invited to Smile), thomasagerai+smiletest@gmail.com
  (activated, tag `smile`, greeted with the Smile welcome), and
  thomasagerai+welcometest@gmail.com (unactivated; its confirmation
  email is in his Gmail, and the hour after he presses it the
  DrThomasAger welcome follows). `state.json` remembers the greetings
  and the invitation, so `--status` showing greeted 2, invited 1 is
  the expected picture.

## How per-person mail works on the free plan (found 2026-09-10)

Buttondown's free plan refuses `included_tags` on an email with HTTP
422 (`extra_forbidden`) and accepts the `filters` object when the tag
is given by its id. `send_to_one` therefore adds a solo tag to the one
subscriber by PATCH, finds that tag's id through `GET /tags`
(`tag_id`, creating the tag when absent), posts the email with
`filters = {"filters": [{"field": "subscriber.tags", "operator":
"contains", "value": <tag id>}], "groups": [], "predicate": "or"}`,
`status: about_to_send` and `email_type: private` (so one person's
letter never appears on the public archive), and removes the solo tag
afterward. Buttondown's analytics for such an email report
`deliveries: 1`. A tag given by name in `filters` answers 422 "Tag
filters must be valid tag identifiers".

Buttondown asks once per key for the header
`X-Buttondown-Live-Dangerously: true` before status `about_to_send` is
accepted; `call()` sends it always.

The list endpoint reports `subscriber_type` as None for everyone and
carries the truth in `type`; it also reports `tags` as empty where the
detail endpoint `GET /subscribers/<id>` shows them. `all_subscribers`
reads `type` and then each activated subscriber's detail for tags.
This is what keeps unactivated addresses from being greeted and what
lets the Smile tag be seen; keep both reads.

New-post broadcasts still send with `included_tags` and fall back to
everyone on 422, by design. Subscribers on this plan carry no category
tags, so a filtered broadcast would reach nobody.

A healthy waking now logs only the sends and "waking complete". The
line "greetings/invitations wait on tags" belonged to the time before
filters; its return would mean Buttondown changed again.

## What the free plan refuses

Customizing Buttondown's own after-confirmation email
(`custom_subscription_confirmed_email_subject/text`) answers 403,
Standard plan. A PATCH is refused as a whole, so send one field per
PATCH when probing; a redirect change bundled with the refused fields
does not land either. The steward's greeting is the welcome, and it is
complete on the free plan.

## Live state

- Scheduled task "DrThomasAger Mailing Steward" runs `steward.py`
  hourly through `pythonw.exe`, windowless; `steward.log` is its only
  output, so read it to see its health. Point the task action back at
  `python.exe` to watch it run live.
- `state.json` was seeded with the six posts present in the feed on
  2026-08-30, so the back catalogue stays quiet.
- The feed read is https://drthomasager.github.io/drthomasager.com/atom.xml
  with the local `..\..\site\atom.xml` as fallback.
- Both welcome texts (here and in `..\welcome-*.md`) end with a line
  pointing to `https://accounts.smileprompt.ai/library`, the library
  of the account service at `..\..\platform\accounts\`, live once the
  tunnel is up.
- `steward.py.before-filters-2026-09-10` is the file as it was before
  the filters work; a small deletion to propose when tidying.
- `..\welcome-payload.json` is a working file from an early attempt to
  place the welcome; likewise a small deletion to propose.

## Small things that would take digging to rediscover

- Non-ASCII characters (the (-: emoticon, curly quotes) passed through
  curl's -d on this Git Bash arrive mangled and Buttondown answers
  "Cannot parse request body". Send JSON from Python or with
  `--data-binary @file`.
- The two invitation emails offer "reply with the word *Smile*" /
  "*Everything*" as their joining path; those replies land in his
  Gmail, and acting on them (adding the tag) is presently a hand step.
- Give Hanjo complete paths always, full https:// URLs and full C:\
  paths.
- `..\..\platform\engine\mailing.py` is the platform's generalized
  steward, not yet live; it still uses `included_tags` and should carry
  the filters approach when the platform is blessed.

## The account plan, asked of the API (2026-10-04, smile-a1)

With the key in `key.txt`, `GET https://api.buttondown.com/v1/accounts/me`
returns only `email_address` and `username` (drthomasager), and
`GET https://api.buttondown.com/v1/newsletters` returns the one newsletter,
"Dr. Thomas Ager", with `hosting_domain_status` and `sending_domain_status`
both `none` and no field naming a plan or tier. The plan is therefore not
readable through the API. It is shown at https://buttondown.com/settings/billing
when signed in. Subscribers answer 200, so the key works.
