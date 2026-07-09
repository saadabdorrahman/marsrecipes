#!/usr/bin/env python3
"""
build_sitemap.py — Generate sitemap.xml for Mars Recipes.

Replaces hand-editing of sitemap.xml. Scans root *.html and recipes/*.html,
classifies each page, and writes the sitemap with the site's established
priority/changefreq conventions:

    homepage 1.0 weekly | recipe 0.9 monthly | pillar 0.85 weekly
    cluster / recipes index 0.8 weekly | about 0.6 yearly
    contact 0.5 yearly | legal 0.3 yearly

lastmod comes from the page's JSON-LD dateModified when present, otherwise
from the file's last git commit date, otherwise today.

    python3 scripts/build_sitemap.py
"""
import os
import re
import subprocess
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://www.marsrecipes.com"
OUT_PATH = os.path.join(BASE, "sitemap.xml")

# Pages that must never appear in the sitemap
EXCLUDED = {"404.html", "feed.html"}


def last_git_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            cwd=BASE,
            capture_output=True,
            text=True,
            timeout=10,
        )
        d = out.stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            return d
    except Exception:
        pass
    return date.today().isoformat()


def page_lastmod(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', content)
    if m:
        return m.group(1)
    return last_git_date(os.path.relpath(path, BASE))


def classify(fname, is_recipe):
    """Return (changefreq, priority) for a page filename."""
    if is_recipe:
        return "monthly", "0.9"
    if fname == "index.html":
        return "weekly", "1.0"
    if fname.startswith("pillar-"):
        return "weekly", "0.85"
    if fname.startswith("cluster-"):
        return "weekly", "0.80"
    if fname == "about.html":
        return "yearly", "0.6"
    if fname == "contact.html":
        return "yearly", "0.5"
    if fname in ("privacy-policy.html", "disclaimer.html"):
        return "yearly", "0.3"
    return "monthly", "0.5"


def url_block(loc, lastmod, changefreq, priority):
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def collect():
    """Return the sitemap sections as (comment, [url_block, ...]) pairs."""
    root_pages = sorted(
        f
        for f in os.listdir(BASE)
        if f.endswith(".html") and f not in EXCLUDED
    )
    recipe_pages = sorted(
        f
        for f in os.listdir(os.path.join(BASE, "recipes"))
        if f.endswith(".html") and f != "index.html"
    )

    sections = []

    # Homepage
    lm = page_lastmod(os.path.join(BASE, "index.html"))
    sections.append(("Homepage", [url_block(f"{SITE_URL}/", lm, "weekly", "1.0")]))

    # Recipes listing
    lm = page_lastmod(os.path.join(BASE, "recipes", "index.html"))
    sections.append(
        ("Recipes listing", [url_block(f"{SITE_URL}/recipes/", lm, "weekly", "0.8")])
    )

    pillars, clusters, statics, legals = [], [], [], []
    for fname in root_pages:
        if fname == "index.html":
            continue
        lm = page_lastmod(os.path.join(BASE, fname))
        cf, pr = classify(fname, is_recipe=False)
        block = url_block(f"{SITE_URL}/{fname}", lm, cf, pr)
        if fname.startswith("pillar-"):
            pillars.append(block)
        elif fname.startswith("cluster-"):
            clusters.append(block)
        elif fname in ("privacy-policy.html", "disclaimer.html"):
            legals.append(block)
        else:
            statics.append(block)

    sections.append(("Pillar Pages (SEO Hub Content)", pillars))
    sections.append(("Cluster Pages (Secondary Hub Content)", clusters))

    recipe_blocks = []
    for fname in recipe_pages:
        lm = page_lastmod(os.path.join(BASE, "recipes", fname))
        recipe_blocks.append(
            url_block(f"{SITE_URL}/recipes/{fname}", lm, "monthly", "0.9")
        )
    sections.append(("Recipe pages", recipe_blocks))

    sections.append(("About & Contact", statics))
    sections.append(("Legal pages", legals))
    return sections


def main():
    sections = collect()
    out = ['<?xml version="1.0" encoding="UTF-8"?>']
    out.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    total = 0
    for comment, blocks in sections:
        if not blocks:
            continue
        out.append("")
        out.append(f"  <!-- {comment} -->")
        out.append("\n".join(b.rstrip("\n") for b in blocks))
        total += len(blocks)
    out.append("")
    out.append("</urlset>")
    out.append("")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"sitemap.xml created with {total} URLs.")
    print("Saved to: " + OUT_PATH)


if __name__ == "__main__":
    main()
