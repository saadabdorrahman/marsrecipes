---
description: Refresh and optimize an existing page (content, SEO, links, freshness)
argument-hint: "<page path or recipe name> [focus: seo|content|links|speed]"
---

Improve an existing marsrecipes.com page. Arguments: **$ARGUMENTS**

Follow the `site-conventions` and `seo-research` skills. Reply in the user's language.

## Steps

1. **Locate the page** — fuzzy-match the Arabic or English name against files in the repo root and `recipes/`. If ambiguous, list the candidates and ask.

2. **Re-research** the page's primary keyword (seo-research skill): current SERP, fresh People-Also-Ask questions, competitor coverage.

3. **Diff research vs. page** and apply improvements according to the focus argument (default: all):
   - **seo** — title/meta lengths and keyword placement, missing/weak OG/Twitter tags, schema completeness (run `python3 scripts/validate_site.py --json` filtered to this page).
   - **content** — thin sections, missing FAQ questions users actually ask, better tips/storage/variations, outdated claims.
   - **links** — add internal links to/from related recipes, pillar and cluster membership (integration-checklist steps 3–6).
   - **speed** — image `width`/`height` attributes, lazy-loading below the fold, unminified asset references.

4. **Freshness:** bump `dateModified` in the Recipe JSON-LD to today (never touch `datePublished`), then `python3 scripts/build_sitemap.py` so `lastmod` follows.

5. **Validate:** `python3 scripts/validate_site.py` must exit 0.

6. **Report** a before/after summary: what changed and why, expected SEO effect, and suggest `/publish` as the next step.
