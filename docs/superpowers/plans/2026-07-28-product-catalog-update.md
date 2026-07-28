# Product Catalog Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the 4 generic placeholder bouquet cards on the single-page "Flowers by Tavi" site with the real 5-product catalog (real copy, real prices, real photos), per `docs/superpowers/specs/2026-07-28-product-catalog-update-design.md`.

**Architecture:** Same static single-page site (`index.html` / `css/style.css` / `js/main.js`, no build step). The `#bouquets` section's `<ul class="bouquet-grid">` gets 5 richer `<li class="bouquet-card">` blocks (image or 2-photo carousel, name, price, description, includes/options lists, note, Enquire button). New CSS classes style the richer card content and the carousel. New JS wires up carousel arrow/dot clicks. Nav label, section heading, and the enquiry form's product field are renamed from "Bouquets" to "Collection" / "Item of interest". No other section changes.

**Tech Stack:** HTML5, CSS3, vanilla JS (existing stack, unchanged). Verification via Playwright MCP against `http://localhost:8000` (`python3 -m http.server 8000` from the project root), matching how this repo was originally verified.

## Global Constraints

- No build step, no node_modules, no framework — files must work served as-is.
- Currency is **£**, written as `&pound;` in HTML.
- Exact product names (used verbatim in `<h3>`, `data-bouquet`, and the dropdown `<option>`s): Blush Basket, Princess Treatment Basket, Luxury Chocolate Gift Cake, Luxury Heart Rose Box, Signature Rose Bouquet.
- Keep existing DOM ids/attributes that JS already depends on unchanged: section id `bouquets`, form field id/name `bouquet`, button class `enquire-btn` with `data-bouquet`, card class `bouquet-card`. Only visible text is renamed ("Bouquets" → "Collection" nav/heading, "Bouquet of interest" → "Item of interest" form label) — no id/name/class renaming.
- No horizontal page scroll at 375px or any width.
- Real product images already exist in `images/`: `1.PNG`, `2.PNG`, `3.PNG`, `4.PNG`, `4.1.PNG`, `5.jpg.jpeg`, `5.1.jpg.jpeg`. Do not modify or move these files.
- Carousels (products 4 & 5 only) are manual (arrow/dot click), no autoplay/timers.

---

### Task 1: Product content & copy in `index.html`

**Files:**
- Modify: `index.html:56-89` (the `#bouquets` section) and `index.html:205-214` (the `#bouquet` select in the enquiry form) and `index.html:31` (nav link)

**Interfaces:**
- Produces the DOM contract Tasks 2–3 style/script against: wrapper `.card-media` (all 5 cards), modifier `.card-carousel` (products 4 & 5 only) containing `.carousel-track` (2 `img`s, first has class `is-active`), `.carousel-prev` / `.carousel-next` buttons, `.carousel-dots` containing 2 `.carousel-dot` buttons (first has class `is-active`); text classes `.card-desc`, `.card-subhead`, `.card-list`, `.card-list-options`, `.card-note`. Existing classes `.bouquet-card`, `.enquire-btn`, `data-bouquet` are reused unchanged.

- [ ] **Step 1: Replace the nav link text**

In `index.html`, change:
```html
        <li><a href="#bouquets">Bouquets</a></li>
```
to:
```html
        <li><a href="#bouquets">Collection</a></li>
```

- [ ] **Step 2: Replace the `#bouquets` section heading and kicker context**

Change:
```html
    <section id="bouquets" class="section bouquets">
      <p class="kicker">Handpicked with love</p>
      <h2>Our Bouquets</h2>
```
to:
```html
    <section id="bouquets" class="section bouquets">
      <p class="kicker">Handpicked with love</p>
      <h2>Our Collection</h2>
```

- [ ] **Step 3: Replace the entire `<ul class="bouquet-grid">` block**

Replace the whole block (currently `index.html:59-88`, the four `<li class="bouquet-card">` placeholder entries) with:

```html
      <ul class="bouquet-grid">
        <li class="bouquet-card">
          <div class="card-media">
            <img src="images/1.PNG" alt="Blush Basket — a floral basket in blush pink and white tones">
          </div>
          <h3>Blush Basket</h3>
          <p class="price">&pound;55</p>
          <p class="card-desc">A soft, elegant floral basket featuring a delicate mix of blush pink and white tones. Perfect for birthdays, thank you gifts, or any occasion that calls for something beautiful and thoughtful.</p>
          <ul class="card-list">
            <li>Fresh floral arrangement</li>
            <li>Decorative basket with ribbon finish</li>
            <li>Carefully arranged premium blooms</li>
          </ul>
          <p class="card-note">Note: Flower types may vary slightly depending on availability while maintaining the overall look and colour theme.</p>
          <button type="button" class="btn btn-outline enquire-btn" data-bouquet="Blush Basket">Enquire</button>
        </li>
        <li class="bouquet-card">
          <div class="card-media">
            <img src="images/2.PNG" alt="Princess Treatment Basket — a pink rose gift basket with beauty add-ons tucked among the flowers">
          </div>
          <h3>Princess Treatment Basket</h3>
          <p class="price">&pound;65</p>
          <p class="card-desc">A luxurious floral gift basket designed to feel extra special. Featuring soft pink tones and premium flowers, this arrangement is perfect for birthdays, surprises, or treating someone like royalty.</p>
          <ul class="card-list">
            <li>Fresh flower arrangement</li>
            <li>Decorative basket with ribbon</li>
          </ul>
          <p class="card-subhead">Optional add-ons</p>
          <ul class="card-list card-list-options">
            <li>&#128140; Full Makeup Set (+&pound;50)</li>
            <li>&#127800; Perfume Add-On (price varies)</li>
          </ul>
          <p class="card-note">Note: Images may include add-ons for display purposes. Final design may vary depending on selected extras.</p>
          <button type="button" class="btn btn-outline enquire-btn" data-bouquet="Princess Treatment Basket">Enquire</button>
        </li>
        <li class="bouquet-card">
          <div class="card-media">
            <img src="images/3.PNG" alt="Luxury Chocolate Gift Cake — heart and round chocolate arrangements finished with roses and ribbon">
          </div>
          <h3>Luxury Chocolate Gift Cake</h3>
          <p class="price">&pound;65</p>
          <p class="card-desc">A beautifully crafted chocolate arrangement designed to look like a cake, perfect for gifting on special occasions. Made with premium chocolates and finished with elegant details. Each design is carefully handmade, making every piece unique.</p>
          <ul class="card-list">
            <li>Size: approx. 25cm</li>
            <li>Available shapes: Heart or Round</li>
            <li>Colour options: Red, White, or Custom</li>
            <li>Personalisation: initials or message included</li>
          </ul>
          <p class="card-note">Note: Designs may vary slightly depending on shape and colour selection. Add-ons are available — please enquire for more details.</p>
          <button type="button" class="btn btn-outline enquire-btn" data-bouquet="Luxury Chocolate Gift Cake">Enquire</button>
        </li>
        <li class="bouquet-card">
          <div class="card-media card-carousel" data-carousel>
            <div class="carousel-track">
              <img src="images/4.PNG" alt="Luxury Heart Rose Box — red and white roses arranged in a heart-shaped box" class="is-active">
              <img src="images/4.1.PNG" alt="Luxury Heart Rose Box — alternate view of the heart-shaped rose box">
            </div>
            <button type="button" class="carousel-arrow carousel-prev" aria-label="Previous photo">&#8249;</button>
            <button type="button" class="carousel-arrow carousel-next" aria-label="Next photo">&#8250;</button>
            <div class="carousel-dots">
              <button type="button" class="carousel-dot is-active" aria-label="Show photo 1"></button>
              <button type="button" class="carousel-dot" aria-label="Show photo 2"></button>
            </div>
          </div>
          <h3>Luxury Heart Rose Box</h3>
          <p class="price">From &pound;70</p>
          <p class="card-desc">A stunning heart-shaped rose arrangement designed to make a lasting impression. Perfect for anniversaries, birthdays, and special occasions. Each rose box is carefully arranged to create a full, luxurious look.</p>
          <p class="card-subhead">Available sizes</p>
          <ul class="card-list card-list-options">
            <li>Small (25 roses) — &pound;70</li>
            <li>Medium (50 roses) — &pound;140</li>
            <li>Large (75 roses) — &pound;170</li>
          </ul>
          <p class="card-subhead">Colour options</p>
          <ul class="card-list card-list-options">
            <li>Red</li>
            <li>White</li>
            <li>Pink</li>
            <li>Red &amp; White Mix</li>
          </ul>
          <p class="card-note">Note: Design and rose placement may vary slightly depending on size and colour selection.</p>
          <button type="button" class="btn btn-outline enquire-btn" data-bouquet="Luxury Heart Rose Box">Enquire</button>
        </li>
        <li class="bouquet-card">
          <div class="card-media card-carousel" data-carousel>
            <div class="carousel-track">
              <img src="images/5.jpg.jpeg" alt="Signature Rose Bouquet — a full bouquet of blush and burgundy roses in pink wrap" class="is-active">
              <img src="images/5.1.jpg.jpeg" alt="Signature Rose Bouquet — red roses in black wrap with a personalised initial and ribbon message">
            </div>
            <button type="button" class="carousel-arrow carousel-prev" aria-label="Previous photo">&#8249;</button>
            <button type="button" class="carousel-arrow carousel-next" aria-label="Next photo">&#8250;</button>
            <div class="carousel-dots">
              <button type="button" class="carousel-dot is-active" aria-label="Show photo 1"></button>
              <button type="button" class="carousel-dot" aria-label="Show photo 2"></button>
            </div>
          </div>
          <h3>Signature Rose Bouquet</h3>
          <p class="price">From &pound;130</p>
          <p class="card-desc">A full, luxury bouquet designed to make a bold statement. Featuring premium roses, elegant wrapping, and a clean, high-end finish — perfect for birthdays, anniversaries, and special occasions.</p>
          <p class="card-subhead">Available sizes</p>
          <ul class="card-list card-list-options">
            <li>50 Roses — &pound;130</li>
            <li>75 Roses — &pound;170</li>
            <li>100 Roses — &pound;220</li>
          </ul>
          <p class="card-subhead">Wrapping options (included)</p>
          <ul class="card-list card-list-options">
            <li>Pink</li>
            <li>Black</li>
            <li>White</li>
          </ul>
          <p class="card-subhead">Optional add-ons</p>
          <ul class="card-list card-list-options">
            <li>Initials (letters on bouquet) +&pound;5</li>
            <li>Personalised ribbon message +&pound;5</li>
          </ul>
          <button type="button" class="btn btn-outline enquire-btn" data-bouquet="Signature Rose Bouquet">Enquire</button>
        </li>
      </ul>
```

