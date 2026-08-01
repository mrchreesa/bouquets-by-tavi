# Enquiry Form — Custom Order Support — Design Spec

**Date:** 2026-08-01
**Status:** Approved by user

## Overview

The enquiry form already has a "Something custom" option in the "Item of
interest" dropdown and a free-text message field, so custom orders technically
work today — but nothing in the form makes that obvious to a customer skimming
it. This spec adds light copy changes plus a couple of conditional fields so
the custom-order path is clear without adding new complexity to the form's
validation or submission logic.

## Decisions (confirmed with user)

| Change | Decision |
|---|---|
| Section subheading | Replace "Tell us about your occasion and we'll craft something beautiful together." with "Tell us about your occasion — from our signature pieces to a fully custom design — and we'll craft something beautiful together." |
| Helper text | Add a short line near the "Item of interest" field: "Choosing 'Something custom' below unlocks a couple of quick questions so we can design something just for you." |
| Trigger | Selecting "Something custom" in the existing `#bouquet` dropdown reveals two new optional fields; selecting anything else re-hides them |
| New field 1 | **Budget range** — select: Under £50 / £50–£100 / £100+ / Not sure yet |
| New field 2 | **Colour & style preference** — short text input, placeholder e.g. "Pastels, bold reds, wildflower look…" |
| Validation | Both new fields stay optional — no new validation added, so they can never block submission |

## Implementation Notes

- **Markup**: a new wrapper (e.g. `.field-row` or reusing the existing
  `.form-row`/`.field` structure) containing the two new fields, given an id
  (e.g. `custom-order-fields`) and the `hidden` attribute by default — matching
  the existing pattern already used for `.field-error` and `#form-success`.
- **Behavior**: a `change` listener on the existing `#bouquet` select in
  `js/main.js` toggles the `hidden` attribute on the wrapper based on whether
  the selected value is `"Something custom"`. No changes needed to `validate()`
  or the submit handler — `FormData` picks up the new inputs automatically
  whenever they're filled in, and empty/hidden fields submit as empty strings
  which Formspree/the fallback email flow already tolerate.
- **Copy-only changes** (subheading, helper text) require no JS.

## Out of Scope

No new required fields, no file/image upload for style inspiration, no changes
to the Formspree submission logic or the "not connected yet" fallback
behavior.
