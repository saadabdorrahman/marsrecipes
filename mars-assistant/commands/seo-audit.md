---
description: Full-site SEO audit (schema, meta, links, images, sitemap, feed) with optional auto-fix
argument-hint: "[--fix] [page path — omit for whole site]"
---

Run an SEO audit of marsrecipes.com. Arguments: **$ARGUMENTS**

Follow the `site-conventions` skill. Reply in the user's language.

## Steps

1. **Mechanical layer:** run `python3 scripts/validate_site.py --json` and parse the results. This covers: JSON-LD validity + required Recipe/FAQPage fields, meta description/title presence and lengths, canonical correctness, Open Graph/Twitter tags, broken internal links, missing images, sitemap coverage/dead entries/`lastmod` freshness, feed completeness, minified-asset references.

2. **Qualitative layer** (what the script can't judge) — inspect a sample (or the named page): title/description compelling and keyword-targeted; primary keyword in H1 + first paragraph; FAQ questions match real search questions; content depth (thin pages < ~800 words); rating consistency between JSON-LD, header stars, and reviews summary; internal-link opportunities between related pages. Optionally use the `seo-research` skill to check current keyword targeting against live SERP data.

3. **Without `--fix`:** produce a report grouped **Critical / Warning / Info**, each item with file, problem, and the exact fix. End with the top-3 highest-impact actions.

4. **With `--fix`:** apply safe fixes — regenerate sitemap/feed via `scripts/`, add missing meta/OG/Twitter tags, shorten over-long titles/descriptions (keep keywords), fix broken internal links, add missing `dateModified` fields (use `datePublished` value), sync inconsistent ratings. **Never** mass-rename images (the `.jpg.png` double extension is a known, intentional decision) and never delete content — flag those for the user instead. Re-run the validator after fixing; Critical count must be 0. Summarize what was fixed vs. what needs the user.
