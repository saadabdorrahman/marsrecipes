---
description: Build, validate, commit, push, and publish to WordPress (WXR or REST, live or draft)
argument-hint: "[commit message] [--wp [--draft]] — --wp publishes directly to WordPress via REST"
---

Publish pending site changes. Arguments: **$ARGUMENTS**

Follow the `site-conventions` skill. Reply in the user's language.

## Steps

1. **Review:** `git status` + `git diff --stat`. Summarize what's about to ship. If the tree is clean, say so and stop.

2. **Build chain:**
   - `python3 scripts/build_feed.py`
   - `python3 scripts/build_sitemap.py`
   - `python3 scripts/minify_assets.py` (only if `css/style.css` or `js/main.js` changed)
   - `python3 scripts/validate_site.py` — **abort and report if it exits 1 (Critical issues)**.

3. **WordPress WXR:** if recipe content changed, ensure new slugs are in `cat_map` in `generate-import.py` (they silently default to `chicken` otherwise), then run `python3 generate-import.py` to refresh `marsrecipes-theme/marsrecipes-import.xml`.

4. **Commit + push:** commit with the user's message (or write a clear one), `git push -u origin <current branch>` (retry on network errors with backoff). If working on a feature branch with an open PR, that's the publish for review; if on the deploy branch, this is the live publish.

5. **Direct WordPress publish (`--wp`):** publish changed recipes straight to the Hostinger WordPress site via REST API:
   - Requires env vars `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` (see `wordpress-plugin/mars-connect/README.md` for setup). If missing, print the setup instructions and skip this step gracefully.
   - Health check first: `curl -s $WP_URL/wp-json/mars-connect/v1/status` (falls back to `/wp-json/wp/v2/types/recipe` if mars-connect isn't installed).
   - Create/update via `POST $WP_URL/wp-json/wp/v2/recipe` (the theme registers the `recipe` CPT with `show_in_rest`), with `--user "$WP_USER:$WP_APP_PASSWORD"`. Use `"status": "draft"` when `--draft` is passed, else `"publish"`. Match existing posts by slug (GET `?slug=<slug>`) to decide create vs update. Set title, slug, content (article body with image URLs rewritten to `/wp-content/uploads/marsrecipes/`), excerpt, and `recipe_category` terms; send recipe meta (`_recipe_*`, `_nutrition_*` keys) — exposed via mars-connect.

6. **Hostinger full deploy** (theme/asset changes, not just content): print the steps — open hPanel terminal → run `install-on-hostinger.sh` (it clones from GitHub, so the push in step 4 must land first) → follow the 4 manual WordPress steps the script prints.

7. **Report:** commit hash, branch, what was published where (git / WXR / WordPress REST live-or-draft), links to the affected URLs, and any skipped steps with reasons.
