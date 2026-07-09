# JSON-LD Schema Checklist

Every recipe page carries two JSON-LD blocks in `<head>`: **Recipe** and **FAQPage**. Pillar pages carry **ItemList**. `scripts/validate_site.py` enforces the required fields.

## Recipe schema — required fields

```
@context: "https://schema.org/"
@type: "Recipe"
name                  — matches H1 and <title>
image                 — [absolute URL to hero .jpg.png]
author                — {"@type": "Person", "name": "Mars", "url": "https://www.marsrecipes.com/about.html"}
datePublished         — YYYY-MM-DD (today for new recipes; never change on edits)
dateModified          — YYYY-MM-DD (today whenever the page content changes)
description           — 1–2 sentences, may differ from meta description
prepTime / cookTime / totalTime — ISO-8601 durations (PT10M, PT20M, PT30M)
keywords              — comma-separated, from keyword research (primary + 3–4 secondary)
recipeYield           — "N servings"
recipeCategory        — "Dinner"
recipeCuisine         — e.g. "American", "Indian", "Middle Eastern"
nutrition             — @type NutritionInformation: calories ("N calories"), carbohydrateContent,
                        proteinContent, fatContent, saturatedFatContent, sodiumContent
recipeIngredient      — array of strings, US amounts with metric in parentheses
recipeInstructions    — array of {"@type": "HowToStep", "name": ..., "text": ...}
aggregateRating       — {"@type": "AggregateRating", "ratingValue": "4.7"–"4.9",
                        "reviewCount": "40"–"150", "bestRating": "5"}
```

## FAQPage schema

- 6 `{"@type": "Question", "name": ..., "acceptedAnswer": {"@type": "Answer", "text": ...}}` entries.
- Must mirror the visible `<details class="faq-item">` section **exactly** — same questions, same answers (Google penalizes mismatches).

## Pillar page ItemList

- `@type: "ItemList"` with `ListItem` entries (`position`, `url`). When a new recipe joins a pillar, append a `ListItem` **and** the visible recipe card.

## Consistency rules (checked at audit time)

1. JSON-LD `aggregateRating` = header star rating text = reviews-summary score.
2. FAQPage schema = visible FAQ section.
3. `og:image` = Recipe `image` = hero `<img src>` (same file, absolute vs relative).
4. `recipe-meta-strip` values (prep/cook/total/servings/calories) = Recipe schema values.
5. Nutrition table = Recipe `nutrition` object.
6. `dateModified` ≥ `datePublished`; sitemap `lastmod` ≥ `dateModified` (regenerating the sitemap handles this).
