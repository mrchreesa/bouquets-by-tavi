# Bouquets by Tavi Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **Also required:** invoke `frontend-design:frontend-design` before writing any HTML/CSS (Tasks 2–3).

**Goal:** A static, single-page, mobile-responsive website for Bouquets by Tavi with an enquiry form (Formspree), styled after `reference.png`.

**Architecture:** One `index.html` with all sections, one stylesheet, one vanilla-JS file for nav toggle / pre-selection / form validation & submission. Placeholder SVG images in `images/`. No build step, no dependencies.

**Tech Stack:** HTML5, CSS3, vanilla JS, Google Fonts (Cormorant Garamond, Great Vibes, Jost), Formspree (form backend), Playwright MCP for verification.

## Global Constraints

- No build step, no node_modules, no framework — files must work served as-is.
- Currency is **£**; bouquet prices are indicative "From £X".
- Brand name is exactly **Bouquets by Tavi**.
- Formspree form ID is a single constant `FORMSPREE_ID` at the top of `js/main.js`, default `"YOUR_FORM_ID"`; unconfigured ID must produce a visible error message on submit, never a silent failure.
- Fallback contact email used in error copy: `hello@bouquetsbytavi.com` (placeholder).
- No horizontal page scroll at 375px or any width.
- Verification is done in a real browser via Playwright MCP against `http://localhost:8000` (`python3 -m http.server 8000` from the project root).

---

### Task 1: Placeholder images

**Files:**
- Create: `images/hero.svg`, `images/bouquet-1.svg`, `images/bouquet-2.svg`, `images/bouquet-3.svg`, `images/bouquet-4.svg`, `images/story.svg`

**Interfaces:**
- Produces: the six image paths above, referenced verbatim by `index.html` in Task 2.

- [ ] **Step 1: Create the six SVG placeholders**

Each is a blush gradient with gold floral line-art and a small monogram — intentional-looking, no "placeholder" text. Template (vary gradient stops slightly and viewBox per slot — hero 560×640, bouquets 400×480, story 480×560):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480" role="img" aria-label="Decorative floral placeholder">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F7E3DE"/>
      <stop offset="1" stop-color="#EDC9C3"/>
    </linearGradient>
  </defs>
  <rect width="400" height="480" fill="url(#g)"/>
  <g fill="none" stroke="#C9A96E" stroke-width="1.5" opacity="0.65">
    <path d="M200 400 C 190 330, 210 300, 200 240"/>
    <path d="M200 300 C 170 280, 150 250, 155 220"/>
    <path d="M200 320 C 230 300, 255 270, 250 235"/>
    <circle cx="200" cy="225" r="22"/>
    <circle cx="152" cy="205" r="16"/>
    <circle cx="252" cy="220" r="16"/>
    <path d="M185 215 q 15 -18 30 0 q -15 18 -30 0"/>
  </g>
  <g font-family="Georgia, serif" text-anchor="middle">
    <circle cx="200" cy="130" r="26" fill="none" stroke="#C9A96E" opacity="0.6"/>
    <text x="200" y="139" font-size="26" fill="#B27680">T</text>
  </g>
</svg>
```

- [ ] **Step 2: Verify they render**

Run: `python3 -m http.server 8000` (background) and open `http://localhost:8000/images/bouquet-1.svg` via Playwright `browser_navigate`.
Expected: gradient + line art renders, no XML errors.

- [ ] **Step 3: Commit**

```bash
git add images && git commit -m "feat: add on-brand placeholder images"
```

---

### Task 2: Page markup (`index.html`)

**Files:**
- Create: `index.html`

**Interfaces:**
- Consumes: image paths from Task 1.
- Produces: DOM contract used by Tasks 3–4 — ids `nav-menu`, `bouquets`, `occasions`, `story`, `enquiry`, `enquiry-form`, `form-success`, `name`, `email`, `phone`, `needed-by`, `occasion`, `bouquet`, `message`; classes `.nav-toggle`, `.enquire-btn` (with `data-bouquet`), `.occasion-tile` (with `data-occasion`), `.field`, `.field-error`, `.form-status`.

- [ ] **Step 1: Invoke `frontend-design:frontend-design`** (governs Tasks 2–3 craft decisions).

- [ ] **Step 2: Write `index.html`** — full page in this order: announcement bar → sticky header (brand + nav links Bouquets/Occasions/Our Story/Contact + hamburger button) → hero (h1 "The Art of *Gifting Flowers*" with script span, tagline, "Enquire Now" → `#enquiry`, hero image) → `#bouquets` grid of 4 cards (Blush Romance £45, Eternal Grace £55, Pure Devotion £60, Couture Peonies £65; each `button.enquire-btn[data-bouquet]`) → `#occasions` 6 tiles (Birthday, Anniversary, Romance, Congratulations, Thank You, Sympathy; each `button.occasion-tile[data-occasion]` with inline gold line-art SVG icon) → `#story` (image + kicker "Our Story", h2 "Thoughtfully Designed. Beautifully Delivered.", paragraph) → `#enquiry` form (fields per spec: name*, email*, phone, needed-by date, occasion select, bouquet select, message*; each required field has a hidden `.field-error` p; `.form-status` live region; separate hidden `#form-success` panel) → footer (trust line, contact placeholders, copyright). `novalidate` on the form (JS owns validation). Google Fonts `<link>`s, emoji favicon via data URI, meta description. Mark each `<img>` with `<!-- REPLACE with real photo -->`.

