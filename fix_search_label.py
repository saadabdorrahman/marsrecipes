"""Add Search label span inside the search button on all HTML pages."""
import os, glob

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/"
files = glob.glob(BASE + "*.html") + glob.glob(BASE + "recipes/*.html")

OLD = 'aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>'
NEW = 'aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><span class="search-btn-label">Search</span></button>'

updated = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if OLD in content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.replace(OLD, NEW))
        updated += 1
        print("Updated:", os.path.basename(path))

print(f"\nDone. {updated} files updated.")