- [ ] **Step 4: Update the enquiry form's product field label and options**

Change:
```html
          <div class="field">
            <label for="bouquet">Bouquet of interest</label>
            <select id="bouquet" name="bouquet">
              <option value="">Not sure yet</option>
              <option>Blush Romance</option>
              <option>Eternal Grace</option>
              <option>Pure Devotion</option>
              <option>Couture Peonies</option>
              <option>Something custom</option>
            </select>
          </div>
```
to:
```html
          <div class="field">
            <label for="bouquet">Item of interest</label>
            <select id="bouquet" name="bouquet">
              <option value="">Not sure yet</option>
              <option>Blush Basket</option>
              <option>Princess Treatment Basket</option>
              <option>Luxury Chocolate Gift Cake</option>
              <option>Luxury Heart Rose Box</option>
              <option>Signature Rose Bouquet</option>
              <option>Something custom</option>
            </select>
          </div>
```

- [ ] **Step 5: Verify structure in the browser**

Run `python3 -m http.server 8000` (background), then Playwright `browser_navigate` to `http://localhost:8000` and take a snapshot.
Expected: nav shows "Collection"; `#bouquets` heading reads "Our Collection"; 5 `bouquet-card` items present with the 5 product names, prices ("£55", "£65", "£65", "From £70", "From £130"), and Enquire buttons; the "Item of interest" dropdown has the 5 new product names plus "Not sure yet" and "Something custom".

- [ ] **Step 6: Commit**

```bash
git add index.html && git commit -m "feat: replace placeholder bouquets with real 5-product catalog"
```

---

### Task 2: Card & carousel styling in `css/style.css`

**Files:**
- Modify: `css/style.css` (the `/* ── Bouquets ── */` section, `css/style.css:315-351`)

