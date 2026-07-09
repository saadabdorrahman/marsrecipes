# mars-assistant — Full-Automation Plugin for marsrecipes.com

A Claude Code plugin that turns blogging, SEO, publishing, and promotion for [marsrecipes.com](https://www.marsrecipes.com) into single commands. You type one instruction — in **English or Arabic** — and Claude researches, writes, optimizes, validates, publishes, and schedules on your behalf, from your computer or your phone.

## Commands

| Command | What it does | Example |
|---|---|---|
| `/new-recipe <dish>` | Keyword research → full SEO'd recipe page (schema, FAQ, images, internal links) → sitemap/feed update → validation | `/new-recipe garlic parmesan pasta` · `/new-recipe دجاج بالليمون والأعشاب` |
| `/seo-audit [--fix]` | Full-site audit: schema, meta, broken links, images, sitemap, feed. `--fix` auto-repairs the safe issues | `/seo-audit --fix` |
| `/improve <page> [focus]` | Refresh an existing page: re-research keyword, fill gaps, bump freshness | `/improve creamy tuscan shrimp seo` |
| `/content-plan [weeks]` | Keyword-gap content calendar vs. niche competitors | `/content-plan 4` |
| `/publish [msg] [--wp [--draft]]` | Build chain → validate → commit/push → WXR refresh; `--wp` publishes straight to WordPress via REST (live or draft) | `/publish "add pasta recipe" --wp --draft` |
| `/promote <recipe>` | Facebook + Pinterest posts via your Zapier/Make connectors, or ready-to-paste content | `/promote garlic parmesan pasta` |
| `/schedule <request>` | Recurring automations (Routines): weekly recipe, weekly audit, monthly report | `/schedule وصفة جديدة كل يوم اثنين` |
| `/site-report` | Two-screen status: content, health, unpublished changes, active routines | `/site-report` |

Commands accept Arabic naturally — Claude replies in your language while all site content stays in English.

## Installation

**In this repo (cloud or local):** nothing to do — the committed `.claude/settings.json` registers the repo as a plugin marketplace and enables `mars-assistant` automatically. On first session start, approve the plugin when prompted.

**In another project / machine:**

```
claude plugin marketplace add saadabdorrahman/marsrecipes
claude plugin install mars-assistant@marsrecipes
```

## Using from your phone

1. Open the Claude app (or claude.ai/code) → Code → start a session on the `marsrecipes` repo.
2. Type any command above — e.g. `/site-report` or `/new-recipe كفتة بالفرن`.
3. For hands-free operation, set up Routines once with `/schedule` — they run in fresh cloud sessions on their own cron, with no app open.

## Publishing pipeline

```
/new-recipe ──► static HTML page + sitemap + feed + validation
                     │
/publish ────────────┼──► git commit + push (this repo = the deployable static site)
                     ├──► generate-import.py → marsrecipes-theme/marsrecipes-import.xml (WXR)
                     └──► --wp: REST publish to Hostinger WordPress (live or --draft)
                              requires the Mars Connect WP plugin — see wordpress-plugin/mars-connect/README.md
/promote ────────────────► Facebook + Pinterest (Zapier/Make connectors or copy-paste)
```

## Repository tooling the plugin relies on

| Script | Purpose |
|---|---|
| `scripts/build_feed.py` | Regenerate `feed.xml` from recipe pages |
| `scripts/build_sitemap.py` | Regenerate `sitemap.xml` (never hand-edit) |
| `scripts/minify_assets.py` | Rebuild `style.min.css` / `main.min.js` |
| `scripts/validate_site.py` | Site-wide validator — schema, meta, links, images, sitemap, feed |

> ⚠️ The root-level `make_rss.py`, `minify.py`, and `fix_*.py` scripts are legacy (hardcoded Windows paths) and deprecated — the `scripts/` versions replace them.

## External connectors used when available

- **Semrush** — keyword volume/difficulty, competitor gap analysis (falls back to plain web search).
- **Zapier / Make** — Facebook page posts and Pinterest pins from `/promote`.
- **Routines (claude.ai/code)** — scheduled sessions for `/schedule`.

## Known site quirks (intentional, don't "fix" blindly)

- Hero images use a `.jpg.png` double extension (`images/<slug>.jpg.png`) — a legacy convention every page's `onerror` fallbacks depend on. New recipes follow it too.
- `robots.txt` deliberately blocks AI crawlers (GPTBot, CCBot, anthropic-ai, Google-Extended).
