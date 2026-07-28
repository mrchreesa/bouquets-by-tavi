# Flowers by Tavi

A single-page, mobile-responsive website for Flowers by Tavi — handcrafted flower bouquets. Static HTML/CSS/JS with no build step: browse bouquets and occasions, then send an enquiry.

## Run it locally

From this folder:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. (Opening `index.html` directly in a browser also works.)

## Connect the enquiry form (one-time setup)

Enquiries are delivered by [Formspree](https://formspree.io) — free, no backend needed.

1. Create a free Formspree account and click **New form**.
2. Set the form's email to the address that should receive enquiries.
3. Copy the form's ID (the part after `/f/` in its endpoint, e.g. `mzbqwxyz`).
4. Open `js/main.js` and replace `YOUR_FORM_ID` on the first line of code:

   ```js
   const FORMSPREE_ID = "mzbqwxyz";
   ```

Until this is done, the form shows visitors a friendly "form not connected yet" message with the fallback email instead of sending.

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

## Deploy

Any static host works. Easiest options:

- **Netlify**: drag this folder onto <https://app.netlify.com/drop>
- **GitHub Pages**: push this repo to GitHub → Settings → Pages → deploy from branch

No build step or configuration needed.
