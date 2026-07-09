---
description: Research, write, and fully integrate a new recipe page (SEO, schema, images, internal links, sitemap, feed)
argument-hint: <dish name or target keyword — English or Arabic>
---

Create a complete new recipe page for marsrecipes.com. The user's request: **$ARGUMENTS**

Follow the `site-conventions` and `seo-research` skills throughout. Reply to the user in their language; all site content stays in English.

## Steps

1. **Parse the request.** If the dish name is in Arabic, translate it to the natural English target keyword (e.g. "دجاج بالليمون والأعشاب" → "lemon herb chicken"). State your interpretation in one line before proceeding.

2. **Research** (seo-research skill): primary keyword, secondary keywords, 6 FAQ questions, competitor angle. Apply the site-fit filter — if the dish doesn't fit the niche or would cannibalize an existing recipe, say so and recommend the alternative instead of writing a duplicate.

3. **Present a 5-line brief** — title, slug, category(ies), primary + secondary keywords, angle/gap — then continue immediately (only pause for approval if the user asked to review first).

4. **Write the page.** Copy an existing recipe of the same category as skeleton (e.g. `recipes/easy-creamy-garlic-chicken.html`) and replace all content per `references/recipe-page-template.md` and `references/schema-checklist.md`. Original, useful content — realistic reviews, accurate nutrition estimates, `datePublished`/`dateModified` = today.

5. **Images:** look for suitable files in `images/`; otherwise create the `images/<slug>.svg` placeholder in the site's flat-illustration style and reference the standard `.jpg.png` names with `onerror` fallbacks. List the photo files the user should add later.

6. **Integrate** — run `references/integration-checklist.md` completely: index card, pillar page (card + ItemList), qualifying clusters, related-recipes links, `python3 scripts/build_sitemap.py`, `python3 scripts/build_feed.py`, `python3 scripts/validate_site.py` (must exit 0).

7. **Report:** file created, every page touched, validation summary, missing photos, and suggest `/publish` (and `/promote` after deployment) as next steps.
