---
name: site-conventions
description: MarsRecipes site structure, page templates, schema formats, image naming, and the mandatory integration checklist for adding or editing any page on marsrecipes.com. Use whenever creating, editing, auditing, or publishing site content.
---

# MarsRecipes Site Conventions

marsrecipes.com is a **static HTML site** (the repo root is the deployable site) with a parallel WordPress theme in `marsrecipes-theme/` for the Hostinger-hosted WordPress version. Everything below applies to the static site; WordPress sync happens via `generate-import.py` (WXR) or the REST API (see the `/publish` command).

## Site map

| Type | Files | Sitemap priority / changefreq |
|---|---|---|
| Homepage | `index.html` | 1.0 weekly |
| Recipes index | `recipes/index.html` (canonical `/recipes/`) | 0.8 weekly |
| Pillar pages | `pillar-quick-chicken-recipes.html`, `pillar-easy-weeknight-beef-meals.html`, `pillar-best-seafood-dinner-recipes.html` | 0.85 weekly |
| Cluster pages | `cluster-30-minute-dinner-recipes.html`, `cluster-high-protein-dinner-recipes.html`, `cluster-sheet-pan-dinner-recipes.html` | 0.80 weekly |
| Recipes | `recipes/<slug>.html` | 0.9 monthly |
| Static | `about.html` 0.6, `contact.html` 0.5, `privacy-policy.html` / `disclaimer.html` 0.3 | yearly |

- URL base: `https://www.marsrecipes.com` (always `www`). Canonical URLs end in `.html` except `/` and `/recipes/`.
- Categories (used as `data-category` on cards in `recipes/index.html`, in pillar mapping, and in `generate-import.py` `cat_map`): `chicken`, `beef`, `seafood`, `pasta`, `quick`, `vegetarian`. A card may carry several, space-separated.
- Niche: easy weeknight dinners, total time ≤ ~40 minutes, US audience, US measurements first (metric in parentheses).

## Images

- Hero: `images/<slug>.jpg.png` — the double extension is an intentional legacy quirk; **keep following it** for new recipes until a site-wide rename happens (one legacy exception exists: `one-pan-beef-shawarma-bowl.png`).
- Step variants: `images/<slug>-ingredients.jpg.png`, `-cooking.jpg.png`, `-serving.jpg.png`.
- Fallback: `images/<slug>.svg` — every `<img>` carries an `onerror` fallback to the SVG, so a recipe can ship before photos exist. If no photo is available, create the SVG placeholder in the site's flat-illustration style and tell the user which photo files to add later.
- Declared og:image dimensions: 800×1200.

## Internal-linking rules (mandatory for every new recipe)

1. Card added to the `recipes/index.html` grid with correct `data-category`.
2. Added to the matching **pillar page** — both the visible card list **and** its ItemList JSON-LD.
3. Added to every qualifying **cluster page** (30-minute = totalTime ≤ 30; high-protein = ≥ 30g protein; sheet-pan = sheet-pan method).
4. The recipe page itself links 2 related recipes in its `related-recipes` grid.

## Tooling — always use `scripts/`, never the root-level legacy scripts

| Task | Command |
|---|---|
| Regenerate RSS feed | `python3 scripts/build_feed.py` |
| Regenerate sitemap | `python3 scripts/build_sitemap.py` |
| Minify CSS/JS (only if `css/style.css` or `js/main.js` changed) | `python3 scripts/minify_assets.py` |
| Validate whole site (run before finishing ANY content task) | `python3 scripts/validate_site.py` (`--json` for machine output; exit 1 = critical issues) |
| Regenerate WordPress WXR import | `python3 generate-import.py` — **add new slugs to its `cat_map` first** or they silently default to `chicken` |

⚠️ The root-level `make_rss.py`, `minify.py`, `fix_*.py`, `add_review*.py`, `update_images.py` are **deprecated** — they hardcode a Windows path and fail here. Do not run them.

**Never hand-edit `sitemap.xml` or `feed.xml`** — regenerate them.

## Language rule

The user may write prompts in Arabic or English. All **site content, file names, commit messages, and code stay in English**. Reply to the user in the language they used.

## References

- `references/recipe-page-template.md` — full page anatomy; copy an existing page as skeleton.
- `references/schema-checklist.md` — required JSON-LD fields and consistency rules.
- `references/integration-checklist.md` — ordered steps to fully integrate a new/edited page. Run it completely, every time.
