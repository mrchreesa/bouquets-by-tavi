# Hero Section Updates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the five hero-section requests from the user's annotated mockup (four in scope, one deferred) per `docs/superpowers/specs/2026-07-30-hero-updates-design.md`: a promo badge, an animated announcement bar, a new tagline + location line, and a two-option hero CTA dropdown (Enquire Now / Order on WhatsApp).

**Architecture:** All changes live in the existing `index.html` header/hero markup, new CSS in `css/style.css`, and one small new JS block in `js/main.js` for the CTA dropdown's close-on-click behavior. No new files, no new pages.

**Tech Stack:** Same as the rest of the site — static HTML/CSS/vanilla JS, no build step. The CTA dropdown uses native `<details>`/`<summary>` (no JS needed for open/close itself). Verified via Playwright MCP against `http://localhost:8000`.

## Global Constraints

- No build step, no framework.
- WhatsApp link: `https://wa.me/447364125646` (derived from the existing site phone number +44 7364 125646 — no leading `+` or `0`), opened with `target="_blank" rel="noopener"`.
- Promo badge text is plain static HTML (`10% off until Monday`) — no date logic, no JS.
- Announcement bar motion must respect `prefers-reduced-motion: reduce` (existing media query at the bottom of `css/style.css`).
- Do not touch the hero `<img>` / `images/hero.svg` — real photos are a future, separate task per the user.
- No horizontal overflow at 375px.

---

### Task 1: Promo badge + animated announcement bar

**Files:**
- Modify: `index.html:16` (the `.announcement` div) and `index.html:20-23` (the `.brand` link)
- Modify: `css/style.css` (`.announcement` rule, and the `prefers-reduced-motion` block at the end of the file)

**Interfaces:**
- Produces: `.announcement-track` (animated span) and `.promo-badge` (static pill inside `.brand`), consumed by no other task — self-contained.

- [ ] **Step 1: Wrap the announcement text for animation**

Change:
```html
  <div class="announcement">Handcrafted bouquets &middot; Free local delivery</div>
```
to:
```html
  <div class="announcement"><span class="announcement-track">Handcrafted bouquets &middot; Free local delivery</span></div>
```

- [ ] **Step 2: Add the promo badge inside the brand mark**

Change:
```html
      <a class="brand" href="#top">
        <span class="brand-name">Flowers</span>
        <span class="brand-sub">by Tavi</span>
      </a>
```
to:
```html
      <a class="brand" href="#top">
        <span class="brand-name">Flowers</span>
        <span class="brand-sub">by Tavi</span>
        <span class="promo-badge">10% off until Monday</span>
      </a>
```

- [ ] **Step 3: Style the announcement animation and promo badge in `css/style.css`**

Find the existing announcement bar rule:
```css
.announcement {
  background: var(--rose);
  color: var(--cream);
  text-align: center;
  font-size: 0.7rem;
  font-weight: 400;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  padding: 0.55em 1em;
}
```
and change it to add `overflow: hidden`, then add the track animation and promo badge rules directly after it:
```css
.announcement {
  background: var(--rose);
  color: var(--cream);
  text-align: center;
  font-size: 0.7rem;
  font-weight: 400;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  padding: 0.55em 1em;
  overflow: hidden;
}

.announcement-track {
  display: inline-block;
  animation: announcement-slide 6s ease-in-out infinite alternate;
}

@keyframes announcement-slide {
  from { transform: translateX(-24px); }
  to { transform: translateX(24px); }
}

.promo-badge {
  display: inline-block;
  margin-top: 0.35rem;
  padding: 0.25em 0.75em;
  border: 1px solid var(--gold);
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--rose-dark);
  background: var(--blush-light);
}
```

Then find the `prefers-reduced-motion` block at the end of the file:
```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { transition: none !important; }
}
```
and add the announcement animation to it:
```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { transition: none !important; }
  .announcement-track { animation: none; }
}
```

- [ ] **Step 4: Verify in the browser**

Run `python3 -m http.server 8000` (background). Playwright `browser_navigate` to `http://localhost:8000`.
- Snapshot: confirm the badge text "10% off until Monday" appears near the brand mark.
- `browser_evaluate`: read `getComputedStyle(document.querySelector('.announcement-track')).animationName` — expect `"announcement-slide"`.
- `browser_evaluate` with `matchMedia('(prefers-reduced-motion: reduce)')` emulated (or check the CSS rule exists via `document.styleSheets`) — confirm the reduced-motion override is present.
- `browser_resize` to 375×800, `browser_evaluate` `document.documentElement.scrollWidth <= 375` — expect true (no overflow from the sliding text or badge).

- [ ] **Step 5: Commit**

```bash
git add index.html css/style.css && git commit -m "feat: add promo badge and animated announcement bar"
```

---

### Task 2: Hero copy + CTA dropdown markup and styling

**Files:**
- Modify: `index.html:43-47` (the `.hero-text` block)
- Modify: `css/style.css` (hero section rules)

**Interfaces:**
- Produces: `.hero-cta` (details), `.hero-cta-menu` (the two-link panel) — consumed by Task 3's JS.

- [ ] **Step 1: Replace the hero text block in `index.html`**

