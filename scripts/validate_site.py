#!/usr/bin/env python3
"""
validate_site.py — Site-wide validator for Mars Recipes.

Checks every HTML page plus sitemap.xml and feed.xml:

  * JSON-LD blocks parse; Recipe/FAQPage schemas have required fields
  * meta description / title / canonical / Open Graph / Twitter tags
  * internal links and image references resolve to real files
  * sitemap covers all pages and has no dead entries; lastmod freshness
  * feed contains the newest recipe
  * pages reference minified assets

Severity: CRITICAL (broken/dead/invalid), WARNING (SEO quality),
INFO (nice to fix). Exit code 1 if any CRITICAL issue is found.

    python3 scripts/validate_site.py [--json]
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://www.marsrecipes.com"

REQUIRED_RECIPE_FIELDS = [
    "name", "image", "author", "datePublished", "dateModified", "description",
    "prepTime", "cookTime", "totalTime", "keywords", "recipeYield",
    "recipeCategory", "recipeCuisine", "nutrition", "recipeIngredient",
    "recipeInstructions", "aggregateRating",
]

SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "javascript:", "data:")

issues = []


def add(severity, page, message):
    issues.append({"severity": severity, "page": page, "message": message})


def site_pages():
    pages = []
    for f in sorted(os.listdir(BASE)):
        if f.endswith(".html"):
            pages.append(f)
    for f in sorted(os.listdir(os.path.join(BASE, "recipes"))):
        if f.endswith(".html"):
            pages.append("recipes/" + f)
    return pages


def local_path_for_url(url):
    """Map a marsrecipes.com URL to a repo-relative file path (or None)."""
    if not url.startswith(SITE_URL):
        return None
    path = url[len(SITE_URL):].split("#")[0].split("?")[0]
    if path in ("", "/"):
        return "index.html"
    if path.endswith("/"):
        return path.strip("/") + "/index.html"
    return path.lstrip("/")


def check_ref_exists(page, ref, kind, has_onerror=False):
    """Verify a relative or same-site absolute reference resolves on disk."""
    if ref.startswith(SKIP_LINK_PREFIXES):
        local = local_path_for_url(ref)
        if local is None:
            return  # external URL — out of scope
        target = os.path.join(BASE, local)
    else:
        bare = ref.split("#")[0].split("?")[0]
        if not bare:
            return  # query/fragment-only self-link
        page_dir = os.path.dirname(os.path.join(BASE, page))
        target = os.path.normpath(os.path.join(page_dir, bare))
    if os.path.isfile(target):
        return
    if kind == "image" and has_onerror:
        add("WARNING", page, f"Image not on disk (onerror fallback covers it): {ref}")
    elif kind == "image":
        add("CRITICAL", page, f"Broken image reference: {ref}")
    else:
        add("CRITICAL", page, f"Broken internal link: {ref}")


def check_page(page):
    path = os.path.join(BASE, page)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    is_recipe = page.startswith("recipes/") and page != "recipes/index.html"
    is_404 = page == "404.html"

    # --- title / meta description ---
    m = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    if not m:
        add("CRITICAL", page, "Missing <title>")
    elif len(m.group(1).strip()) > 65:
        add("WARNING", page, f"Title is {len(m.group(1).strip())} chars (> 65, may truncate in SERPs)")

    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    if not m:
        add("CRITICAL" if not is_404 else "INFO", page, "Missing meta description")
    else:
        n = len(m.group(1))
        if n < 50:
            add("WARNING", page, f"Meta description only {n} chars (< 50)")
        elif n > 165:
            add("WARNING", page, f"Meta description {n} chars (> 165, will truncate)")

    # --- canonical ---
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    if not m:
        if not is_404:
            add("CRITICAL", page, "Missing canonical link")
    else:
        expected = f"{SITE_URL}/" if page == "index.html" else f"{SITE_URL}/{page}"
        if page == "recipes/index.html":
            expected = (f"{SITE_URL}/recipes/", f"{SITE_URL}/recipes/index.html")
        ok = m.group(1) in expected if isinstance(expected, tuple) else m.group(1) == expected
        if not ok:
            add("CRITICAL", page, f"Canonical mismatch: {m.group(1)} (expected {expected})")

    # --- Open Graph / Twitter ---
    if not is_404:
        for prop in ("og:title", "og:description", "og:image", "og:url"):
            if f'property="{prop}"' not in content:
                add("WARNING", page, f"Missing Open Graph tag: {prop}")
        if 'name="twitter:card"' not in content:
            add("WARNING", page, "Missing Twitter card tag")

    # --- JSON-LD ---
    blocks = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', content, re.DOTALL
    )
    recipe_schema = None
    has_faq = False
    for b in blocks:
        try:
            data = json.loads(b)
        except json.JSONDecodeError as e:
            add("CRITICAL", page, f"JSON-LD block does not parse: {e}")
            continue
        t = data.get("@type")
        if t == "Recipe":
            recipe_schema = data
        elif t == "FAQPage":
            has_faq = True

    if is_recipe:
        if recipe_schema is None:
            add("CRITICAL", page, "Recipe page has no Recipe JSON-LD schema")
        else:
            for field in REQUIRED_RECIPE_FIELDS:
                if field not in recipe_schema:
                    add("WARNING", page, f"Recipe schema missing field: {field}")
            for field in ("datePublished", "dateModified"):
                v = recipe_schema.get(field, "")
                if v and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                    add("WARNING", page, f"{field} not in YYYY-MM-DD format: {v}")
        if not has_faq:
            add("WARNING", page, "Recipe page has no FAQPage schema")

    # --- asset references ---
    if "style.min.css" not in content and "css/style" in content:
        add("WARNING", page, "References unminified style.css")
    if "main.min.js" not in content and "js/main" in content:
        add("WARNING", page, "References unminified main.js")

    # --- internal links ---
    for href in re.findall(r'<a[^>]+href="([^"]+)"', content):
        check_ref_exists(page, href, "link")

    # --- images ---
    for tag in re.findall(r"<img[^>]+>", content):
        src_m = re.search(r'src="([^"]+)"', tag)
        if src_m:
            check_ref_exists(page, src_m.group(1), "image", has_onerror="onerror=" in tag)

    return recipe_schema


def check_sitemap(recipe_dates):
    path = os.path.join(BASE, "sitemap.xml")
    if not os.path.isfile(path):
        add("CRITICAL", "sitemap.xml", "sitemap.xml is missing")
        return
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        add("CRITICAL", "sitemap.xml", f"sitemap.xml does not parse: {e}")
        return
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = {}
    for url in tree.getroot().findall("sm:url", ns):
        loc = url.findtext("sm:loc", "", ns)
        lastmod = url.findtext("sm:lastmod", "", ns)
        local = local_path_for_url(loc)
        if local is None or not os.path.isfile(os.path.join(BASE, local)):
            add("CRITICAL", "sitemap.xml", f"Sitemap entry points to missing page: {loc}")
            continue
        entries[local] = lastmod

    for page in site_pages():
        if page == "404.html":
            if page in entries:
                add("WARNING", "sitemap.xml", "404.html should not be in the sitemap")
            continue
        key = "index.html" if page == "index.html" else page
        if key not in entries and page != "recipes/index.html":
            add("CRITICAL", "sitemap.xml", f"Page missing from sitemap: {page}")
        if page == "recipes/index.html" and "recipes/index.html" not in entries:
            add("CRITICAL", "sitemap.xml", "Recipes index missing from sitemap")

    for page, modified in recipe_dates.items():
        lastmod = entries.get(page)
        if lastmod and modified and lastmod < modified:
            add("WARNING", "sitemap.xml", f"lastmod {lastmod} older than page dateModified {modified}: {page}")


def check_feed():
    path = os.path.join(BASE, "feed.xml")
    if not os.path.isfile(path):
        add("CRITICAL", "feed.xml", "feed.xml is missing")
        return
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        add("CRITICAL", "feed.xml", f"feed.xml does not parse: {e}")
        return
    links = {
        local_path_for_url(item.findtext("link", ""))
        for item in tree.getroot().iter("item")
    }
    for f in sorted(os.listdir(os.path.join(BASE, "recipes"))):
        if f.endswith(".html") and f != "index.html":
            if "recipes/" + f not in links:
                add("WARNING", "feed.xml", f"Recipe missing from RSS feed: recipes/{f} (run scripts/build_feed.py)")


def check_root_files():
    for f in ("robots.txt", "ads.txt", "favicon.ico"):
        if not os.path.isfile(os.path.join(BASE, f)):
            add("WARNING", f, f"{f} is missing")


def main():
    as_json = "--json" in sys.argv

    recipe_dates = {}
    for page in site_pages():
        schema = check_page(page)
        if schema:
            recipe_dates[page] = schema.get("dateModified", "")

    check_sitemap(recipe_dates)
    check_feed()
    check_root_files()

    order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    issues.sort(key=lambda i: (order[i["severity"]], i["page"]))
    counts = {s: sum(1 for i in issues if i["severity"] == s) for s in order}

    if as_json:
        print(json.dumps({"counts": counts, "issues": issues}, indent=2))
    else:
        for sev in ("CRITICAL", "WARNING", "INFO"):
            group = [i for i in issues if i["severity"] == sev]
            if not group:
                continue
            print(f"\n=== {sev} ({len(group)}) ===")
            for i in group:
                print(f"  [{i['page']}] {i['message']}")
        print(
            f"\nSummary: {counts['CRITICAL']} critical, "
            f"{counts['WARNING']} warnings, {counts['INFO']} info."
        )
        if not issues:
            print("Site is clean. ✔")

    sys.exit(1 if counts["CRITICAL"] else 0)


if __name__ == "__main__":
    main()
