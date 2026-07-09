#!/usr/bin/env python3
"""
build_feed.py — Generate RSS 2.0 feed for Mars Recipes.

Portable replacement for the legacy make_rss.py (which hardcodes a Windows
path). Reads metadata from each recipe HTML file and writes feed.xml at the
repository root. Run from anywhere:

    python3 scripts/build_feed.py
"""
import os
import re
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE, "recipes")
OUT_PATH = os.path.join(BASE, "feed.xml")
SITE_URL = "https://www.marsrecipes.com"


def get_meta(content, prop):
    m = re.search(r'<meta property="' + prop + r'" content="([^"]+)"', content)
    if m:
        return m.group(1)
    m = re.search(r'<meta name="' + prop + r'" content="([^"]+)"', content)
    if m:
        return m.group(1)
    return ""


def get_date(content):
    m = re.search(r'"datePublished":\s*"([^"]+)"', content)
    if m:
        try:
            d = datetime.strptime(m.group(1), "%Y-%m-%d")
            # RFC 822 format for RSS
            return d.strftime("%a, %d %b %Y 09:00:00 +0000")
        except ValueError:
            pass
    return "Mon, 01 Jan 2026 09:00:00 +0000"


def get_canonical(content):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    return m.group(1) if m else ""


def escape_xml(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def collect_recipes():
    recipes = []
    for fname in sorted(os.listdir(RECIPES_DIR)):
        if not fname.endswith(".html") or fname == "index.html":
            continue
        with open(os.path.join(RECIPES_DIR, fname), "r", encoding="utf-8") as f:
            content = f.read()

        title = get_meta(content, "og:title")
        description = get_meta(content, "og:description")
        image = get_meta(content, "og:image")
        link = get_canonical(content)
        pub_date = get_date(content)

        if not title or not link:
            continue

        recipes.append(
            {
                "title": title,
                "description": description,
                "image": image,
                "link": link,
                "pub_date": pub_date,
                "fname": fname,
            }
        )

    def parse_date(r):
        try:
            return datetime.strptime(r["pub_date"][:16], "%a, %d %b %Y")
        except ValueError:
            return datetime.min

    recipes.sort(key=parse_date, reverse=True)
    return recipes


def build_rss(recipes):
    items_xml = ""
    for r in recipes:
        items_xml += """
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <description>{description}</description>
    <pubDate>{pub_date}</pubDate>
    <enclosure url="{image}" type="image/png" length="0"/>
    <media:content url="{image}" medium="image"/>
  </item>""".format(
            title=escape_xml(r["title"]),
            link=r["link"],
            description=escape_xml(r["description"]),
            pub_date=r["pub_date"],
            image=r["image"],
        )

    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:media="http://search.yahoo.com/mrss/"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Mars Recipes</title>
    <link>{site_url}</link>
    <description>Easy, delicious recipes for busy weeknights. Weeknight dinners, one-pan wonders, and comfort food classics ready in 30 minutes or less.</description>
    <language>en-us</language>
    <copyright>2026 Mars Recipes</copyright>
    <managingEditor>hello@marsrecipes.com (Mars)</managingEditor>
    <webMaster>hello@marsrecipes.com (Mars)</webMaster>
    <lastBuildDate>{build_date}</lastBuildDate>
    <ttl>1440</ttl>
    <image>
      <url>{site_url}/images/og-default.svg</url>
      <title>Mars Recipes</title>
      <link>{site_url}</link>
    </image>
    <atom:link href="{site_url}/feed.xml" rel="self" type="application/rss+xml"/>
{items}
  </channel>
</rss>""".format(
        site_url=SITE_URL,
        build_date=datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"),
        items=items_xml,
    )


def main():
    recipes = collect_recipes()
    rss = build_rss(recipes)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(rss)
    print("feed.xml created with %d recipes." % len(recipes))
    print("Saved to: " + OUT_PATH)


if __name__ == "__main__":
    main()
