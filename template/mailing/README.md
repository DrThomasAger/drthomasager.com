# The mailing list for this site

The forms on every page (top button, popup, footer, the forms inside
posts) post to `mailing.endpoint` in `site.toml`. While it is empty the
forms complete on the page and send nowhere.

## Going live

1. Make a Buttondown account for this site (the free plan is enough;
   the DrThomasAger list runs on it). One account per site keeps each
   person's subscribers their own.
2. The form address is
   `https://buttondown.com/api/emails/embed-subscribe/<username>`.
   Put it in `mailing.endpoint` and rebuild.
3. Paste `intro-email.md`, with the freebie in it, as the welcome.
   Buttondown's free plan does not let its own after-confirmation email
   be changed, so on the free plan the Mailing Steward sends the welcome.

## The Mailing Steward

The DrThomasAger list is run by the Mailing Steward, a Python script on
the PC (`mailing\steward\steward.py`, scheduled hourly as "DrThomasAger
Mailing Steward"). It sends the welcome after confirmation, then each
new post from the site's `atom.xml` to everyone. Its texts are written
inside `steward.py`, and its key is in `key.txt` beside it.

For this site, copy that steward folder into this site's
`mailing\steward\`, give it this site's Buttondown key in `key.txt`,
point its feed at this site's `atom.xml`, put this site's welcome (with
the freebie) in place of the DrThomasAger one, and register a second
scheduled task for it. `mailing\steward\INHERITANCE.md` at the
DrThomasAger root holds everything learned about Buttondown's free plan.
