# Enquiry Backend — Design Spec

**Date:** 2026-08-10
**Status:** Approved by user

## Overview

The enquiry form on flowersbytavi.co.uk has never delivered an enquiry. `FORMSPREE_ID`
is still the placeholder `"YOUR_FORM_ID"`, so `js/main.js` returns early on its
"not connected yet" branch and shows visitors a message telling them to email
instead. Every enquiry submitted since launch has required the visitor to give up
and start again in their email client.

This spec replaces Formspree with a self-hosted backend: a small serverless API,
owned entirely by us, that validates a submission, screens it for bots, and emails
it on. No third-party form service ever sees a customer's details.

The pattern deliberately mirrors the existing Fresh & Clean backend
(`/Users/kreeza/Desktop/WebM8/Fresh&Clean/fresh-clean-14b943.webflow/server/server.js`)
so it is familiar to maintain, with four hardening additions that setup lacks.

## Decisions (confirmed with user)

| Decision | Choice | Why |
|---|---|---|
| Hosting | Vercel serverless | Same as Fresh & Clean; free; Node runtime |
| Repo layout | **Separate private repo** | `bouquets-by-tavi` is public and GitHub Pages serves everything in it. A `/server` folder would publish the validation rules, rate limits and honeypot field name at `flowersbytavi.co.uk/server/` — precisely what someone needs to bypass them |
| Email transport | **Gmail + app password** via nodemailer | User's choice, matching Fresh & Clean. See the risk note below |
| Bot protection | Cloudflare Turnstile | Free, unlimited, invisible to most visitors |
| Rate limiting | Upstash Redis free tier | Serverless functions are stateless — an in-memory counter resets on cold start and is not shared between concurrent instances, so it barely limits anything |
| Frontend hosting | Unchanged — GitHub Pages | Only the delivery mechanism changes |

### Risk accepted on the transport

Microsoft is retiring Basic Authentication for SMTP AUTH, and app passwords depend
on it, so the originally-planned Outlook route is on a deadline (sources conflict
between April and December 2026). Google has been tightening the same screws. The
user chose Gmail knowing this. The design isolates the transport behind a single
nodemailer transport object so swapping to an HTTP email API later is a contained
change, not a rewrite.

Note: the `APP_PASSWORD` currently in the site repo's `.env` was generated for
Outlook. A **Gmail** app password is required instead, and it belongs in the API
repo's environment, not the site repo's.

## Architecture

```
browser (flowersbytavi.co.uk, GitHub Pages)
   │  POST JSON  { …fields, turnstileToken, website }
   ▼
Vercel serverless function  (private repo)
   │
   ├─ 1. origin allowlist
   ├─ 2. honeypot filled?        → 400, drop silently
   ├─ 3. Turnstile token valid?  → 403
   ├─ 4. rate limit (Upstash)    → 429
   ├─ 5. validate + sanitise     → 400 with field errors
   └─ 6. nodemailer → Gmail SMTP → 200
                │
                ▼
     flowersbytavi@outlook.com
```

**Check order is load-bearing.** The two free local checks (origin, honeypot) run
before Turnstile, which costs an outbound HTTPS call, and before the rate limiter,
which costs a Redis round trip. A flood of naive junk is rejected without spending
either, and never touches the email quota.

## Security layers

Defence in depth — no single layer is trusted alone.

| Layer | Stops | Notes |
|---|---|---|
| Honeypot (`website` field, hidden) | Naive form-filling bots | Same technique as Fresh & Clean. Silent 400 — never tell a bot why it failed |
| Cloudflare Turnstile | Real bot traffic | The primary defence. Token verified server-side against Cloudflare; a token is single-use |
| Upstash rate limit | Anyone past Turnstile exhausting the send quota | Per-IP. Two windows: short-burst and daily |
| Server-side validation | Malformed or oversized payloads | Never trust the client's own validation — it is trivially bypassed |
| Header-injection guard | CR/LF injected into the email subject | Fresh & Clean puts `formData.Name` straight into the subject unvalidated; this design strips newlines from anything reaching a header |

**CORS is configured but is not counted as a defence.** It only constrains browsers.
A bot using `curl` ignores it entirely, which is why the Fresh & Clean endpoint is
effectively open to the internet today despite having CORS set up.

### Rate limit values

