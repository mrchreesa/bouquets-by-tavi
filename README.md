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

## Deploy

Any static host works. Easiest options:

- **Netlify**: drag this folder onto <https://app.netlify.com/drop>
- **GitHub Pages**: push this repo to GitHub → Settings → Pages → deploy from branch

No build step or configuration needed.