Key structural skeleton (attributes/ids must match exactly):

```html
<header class="site-header">
  <nav class="nav" aria-label="Main">
    <a class="brand" href="#top">Bouquets <span>by Tavi</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu">…</button>
    <ul id="nav-menu" class="nav-menu">
      <li><a href="#bouquets">Bouquets</a></li>
      <li><a href="#occasions">Occasions</a></li>
      <li><a href="#story">Our Story</a></li>
      <li><a href="#enquiry">Contact</a></li>
    </ul>
  </nav>
</header>
…
<form id="enquiry-form" novalidate>
  …
  <button type="submit" class="btn">Send Enquiry</button>
  <p class="form-status" role="status" aria-live="polite" hidden></p>
</form>
<div id="form-success" hidden>…thank-you copy…</div>
```

- [ ] **Step 3: Verify structure**

Playwright `browser_navigate` to `http://localhost:8000`, take snapshot.
Expected: all sections present in order; form has all 7 fields; 4 bouquet cards; 6 occasion tiles.

- [ ] **Step 4: Commit**

```bash
git add index.html && git commit -m "feat: add single-page markup"
```

---

### Task 3: Styling (`css/style.css`)

**Files:**
- Create: `css/style.css` (linked from Task 2's `<head>`)

**Interfaces:**
- Consumes: DOM contract from Task 2.
- Produces: class `.open` on `.nav-menu` = mobile menu visible (Task 4 toggles it); `.field-error` visible when not `[hidden]`; `.form-status.error` styled as error.

- [ ] **Step 1: Write the stylesheet** — design tokens, then sections, mobile-first:

```css
:root {
  --cream: #FDF8F3; --blush: #F7E3DE; --blush-deep: #EDC9C3;
  --rose: #C98B93; --rose-dark: #B27680; --gold: #B99668;
  --ink: #43383A; --text: #6E5F5C;
  --font-display: "Cormorant Garamond", Georgia, serif;
  --font-script: "Great Vibes", cursive;
  --font-body: "Jost", "Helvetica Neue", sans-serif;
}
html { scroll-behavior: smooth; }
section[id] { scroll-margin-top: 90px; }
```

Required behaviors (implement with real CSS, guided by frontend-design skill):
- Sticky header; nav links small-caps letterspaced; below **760px** nav links hide behind hamburger (`.nav-menu` closed by default, shown when `.open`), hamburger hidden ≥760px.
- Hero: two columns ≥760px, stacked below; script span in `--font-script` gold/rose.
- Bouquet grid: 4 columns ≥1000px → 2 columns ≥560px → 1 column below.
- Occasion tiles: arched (large top border-radius), 6 columns ≥1000px → 3 → 2.
- Scalloped edge on at least one section boundary (radial-gradient repeating background strip, as in reference).
- Form: 2-column rows ≥640px, full-width below; visible focus states; `.field-error` in a clear red-rose tone.
- Buttons: `.btn` filled rose, `.btn-outline` bordered; uppercase letterspaced labels.
- `img { max-width: 100%; height: auto; display: block; }` — no horizontal overflow anywhere.

- [ ] **Step 2: Verify visually at both widths**

Playwright: `browser_resize` 1280×900 → screenshot; `browser_resize` 375×800 → screenshot; also `browser_evaluate` `document.documentElement.scrollWidth <= 375`.
Expected: matches reference aesthetic; hamburger visible at 375; no horizontal overflow.

- [ ] **Step 3: Commit**

```bash
git add css && git commit -m "feat: style the page after the reference design"
```

---

### Task 4: Behavior (`js/main.js`)

**Files:**
- Create: `js/main.js` (loaded at end of `<body>` from Task 2)

**Interfaces:**
- Consumes: DOM contract from Task 2; `.open` class contract from Task 3.

- [ ] **Step 1: Write `js/main.js`** — complete file:

```js
// ── Configuration ────────────────────────────────────────────────
// Create a free form at https://formspree.io and paste its ID here.
const FORMSPREE_ID = "YOUR_FORM_ID";
const FALLBACK_EMAIL = "hello@bouquetsbytavi.com";

// ── Mobile navigation ────────────────────────────────────────────
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.getElementById("nav-menu");

navToggle.addEventListener("click", () => {
  const open = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!open));
  navMenu.classList.toggle("open", !open);
});

navMenu.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    navToggle.setAttribute("aria-expanded", "false");
    navMenu.classList.remove("open");
  }
});

// ── Pre-selection from bouquet cards and occasion tiles ──────────
const bouquetSelect = document.getElementById("bouquet");
const occasionSelect = document.getElementById("occasion");
const enquirySection = document.getElementById("enquiry");

function scrollToForm() {
  enquirySection.scrollIntoView({ behavior: "smooth" });
}

document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    bouquetSelect.value = button.dataset.bouquet;
    scrollToForm();
  });
});

document.querySelectorAll(".occasion-tile").forEach((tile) => {
  tile.addEventListener("click", () => {
    occasionSelect.value = tile.dataset.occasion;
    scrollToForm();
  });
});

// ── Enquiry form ─────────────────────────────────────────────────
const form = document.getElementById("enquiry-form");
const statusEl = form.querySelector(".form-status");
const successEl = document.getElementById("form-success");

function setFieldError(input, show) {
  const error = input.closest(".field").querySelector(".field-error");
  if (error) error.hidden = !show;
  input.setAttribute("aria-invalid", String(show));
}

function validate() {
  const email = form.elements.email;
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
  const checks = [
    [form.elements.name, form.elements.name.value.trim() !== ""],
    [email, emailOk],
    [form.elements.message, form.elements.message.value.trim() !== ""],
  ];
  let valid = true;
  for (const [input, ok] of checks) {
    setFieldError(input, !ok);
    if (!ok) valid = false;
  }
  return valid;
}

["name", "email", "message"].forEach((id) => {
  form.elements[id].addEventListener("input", () => setFieldError(form.elements[id], false));
});

function showStatus(text, isError) {
  statusEl.textContent = text;
  statusEl.hidden = false;
  statusEl.classList.toggle("error", isError);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.hidden = true;

  if (!validate()) {
    form.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  if (FORMSPREE_ID === "YOUR_FORM_ID") {
    showStatus(`The enquiry form isn't connected yet — please email us at ${FALLBACK_EMAIL}.`, true);
    return;
  }

  const submitButton = form.querySelector('[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Sending…";

  try {
    const response = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`Formspree responded ${response.status}`);
    form.hidden = true;
    successEl.hidden = false;
    successEl.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch {
    showStatus(`Something went wrong sending your enquiry — please try again, or email us at ${FALLBACK_EMAIL}.`, true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Send Enquiry";
  }
});
```

- [ ] **Step 2: Verify behaviors in the browser (Playwright)**

At 375×800:
1. Click hamburger → menu opens; click "Contact" → menu closes, page at `#enquiry`.

