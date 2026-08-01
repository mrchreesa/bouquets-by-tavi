# Enquiry Form Custom Order Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing "Send an Enquiry" form on `index.html` clearly support fully custom bouquet orders, by clarifying the copy and revealing two optional detail fields when the customer picks "Something custom".

**Architecture:** This is a static site with no build step and no test framework — `index.html` (markup), `css/style.css` (styles), `js/main.js` (vanilla JS, no dependencies). Changes are plain HTML/CSS additions plus a small `change`-listener addition in `main.js` that toggles a `hidden` attribute, following the same pattern already used for `.field-error` and `#form-success` in that file. Verification is manual, via a local static server and a real browser (no automated test suite exists in this repo).

**Tech Stack:** HTML5, CSS3, vanilla JavaScript (ES6), Formspree (unchanged).

## Global Constraints

- No new required fields — the two new fields (Budget range, Colour & style preference) must stay optional so submission can never be blocked by them.
- No changes to `validate()` or the Formspree submit handler in `js/main.js` — `FormData` already picks up any input present in the `<form>`, hidden or not.
- Match existing code conventions exactly: `id`/`name` casing (`kebab-case` ids, `snake_case` names, e.g. existing `needed-by` / `needed_by`), the `.field` / `.form-row` / `.optional` class structure, and the `hidden` attribute (not a CSS class) for show/hide state, as already used for `.field-error` and `#form-success`.
- Preview via `python3 -m http.server 8000` from the repo root, then `http://localhost:8000` (per `README.md`) — do not invent a different dev server.

---

### Task 1: Clarify the enquiry section copy

**Files:**
- Modify: `index.html:272-323` (section subheading + "Item of interest" field)
- Modify: `css/style.css` (add `.field-hint` rule near the existing `.field-error` rule, `css/style.css:703-710`)

