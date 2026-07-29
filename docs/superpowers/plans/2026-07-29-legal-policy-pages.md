# Legal Policy Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four static policy pages (Privacy Policy, Terms & Conditions, Delivery & Order Policy, Returns & Cancellations) to the "Flowers by Tavi" site, linked from the footer, per `docs/superpowers/specs/2026-07-29-legal-policy-pages-design.md`.

**Architecture:** Four new static HTML files at the project root (`privacy.html`, `terms.html`, `delivery.html`, `returns.html`), each a minimal page (brand header + back-to-site link, prose `<main>`, copyright-only footer) sharing the existing `css/style.css` and Google Fonts. No `js/main.js` on these pages. `index.html`'s footer gets one new link row.

**Tech Stack:** Same as the rest of the site — static HTML/CSS, no build step, no JS on the new pages. Verified via Playwright MCP against `http://localhost:8000`.

## Global Constraints

- No build step, no framework — plain static HTML files.
- Currency is **£**; write it as `&pound;` (only appears once, in `terms.html`).
- Contact details used verbatim on every legal page: `flowersbytavi@outlook.com`, `+44 7364 125646`.
- Do **not** add a visible legal trading name/registration number anywhere — per the user, that's deferred. `terms.html` gets a non-rendered HTML comment (`<!-- Add full legal trading name / registration details here -->`) marking where to add it later.
- No cookie-consent banner — the site sets no cookies, confirmed by grep of `index.html`/`js/main.js`.
- Do not modify `js/main.js` or any existing section of `index.html` other than the footer.
- No horizontal overflow at 375px on the new pages either.

---

### Task 1: Footer links + shared legal-page styling

**Files:**
- Modify: `index.html:324-336` (the `<footer class="site-footer">` block)
- Modify: `css/style.css` (append a new `/* ── Legal pages ── */` section, after the existing footer rules and before the `/* ── Motion preferences ── */` section)

**Interfaces:**
- Produces: `.legal-header`, `.legal-back`, `.legal-main`, `.legal-footer` classes that Task 2's four pages consume; `.policy-links` class used in `index.html`'s footer.

- [ ] **Step 1: Add the footer link row to `index.html`**

Change:
```html
  <footer class="site-footer">
    <ul class="trust-line">
      <li>Handcrafted daily</li>
      <li>Free local delivery</li>
      <li>Made with love</li>
    </ul>
    <div class="footer-contact">
      <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a>
      <a href="tel:+447364125646">+44 7364 125646</a>
      <a href="https://instagram.com/flowersbytavi_" rel="noopener">Instagram @flowersbytavi_</a>
    </div>
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
```
to:
```html
  <footer class="site-footer">
    <ul class="trust-line">
      <li>Handcrafted daily</li>
      <li>Free local delivery</li>
      <li>Made with love</li>
    </ul>
    <div class="footer-contact">
      <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a>
      <a href="tel:+447364125646">+44 7364 125646</a>
      <a href="https://instagram.com/flowersbytavi_" rel="noopener">Instagram @flowersbytavi_</a>
    </div>
    <ul class="policy-links">
      <li><a href="privacy.html">Privacy Policy</a></li>
      <li><a href="terms.html">Terms &amp; Conditions</a></li>
      <li><a href="delivery.html">Delivery &amp; Order Policy</a></li>
      <li><a href="returns.html">Returns &amp; Cancellations</a></li>
    </ul>
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
```

- [ ] **Step 2: Append the legal-page CSS section to `css/style.css`**

Add this new section directly before the existing `/* ── Motion preferences ── */` comment at the end of the file:

```css
/* ── Legal pages ──────────────────────────────────────────────── */

.policy-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem 0;
  font-size: 0.72rem;
  font-weight: 400;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 1.4rem;
}

.policy-links a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.policy-links a:hover { color: var(--rose-dark); border-color: var(--rose-dark); }

.policy-links li + li::before { content: "\00B7"; margin: 0 0.9rem; color: var(--gold); }

.legal-header {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.25rem 1.25rem 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.legal-back {
  font-size: 0.74rem;
  font-weight: 400;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px solid rgba(67, 56, 58, 0.25);
  white-space: nowrap;
}

.legal-back:hover { color: var(--rose-dark); border-color: var(--rose-dark); }

.legal-main {
  max-width: 42rem;
  margin: 0 auto;
  padding: 2.5rem 1.25rem 5rem;
}

.legal-main .kicker { text-align: left; }

.legal-main h1 { font-size: clamp(2rem, 5vw, 2.6rem); margin-bottom: 0.4rem; }

.legal-updated {
  font-size: 0.82rem;
  color: var(--text);
  opacity: 0.75;
  margin-bottom: 2.2rem;
}

.legal-main h2 { font-size: 1.3rem; margin: 2rem 0 0.7rem; }

.legal-main p { font-size: 0.96rem; margin-bottom: 1rem; }

.legal-main a { color: var(--rose-dark); }

.legal-footer { padding: 2rem 1.25rem; }
```

- [ ] **Step 3: Verify in the browser**

