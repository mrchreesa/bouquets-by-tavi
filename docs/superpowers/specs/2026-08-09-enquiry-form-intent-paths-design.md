# Enquiry Form — Intent Paths — Design Spec

**Date:** 2026-08-09
**Status:** Approved by user

## Overview

The enquiry form has grown to nine fields, two of them conditional, plus a hint
paragraph explaining a hidden interaction. The root cause is not the field count
— it is that one form is quietly serving three different jobs: buying a listed
product, commissioning a custom design, and (per the Princess Treatment Basket
copy) customising an order already placed.

This spec splits the section into an explicit intent choice followed by a short
form that renders only the chosen path's fields. Custom orders become a
first-class, visible option instead of a dropdown entry, and the compound
"Send an Enquiry / Customise Orders" heading — which was the confusion showing
through in the copy — goes away.

## Problems being fixed

| Symptom | Cause |
|---|---|
| Slash-compound heading | One heading covering two unrelated jobs |
| Duplicate asks | Message placeholder prompts for "colours, budget, delivery" while Budget and Colour & style already exist as fields |
| Hint explaining hidden UI | "Choosing 'Something custom' unlocks a couple of quick questions" is a label apologising for the interaction |
| Occasion asked twice | Occasion tiles set it, then the dropdown asks again |
| Delivery detail missing | New pickup slots, zones and same-day pricing need delivery-vs-pickup to quote, and nothing captures it |
| Copy references a checkout that does not exist | Princess Treatment Basket and delivery policy mention "checkout" and "order number"; the shop is not live yet |

## Decisions (confirmed with user)

| Decision | Choice |
|---|---|
| Shape | Intent cards, then a short adaptive form |
| Optimise for | Fewer fields, more enquiries |
| Checkout status | Not live yet, planned — soften copy now, leave room for an order-number path later |
| Contact fields | Email stays its own required field (Formspree uses `email` for reply-to; a combined "email or phone" field breaks replies) |
| Phone field | **Cut.** It was optional and rarely load-bearing, WhatsApp is already a prominent CTA in the hero and footer, and cutting it is what gets each path to seven fields |
| Card default | Nothing preselected — the section opens as two choices, not a wall of inputs |

## Structure

```
kicker: "Get in touch"
h2:     "What can we help you with?"

[ 💐 Order from the collection ]  [ ✨ Design something custom ]

  ── path-specific field ──
  ── shared details ──
  [ Submit ]
```

Cards are radio inputs styled as tiles, reusing the visual family of the
existing `.occasion-tile`. Radios rather than buttons so keyboard navigation,
focus order and screen-reader grouping come for free.

## Fields

Seven visible fields on either path, down from nine, two of them conditional.

**Path-specific**

| Path | Field | Name | Required |
|---|---|---|---|
| Collection | Which piece | `bouquet` | yes |
| Custom | Budget | `budget` | no |

**Shared** (revealed once a card is chosen)

| Field | Name | Required |
|---|---|---|
| Occasion | `occasion` | no |
| When for | `needed_by` | no |
| Delivery or pickup | `fulfilment` | no |
| Name | `name` | yes |
| Email | `email` | yes |
| Message | `message` | custom only |

The message field's label, placeholder and `required` state swap by path:

- Collection → "Anything else" / optional / placeholder prompts for size and
  colour, e.g. "Size, colours, a note for the card…"
- Custom → "What you have in mind" / required / placeholder prompts for the
  design brief, e.g. "Colours, style, who it's for…"

Size (25/35/50/75 stems) deliberately gets no field of its own — it lives in the
collection placeholder. That is the trade for staying at seven.

Existing `name` attributes are preserved so submissions stay consistent with
anything already in the Formspree inbox. `fulfilment` is the only genuinely new
one; `budget` carries over from the old conditional block.

Two of today's fields are dropped outright: `phone` (see Decisions) and
`style_preference`, whose "Pastels, bold reds, wildflower look…" prompt folds
into the custom path's message placeholder rather than occupying its own field.

The `bouquet` select drops its "Something custom" option — the intent card now
carries that meaning. "Not sure yet" stays.

## Behaviour

- **Path toggle**: a `change` listener on the intent radios sets `hidden` and
  `disabled` on the inactive path's fieldset. `disabled` matters — it keeps the
  other path's empty fields out of `FormData` entirely, so Formspree never
  receives a submission carrying both paths' keys.
- **Initial state**: with no card chosen, both path fieldsets *and* the shared
  details block are hidden, and the submit button with them — the section shows
  only the heading and the two cards. Choosing a card reveals the shared block
  and the matching path fieldset together. Switching cards afterwards swaps the
  path fieldset and leaves anything already typed into the shared block intact.
- **Progressive enhancement**: markup ships with every fieldset visible; JS
  hides them on init, matching the existing `toggleCustomOrderFields()` pattern.
  With JS off the form degrades to a single long form that still submits, rather
  than to an unusable section with everything hidden.
- **Enquire buttons**: check the collection radio, set `bouquet`, fire the
  toggle, then scroll — an extension of the existing `.enquire-btn` handler.
- **Occasion tiles**: set the shared `occasion` select and scroll, without
  forcing a path. The select is in the DOM from load, so the value persists and
  is already filled in when the visitor picks a card. Tiles deliberately do not
  imply custom-vs-collection.
- **Validation**: `name` and `email` always; `bouquet` when the collection path
  is active; `message` only when the custom path is active. `validate()` reads
  the active path rather than a fixed list.

## Bundled fixes

- **`js/main.js:150`** resets the submit button's label to the hardcoded string
  `"Send Enquiry"` after a failed send, so an error silently relabels the button.
  Read the original label once at init and restore that instead.
- **Princess Treatment Basket note** — drop the "purchase at checkout, then send
  your enquiry with your order number" instruction, which points at a checkout
  that does not exist. Replace with an enquiry-based instruction.
- **Delivery policy** — "Outside our zones — £15, calculated at checkout"
  becomes wording tied to the enquiry reply instead.
- **Submit button** — the uncommitted `Submit` label change folds into this work.

## Room for the third path

When the shop goes live, a third card ("Customise an order I've placed") drops
in beside the other two with a single path-specific field (order number). The
fieldset toggle, validation lookup and disabled-fieldset submission handling all
generalise to N paths as written, so no restructuring is required. Nothing for
that path is built now.

## Out of scope

No order-number field or checkout integration before the shop exists. No file
upload for style inspiration, no size selector, no validation-on-blur, no draft
autosave, and no change to the Formspree submission flow or the "not connected
yet" fallback.
