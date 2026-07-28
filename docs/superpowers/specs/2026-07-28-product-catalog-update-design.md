# Product Catalog Update — Design Spec

**Date:** 2026-07-28
**Status:** Approved by user

## Overview

Replace the 4 generic placeholder bouquet cards in the existing "Flowers by Tavi" site
(see `docs/superpowers/specs/2026-07-15-bouquets-by-tavi-design.md`) with the real
5-product catalog and real product photos supplied by the user. This is a content and
card-layout update on top of the already-approved site; it does not change the
announcement bar, hero, occasions, story, footer, or overall page architecture.

## Product Data (source of truth — exact copy to use)

### 1. Blush Basket — £55
A soft, elegant floral basket featuring a delicate mix of blush pink and white tones.
Perfect for birthdays, thank you gifts, or any occasion that calls for something
beautiful and thoughtful.

- Includes: Fresh floral arrangement; Decorative basket with ribbon finish; Carefully
  arranged premium blooms
- Note: Flower types may vary slightly depending on availability while maintaining the
  overall look and colour theme.
- Image: `images/1.PNG` (single image)

### 2. Princess Treatment Basket — £65
A luxurious floral gift basket designed to feel extra special. Featuring soft pink
tones and premium flowers, this arrangement is perfect for birthdays, surprises, or
treating someone like royalty.

- Includes: Fresh flower arrangement; Decorative basket with ribbon
- Optional Add-Ons: 💄 Full Makeup Set (+£50); 🌸 Perfume Add-On (price varies)
- Note: Images may include add-ons for display purposes. Final design may vary
  depending on selected extras.
- Image: `images/2.PNG` (single image)

### 3. Luxury Chocolate Gift Cake — £65
A beautifully crafted chocolate arrangement designed to look like a cake, perfect for
gifting on special occasions. Made with premium chocolates and finished with elegant
details.

- Details: Size approx. 25cm; Available Shapes: Heart or Round; Colour Options: Red,
  White, or Custom; Personalisation: Initials or message included
- Note: Designs may vary slightly depending on shape and colour selection. Add-ons are
  available — please enquire for more details.
- Image: `images/3.PNG` (single image)

### 4. Luxury Heart Rose Box — From £70
A stunning heart-shaped rose arrangement designed to make a lasting impression.
Perfect for anniversaries, birthdays, and special occasions.

- Sizes: Small (25 roses) — £70; Medium (50 roses) — £140; Large (75 roses) — £170
- Colour Options: Red; White; Pink; Red & White Mix
- Each rose box is carefully arranged to create a full, luxurious look.
- Note: Design and rose placement may vary slightly depending on size and colour
  selection.
- Images: `images/4.PNG`, `images/4.1.PNG` — 2-photo fade carousel

### 5. Signature Rose Bouquet — From £130
A full, luxury bouquet designed to make a bold statement. Featuring premium roses,
elegant wrapping, and a clean, high-end finish — perfect for birthdays, anniversaries,
and special occasions.

- Sizes: 50 Roses — £130; 75 Roses — £170; 100 Roses — £220
- Wrapping Options (included): Pink; Black; White
- Optional Add-Ons: Initials (letters on bouquet) +£5; Personalised ribbon message +£5
- Images: `images/5.jpg.jpeg`, `images/5.1.jpg.jpeg` — 2-photo fade carousel (the
  `.1` photo shows the black-wrap + initial + ribbon-message add-ons in use, a good
  real illustration of the options above)

## Decisions (confirmed with user)

| Decision | Choice |
|---|---|
| Multi-photo cards (products 4 & 5) | Simple fade carousel: ‹ › arrow buttons + dot indicators, manual only, no autoplay |
| Section/nav naming | Renamed from "Bouquets" to "Collection" throughout (nav link, section heading, form field label) — the catalog now includes a chocolate cake and gift baskets, not just florals |
| Grid columns | 3-column desktop breakpoint (was 4), so 5 cards lay out 3+2 instead of leaving an orphan card |
| Scope boundary | Hero image, Our Story section/photo, Occasions tiles, footer — untouched |

## Card Layout (per product, new structure)

Each `.bouquet-card` (class name kept as-is to avoid an unnecessary rename of existing
CSS/JS hooks) gains richer content than the current image + name + price + button:

1. Image, or for products 4 & 5, a fade carousel (‹ › controls + dot indicators)
2. Name (`h3`)
3. Price line — fixed price for products 1–3; "From £X" (lowest size price) for
   products 4–5
4. One-line description (from the product copy above)
5. "Includes" bullet list — products 1–3 only (the source copy gives explicit
   Includes/Details lists for these three; products 4–5 have no such list and go
   straight to their Options bullets)
6. "Options" bullet list where applicable — sizes with prices, colour/shape options,
   add-ons with their price deltas (all 5 products have at least one such line: 1 has
   none, 2 has add-ons, 3 has shape/colour, 4 has sizes+colours, 5 has
   sizes+wrapping+add-ons)
7. Small italic note line (the "may vary" / "please enquire" disclaimer)
8. Enquire button — `data-bouquet` attribute set to the exact product name, pre-fills
   the enquiry form's product dropdown, scrolls to the form (existing JS behavior,
   unchanged)

## Form & Nav Changes

- Nav link: "Bouquets" → "Collection"
- Section heading: "Our Bouquets" → "Our Collection" (kicker text "Handpicked with
  love" stays)
- Enquiry form label: "Bouquet of interest" → "Item of interest"
- Dropdown `<option>`s replaced with the 5 real product names: Blush Basket, Princess
  Treatment Basket, Luxury Chocolate Gift Cake, Luxury Heart Rose Box, Signature Rose
  Bouquet (keep the existing "Not sure yet" default and "Something custom" trailing
  option)

## Carousel Behavior Spec

- Each multi-image card renders both `<img>`s stacked (absolute position), only one
  visible at a time via a CSS class (e.g. `.is-active`), cross-fade via `opacity`
  transition
- ‹ / › buttons step the active index; dot indicators show current position and are
  clickable
- Keyboard accessible (real `<button>` elements, focus-visible outline from existing
  `:focus-visible` rule)
- No timers/autoplay — matches the site's otherwise static, no-JS-dependency-heavy
  philosophy
- Single-image cards (1, 2, 3) render a plain `<img>`, no carousel markup

## Error Handling / Edge Cases

- N/A — this is static content; no new form validation, no new network calls
- If a product image fails to load, existing `img` browser fallback behavior applies
  (no custom error UI, consistent with rest of site)

## Testing / Verification

Drive the real page in a browser (Playwright) at mobile (~375px) and desktop
(~1280px):

- All 5 cards render with correct name, price, description, includes/options/notes
  text matching the source copy above
- Products 4 & 5 carousels: arrow clicks and dot clicks swap the visible image;
  starts on the first image; no layout shift when swapping
- Enquire button on each card pre-selects the correct option in "Item of interest"
  and scrolls to the form
- Nav link reads "Collection" and scrolls to `#bouquets` (anchor id unchanged)
  section, which now reads "Our Collection"
- No horizontal overflow at 375px
- Grid is 3 columns ≥1000px, 2 columns ≥560px, 1 column below

## Out of Scope

Hero image/copy, Our Story section, Occasions tiles, footer contact details, form
submission/Formspree wiring — none of these change in this update.
