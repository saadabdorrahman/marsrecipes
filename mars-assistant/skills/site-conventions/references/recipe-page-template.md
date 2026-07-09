# Recipe Page Anatomy

**Do not write a recipe page from scratch.** Copy `recipes/easy-creamy-garlic-chicken.html` (or another recipe of the same category) as the skeleton and replace the content. The layout, class names, and section order are fixed; only the content varies.

## `<head>` (in this order)

1. Charset + viewport, DNS prefetch (`googletagmanager.com`, `fonts.googleapis.com`)
2. Favicon set (5 links, all `../`-relative)
3. `<meta name="description">` — 120–160 chars, includes primary keyword + time promise
4. `<meta name="robots" content="index, follow">`, `<meta name="author" content="Mars Recipes">`
5. Open Graph: `og:type=article`, `og:title`, `og:description`, `og:image:alt`, `og:image` (absolute URL, `.jpg.png`), `og:image:width=800`, `og:image:height=1200`, `og:url`, `og:site_name=Mars Recipes`
6. Twitter card: `summary_large_image`, title, description, `image:alt`, image
7. `<link rel="canonical">` — absolute `https://www.marsrecipes.com/recipes/<slug>.html`
8. Google Fonts: Playfair Display + Lato, preconnect + preload pattern
9. `<link rel="stylesheet" href="../css/style.min.css">` (always the `.min` file)
10. **Recipe JSON-LD** `<script type="application/ld+json">` — see `schema-checklist.md`
11. `<title>` — `<Recipe Name> – <Hook, e.g. Ready in 30 Minutes> | Mars Recipes`, ≤ 65 chars
12. RSS alternate link
13. **FAQPage JSON-LD** — mirrors the visible FAQ section exactly

## `<body>` section order (class names are load-bearing)

1. `site-header` → `container header-inner` → `nav-primary` + `nav-mobile`
2. `breadcrumb` — Home › Recipes › <Name>
3. `jump-bar` — anchor links (Jump to Recipe → `#recipe-card`)
4. `recipe-page-layout` (grid: main + sidebar)
5. `recipe-hero-image` — hero `<img>` with `onerror` SVG fallback, width/height attributes, descriptive alt
6. `recipe-article-header` — H1, `article-meta` (date, author), `article-rating` (stars + count — must match JSON-LD `aggregateRating`), `share-bar`
7. `article-body`:
   - Lead paragraphs (2–3, primary keyword in first 100 words)
   - `why-love-list` — "Why You'll Love This Recipe" bullets
   - `ad-slot ad-slot--rectangle` (keep placement)
   - Ingredients prose section (with `-ingredients` step image)
   - Tools/equipment paragraph
   - `recipe-card-block` (`id="recipe-card"`): `recipe-card-block-header`, `recipe-meta-strip` (prep/cook/total/servings/calories — must match JSON-LD), `recipe-card-actions` (print/pin), `recipe-ingredients` with `servings-adjuster` (checkbox list, `data-*` amounts), numbered instructions with `step-content` blocks (with `-cooking` image)
   - `tips-box` — pro tips
   - Variations + serving suggestions prose (with `-serving` image)
   - `storage-box` — 3 `storage-item`s (fridge / freezer / reheat)
   - `faq-section` — 6 `<details class="faq-item">` with `faq-answer`; questions come from keyword research (People Also Ask)
   - Nutrition table (matches JSON-LD `nutrition`)
   - `related-recipes` → `grid-3` with 2 `recipe-card`s linking sibling recipes
   - Pinterest CTA
8. `recipe-sidebar` — popular recipes + `ad-slot`
9. `reader-reviews` — `reviews-summary` (score must match JSON-LD rating), 5 `review-card`s (varied, realistic names/dates/texts), `review-form-wrap`
10. `site-footer` + cookie banner (`href="../privacy-policy.html"` — note the `../`)
11. `<script src="../js/main.min.js">`

## Content quality bar

- 1,200–1,800 words of genuinely useful, non-padded prose. Write like a home cook who has made the dish, not like an AI summary.
- US measurements first with metric in parentheses; internal temps in °F and °C.
- Primary keyword in: title, H1, meta description, first paragraph, one H2, image alt, JSON-LD keywords.
- Secondary keywords woven into H2s and FAQ questions naturally.
- `aggregateRating` seeded realistically (4.7–4.9, review count 40–150) and consistent everywhere it appears (JSON-LD, header stars, reviews summary).
