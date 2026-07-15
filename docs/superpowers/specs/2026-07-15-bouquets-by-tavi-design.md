# Bouquets by Tavi — Website Design Spec

**Date:** 2026-07-15
**Status:** Approved by user

## Overview

A static, single-page, mobile-responsive website for the florist brand **Bouquets by Tavi**, visually modeled on `reference.png` (soft blush/cream/rose-gold floral e-commerce aesthetic, "Maison Fleur"). The shop/checkout machinery from the reference is replaced by an **enquiry flow**: visitors browse bouquets and occasions, then submit an enquiry form that emails Tavi via Formspree.

## Decisions (confirmed with user)

| Decision | Choice |
|---|---|
| Pricing display | Indicative "From £X" prices with **Enquire** buttons (no fixed prices, no cart) |
| Form delivery | **Formspree** — form POSTs to Formspree endpoint; enquiries land in Tavi's inbox. Form ID is a single clearly-marked constant to paste in |
| Tech stack | **Static HTML/CSS/vanilla JS** — no build step, no dependencies; deployable to any static host |
| Structure | **Single scrolling page** with anchor navigation |
| Imagery | **On-brand placeholders** (blush gradient / floral line-art SVG) in clearly named slots (`images/bouquet-1.svg` etc.) so real photos drop in with no code changes |

## Page Sections (top to bottom)

1. **Announcement bar** — slim strip: "Handcrafted bouquets · Free local delivery". Plain HTML, easy to edit or delete.
2. **Header** — "Bouquets by Tavi" logotype centered; nav links scroll to sections: Bouquets, Occasions, Our Story, Contact. Sticky. Collapses to hamburger menu on mobile. No search/account/cart icons.
3. **Hero** — serif headline + script accent line (e.g. "The Art of / *Gifting Flowers*" adapted for Tavi), short tagline, "Enquire Now" button scrolling to the form, placeholder bouquet image.
4. **Our Bouquets** — grid of 4 cards: image, name, "From £X", Enquire button. Clicking Enquire scrolls to the form with that bouquet pre-selected in the "Bouquet of interest" dropdown.
5. **Shop by Occasion** — 6 arched icon tiles: Birthday, Anniversary, Romance, Congratulations, Thank You, Sympathy. Clicking a tile scrolls to the form with that occasion pre-selected.
6. **Our Story** — photo placeholder + short editable text block about Tavi.
7. **Enquiry form** — fields:
   - Name (required)
   - Email (required, validated)
   - Phone (optional)
   - Occasion (dropdown, optional)
   - Bouquet of interest (dropdown, optional)
   - Needed by (optional date)
   - Message (required)

   Client-side validation with inline error messages. Submits via `fetch` POST to Formspree; inline success/error state, no page reload. If the Formspree ID has not been configured, the form shows a clear "form not yet connected" error rather than failing silently.
8. **Footer** — trust line (handcrafted · local delivery · made with love), contact placeholders (email, phone, Instagram), copyright.

**Dropped from reference (add later if wanted):** search, account, cart, Weddings/Journal pages, newsletter signup, wishlist hearts.

## Visual Design

- **Palette:** blush pink, cream, deep rose, gold accents — matched from reference.
- **Typography:** serif display (Cormorant Garamond), script accent (Great Vibes or similar), clean body font. Loaded from Google Fonts.
- **Details:** scalloped section edges, floral line-art accents, arched tiles — echoing the reference mockup.
- Placeholder images are SVGs styled to the palette so the site looks intentional before real photos exist.

## Files

```
index.html
css/style.css
js/main.js
images/           (placeholder SVGs: hero, bouquet-1..4, story)
reference.png     (design reference, kept in repo)
```

## Responsive Behavior

Mobile-first, per the phone mockup in the reference:

- Hamburger nav on small screens; inline nav on desktop
- Hero stacks (text above image) on mobile
- Bouquet grid: 4 columns desktop → 2 columns tablet → 1 column small mobile
- Occasion tiles: 6 across desktop → 3×2 → 2×3 on mobile
- Form fields full-width on mobile
- No horizontal page scroll at any width

## Error Handling

- Form validation errors shown inline per-field on submit attempt
- Network/Formspree failure shows a friendly retry message with Tavi's email as fallback
- Unconfigured Formspree ID produces a visible, explicit message

## Testing / Verification

Drive the real page in a browser (Playwright) at mobile (~375px) and desktop (~1280px) widths:

- Nav links and Enquire buttons scroll to correct sections
- Hamburger menu opens/closes on mobile
- Bouquet card Enquire pre-selects the bouquet; occasion tile pre-selects the occasion
- Form validation blocks empty/invalid submissions with inline errors
- Successful submit path shows success state (Formspree request mocked/intercepted)
- No horizontal overflow at 375px

## Out of Scope

Booking/checkout, payments, CMS, newsletter, multiple pages, analytics, SEO beyond basic meta tags.
