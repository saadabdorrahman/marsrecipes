---
name: seo-research
description: Keyword, competitor, and SERP research workflow for marsrecipes.com using Semrush MCP tools with a WebSearch fallback. Use before writing or improving any recipe or article, and for content-gap analysis.
---

# SEO Research Workflow

## Tool selection (try in this order)

1. **Semrush MCP** (available in remote sessions when the Semrush connector is on):
   - `mcp__Semrush__keyword_research` — volume, difficulty, related keywords, questions. Database: `us`.
   - `mcp__Semrush__organic_research` — what competitor domains rank for (gap analysis).
   - `mcp__Semrush__overview_research` / `url_research` — SERP and page-level competitive data.
   - Follow the server's discovery → `get_report_schema` → `execute_report` flow for complex reports.
2. **Fallback — free tools** (if Semrush is unavailable or errors): `WebSearch` the target keyword, note the top 10 results, then `WebFetch` the top 3 competitor recipe pages and analyze their structure, word count, and FAQ coverage. Use "People also ask"-style question phrasing from search results.

Never block on a missing tool — degrade gracefully and note in the final report which data source was used.

## What to extract (research brief)

- **Primary keyword** — the exact phrase to target (with volume + difficulty when available). Prefer long-tail with clear intent, e.g. "easy garlic parmesan pasta" over "pasta".
- **5–10 secondary keywords** → JSON-LD `keywords`, H2 headings, image alts.
- **6 question keywords** (People Also Ask) → the FAQ section + FAQPage schema.
- **Competitor angle** — what the top 3 results do well, what they miss (the gap the new page will fill: faster method, fewer ingredients, better storage guidance, clearer substitutions…).
- **Suggested title** (≤ 65 chars, keyword + hook) and **meta description** (120–160 chars).

## Site-fit filter (apply before writing anything)

- Fits the niche: easy weeknight dinner, total time ≤ ~40 minutes, accessible ingredients.
- Maps to one of the site categories: `chicken`, `beef`, `seafood`, `pasta`, `quick`, `vegetarian`.
- **No cannibalization**: check `recipes/` for an existing page targeting the same primary keyword. If one exists, recommend `/improve` on it instead of a new page.
- Current known gaps worth prioritizing: `pasta` (1 recipe) and `vegetarian` (0 recipes).

## Competitor set for gap analysis

When doing content-gap or `/content-plan` work, compare marsrecipes.com against domains like `wellplated.com`, `budgetbytes.com`, `damndelicious.net`, `saltandlavender.com` (same easy-dinner niche).