**Interfaces:**
- Consumes: DOM contract from Task 1 (`.card-media`, `.card-carousel`, `.carousel-track`, `.carousel-prev`/`.carousel-next`, `.carousel-dots`/`.carousel-dot`, `.card-desc`, `.card-subhead`, `.card-list`/`.card-list-options`, `.card-note`).
- Produces: visual rule that `.is-active` on a carousel `img`/`.carousel-dot` = the currently shown photo/dot (Task 3's JS toggles this class; no other class name is used for "active").

- [ ] **Step 1: Replace the grid column count and card image rule, and add new card content + carousel styles**

Change the 1000px breakpoint rule:
```css
@media (min-width: 1000px) {
  .bouquet-grid { grid-template-columns: repeat(4, 1fr); }
}
```
to:
```css
@media (min-width: 1000px) {
  .bouquet-grid { grid-template-columns: repeat(3, 1fr); }
}
```

Replace the existing `.bouquet-card img` rule:
```css
.bouquet-card img {
  border-radius: 4px;
  box-shadow: 0 14px 30px -18px rgba(169, 106, 116, 0.4);
}
```
with a `.card-media` wrapper rule (covers both plain-photo and carousel cards) plus the new content and carousel styles, inserted directly after it in the same `/* ── Bouquets ── */` section:
```css
.card-media {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 4px;
  box-shadow: 0 14px 30px -18px rgba(169, 106, 116, 0.4);
}

.card-media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.card-desc,
.card-note,
.card-list {
  text-align: left;
}

.card-desc {
  font-size: 0.92rem;
  margin: 0.9rem 0;
}

.card-subhead {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold);
  text-align: left;
  margin: 1rem 0 0.4rem;
}

.card-list {
  list-style: disc;
  font-size: 0.88rem;
  margin: 0 0 0.3rem;
  padding-left: 1.15rem;
}

.card-list li { margin-bottom: 0.25rem; }

.card-note {
  font-size: 0.78rem;
  font-style: italic;
  opacity: 0.85;
  margin: 0.9rem 0 1.1rem;
}

/* Carousel (products with 2 photos) */

.card-carousel .carousel-track {
  position: relative;
  width: 100%;
  height: 100%;
}

.card-carousel img {
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-carousel img.is-active { opacity: 1; }

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: rgba(253, 248, 242, 0.85);
  color: var(--ink);
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s ease;
}

.carousel-arrow:hover { background: var(--cream-card); }

.carousel-prev { left: 8px; }
.carousel-next { right: 8px; }

.carousel-dots {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
}

.carousel-dot {
  width: 7px;
  height: 7px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: rgba(253, 248, 242, 0.65);
  cursor: pointer;
}

.carousel-dot.is-active { background: var(--cream-card); box-shadow: 0 0 0 1px var(--gold); }
```

- [ ] **Step 2: Verify visually at both widths**

Playwright: `browser_resize` 1280×900 → screenshot of `#bouquets`; `browser_resize` 375×800 → screenshot of `#bouquets`; `browser_evaluate` `document.documentElement.scrollWidth <= 375` at the mobile width.
Expected: 3-column grid ≥1000px (3 cards top row, 2 below), 2-column ≥560px, 1-column below; card photos crop to a square via `object-fit: cover` with no distortion; carousel arrows/dots visible and legible over the photo on products 4 & 5; no horizontal overflow at 375px.

- [ ] **Step 3: Commit**

```bash
git add css/style.css && git commit -m "style: card content layout and photo carousel for the product catalog"
```

---

### Task 3: Carousel behavior in `js/main.js`

**Files:**
- Modify: `js/main.js` (add a new block; existing nav/pre-selection/form code is untouched and needs no changes since `data-bouquet` values and the `#bouquet` select still line up)

**Interfaces:**
- Consumes: `.card-carousel` wrapper, `.carousel-track img`, `.carousel-prev`/`.carousel-next`, `.carousel-dot` from Task 1; `.is-active` styling contract from Task 2.

- [ ] **Step 1: Add the carousel behavior block**

Add this block to `js/main.js`, after the "Mobile navigation" block and before the "Pre-selection from bouquet cards and occasion tiles" block:

```js
// ── Product photo carousels ──────────────────────────────────────
document.querySelectorAll(".card-carousel").forEach((carousel) => {
  const images = carousel.querySelectorAll(".carousel-track img");
  const dots = carousel.querySelectorAll(".carousel-dot");
  let activeIndex = 0;

  function show(nextIndex) {
    images[activeIndex].classList.remove("is-active");
    dots[activeIndex].classList.remove("is-active");
    activeIndex = (nextIndex + images.length) % images.length;
    images[activeIndex].classList.add("is-active");
    dots[activeIndex].classList.add("is-active");
  }

  carousel.querySelector(".carousel-prev").addEventListener("click", () => show(activeIndex - 1));
  carousel.querySelector(".carousel-next").addEventListener("click", () => show(activeIndex + 1));
  dots.forEach((dot, dotIndex) => dot.addEventListener("click", () => show(dotIndex)));
});
```

- [ ] **Step 2: Verify carousel behavior in the browser (Playwright)**

At 1280×900:
1. Navigate to `http://localhost:8000`, find the "Luxury Heart Rose Box" card. Confirm the first image (`4.PNG`) is visible (has `is-active`) and the second is not.
2. Click its `.carousel-next` button → confirm the second image (`4.1.PNG`) now has `is-active` and the second dot has `is-active`.
3. Click `.carousel-prev` → confirm it returns to the first image/dot.
4. Click the second `.carousel-dot` directly on the "Signature Rose Bouquet" card → confirm its second image (`5.1.jpg.jpeg`) becomes active.
5. Click "Enquire" on the "Luxury Heart Rose Box" card → confirm `#bouquet` select value becomes "Luxury Heart Rose Box" and the page scrolls to `#enquiry` (existing pre-selection behavior, now exercised with a real product name).
6. Click the "Collection" nav link → confirm it scrolls to `#bouquets`.

Expected: all six checks pass; no console errors (`browser_console_messages`).

- [ ] **Step 3: Commit**

```bash
git add js/main.js && git commit -m "feat: add click-through photo carousel for multi-photo products"
```

---

### Task 4: README update + full verification

**Files:**
- Modify: `README.md` (the "Replace the placeholder images" and "Edit bouquets, prices, and copy" sections, which still describe the old 4-placeholder-SVG setup)

**Interfaces:**
- None (documentation only).

- [ ] **Step 1: Update the README's image and copy-editing sections**

Replace:
```markdown
## Replace the placeholder images

The soft pink illustrations in `images/` are placeholders. To use real photos:

1. Drop your photo into `images/` (e.g. `images/bouquet-1.jpg`).
2. In `index.html`, find the matching `<!-- REPLACE with a real photo -->` comment and update the `src` on the line below it.

Slots: `hero.svg` (main photo), `bouquet-1.svg` … `bouquet-4.svg` (the four bouquet cards), `story.svg` (About photo). Portrait-orientation photos work best (roughly 5:6).

## Edit bouquets, prices, and copy

Everything is plain text in `index.html`:

- **Bouquet names and prices** — the `bouquet-card` blocks in the "Our Bouquets" section. If you rename a bouquet, also update its `data-bouquet` attribute and the matching `<option>` in the "Bouquet of interest" dropdown.
- **Contact details** — email, phone, and Instagram links in the footer.
- **Announcement bar, story text, thank-you message** — edit in place.
```
with:
```markdown
## Replace or add product photos

Product photos live in `images/` (`1.PNG`, `2.PNG`, `3.PNG`, `4.PNG`/`4.1.PNG`, `5.jpg.jpeg`/`5.1.jpg.jpeg`). To swap one out, drop the new file into `images/` and update the matching `<img src="...">` in the `#bouquets` section of `index.html`. Cards are square-cropped (`object-fit: cover`), so any photo aspect ratio works. The hero and Our Story photos (`hero.svg`, `story.svg`) are separate and still placeholders — see the section below.

Two products (Luxury Heart Rose Box, Signature Rose Bouquet) show a 2-photo carousel. To add a second photo to any other product, wrap its `<img>` in a `<div class="card-media card-carousel" data-carousel>` with a `.carousel-track` containing both images plus the arrow/dot buttons — copy the markup from one of the existing carousel cards.

## Replace the remaining placeholder images

`hero.svg` (hero photo) and `story.svg` (Our Story photo) are still on-brand SVG placeholders. Drop a real photo into `images/`, then update the matching `src` next to the `<!-- REPLACE with a real photo -->` comment in `index.html`.

## Edit products, prices, and copy

Everything is plain text in `index.html`:

- **Product names, prices, descriptions, and options** — the `bouquet-card` blocks in the "Our Collection" section. If you rename a product, also update its `data-bouquet` attribute and the matching `<option>` in the "Item of interest" dropdown.
- **Contact details** — email, phone, and Instagram links in the footer.
- **Announcement bar, story text, thank-you message** — edit in place.
```

- [ ] **Step 2: Full verification pass**

With the server still running, use Playwright to re-run the checklist from the design spec's Testing section:
- All 5 cards show correct name/price/description/includes/options/note text (spot-check against `docs/superpowers/specs/2026-07-28-product-catalog-update-design.md`).
- Both carousels work (arrow + dot clicks).
- Enquire buttons pre-select the right dropdown option for all 5 products.
- Nav "Collection" link and heading "Our Collection" both correct.
- Full-page screenshots at 375×800 and 1280×900, no horizontal overflow at 375px.
- Existing nav/hamburger, occasions tiles, and form validation still work unchanged (quick smoke check — these were not touched by this plan).

- [ ] **Step 3: Commit**

```bash
git add README.md && git commit -m "docs: update README for the real product catalog"
```
