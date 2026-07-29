# Legal Policy Pages — Design Spec

**Date:** 2026-07-29
**Status:** Approved by user

## Overview

Add four standard policy pages to the "Flowers by Tavi" site — Privacy Policy, Terms
& Conditions, Delivery & Order Policy, and Returns & Cancellations — linked from the
footer of the existing single-page site (`index.html`). The main page itself is
unchanged except for the new footer links.

## Decisions (confirmed with user)

| Decision | Choice |
|---|---|
| Which policies | All four: Privacy Policy, Terms & Conditions, Delivery & Order Policy, Returns & Cancellations |
| Placement | Separate static pages (`privacy.html`, `terms.html`, `delivery.html`, `returns.html`), linked from the site footer — not sections on the main scrolling page |
| Legal trading name | User does not want their full legal name added yet. `terms.html` gets a hidden HTML comment marking where to add it later; no visible placeholder text, no fabricated name |
| Delivery terms | Generic — states free local delivery exists (matches the announcement bar) but exact area/timing/fees are confirmed per enquiry, since no fixed radius or fee is defined anywhere in the business's existing content |
| Cancellation/refund terms | Generic, case-by-case — no invented deposit percentages or fixed notice-period deadlines |
| Cookies/analytics | Confirmed via grep of `index.html`/`js/main.js`: the site sets no cookies and runs no analytics/tracking scripts. Privacy Policy states this plainly and separately notes Google Fonts (already loaded in `<head>`) as the one third-party request the site makes |

## Page Architecture

- Four new static HTML files at the project root, sharing `css/style.css` (new
  `/* Legal pages */` section appended, no changes to existing rules) and the same
  Google Fonts `<link>`s as `index.html`.
- Each page: a simple non-sticky header (brand mark linking to `index.html`, plus a
  "← Back to site" link) — not the full nav with hamburger/Collection/Occasions/etc.,
  since these are content pages, not sections of the scrolling homepage.
- No `js/main.js` on these pages — that script queries `.nav-toggle`, `#enquiry-form`,
  `.card-carousel`, etc., none of which exist here, so including it would throw on
  load for no benefit.
- Body copy in a centered, readable prose column (reuses `--font-display` for
  headings, `--font-body` for text, same palette as the rest of the site).
- Footer on each legal page: just copyright, no repeated trust-line/contact block.
- Each page states "Last updated: 29 July 2026" under its `<h1>`.

## Content (source of truth — exact copy to use)

### Privacy Policy (`privacy.html`)

1. **Intro** — Flowers by Tavi ("we", "us"), contact via
   flowersbytavi@outlook.com / +44 7364 125646. This policy explains how personal
   information submitted through this website is handled.
2. **Information we collect** — via the enquiry form only: name, email, phone
   (optional), occasion, item of interest, needed-by date (optional), and your
   message. No payment or account information is collected on this site.
3. **How we use it** — solely to respond to and fulfil your enquiry. Not used for
   marketing unless you separately opt in, and never sold or shared with third
   parties for their own marketing.
4. **How enquiries are processed** — the form is delivered via Formspree, a
   third-party form-processing service, which receives and stores your submission
   so we can read and reply to it.
5. **Cookies & tracking** — this site does not use cookies or analytics tracking.
   It loads fonts from Google Fonts, which may receive your device's IP address as
   part of loading those font files.
6. **How long we keep your data** — only as long as needed to respond to and fulfil
   your enquiry, or as required by law (e.g. order/invoice records).
7. **Your rights** — under UK data protection law, you can ask to see, correct, or
   delete the personal data we hold about you by emailing us.
8. **Changes to this policy** — this policy may be updated from time to time; the
   "last updated" date at the top reflects the latest version.
9. **Contact** — email/phone.

### Terms & Conditions (`terms.html`)

1. **About these terms** — by using this website or sending an enquiry, you agree
   to these terms.
2. **About us** — Flowers by Tavi is a UK-based small business providing
   handcrafted flower and gift arrangements. `<!-- Add full legal trading name /
   registration details here -->` (HTML comment, not rendered) sits directly below
   this paragraph for later use. Contact via email/phone.
3. **How enquiries & orders work** — this site is not an instant checkout; prices
   shown are indicative starting prices; final design, price, and availability are
   confirmed directly with us after an enquiry is submitted. An order is only
   confirmed once details are agreed with you — not automatically on form
   submission.
4. **Product variation** — as noted on individual product listings, flowers,
   chocolates, and materials may vary slightly depending on availability and season
   while keeping the overall look/theme; add-ons and customisation are subject to
   availability.
5. **Pricing** — prices are shown in GBP (£) and may change without notice; the
   price agreed when your order is confirmed is the price that applies to that
   order.
6. **Intellectual property** — the text, photos, and design of this website belong
   to Flowers by Tavi and may not be reused without permission.
7. **Liability** — arrangements are handmade from natural/perishable materials; we
   take care in preparation and delivery but can't guarantee against the natural
   variation described above.
8. **Governing law** — these terms are governed by the laws of England and Wales.
9. **Contact** — email/phone.

### Delivery & Order Policy (`delivery.html`)

1. **How delivery works** — after an enquiry is sent, we confirm whether delivery
   is available for the requested date, area, and arrangement.
2. **Local delivery** — free local delivery is offered (as noted on the site);
   exact delivery areas, timing, and any charges for delivery outside the local area
   are confirmed individually when we respond to an enquiry.
3. **Timing** — enquire as early as possible, especially around busy occasions
   (e.g. Valentine's Day, Mother's Day, Christmas), as availability and delivery
   slots can be limited.
4. **Delivery issues** — if there's any trouble receiving an order (wrong address,
   no one available, etc.), contact us as soon as possible so we can help resolve
   it.
5. **Contact** — email/phone.

### Returns & Cancellations (`returns.html`)

1. **Made-to-order & perishable** — each arrangement is freshly handmade to order
   using flowers, chocolates, and other perishable materials, so returns can't be
   accepted once an order has been completed or delivered.
2. **Cancellations & changes** — contact us as soon as possible to cancel or change
   an order; because arrangements are made close to the delivery date, changes may
   not be possible once preparation has begun. Requests are handled case-by-case.
3. **Quality concerns** — if something isn't right with an order (e.g. damaged in
   transit), contact us as soon as possible, ideally within 24 hours of delivery,
   with a photo where possible, so we can put it right.
4. **Contact** — email/phone.

## Footer Changes (`index.html`)

Add a new link row between `.footer-contact` and `.copyright`:

```html
<ul class="policy-links">
  <li><a href="privacy.html">Privacy Policy</a></li>
  <li><a href="terms.html">Terms &amp; Conditions</a></li>
  <li><a href="delivery.html">Delivery &amp; Order Policy</a></li>
  <li><a href="returns.html">Returns &amp; Cancellations</a></li>
</ul>
```

Styled similarly to `.trust-line` (small caps, centered, muted separators).

## Out of Scope

No cookie consent banner (site sets no cookies, so none is legally required). No
changes to the enquiry form, Formspree wiring, or any other existing section. No
sitemap/robots.txt changes.
