# Enquiry Form Intent Paths Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the single nine-field enquiry form on `index.html` with an explicit intent choice ("Order from the collection" / "Design something custom") followed by a seven-field form that renders only the chosen path's fields.

**Architecture:** Static site, no build step, no test framework — `index.html` (markup), `css/style.css` (styles), `js/main.js` (vanilla ES6, no dependencies). The intent choice is a pair of radio inputs styled as tiles, reusing the visual language of the existing `.occasion-tile`. Two `<fieldset>` elements hold the path-specific fields and are toggled with both `hidden` and `disabled` — `disabled` keeps the inactive path out of `FormData` so Formspree never receives both paths' keys. A shared details block holds the fields common to both paths, so no `id` or `name` is ever duplicated. Verification is manual in a real browser; this repo has no automated test suite.

**Tech Stack:** HTML5, CSS3 (`:has()` selector), vanilla JavaScript (ES6), Formspree (submission flow unchanged).

## Global Constraints

- **Preserve existing `name` attributes** so submissions stay consistent with anything already in the Formspree inbox: `name`, `email`, `needed_by`, `occasion`, `bouquet`, `budget`, `message`. `fulfilment` is the only genuinely new one. `intent` is added for the radio group.
- **Two fields are removed outright:** `phone` and `style_preference`. Do not preserve them.
- **No changes to the Formspree submit flow** or the "not connected yet" fallback behaviour, beyond the button-label fix in Task 6.
- **Do not touch `FORMSPREE_ID`** in `js/main.js` (per `AGENTS.md` — it is live production config).
- **Match existing conventions exactly:** kebab-case `id`s, snake_case `name`s (e.g. `needed-by` / `needed_by`), the `.field` / `.form-row` / `.optional` class structure, and the `hidden` attribute (not a CSS class) for show/hide state.
- **Progressive enhancement:** markup ships with every fieldset visible. JS hides them on init. With JS disabled the form degrades to one long working form, never to an empty section.
- **Preview with `python3 -m http.server 8000`** from the repo root, then `http://localhost:8000` (per `README.md`). If port 8000 is occupied by another project, use `8123`.
- **Do not push to `main` without explicit approval** — this repo auto-deploys to flowersbytavi.co.uk on merge, with no staging environment.
- **The submit button already reads "Submit"** (committed in `df90ab7`, before this plan began). Task 2 replaces that whole block and carries `Submit` forward — keep it that way; do not restore the old "Send Enquiry / Customise Orders" label.
- **Formspree is being replaced entirely in a follow-on phase** (self-hosted backend on Vercel sending via Outlook SMTP). That is out of scope here. Do not remove, rewire, or "tidy up" the Formspree submission code in this plan — the restructure lands first so the backend can be built against the final field names.

---

### Task 1: Add the intent cards

**Files:**
- Modify: `index.html` (enquiry section heading + top of `#enquiry-form`)
- Modify: `css/style.css` (new rules after the `.field-hint` rule)

**Interfaces:**
- Produces: radio group `input[name="intent"]` with the exact values `"Order from the collection"` and `"Design something custom"`. Tasks 3, 4 and 5 match on these strings verbatim.
- Produces: CSS classes `.intent-fieldset`, `.intent-grid`, `.intent-card`.

- [ ] **Step 1: Replace the section heading and subheading**

In `index.html`, find:
```html
      <p class="kicker">Get in touch</p>
      <h2>Send an Enquiry / Customise Orders</h2>
      <p class="section-sub">Tell us about your occasion &mdash; from our signature pieces to a fully custom design &mdash; and we&rsquo;ll craft something beautiful together.</p>
```
Replace with:
```html
      <p class="kicker">Get in touch</p>
      <h2>What can we help you with?</h2>
      <p class="section-sub">Pick the option that fits and we&rsquo;ll take it from there.</p>
```

- [ ] **Step 2: Insert the intent cards at the top of the form**

