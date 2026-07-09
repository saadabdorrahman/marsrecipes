# Integration Checklist

Run this **complete, in order** whenever a page is added, renamed, or meaningfully edited. Skipping steps is how orphan pages and stale feeds happen.

1. **Page file** exists at its final path (`recipes/<slug>.html` for recipes) and follows `recipe-page-template.md`.
2. **Images**: hero `images/<slug>.jpg.png` (+ `-ingredients`, `-cooking`, `-serving` variants) present, or `images/<slug>.svg` placeholder created and all `<img>` tags carry `onerror` fallbacks. Note missing photos in the final report.
3. **Recipes index**: card added/updated in `recipes/index.html` grid with correct `data-category` (space-separated if multiple).
4. **Pillar page**: recipe added to the matching pillar's visible card list **and** ItemList JSON-LD (chicken → `pillar-quick-chicken-recipes.html`, beef → `pillar-easy-weeknight-beef-meals.html`, seafood → `pillar-best-seafood-dinner-recipes.html`).
5. **Cluster pages**: added to each qualifying cluster (totalTime ≤ 30 min → `cluster-30-minute-dinner-recipes.html`; ≥ 30g protein → `cluster-high-protein-dinner-recipes.html`; sheet-pan method → `cluster-sheet-pan-dinner-recipes.html`).
6. **Related recipes**: the new page links 2 sibling recipes; consider adding the new recipe to one or two siblings' `related-recipes` grids.
7. **Sitemap**: `python3 scripts/build_sitemap.py`
8. **Feed**: `python3 scripts/build_feed.py`
9. **Minify** (only if `css/style.css` or `js/main.js` changed): `python3 scripts/minify_assets.py`
10. **Validate**: `python3 scripts/validate_site.py` — must exit 0 (no CRITICAL). Fix anything it reports about the pages you touched.
11. **WordPress WXR** (when the change should reach WordPress): add the slug to `cat_map` in `generate-import.py`, then `python3 generate-import.py`.
12. **Report** to the user: files created/changed, validation summary, missing photos, and the suggested next step (`/publish`).