Run `python3 -m http.server 8000` (background), Playwright `browser_navigate` to `http://localhost:8000`, scroll to the footer, take a snapshot.
Expected: footer shows 4 new links — "Privacy Policy", "Terms & Conditions", "Delivery & Order Policy", "Returns & Cancellations" — above the copyright line. (Links will 404 until Task 2 adds the target pages — that's expected at this point.)

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css && git commit -m "feat: add footer links and shared styling for legal policy pages"
```

---

### Task 2: The four policy pages

**Files:**
- Create: `privacy.html`, `terms.html`, `delivery.html`, `returns.html`

**Interfaces:**
- Consumes: `.legal-header`, `.legal-back`, `.legal-main`, `.legal-footer` from Task 1's CSS; the footer links from Task 1's `index.html`.

- [ ] **Step 1: Create `privacy.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy — Flowers by Tavi</title>
  <meta name="description" content="How Flowers by Tavi collects and uses personal information submitted through this website.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%92%90%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Great+Vibes&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="legal-header">
    <a class="brand" href="index.html">
      <span class="brand-name">Flowers</span>
      <span class="brand-sub">by Tavi</span>
    </a>
    <a class="legal-back" href="index.html">&larr; Back to site</a>
  </header>
  <main class="legal-main">
    <p class="kicker">Legal</p>
    <h1>Privacy Policy</h1>
    <p class="legal-updated">Last updated: 29 July 2026</p>

    <p>Flowers by Tavi (&ldquo;we&rdquo;, &ldquo;us&rdquo;) can be reached at <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or <a href="tel:+447364125646">+44 7364 125646</a>. This policy explains how we handle personal information submitted through this website.</p>

    <h2>Information we collect</h2>
    <p>We only collect what you give us through the enquiry form: your name, email, phone (optional), occasion, item of interest, needed-by date (optional), and your message. We do not collect any payment or account information on this site.</p>

    <h2>How we use it</h2>
    <p>We use this information solely to respond to and fulfil your enquiry. We do not use it for marketing unless you separately opt in, and we never sell or share it with third parties for their own marketing.</p>

    <h2>How enquiries are processed</h2>
    <p>Enquiry form submissions are delivered via <a href="https://formspree.io" rel="noopener">Formspree</a>, a third-party form-processing service, which receives and stores your submission so we can read and reply to it.</p>

    <h2>Cookies &amp; tracking</h2>
    <p>This site does not use cookies or analytics tracking. It loads fonts from Google Fonts, which may receive your device&rsquo;s IP address as part of loading those font files.</p>

    <h2>How long we keep your data</h2>
    <p>We keep your information only as long as needed to respond to and fulfil your enquiry, or as required by law (for example, order or invoice records).</p>

    <h2>Your rights</h2>
    <p>Under UK data protection law, you can ask to see, correct, or delete the personal data we hold about you by emailing us at <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a>.</p>

    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. The &ldquo;last updated&rdquo; date at the top of this page reflects the latest version.</p>

    <h2>Contact</h2>
    <p>If you have any questions about this policy, email <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or call <a href="tel:+447364125646">+44 7364 125646</a>.</p>
  </main>
  <footer class="site-footer legal-footer">
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Create `terms.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Terms &amp; Conditions — Flowers by Tavi</title>
  <meta name="description" content="Terms and conditions for using the Flowers by Tavi website and sending an enquiry.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%92%90%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Great+Vibes&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="legal-header">
    <a class="brand" href="index.html">
      <span class="brand-name">Flowers</span>
      <span class="brand-sub">by Tavi</span>
    </a>
    <a class="legal-back" href="index.html">&larr; Back to site</a>
  </header>
  <main class="legal-main">
    <p class="kicker">Legal</p>
    <h1>Terms &amp; Conditions</h1>
    <p class="legal-updated">Last updated: 29 July 2026</p>

    <h2>About these terms</h2>
    <p>By using this website or sending us an enquiry, you agree to these terms.</p>

    <h2>About us</h2>
    <p>Flowers by Tavi is a UK-based small business providing handcrafted flower and gift arrangements.</p>
    <!-- Add full legal trading name / registration details here -->
    <p>You can contact us at <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or <a href="tel:+447364125646">+44 7364 125646</a>.</p>

    <h2>How enquiries &amp; orders work</h2>
    <p>This site is not an instant checkout. Prices shown are indicative starting prices, and the final design, price, and availability are confirmed directly with us after you submit an enquiry. An order is only confirmed once we&rsquo;ve agreed the details with you &mdash; not automatically when you submit the enquiry form.</p>

    <h2>Product variation</h2>
    <p>As noted on individual product listings, flowers, chocolates, and materials may vary slightly depending on availability and season while keeping the overall look and colour theme. Add-ons and customisation are subject to availability.</p>

    <h2>Pricing</h2>
    <p>Prices are shown in pounds sterling (&pound;) and may change without notice. The price agreed when your order is confirmed is the price that applies to that order.</p>

    <h2>Intellectual property</h2>
    <p>The text, photos, and design of this website belong to Flowers by Tavi and may not be reused without permission.</p>

    <h2>Liability</h2>
    <p>Our arrangements are handmade from natural, perishable materials. We take great care in preparation and delivery, but we can&rsquo;t guarantee against the natural variation described above.</p>

    <h2>Governing law</h2>
    <p>These terms are governed by the laws of England and Wales.</p>

    <h2>Contact</h2>
    <p>If you have any questions about these terms, email <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or call <a href="tel:+447364125646">+44 7364 125646</a>.</p>
  </main>
  <footer class="site-footer legal-footer">
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
</body>
</html>
```

- [ ] **Step 3: Create `delivery.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Delivery &amp; Order Policy — Flowers by Tavi</title>
  <meta name="description" content="How delivery and orders work at Flowers by Tavi.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%92%90%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Great+Vibes&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="legal-header">
    <a class="brand" href="index.html">
      <span class="brand-name">Flowers</span>
      <span class="brand-sub">by Tavi</span>
    </a>
    <a class="legal-back" href="index.html">&larr; Back to site</a>
  </header>
  <main class="legal-main">
    <p class="kicker">Legal</p>
    <h1>Delivery &amp; Order Policy</h1>
    <p class="legal-updated">Last updated: 29 July 2026</p>

    <h2>How delivery works</h2>
    <p>After you send an enquiry, we&rsquo;ll confirm whether delivery is available for your requested date, area, and arrangement.</p>

    <h2>Local delivery</h2>
    <p>We offer free local delivery, as noted on the site. Exact delivery areas, timing, and any charges for delivery outside our local area are confirmed individually when we respond to your enquiry.</p>

    <h2>Timing</h2>
    <p>Please enquire as early as possible, especially around busy occasions such as Valentine&rsquo;s Day, Mother&rsquo;s Day, and Christmas, as availability and delivery slots can be limited.</p>

    <h2>Delivery issues</h2>
    <p>If there&rsquo;s any trouble receiving your order &mdash; a wrong address, no one available to receive it, or anything else &mdash; please contact us as soon as possible so we can help resolve it.</p>

    <h2>Contact</h2>
    <p>Email <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or call <a href="tel:+447364125646">+44 7364 125646</a>.</p>
  </main>
  <footer class="site-footer legal-footer">
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
</body>
</html>
```

- [ ] **Step 4: Create `returns.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Returns &amp; Cancellations — Flowers by Tavi</title>
  <meta name="description" content="Our returns, cancellation, and quality policy at Flowers by Tavi.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%92%90%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Great+Vibes&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="legal-header">
    <a class="brand" href="index.html">
      <span class="brand-name">Flowers</span>
      <span class="brand-sub">by Tavi</span>
    </a>
    <a class="legal-back" href="index.html">&larr; Back to site</a>
  </header>
  <main class="legal-main">
    <p class="kicker">Legal</p>
    <h1>Returns &amp; Cancellations</h1>
    <p class="legal-updated">Last updated: 29 July 2026</p>

    <h2>Made-to-order &amp; perishable</h2>
    <p>Each arrangement is freshly handmade to order using flowers, chocolates, and other perishable materials, so we&rsquo;re unable to accept returns once an order has been completed or delivered.</p>

    <h2>Cancellations &amp; changes</h2>
    <p>If you need to cancel or change your order, please contact us as soon as possible. Because arrangements are made close to the delivery date, we may not be able to make changes once preparation has begun. We handle every request on a case-by-case basis and will always try to help.</p>

    <h2>Quality concerns</h2>
    <p>If something isn&rsquo;t right with your order &mdash; for example, damage in transit &mdash; please contact us as soon as possible, ideally within 24 hours of delivery, with a photo where possible, so we can put it right.</p>

    <h2>Contact</h2>
    <p>Email <a href="mailto:flowersbytavi@outlook.com">flowersbytavi@outlook.com</a> or call <a href="tel:+447364125646">+44 7364 125646</a>.</p>
  </main>
  <footer class="site-footer legal-footer">
    <p class="copyright">&copy; 2026 Flowers by Tavi. All rights reserved.</p>
  </footer>
</body>
</html>
```

- [ ] **Step 5: Verify each page in the browser**

With the server running (from Task 1), for each of the 4 URLs (`/privacy.html`, `/terms.html`, `/delivery.html`, `/returns.html`): Playwright `browser_navigate`, take a snapshot.
Expected per page: correct `<title>`, correct `<h1>`, all listed `<h2>` sections present with their text, "← Back to site" link present, no console errors. Click "← Back to site" → lands on `http://localhost:8000/`. Click the brand mark → same.

- [ ] **Step 6: Verify the footer links from the homepage**

From `http://localhost:8000/`, click each of the 4 new footer links in turn and confirm each navigates to the correct page (no 404s now that Task 2 exists).

- [ ] **Step 7: Mobile check**

`browser_resize` to 375×800, navigate to each of the 4 pages, `browser_evaluate` `document.documentElement.scrollWidth <= 375` on each.
Expected: no horizontal overflow on any of the 4 pages.

- [ ] **Step 8: Commit**

```bash
git add privacy.html terms.html delivery.html returns.html && git commit -m "feat: add Privacy, Terms, Delivery, and Returns policy pages"
```