**Interfaces:**
- Produces: `.field-hint` CSS class, usable by Task 2 if needed (it is not needed there, but must exist for this task's markup to render correctly).

- [ ] **Step 1: Update the section subheading**

In `index.html`, find:
```html
      <p class="section-sub">Tell us about your occasion and we&rsquo;ll craft something beautiful together.</p>
```
Replace with:
```html
      <p class="section-sub">Tell us about your occasion &mdash; from our signature pieces to a fully custom design &mdash; and we&rsquo;ll craft something beautiful together.</p>
```

- [ ] **Step 2: Add the helper line under "Item of interest"**

In `index.html`, find the "Item of interest" field:
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
Replace with (adds one `<p class="field-hint">` line before the closing `</div>`):
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
            <p class="field-hint">Choosing &ldquo;Something custom&rdquo; below unlocks a couple of quick questions so we can design something just for you.</p>
          </div>
```

- [ ] **Step 3: Add the `.field-hint` style**

In `css/style.css`, find:
```css
.field-error {
  color: var(--error);
  font-size: 0.82rem;
  font-weight: 400;
  margin-top: 0.4rem;
}
```
Add directly after it:
```css

.field-hint {
  color: var(--text);
  font-size: 0.82rem;
  font-weight: 300;
  margin-top: 0.4rem;
}
```

- [ ] **Step 4: Verify visually**

Run `python3 -m http.server 8000` from the repo root, open `http://localhost:8000`, scroll to "Send an Enquiry". Confirm:
- The subheading reads "...from our signature pieces to a fully custom design...".
- A small muted line appears under the "Item of interest" dropdown reading "Choosing "Something custom" below unlocks a couple of quick questions so we can design something just for you."
- The line does not look like an error (no red/pink coloring) — it should read as neutral/muted text, same size as the existing field-error text but in the normal text color.

- [ ] **Step 5: Commit**

```bash
git add index.html css/style.css
git commit -m "content: clarify that the enquiry form supports custom orders"
```

---

### Task 2: Add conditional custom-order fields

**Files:**
- Modify: `index.html:298-324` (insert a new `.form-row` after the Occasion/Item-of-interest row, before the Message field)
- Modify: `js/main.js:49-70` (add the toggle behavior)

**Interfaces:**
- Consumes: `.field-hint` styling from Task 1 (not directly used by this task's new markup, but Task 1 must already be applied to this file).
- Consumes: existing `bouquetSelect` constant (`js/main.js:50`), existing `.enquire-btn` click handler (`js/main.js:58-63`).
- Produces: `#custom-order-fields` wrapper div (id used only by this task), `#budget` / `#style-preference` form inputs whose values flow into the existing unmodified Formspree `FormData` submission.

- [ ] **Step 1: Add the new fields to the form markup**

In `index.html`, find the closing of the Occasion/Item-of-interest row (right after the `</div>` that closes the "Item of interest" `.field` added in Task 1, and right before the Message `.field`):
```html
        </div>
        <div class="field">
          <label for="message">Message <span aria-hidden="true">*</span></label>
```
Replace with (inserts a new hidden-by-default `.form-row` in between):
```html
        </div>
        <div class="form-row" id="custom-order-fields" hidden>
          <div class="field">
            <label for="budget">Budget range <span class="optional">(optional)</span></label>
            <select id="budget" name="budget">
              <option value="">Not sure yet</option>
              <option>Under &pound;50</option>
              <option>&pound;50&ndash;&pound;100</option>
              <option>&pound;100+</option>
            </select>
          </div>
          <div class="field">
            <label for="style-preference">Colour &amp; style preference <span class="optional">(optional)</span></label>
            <input type="text" id="style-preference" name="style_preference" placeholder="Pastels, bold reds, wildflower look&hellip;">
          </div>
        </div>
        <div class="field">
          <label for="message">Message <span aria-hidden="true">*</span></label>
```

- [ ] **Step 2: Add the toggle behavior in `main.js`**

In `js/main.js`, find:
```js
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
```
Replace with:
```js
const bouquetSelect = document.getElementById("bouquet");
const occasionSelect = document.getElementById("occasion");
const enquirySection = document.getElementById("enquiry");
const customOrderFields = document.getElementById("custom-order-fields");

function scrollToForm() {
  enquirySection.scrollIntoView({ behavior: "smooth" });
}

function toggleCustomOrderFields() {
  customOrderFields.hidden = bouquetSelect.value !== "Something custom";
}

bouquetSelect.addEventListener("change", toggleCustomOrderFields);
toggleCustomOrderFields();

document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    bouquetSelect.value = button.dataset.bouquet;
    toggleCustomOrderFields();
    scrollToForm();
  });
});
```

- [ ] **Step 3: Verify the toggle behavior in a real browser**

Run `python3 -m http.server 8000` from the repo root (if not already running) and open `http://localhost:8000`.

1. Scroll to "Send an Enquiry".
2. Confirm the "Budget range" / "Colour & style preference" row is NOT visible initially.
3. Select "Something custom" from "Item of interest". Confirm the new row appears immediately, showing "Budget range" (a select defaulting to "Not sure yet", with options "Under £50", "£50–£100", "£100+") and "Colour & style preference" (a text input with placeholder "Pastels, bold reds, wildflower look…").
4. Change "Item of interest" to any other option (e.g. "Blush Basket"). Confirm the row disappears again.
5. Select "Something custom" again, fill in both new fields, then click any `.enquire-btn` ("Enquire" button on a product card). Confirm the row hides again (since the button sets a specific product, not "Something custom") and the page scrolls to the form.
6. Fill in Name, Email, and Message, then submit. Since `FORMSPREE_ID` is still `"YOUR_FORM_ID"` (unchanged), confirm the existing "form isn't connected yet" fallback message still appears — i.e. submission behavior for the rest of the form is unaffected.

- [ ] **Step 4: Commit**

```bash
git add index.html js/main.js
git commit -m "feat: reveal budget and style fields when a custom order is selected"
```

---

## Out of Scope

No new required fields, no file/image upload for style inspiration, no changes to the Formspree submission logic or the "not connected yet" fallback behavior (per the design spec, `docs/superpowers/specs/2026-08-01-enquiry-form-custom-orders-design.md`).