In `index.html`, find the opening form tag and the first row that follows it:
```html
      <form id="enquiry-form" class="enquiry-form" novalidate>
        <div class="form-row">
          <div class="field">
            <label for="name">Name <span aria-hidden="true">*</span></label>
```
Insert the intent fieldset immediately after the `<form ...>` line, so it reads:
```html
      <form id="enquiry-form" class="enquiry-form" novalidate>
        <fieldset class="intent-fieldset">
          <legend class="visually-hidden">What can we help you with?</legend>
          <div class="intent-grid">
            <label class="intent-card">
              <input type="radio" name="intent" value="Order from the collection" class="visually-hidden">
              <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true">
                <path d="M16 27 v-9"/><path d="M16 18 q -7 -1 -7 -9 q 7 1 7 9"/><path d="M16 18 q 7 -1 7 -9 q -7 1 -7 9"/><path d="M11 24 h10"/>
              </svg>
              <span>Order from the collection</span>
            </label>
            <label class="intent-card">
              <input type="radio" name="intent" value="Design something custom" class="visually-hidden">
              <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true">
                <path d="M16 5 v7 M16 20 v7 M5 16 h7 M20 16 h7"/><path d="M9.5 9.5 l4 4 M18.5 18.5 l4 4 M22.5 9.5 l-4 4 M13.5 18.5 l-4 4"/>
              </svg>
              <span>Design something custom</span>
            </label>
          </div>
        </fieldset>
        <div class="form-row">
          <div class="field">
            <label for="name">Name <span aria-hidden="true">*</span></label>
```

- [ ] **Step 3: Add the intent card styles**

In `css/style.css`, find the `.field-hint` rule:
```css
.field-hint {
  color: var(--text);
  font-size: 0.82rem;
  font-weight: 300;
  margin-top: 0.4rem;
}
```
Insert immediately after it:
```css
.intent-fieldset {
  border: 0;
  padding: 0;
  margin: 0 0 1.8rem;
}

.intent-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.intent-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem;
  padding: 1.5rem 0.75rem 1.2rem;
  text-align: center;
  background: var(--cream-card);
  border: 1px solid rgba(185, 150, 104, 0.28);
  border-radius: 999px 999px 10px 10px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.intent-card:hover {
  transform: translateY(-4px);
  border-color: var(--gold);
  box-shadow: 0 14px 26px -16px rgba(169, 106, 116, 0.5);
}

.intent-card svg { width: 30px; height: 30px; color: var(--gold); }

.intent-card span {
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink);
}

.intent-card:has(input:checked) {
  border-color: var(--rose-dark);
  background: var(--blush-light);
  box-shadow: 0 14px 26px -18px rgba(169, 106, 116, 0.6);
}

.intent-card:has(input:focus-visible) {
  outline: 2px solid var(--rose);
  outline-offset: 2px;
}
```

- [ ] **Step 4: Verify the cards render and select**

Run: `python3 -m http.server 8000` from the repo root, open `http://localhost:8000#enquiry`.

Expected:
- Two tiles side by side above the form, matching the rounded-top shape of the occasion tiles.
- Clicking either tile visibly selects it (blush background, rose border); clicking the other moves the selection.
- Pressing `Tab` reaches the group and arrow keys move between the two options, with a visible focus ring on the tile.
- The rest of the form is unchanged and still visible below.

- [ ] **Step 5: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add intent cards to the enquiry form"
```

---

### Task 2: Restructure the form fields into path fieldsets and a shared block

**Files:**
- Modify: `index.html` (everything inside `#enquiry-form` below the intent fieldset)
- Modify: `css/style.css` (radio row + fieldset reset rules)

**Interfaces:**
- Consumes: the `.intent-fieldset` markup from Task 1.
- Produces: `#path-collection`, `#path-custom`, `#enquiry-details` — the three containers Task 3 toggles.
- Produces: `#bouquet` (select, required on the collection path), `#budget` (select), `#occasion`, `#needed-by`, `#message`, `input[name="fulfilment"]`.