Change:
```html
        <div class="hero-text">
          <h1>The Art of <span class="script">Gifting Flowers</span></h1>
          <p class="hero-tagline">Handcrafted bouquets that capture beauty, emotion &amp; timeless elegance.</p>
          <a class="btn" href="#enquiry">Enquire Now</a>
        </div>
```
to:
```html
        <div class="hero-text">
          <h1>The Art of <span class="script">Gifting Flowers</span></h1>
          <p class="hero-tagline">Luxury blooms designed to make someone feel unforgettable.</p>
          <p class="hero-location">London, United Kingdom</p>
          <details class="hero-cta">
            <summary class="btn">Get in Touch</summary>
            <div class="hero-cta-menu">
              <a href="#enquiry">Enquire Now</a>
              <a href="https://wa.me/447364125646" target="_blank" rel="noopener">Order on WhatsApp</a>
            </div>
          </details>
        </div>
```

- [ ] **Step 2: Add the new hero CSS**

Find `.hero-tagline` in `css/style.css`:
```css
.hero-tagline {
  font-size: 0.8rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  max-width: 26rem;
  margin: 1.6rem auto 2.2rem;
  line-height: 2;
}
```
and add `.hero-location` and the `.hero-cta`/`.hero-cta-menu` rules directly after it:
```css
.hero-location {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
  max-width: 26rem;
  margin: -1.2rem auto 2rem;
}

.hero-cta { position: relative; display: inline-block; }

.hero-cta summary {
  list-style: none;
  cursor: pointer;
}

.hero-cta summary::-webkit-details-marker { display: none; }

.hero-cta summary::after {
  content: " \25BE";
  font-size: 0.7em;
}

.hero-cta-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  min-width: 100%;
  background: var(--cream-card);
  border: 1px solid rgba(185, 150, 104, 0.28);
  border-radius: 4px;
  box-shadow: 0 14px 30px -14px rgba(169, 106, 116, 0.45);
  overflow: hidden;
  z-index: 20;
}

.hero-cta-menu a {
  display: block;
  padding: 0.85em 1.4em;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink);
  text-decoration: none;
  white-space: nowrap;
}

.hero-cta-menu a:hover { background: var(--blush); color: var(--rose-dark); }

.hero-cta-menu a + a { border-top: 1px solid rgba(185, 150, 104, 0.2); }
```

Then find the desktop hero media query:
```css
@media (min-width: 820px) {
  .hero { padding: 5rem 1.25rem 5.5rem; }
  .hero-inner { grid-template-columns: 1.05fr 1fr; }
  .hero-text { text-align: left; }
  .hero-tagline { margin-left: 0; }
}
```
and add `.hero-location` to it:
```css
@media (min-width: 820px) {
  .hero { padding: 5rem 1.25rem 5.5rem; }
  .hero-inner { grid-template-columns: 1.05fr 1fr; }
  .hero-text { text-align: left; }
  .hero-tagline { margin-left: 0; }
  .hero-location { margin-left: 0; }
}
```

- [ ] **Step 3: Verify in the browser**

Playwright `browser_navigate` to `http://localhost:8000`, snapshot.
Expected: tagline reads "Luxury blooms designed to make someone feel unforgettable."; "London, United Kingdom" appears below it; a "Get in Touch" button/summary is present (no visible "Enquire Now" button at the top level anymore).
Click the "Get in Touch" summary → `.hero-cta-menu` becomes visible with "Enquire Now" and "Order on WhatsApp" links. Confirm the WhatsApp link's `href` is exactly `https://wa.me/447364125646` and it has `target="_blank"`.

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css && git commit -m "feat: update hero tagline, add location line and WhatsApp CTA dropdown"
```

---

### Task 3: CTA dropdown close-on-click behavior + full verification

**Files:**
- Modify: `js/main.js` (add a new block)

**Interfaces:**
- Consumes: `.hero-cta`, `.hero-cta-menu a` from Task 2.

- [ ] **Step 1: Add the close-on-click block to `js/main.js`**

Add this directly after the "Mobile navigation" block (before the carousel block):

```js
// ── Hero CTA dropdown ─────────────────────────────────────────────
document.querySelectorAll(".hero-cta-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    link.closest(".hero-cta").removeAttribute("open");
  });
});
```

- [ ] **Step 2: Full verification in the browser (Playwright)**

At 1280×900:
1. Click "Get in Touch" → menu opens. Click "Enquire Now" → page scrolls to `#enquiry` and the `<details>` no longer has the `open` attribute.
2. Reopen "Get in Touch" → click "Order on WhatsApp" → a new tab/page opens to `https://wa.me/447364125646` (check via `browser_tabs` or the page that opens), and the original `<details>` closes.
3. Confirm no console errors (`browser_console_messages`).

At 375×800:
4. `browser_evaluate` `document.documentElement.scrollWidth <= 375` — expect true.
5. Confirm the promo badge and announcement bar both render without wrapping oddly or overflowing.

Regression check (existing behavior, not touched by this plan but worth a quick look since the header markup changed):
6. Click the hamburger menu → still opens/closes correctly; nav links still scroll to their sections.

- [ ] **Step 3: Commit**

```bash
git add js/main.js && git commit -m "feat: close hero CTA dropdown when a menu link is clicked"
```
