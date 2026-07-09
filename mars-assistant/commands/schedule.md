---
description: Set up, list, or cancel recurring automations (weekly recipe, weekly audit, reports)
argument-hint: "<what to automate, e.g. 'new recipe every Monday'> | list | cancel <name>"
---

Manage scheduled automations for marsrecipes.com. Arguments: **$ARGUMENTS**

Reply in the user's language.

## Parse the request

- `list` → show existing routines.
- `cancel <name>` → find and delete the matching routine.
- Anything else (Arabic or English) → parse into **cadence** (cron) + **task** (which slash command the routine should run, with what arguments).

## Mechanisms (try in this order)

1. **Routines (Claude Code remote / cloud)** — primary. Use the `create_trigger` tool with `create_new_session_on_fire: true` and a **standalone** prompt (each firing starts a fresh session with this plugin loaded), e.g.:
   - Weekly recipe: prompt `Run /content-plan 1 and then /new-recipe the top suggestion, then /publish`, cron `0 9 * * 1`.
   - Weekly SEO audit: prompt `Run /seo-audit --fix, then /publish "chore: weekly seo fixes"`, cron `0 9 * * 5`.
   - Monthly report: prompt `Run /site-report and email me the summary`, cron `0 9 1 * *`.
   Use `list_triggers` / `delete_trigger` / `update_trigger` for list/cancel/edit. One-shots use `run_once_at`.
2. **CronCreate** — if the Routines tools aren't available but CronCreate is, use it with equivalent prompts.
3. **Neither available (plain local CLI):** print copy-paste fallbacks — OS cron or GitHub Actions running `claude -p "/seo-audit --fix"` on a schedule — and explain that cloud sessions at claude.ai/code support Routines natively.

## Guardrails

- Confirm the parsed schedule with the user in one line ("Every Monday 09:00 UTC: create + publish a new recipe — OK?") before creating, unless they gave exact parameters.
- Prompts must be self-contained: fresh sessions have no memory of this conversation.
- Anything that posts to social media from a routine must state that in the routine prompt explicitly (e.g. "then /promote it and post WITHOUT asking"), otherwise `/promote` will stop at the draft stage.
- After creating, report the routine name, schedule (with timezone note — cron is UTC), and how to cancel it (`/schedule cancel <name>`).

## Suggested starter routines (offer these when the user is unsure)

| Routine | Cron | What it does |
|---|---|---|
| Weekly recipe | `0 9 * * 1` | content-plan → new-recipe → publish |
| Weekly SEO check | `0 9 * * 5` | seo-audit --fix → publish |
| Monthly report | `0 9 1 * *` | site-report summary |