This task is markup only. Everything stays visible and the form keeps submitting; Task 3 adds the hiding.

- [ ] **Step 1: Replace the form body**

In `index.html`, find everything from the first `<div class="form-row">` after the intent fieldset down to and including the closing `</form>`:
```html
        <div class="form-row">
          <div class="field">
            <label for="name">Name <span aria-hidden="true">*</span></label>
```
…through…
```html
        <button type="submit" class="btn">Submit</button>
        <p class="form-status" role="status" aria-live="polite" hidden></p>
      </form>
```
Replace that entire block with:
```html
        <fieldset id="path-collection" class="path-fieldset">
          <legend class="visually-hidden">Your piece</legend>
          <div class="field">
            <label for="bouquet">Which piece <span aria-hidden="true">*</span></label>
            <select id="bouquet" name="bouquet">
              <option value="">Choose a piece&hellip;</option>
              <option>Blush Basket</option>
              <option>Princess Treatment Basket</option>
              <option>Luxury Chocolate Gift Cake</option>
              <option>Luxury Rose Box</option>
              <option>Signature Rose Bouquet</option>
              <option>Not sure yet</option>
            </select>
            <p class="field-error" hidden>Please choose which piece you&rsquo;re interested in.</p>
          </div>
        </fieldset>

        <fieldset id="path-custom" class="path-fieldset">
          <legend class="visually-hidden">Your custom design</legend>
          <div class="field">
            <label for="budget">Budget range <span class="optional">(optional)</span></label>
            <select id="budget" name="budget">
              <option value="">Not sure yet</option>
              <option>Under &pound;50</option>
              <option>&pound;50&ndash;&pound;100</option>
              <option>&pound;100+</option>
            </select>
          </div>
        </fieldset>

        <div id="enquiry-details">
          <div class="form-row">
            <div class="field">
              <label for="occasion">Occasion <span class="optional">(optional)</span></label>
              <select id="occasion" name="occasion">
                <option value="">Choose an occasion&hellip;</option>
                <option>Birthday</option>
                <option>Anniversary</option>
                <option>Romance</option>
                <option>Congratulations</option>
                <option>Thank You</option>
                <option>Sympathy</option>
                <option>Other</option>
              </select>
            </div>
            <div class="field">
              <label for="needed-by">When for <span class="optional">(optional)</span></label>
              <input type="date" id="needed-by" name="needed_by">
            </div>
          </div>
          <div class="field">
            <span class="field-label">Delivery or pickup <span class="optional">(optional)</span></span>
            <div class="radio-row">
              <label class="radio-option">
                <input type="radio" name="fulfilment" value="Delivery"> Delivery
              </label>
              <label class="radio-option">
                <input type="radio" name="fulfilment" value="Pickup"> Pickup
              </label>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="name">Name <span aria-hidden="true">*</span></label>
              <input type="text" id="name" name="name" required autocomplete="name">
              <p class="field-error" hidden>Please tell us your name.</p>
            </div>
            <div class="field">
              <label for="email">Email <span aria-hidden="true">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email">
              <p class="field-error" hidden>Please enter a valid email address.</p>
            </div>
          </div>
          <div class="field">
            <label for="message">Anything else <span class="optional">(optional)</span></label>
            <textarea id="message" name="message" rows="5" placeholder="Size, colours, a note for the card&hellip;"></textarea>
            <p class="field-error" hidden>Please tell us a little about what you&rsquo;re looking for.</p>
          </div>
          <button type="submit" class="btn">Submit</button>
          <p class="form-status" role="status" aria-live="polite" hidden></p>
        </div>
      </form>
```

- [ ] **Step 2: Add the fieldset and radio-row styles**

