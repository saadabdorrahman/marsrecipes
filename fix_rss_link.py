"""
fix_rss_link.py — Add RSS autodiscovery <link> tag to all HTML pages
"""
import os, glob

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/"

RSS_LINK_ROOT    = '  <link rel="alternate" type="application/rss+xml" title="Mars Recipes Feed" href="https://www.marsrecipes.com/feed.xml">'
RSS_LINK_RECIPE  = '  <link rel="alternate" type="application/rss+xml" title="Mars Recipes Feed" href="https://www.marsrecipes.com/feed.xml">'

html_files = glob.glob(BASE + "*.html") + glob.glob(BASE + "recipes/*.html")
updated = 0
for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if 'application/rss+xml' in content:
        continue
    if '</head>' not in content:
        continue
    content = content.replace('</head>', RSS_LINK_ROOT + '\n</head>', 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    updated += 1

print("RSS link added to %d pages." % updated)
