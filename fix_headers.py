"""
fix_headers.py
Replace old main-nav/hamburger header with the new consistent nav-primary/nav-toggle/nav-mobile header
on the 5 recipe pages that still use the old structure.
"""
import re, os

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

OLD_PAGES = [
    "beef-broccoli-stir-fry",
    "creamy-sun-dried-tomato-pasta",
    "easy-chicken-tikka-masala",
    "smoky-paprika-baked-salmon",
    "spicy-garlic-butter-shrimp",
]

NEW_HEADER = """\
<header class="site-header" role="banner">
  <div class="container header-inner">
    <a href="../index.html" class="logo" aria-label="Mars Recipes \u2013 Home">
      <span class="logo-text"><span>Mars</span> Recipes</span>
    </a>
    <nav class="nav-primary" aria-label="Main navigation">
      <ul>
        <li><a href="../recipes/index.html">Recipes</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
    <button class="search-btn" id="searchToggle" aria-label="Search recipes" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-mobile" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav id="nav-mobile" class="nav-mobile" aria-hidden="true" aria-label="Mobile navigation">
    <ul>
      <li><a href="../recipes/index.html">All Recipes</a></li>
      <li><a href="../about.html">About</a></li>
      <li><a href="../contact.html">Contact</a></li>
    </ul>
  </nav>
</header>"""

for slug in OLD_PAGES:
    path = BASE + slug + ".html"
    if not os.path.exists(path):
        print("SKIP (not found):", slug)
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Match the old header block: from <header ... id="site-header"> to </header>
    # We use a non-greedy match capturing everything inside the header tags
    new_content = re.sub(
        r'<header[^>]*id="site-header"[^>]*>.*?</header>',
        NEW_HEADER,
        content,
        count=1,
        flags=re.DOTALL
    )

    if new_content == content:
        print("No change (old header not found?):", slug)
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed:", slug + ".html")

print("\nDone.")