In `css/style.css`, find the `.intent-card:has(input:focus-visible)` rule added in Task 1 and insert immediately after it:
```css
.path-fieldset {
  border: 0;
  padding: 0;
  margin: 0;
}

.path-fieldset[hidden] { display: none; }

#enquiry-details[hidden] { display: none; }

.field-label {
  display: block;
  font-size: 0.74rem;
  font-weight: 400;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 0.45rem;
}

.radio-row { display: flex; gap: 1.6rem; }

.field .radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
  font-size: 0.95rem;
  font-weight: 300;
  letter-spacing: 0.04em;
  text-transform: none;
  color: var(--ink);
  cursor: pointer;
}

.field .radio-option input {
  width: auto;
  margin: 0;
  padding: 0;
  accent-color: var(--rose-dark);
}
```

- [ ] **Step 3: Verify the restructured form**

Reload `http://localhost:8000#enquiry`.

Expected:
- Field order top to bottom: intent cards, Which piece, Budget range, Occasion + When for, Delivery/Pickup radios, Name + Email, Anything else, Submit.
- The Delivery/Pickup label matches the other field labels (uppercase, letter-spaced), and the two radio options sit on one row in normal sentence case — **not** stretched full-width or uppercased.
- No Phone field and no "Colour & style preference" field anywhere.
- The "Which piece" dropdown has no "Something custom" option.

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "refactor: split enquiry form into path fieldsets and shared details"
```

---

### Task 3: Wire the path toggle

**Files:**
- Modify: `js/main.js` (replace the custom-order toggle block)

**Interfaces:**
- Consumes: `input[name="intent"]`, `#path-collection`, `#path-custom`, `#enquiry-details`, `#message` from Tasks 1–2.
- Produces: `selectedIntent()` returning the checked intent value or `""`, and `applyIntent()` which reconciles all visibility and message-field state. Tasks 4 and 5 call both.

- [ ] **Step 1: Replace the custom-order toggle block**

In `js/main.js`, find:
```js
// ── Pre-selection from bouquet cards and occasion tiles ──────────
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
```
Replace with:
```js
// ── Pre-selection from bouquet cards and occasion tiles ──────────
const bouquetSelect = document.getElementById("bouquet");
const occasionSelect = document.getElementById("occasion");
const enquirySection = document.getElementById("enquiry");

function scrollToForm() {
  enquirySection.scrollIntoView({ behavior: "smooth" });
}

// ── Enquiry intent paths ─────────────────────────────────────────
const COLLECTION = "Order from the collection";
const CUSTOM = "Design something custom";

const pathFieldsets = {
  [COLLECTION]: document.getElementById("path-collection"),
  [CUSTOM]: document.getElementById("path-custom"),
};
const enquiryDetails = document.getElementById("enquiry-details");
const messageField = document.getElementById("message");
const messageLabel = document.querySelector('label[for="message"]');

// The message field does double duty: an optional extras box when ordering a
// listed piece, and the required design brief when commissioning something new.
const MESSAGE_COPY = {
  [COLLECTION]: {
    label: 'Anything else <span class="optional">(optional)</span>',
    placeholder: "Size, colours, a note for the card…",
    required: false,
  },
  [CUSTOM]: {
    label: 'What you have in mind <span aria-hidden="true">*</span>',
    placeholder: "Colours, style, who it's for…",
    required: true,
  },
};

function selectedIntent() {
  return document.querySelector('input[name="intent"]:checked')?.value || "";
}

function applyIntent() {
  const intent = selectedIntent();
  for (const [value, fieldset] of Object.entries(pathFieldsets)) {
    const active = value === intent;
    fieldset.hidden = !active;
    // `disabled` keeps the inactive path out of FormData entirely, so a
    // submission never carries both paths' keys.
    fieldset.disabled = !active;
  }
  enquiryDetails.hidden = intent === "";

  const copy = MESSAGE_COPY[intent];
  if (copy) {
    messageLabel.innerHTML = copy.label;
    messageField.placeholder = copy.placeholder;
    messageField.required = copy.required;
  }
}

document.querySelectorAll('input[name="intent"]').forEach((radio) => {
  radio.addEventListener("change", applyIntent);
});
applyIntent();
```

