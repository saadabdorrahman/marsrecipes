---
description: Quick phone-friendly status report of the site
---

Produce a short status report for marsrecipes.com. Reply in the user's language. Keep it to two phone screens max — this command is often run from mobile.

## Gather

1. **Content:** recipe count per category (from `recipes/index.html` `data-category`), newest and oldest `datePublished`, pages still using SVG-only placeholder images (recipes whose `images/<slug>.jpg.png` is missing).
2. **Health:** `python3 scripts/validate_site.py --json` → counts of Critical/Warning/Info, and the top 3 issues worth fixing.
3. **Pipeline:** `git log --oneline -5` (recent work), `git status --short` (unpublished changes), whether `feed.xml`/`sitemap.xml` are older than the newest recipe.
4. **Scheduled routines:** if `list_triggers` is available, list active routines and their next run.

## Report format

- 📊 Content: N recipes (breakdown), last published X
- 🩺 Health: N critical / N warnings — top issues one-liners
- 🚚 Unpublished: N changed files (or "all published")
- ⏰ Routines: active schedules (or "none")
- 👉 One suggested next action (e.g. `/seo-audit --fix`, `/new-recipe` for a gap category, `/publish`)
