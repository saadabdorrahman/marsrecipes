# Mars Connect (WordPress companion plugin)

Enables the `mars-assistant` Claude Code plugin to publish recipes directly to the Hostinger-hosted WordPress site — live or as drafts — over the WordPress REST API.

The marsrecipes theme already registers the `recipe` post type and taxonomies with `show_in_rest`. This plugin adds the two missing pieces:

1. **REST-exposed recipe meta** — the `_recipe_*` / `_nutrition_*` keys the theme reads are underscore-protected by default; Mars Connect registers them for authenticated REST writes.
2. **Health endpoint** — `GET /wp-json/mars-connect/v1/status` returns plugin/theme status and recipe counts so `/publish --wp` can verify connectivity before writing.

## Install (once)

1. In hPanel / WordPress admin → Plugins → Add New → Upload, upload a zip of the `mars-connect` folder (or copy the folder to `wp-content/plugins/`).
2. Activate **Mars Connect**.
3. Create an **Application Password**: WordPress admin → Users → your user → Application Passwords → name it `mars-assistant` → copy the generated password.

## Configure the Claude side

Set these environment variables in the environment where Claude Code runs (for cloud sessions: environment settings at claude.ai/code; locally: your shell profile — never commit them):

```
WP_URL=https://your-wordpress-site.example
WP_USER=your-wp-username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

## Verify

```
curl -s $WP_URL/wp-json/mars-connect/v1/status
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_URL/wp-json/wp/v2/recipe?per_page=1"
```

Both should return JSON. After that, `/publish --wp` (live) and `/publish --wp --draft` work end to end.