- [ ] **Step 2: Verify the toggle**

Reload `http://localhost:8000#enquiry`.

Expected:
- On load, only the heading and the two cards show — no fields, no Submit button.
- Choosing **Order from the collection** reveals "Which piece" plus the shared block; the Budget field stays hidden. The textarea is labelled "Anything else (optional)".
- Choosing **Design something custom** hides "Which piece", reveals "Budget range", and relabels the textarea to "What you have in mind *" with the design-brief placeholder.
- Typing into Name, then switching cards, leaves the typed Name intact.

- [ ] **Step 3: Verify the no-JS fallback**

In browser devtools, disable JavaScript, then reload `http://localhost:8000#enquiry`.

Expected: every field and the Submit button are visible (one long form), rather than an empty section. Re-enable JavaScript afterwards.

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "feat: toggle enquiry form fields by selected intent"
```

---

### Task 4: Rewire the Enquire buttons and occasion tiles

**Files:**
- Modify: `js/main.js` (the `.enquire-btn` handler)

**Interfaces:**
- Consumes: `applyIntent()` and the `COLLECTION` constant from Task 3, `bouquetSelect` and `occasionSelect`.

The occasion-tile handler needs no change — it sets `occasionSelect.value` on an element that is in the DOM from load, so the value persists and is already filled in once a card is chosen. Tiles deliberately do not select a path.

- [ ] **Step 1: Update the Enquire button handler**

In `js/main.js`, find:
```js
document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    bouquetSelect.value = button.dataset.bouquet;
    toggleCustomOrderFields();
    scrollToForm();
  });
});
```
Replace with:
```js
document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const collectionRadio = document.querySelector(
      `input[name="intent"][value="${COLLECTION}"]`
    );
    collectionRadio.checked = true;
    applyIntent();
    bouquetSelect.value = button.dataset.bouquet;
    scrollToForm();
  });
});
```

- [ ] **Step 2: Verify both entry points**

Reload `http://localhost:8000`.

Expected:
- Clicking **Enquire** on the Luxury Rose Box card scrolls to the form, selects the "Order from the collection" tile, reveals the fields, and pre-selects "Luxury Rose Box" in Which piece.
- Clicking the **Birthday** occasion tile scrolls to the form and leaves both cards unselected; after then choosing a card, Occasion already reads "Birthday".

- [ ] **Step 3: Commit**

```bash
git add js/main.js
git commit -m "feat: select the collection path from the Enquire buttons"
```

---

### Task 5: Make validation path-aware

**Files:**
- Modify: `js/main.js` (`validate()` and the input-listener loop)

**Interfaces:**
- Consumes: `selectedIntent()`, `COLLECTION`, `CUSTOM` from Task 3.

`form.elements` still includes controls inside a disabled fieldset, so `form.elements.bouquet` resolves on either path — which is exactly why validation must key off the selected intent rather than off presence.

- [ ] **Step 1: Replace `validate()`**

In `js/main.js`, find:
```js
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
```
Replace with:
```js
function validate() {
  const email = form.elements.email;
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
  const intent = selectedIntent();
  const checks = [
    [form.elements.name, form.elements.name.value.trim() !== ""],
    [email, emailOk],
  ];
  if (intent === COLLECTION) {
    checks.push([form.elements.bouquet, form.elements.bouquet.value !== ""]);
  }
  if (intent === CUSTOM) {
    checks.push([form.elements.message, form.elements.message.value.trim() !== ""]);
  }
  let valid = true;
  for (const [input, ok] of checks) {
    setFieldError(input, !ok);
    if (!ok) valid = false;
  }
  return valid;
}
```

- [ ] **Step 2: Clear the piece error as soon as it is answered**

