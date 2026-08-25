# Mailing list — the full picture

The site's forms (hero, popup) are fully built and collect: name, email,
and category interests from the advanced dropdown. They POST to the
endpoint named at the top of `build.py` (`MAILING_ENDPOINT`). Until a
provider account exists, that endpoint is a placeholder and the form
completes locally with a welcome message.

## What the provider is configured to do (once chosen)

1. **Double opt-in** — a confirmation email on signup, then the intro
   email in `intro-email.md` sends automatically as the welcome message.
2. **Auto-subscription to all future posts** — every new post published
   triggers a broadcast (via the provider's RSS-to-email automation
   pointed at the site's feed, or a manual send). Subscribers receive
   everything by default.
3. **Category selection** — the dropdown's checkbox values
   (`prompt-engineering`, `prompt-language-development`, `free-prompts`,
   `tutorial`, `spirituality`, `songs-of-enlightenment`, `commentaries`)
   map to provider tags. Broadcasts are sent per-tag so subscribers who
   narrowed their choice receive only their categories.

## What is needed to go live

- A provider account (Buttondown, ConvertKit/Kit, or Mailchimp all
  support tags + RSS automation + welcome emails).
- Paste its form endpoint into `MAILING_ENDPOINT` in `build.py`, rebuild.
- Paste `intro-email.md` into the provider's welcome automation.
