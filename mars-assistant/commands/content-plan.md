---
description: Build a keyword-gap content calendar for upcoming recipes
argument-hint: "[number of weeks, default 4]"
---

Build a content plan for marsrecipes.com. Arguments: **$ARGUMENTS** (default: 4 weeks, 1 recipe/week).

Follow the `site-conventions` and `seo-research` skills. Reply in the user's language.

## Steps

1. **Inventory:** list existing recipes with categories from `recipes/index.html` `data-category` attributes. Note category balance (known gaps: `pasta` has 1 recipe, `vegetarian` has 0) and pillar/cluster coverage.

2. **Gap research** (seo-research skill): when Semrush is available, run `organic_research` on the niche competitor set (wellplated.com, budgetbytes.com, damndelicious.net, saltandlavender.com) to find keywords they rank for that fit our niche and we don't cover; otherwise use `WebSearch` for seasonal + evergreen easy-dinner keyword ideas. Apply the site-fit filter to every candidate.

3. **Output the calendar** as a table: **Week | Dish | Target keyword (volume/difficulty if known) | Category | Pillar/cluster placement | Rationale**. Balance categories, favor gap categories, and mind seasonality (current date matters).

4. **Offer next steps:** run `/new-recipe <first dish>` now, and/or `/schedule` the whole calendar as a weekly routine.