In `js/main.js`, find:
```js
["name", "email", "message"].forEach((id) => {
  form.elements[id].addEventListener("input", () => setFieldError(form.elements[id], false));
});
```
Replace with:
```js
["name", "email", "message"].forEach((id) => {
  form.elements[id].addEventListener("input", () => setFieldError(form.elements[id], false));
});

bouquetSelect.addEventListener("change", () => setFieldError(bouquetSelect, false));
```

- [ ] **Step 3: Verify per-path validation**

Reload `http://localhost:8000#enquiry`.

Expected:
- **Collection path**, Submit with everything blank → errors on Name, Email and Which piece. The "Anything else" textarea shows **no** error.
- Choose a piece → its error clears immediately.
- **Custom path**, Submit with everything blank → errors on Name, Email and the message field. No error about choosing a piece.
- Fill Name and a valid Email on the collection path, choose a piece, leave the textarea empty, Submit → passes validation and reaches the "form isn't connected yet" notice (expected, since `FORMSPREE_ID` is still `YOUR_FORM_ID`).

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "fix: validate required fields per selected enquiry path"
```

---

### Task 6: Fix the submit-button label reset

**Files:**
- Modify: `js/main.js` (submit handler)

The handler currently restores the hardcoded string `"Send Enquiry"` after a failed send, so any error silently relabels the button — visible today because the button reads "Submit".

- [ ] **Step 1: Capture the real label once, at module scope**

In `js/main.js`, find:
```js
const form = document.getElementById("enquiry-form");
const statusEl = form.querySelector(".form-status");
const successEl = document.getElementById("form-success");
```
Replace with:
```js
const form = document.getElementById("enquiry-form");
const statusEl = form.querySelector(".form-status");
const successEl = document.getElementById("form-success");
const submitButton = form.querySelector('[type="submit"]');
const submitLabel = submitButton.textContent;
```

- [ ] **Step 2: Use the captured label in the submit handler**

In `js/main.js`, find:
```js
  const submitButton = form.querySelector('[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Sending…";
```
Replace with:
```js
  submitButton.disabled = true;
  submitButton.textContent = "Sending…";
```

Then find:
```js
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Send Enquiry";
  }
```
Replace with:
```js
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = submitLabel;
  }
```

- [ ] **Step 3: Verify the fix by inspection**

Do **not** modify `FORMSPREE_ID` — it is protected by this plan's Global Constraints and by `AGENTS.md`.

Run: `grep -n 'submitLabel\|submitButton\|Send Enquiry' js/main.js`

Expected:
- `const submitButton = form.querySelector('[type="submit"]');` and `const submitLabel = submitButton.textContent;` each appear exactly once, at module scope.
- No second `const submitButton` declaration inside the submit handler.
- `submitButton.textContent = submitLabel;` appears in the `finally` block.
- The string `"Send Enquiry"` no longer appears anywhere in the file.

Also confirm the constant is untouched: `grep -n 'FORMSPREE_ID = ' js/main.js` must read `const FORMSPREE_ID = "YOUR_FORM_ID";`.

The failed-send path cannot be exercised while the form is unconnected — the handler returns early on the "not connected yet" branch before reaching the `try`/`finally`. It gets exercised end-to-end in the follow-on backend phase, where pointing the API URL at a stopped local server produces a real failure with no production config involved.

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "fix: restore the real submit button label after a failed send"
```

---

### Task 7: Soften the copy that references a checkout

**Files:**
- Modify: `index.html` (Princess Treatment Basket card)
- Modify: `delivery.html` (delivery zones list)

The shop is not live yet, so both strings currently send customers looking for a checkout that does not exist.

- [ ] **Step 1: Rewrite the Princess Treatment Basket note**

