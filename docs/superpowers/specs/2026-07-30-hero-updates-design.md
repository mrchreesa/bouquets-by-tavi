# Hero Section Updates — Design Spec

**Date:** 2026-07-30
**Status:** Approved by user (via annotated mockup + clarifying questions)

## Overview

The user provided an annotated screenshot of the live hero section with handwritten
callouts requesting five changes. Four were clarified via follow-up questions; the
fifth ("Photoshoot pics will go here", pointing at the hero image) is a note about
future real photos and requires no action now — it's called out as out of scope
below.

## Decisions (confirmed with user)

| Change | Decision |
|---|---|
| Promo badge | Add a static "10% off until Monday" text badge near the brand mark in the header. Plain HTML text, manually edited by the user whenever the offer changes — no countdown logic |
| Motion | The **announcement bar** ("Handcrafted bouquets · Free local delivery") slides back and forth horizontally on a loop (not the promo badge) |
| Tagline | Replace "Handcrafted bouquets that capture beauty, emotion & timeless elegance." with "Luxury blooms designed to make someone feel unforgettable." (smoothed from the mockup's "him/her" wording) |
| Location line | Add "London, United Kingdom" under the new tagline |
| Hero CTA | Replace the single "Enquire Now" button with a dropdown offering two choices: "Enquire Now" (scrolls to the form, existing behavior) and "Order on WhatsApp" (opens a WhatsApp chat) |
| WhatsApp number | Reuses the existing site phone number, +44 7364 125646, as a `wa.me` link: `https://wa.me/447364125646` |
| Hero image | Out of scope — "Photoshoot pics will go here" is a note about future real photos; the current placeholder SVG is untouched |

## Implementation Notes

- **Promo badge**: a small pill (`.promo-badge`) placed inline next to the brand
  mark in `.site-header .nav`, not absolutely positioned over the announcement
  bar/header boundary — simpler and robust across breakpoints, while still reading
  as "a promo badge near the logo" per the mockup's intent.
- **Announcement bar motion**: the existing `.announcement` div gets its text
  wrapped in a new inline span (`.announcement-track`) animated with a CSS
  `@keyframes` that slides it back and forth (`translateX` oscillating, using
  `animation-direction: alternate`), looping continuously. Respects
  `prefers-reduced-motion: reduce` (existing media query at the bottom of
  `style.css` gets this animation added to its `animation: none` override).
- **Hero CTA dropdown**: implemented with native `<details class="hero-cta">` /
  `<summary>` (no extra JS needed for the open/close toggle itself, keyboard
  accessible by default). A small addition to `js/main.js` closes the `<details>`
  when either menu link is clicked, matching the existing pattern used for closing
  the mobile nav menu on link click.
- **WhatsApp link**: `target="_blank" rel="noopener"` since it leaves the site.

## Out of Scope

Hero image/photo (still the placeholder SVG — real photoshoot photos to be added
later, per the user's own note on the mockup). No other page section changes.