- **10 submissions per IP per hour** — generous for a human, useless for a flood.
- **30 submissions per IP per day** — a hard backstop.
- Exceeding either returns `429` with a message telling the visitor to try later or
  email directly, so a legitimate user who trips it is never left stuck.

Gmail's own ceiling is roughly 500 messages/day. These limits keep any single IP far
below it, so one abuser cannot silently consume the day's capacity and block real
enquiries — the failure mode that matters most, because it is invisible.

## Validation rules

Server-side, mirroring the client rules the form already enforces:

| Field | Rule |
|---|---|
| `name` | Required, 1–100 chars after trim |
| `email` | Required, must match a basic address shape, ≤ 254 chars |
| `intent` | Required, must be exactly `Order from the collection` or `Design something custom` |
| `bouquet` | Required **only** when intent is `Order from the collection`; ≤ 100 chars |
| `budget` | Optional; ≤ 100 chars |
| `message` | Required **only** when intent is `Design something custom`; ≤ 5000 chars |
| `occasion`, `needed_by`, `fulfilment` | Optional; ≤ 100 chars each |

**Deliberately not allowlisted: product names, occasions, budgets and fulfilment
values.** The obvious instinct is to check `bouquet` against the known product list,
but that would put the product catalogue in two repos at once. Renaming a product in
`index.html` — a routine content edit, and one the docs actively invite — would then
silently reject every enquiry for that product until someone remembered to update the
API too. The failure would be invisible: the customer sees an error, the owner sees
nothing at all.

The security gain does not justify that. These values are length-capped, sanitised,
and land in the email body rather than a header, so the worst case for an unexpected
value is a slightly odd line in an email only the owner reads.

`intent` **is** allowlisted, because it is structural rather than content: it decides
which other fields are required, so an unrecognised value is a genuine error rather
than a content change.

Any unknown field in the payload is ignored rather than forwarded, so a crafted
request cannot inject extra content into the email body. Total payload capped at
16 KB.

## The email

- **From:** the Gmail account, display name "Flowers by Tavi"
- **To:** `flowersbytavi@outlook.com` (an env var, so it can change without a code edit)
- **Reply-To:** the enquirer's address, so hitting Reply answers the customer directly
- **Subject:** `New enquiry from <name> — <intent>`, with newlines stripped from `<name>`
- **Body:** every submitted field, one per line, with empty optional fields shown as
  `—` rather than omitted, so at a glance it is clear what the customer chose to skip

## Frontend changes (`bouquets-by-tavi`)

- Remove `FORMSPREE_ID`; add `API_URL`, resolving to localhost during development and
  the Vercel URL in production, matching the pattern in Fresh & Clean's `form-handler.js`.
- Load the Turnstile script and render its widget in the form, above Submit.
- Add the hidden honeypot input.
- Submit handler posts JSON instead of `FormData`, including the Turnstile token.
- Handle the new failure cases distinctly — rate-limited (429) and rejected (403)
  need their own messages, not the existing generic "something went wrong".
- Remove the "form isn't connected yet" branch and `FALLBACK_EMAIL` early return.

The existing success panel, error styling, field-error mechanism and path-aware
validation all stay exactly as they are.

## Configuration

All secrets live in Vercel environment variables on the API project. None are ever
committed.

| Variable | Purpose |
|---|---|
| `GMAIL_USER` | Sending account |
| `GMAIL_APP_PASSWORD` | Gmail app password (2FA required to generate) |
| `MAIL_TO` | Where enquiries are delivered |
| `TURNSTILE_SECRET` | Server-side token verification |
| `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN` | Rate limit store |
| `ALLOWED_ORIGINS` | Comma-separated origin allowlist |

The API repo carries a committed `.env.example` documenting every variable with
placeholder values, and a `.gitignore` covering `.env` from the first commit — Fresh
& Clean has a real `.env` with live credentials and **no `.gitignore` at all**,
protected only by nobody having run `git add -A`.

## Out of scope

No enquiry database, admin UI or dashboard. No file uploads. No auto-reply to the
customer. No migration of Fresh & Clean to this hardened pattern — that is worth
doing afterwards, and its currently-unprotected endpoint is tracked separately.

## Follow-up not covered here

`AGENTS.md` and `README.md` tell maintainers to keep "three things" in sync when
renaming a product, but a product name appears in five places in `index.html` —
the `<h3>`, the `data-bouquet` attribute, the `<option>`, and two `<img alt>`
attributes. A rename following the rule leaves alt text describing the old product.