In `index.html`, find:
```html
          <p class="card-note">Personalised makeup products are available. Please purchase the standard Princess Treatment Basket at checkout, then send your enquiry with your order number to customise your items.</p>
```
Replace with:
```html
          <p class="card-note">Personalised makeup products are available &mdash; send us an enquiry and we&rsquo;ll arrange the details with you.</p>
```

- [ ] **Step 2: Rewrite the out-of-zone delivery line**

In `delivery.html`, find:
```html
      <li>Outside our zones &mdash; &pound;15, calculated at checkout</li>
```
Replace with:
```html
      <li>Outside our zones &mdash; &pound;15, confirmed when we reply to your enquiry</li>
```

- [ ] **Step 3: Verify no stray checkout references remain**

Run: `grep -rni "checkout\|order number" *.html`
Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add index.html delivery.html
git commit -m "content: drop checkout references while the shop isn't live"
```

---

### Task 8: Full manual QA sweep

**Files:**
- Modify: `README.md` (enquiry form section, only if its description is now stale)

- [ ] **Step 1: Desktop sweep**

Serve the site and walk `http://localhost:8000` at a 1280px-wide window:

- Section opens as heading + two cards only.
- Each card selects, reveals the right fields, and relabels the textarea.
- Enquire on all five product cards pre-selects the matching piece — check **Luxury Rose Box** and **Signature Rose Bouquet** specifically, since both have carousels above the button.
- All six occasion tiles populate Occasion.
- Validation behaves per Task 5's expectations on both paths.

- [ ] **Step 2: Mobile sweep**

Resize to 390px wide and repeat the card selection and one full form fill.

Expected: the two intent cards stay side by side and readable, the radio row does not wrap awkwardly, and the Submit button is full-width as before.

- [ ] **Step 3: Check for orphaned references**

Run: `grep -rn "custom-order-fields\|style_preference\|style-preference\|toggleCustomOrderFields\|Something custom\|field-hint" index.html js/main.js css/style.css`

Expected: no output from `index.html` or `js/main.js`. A surviving `.field-hint` rule in `css/style.css` is acceptable only if some other markup still uses it — verify with `grep -rn "field-hint" *.html`; if that returns nothing, delete the `.field-hint` rule from `css/style.css`.

- [ ] **Step 4: Update the README if stale**

Run: `grep -rn "enquiry\|Enquiry" README.md`

The "Connect the enquiry form" section covers Formspree setup only and stays as is. The "Edit products, prices, and copy" section contains this line, which is now wrong because the dropdown no longer carries a custom option:
```markdown
- **Product names, prices, descriptions, and options** — the `bouquet-card` blocks in the "Our Collection" section. If you rename a product, also update its `data-bouquet` attribute and the matching `<option>` in the "Item of interest" dropdown.
```
Replace it with:
```markdown
- **Product names, prices, descriptions, and options** — the `bouquet-card` blocks in the "Our Collection" section. If you rename a product, also update its `data-bouquet` attribute and the matching `<option>` in the "Which piece" dropdown inside `#path-collection`.
```
If `grep` shows the line already reads "Which piece", leave it alone.

- [ ] **Step 5: Update the matching hard rule in AGENTS.md**

`AGENTS.md` carries the same now-stale instruction as a hard rule for automated edits. Find:
```markdown
- When renaming or adding a product in `index.html`, keep three things in sync: the `bouquet-card` block, its `data-bouquet` attribute, and the matching `<option>` in the "Item of interest" dropdown.
```
Replace with:
```markdown
- When renaming or adding a product in `index.html`, keep three things in sync: the `bouquet-card` block, its `data-bouquet` attribute, and the matching `<option>` in the "Which piece" dropdown inside `#path-collection`.
```

- [ ] **Step 6: Commit any cleanup**

```bash
git add -A
git commit -m "chore: clean up after the enquiry form restructure"
```

- [ ] **Step 7: Stop and report before pushing**

Do **not** push. Summarise what changed and confirm with the user first — merging to `main` deploys to flowersbytavi.co.uk immediately, with no staging environment.
