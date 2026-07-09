---
description: Promote a recipe on Facebook and Pinterest (via Zapier/Make connectors, or generate ready-to-post content)
argument-hint: <recipe name or slug> [--facebook] [--pinterest] — omit flags for both
---

Promote a published recipe on social media. Arguments: **$ARGUMENTS**

Reply in the user's language. Post content stays in English (the site's audience).

## Steps

1. **Locate the recipe** (fuzzy-match Arabic/English name → `recipes/<slug>.html`) and extract: title, description, canonical URL, hero image URL, 2–3 selling points from the "why you'll love it" list.

2. **Draft the posts** and show them to the user before sending:
   - **Facebook**: 2–4 warm, appetite-driven sentences + the recipe link. One emoji max per sentence, no hashtag walls (2–3 niche hashtags).
   - **Pinterest**: pin title (≤ 100 chars, keyword-first), description (≤ 500 chars, keywords woven naturally, call to action), destination link = canonical URL, image = hero image URL. Suggest the best board (e.g. "Easy Weeknight Dinners").

3. **Send via connectors** (first one available wins):
   - **Zapier MCP**: `list_enabled_zapier_actions`; if a Facebook Pages "create page post" or Pinterest "create pin" action is enabled, execute it with the drafted content (`execute_zapier_write_action`). If the app isn't enabled yet, offer `discover_zapier_actions` → `enable_zapier_action` and guide the user through the one-time connection.
   - **Make MCP**: look for an existing scenario (`scenarios_list`) that posts to Facebook/Pinterest and run it (`scenarios_run`) with the drafted content; offer to help create one if none exists.

4. **Fallback — no connector available:** output the finished posts as copy-paste blocks (Facebook text, Pinterest title + description + link + image URL) and the direct sharing URLs:
   - Facebook: `https://www.facebook.com/sharer/sharer.php?u=<canonical-url>`
   - Pinterest: `https://pinterest.com/pin/create/button/?url=<canonical-url>&media=<image-url>&description=<pin-description>`

5. **Confirm before posting.** Publishing to social accounts is outward-facing — always show the final content and get a yes before executing a write action, unless the user already told you to post without asking (e.g. in a scheduled routine they configured that way).

6. **Report:** what was posted where (with post/pin links if returned), or the ready-to-paste content.
