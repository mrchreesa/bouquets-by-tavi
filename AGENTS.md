# Agent instructions

Static HTML/CSS/JS site for Flowers by Tavi. No build step, no package manager, no dependencies to install — just edit files directly.

See `README.md` first for the human-facing guide to common edits (prices, copy, photos, deploy). The notes below are hard constraints for automated edits.

## Hard rules

- **Never hand-edit `images/hero-bouquet.svg`.** It's generated arithmetically by `tools/gen_hero_bouquet.py`. To change the hero animation, edit that script and regenerate with `python3 tools/gen_hero_bouquet.py images/hero-bouquet.svg`.
- **Don't touch `FORMSPREE_ID` in `js/main.js`** unless explicitly given a real Formspree form ID to set — it's live production config, not a placeholder to guess at.
- When renaming or adding a product in `index.html`, keep three things in sync: the `bouquet-card` block, its `data-bouquet` attribute, and the matching `<option>` in the "Item of interest" dropdown.
- This repo deploys **automatically on merge to `main`** via GitHub Pages (live at flowersbytavi.co.uk) — there is no staging environment and no CI gate. Treat a merge to `main` as instantly public.

## Local preview

```bash
python3 -m http.server 8000
```
Then open <http://localhost:8000>. Always sanity-check a change this way (or by opening `index.html` directly) before it's merged.
