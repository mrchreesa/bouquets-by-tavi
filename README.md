# Flowers by Tavi

A single-page, mobile-responsive website for Flowers by Tavi — handcrafted flower bouquets. Static HTML/CSS/JS with no build step: browse bouquets and occasions, then send an enquiry.

## Run it locally

From this folder:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. (Opening `index.html` directly in a browser also works.)

## How the enquiry form delivers

Enquiries are handled by our own API, not a third-party form service. The
server lives in the private `flowers-by-tavi-api` repo and runs on Vercel;
this site posts JSON to it. It screens each submission with a honeypot,
Cloudflare Turnstile, per-IP rate limiting and server-side validation, then
emails the enquiry to flowersbytavi@outlook.com with Reply-To set to the
customer.

To change where enquiries are delivered, update `MAIL_TO` in the API
project's Vercel environment variables — no code change needed here.

If the API host ever changes, update `API_URL` at the top of `js/main.js`.

## Replace or add product photos

Product photos live in `images/` (`1.PNG`, `2.PNG`, `3.PNG`, `4.PNG`/`4.1.PNG`, `5.jpg.jpeg`/`5.1.jpg.jpeg`). To swap one out, drop the new file into `images/` and update the matching `<img src="...">` in the `#bouquets` section of `index.html`. Cards are square-cropped (`object-fit: cover`), so any photo aspect ratio works. The hero image and the Our Story image are both generated animated illustrations (see below), not photos.

Two products (Luxury Rose Box, Signature Rose Bouquet) show a 2-photo carousel. To add a second photo to any other product, wrap its `<img>` in a `<div class="card-media card-carousel" data-carousel>` with a `.carousel-track` containing both images plus the arrow/dot buttons — copy the markup from one of the existing carousel cards.

## The animated hero bouquet

`images/hero-bouquet.svg` is the animated bouquet mark in the hero — roses, peonies and a cream rose in jewel tones, wrapped in florist's paper with a gold ribbon and the Tavi monogram. It blooms open on load, then settles into a continuous sway.

**Don't hand-edit the SVG** — it is generated, and its ~350 petals are laid out arithmetically. Edit `tools/gen_hero_bouquet.py` instead and regenerate:

```bash
python3 tools/gen_hero_bouquet.py images/hero-bouquet.svg
```

The bloom layout (positions, sizes, flower type, colour family, timing) lives in the `blooms` list; colours live in `TONES`; all motion is in the `<style>` block at the bottom of `build()`.

The file is 240 KB raw but ~22 KB gzipped, which is what GitHub Pages actually serves. It is loaded via a plain `<img>` tag, which keeps its CSS scoped to the SVG and out of the page. All motion sits behind `prefers-reduced-motion: no-preference`, so visitors who ask for reduced motion get the finished bouquet with no animation at all.

## The animated Our Story bouquet

`images/story.svg` is a generated illustration too — a delicate gold line-art bouquet in front of a softly pulsing blush heart, matching the hero's palette at a much smaller scale. Same rule applies: **don't hand-edit the SVG**, edit `tools/gen_story_bouquet.py` and regenerate:

```bash
python3 tools/gen_story_bouquet.py images/story.svg
```

If you'd rather use a real photo of Tavi instead, just drop it into `images/` and update the `<img src="...">` in the `#story` section of `index.html` — no need to keep the generated illustration once you have one.

## Edit products, prices, and copy

Everything is plain text in `index.html`:

- **Product names, prices, descriptions, and options** — the `bouquet-card` blocks in the "Our Collection" section. If you rename a product, also update its `data-bouquet` attribute and the matching `<option>` in the "Which piece" dropdown inside `#path-collection`.
- **Contact details** — email, phone, and Instagram links in the footer.
- **Announcement bar, story text, thank-you message** — edit in place.

## Deploy

Any static host works. Easiest options:

- **Netlify**: drag this folder onto <https://app.netlify.com/drop>
- **GitHub Pages**: push this repo to GitHub → Settings → Pages → deploy from branch

No build step or configuration needed.