At 1280×900:
2. Click "Enquire" on the Eternal Grace card → `#bouquet` select value is "Eternal Grace", viewport at form.
3. Click the "Sympathy" tile → `#occasion` select value is "Sympathy".
4. Submit empty form → three `.field-error` messages visible, focus on name field, no network request.
5. Fill name/email/message with valid values, submit → status shows the "isn't connected yet" message (FORMSPREE_ID unconfigured).
6. Stub success path: `browser_evaluate` to set a fake ID is impossible (const) — instead stub fetch **before** submit:
   `window.fetch = async () => new Response("{}", { status: 200 })` — but the unconfigured guard fires first, so ALSO test with the guard bypassed by serving a temp copy… **Simpler accepted approach:** temporarily edit `FORMSPREE_ID` to `"TESTID"` locally (do not commit), stub `window.fetch` via `browser_evaluate`, submit, expect form hidden + `#form-success` visible; then revert the edit (`git checkout -- js/main.js` shows no diff after revert).
7. Same temp setup with `window.fetch = async () => new Response("{}", { status: 500 })` → error status message shown, form still visible.

Expected: all seven pass.

- [ ] **Step 3: Commit**

```bash
git add js && git commit -m "feat: add nav, pre-selection, and enquiry form behavior"
```

---

### Task 5: README + final polish + full verification

**Files:**
- Create: `README.md`
- Modify: `index.html` (only if final pass finds issues)

- [ ] **Step 1: Write `README.md`** covering: what the site is; how to run locally (`python3 -m http.server 8000`); how to connect Formspree (create form → paste ID into `FORMSPREE_ID` in `js/main.js`); how to replace placeholder images (drop photo in `images/`, update the marked `src` line in `index.html`); how to edit prices/copy; how to deploy (Netlify/GitHub Pages drag-and-drop).

- [ ] **Step 2: Full spec-checklist verification** — run every item in the spec's Testing section (nav scroll, hamburger, pre-selects, validation, success path, no overflow at 375px) plus a desktop and mobile full-page screenshot for the user.

- [ ] **Step 3: Commit**

```bash
git add README.md && git commit -m "docs: add README with setup and handoff instructions"
```
