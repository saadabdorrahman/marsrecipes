"""
fix_footer_and_misc.py
Fix old-style recipe pages (5 pages):
1. Replace old <footer class="site-footer"> (footer-inner) with new footer-grid
2. Fix back-to-top: id="back-to-top" -> id="backToTop" + SVG icon
3. Fix cookie consent privacy link: href="privacy-policy.html" -> href="../privacy-policy.html"
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

NEW_FOOTER = """\
<footer class="site-footer" role="contentinfo">
  <div class="container footer-grid">
    <div class="footer-brand">
      <span class="logo-text"><span>Mars</span> Recipes</span>
      <p>Easy, delicious recipes for busy weeknights. Tested and trusted.</p>
      <div class="footer-social">
        <a href="https://www.pinterest.com/saadabdorrahman/pie/" class="social-link" aria-label="Pinterest" target="_blank" rel="noopener">P</a>
        <a href="https://www.facebook.com/profile.php?id=61569030950569" class="social-link" aria-label="Facebook" target="_blank" rel="noopener">f</a>
      </div>
    </div>
    <div class="footer-nav"><h3>Recipes</h3><ul><li><a href="../recipes/index.html?filter=chicken">Chicken</a></li><li><a href="../recipes/index.html?filter=beef">Beef</a></li><li><a href="../recipes/index.html?filter=seafood">Seafood</a></li></ul></div>
    <div class="footer-nav"><h3>Site</h3><ul><li><a href="../about.html">About</a></li><li><a href="../contact.html">Contact</a></li></ul></div>
    <div class="footer-nav"><h3>Legal</h3><ul><li><a href="../privacy-policy.html">Privacy Policy</a></li><li><a href="../disclaimer.html">Disclaimer</a></li></ul></div>
  </div>
  <div class="footer-bottom"><p>\u00a9 2026 Mars Recipes \u00b7 All rights reserved</p></div>
</footer>"""

NEW_BACK_TO_TOP = """\
<button class="back-to-top" id="backToTop" aria-label="Back to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"></polyline></svg>
</button>"""

for slug in OLD_PAGES:
    path = BASE + slug + ".html"
    if not os.path.exists(path):
        print("SKIP (not found):", slug)
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # 1. Replace old footer
    content = re.sub(
        r'<!-- ===== FOOTER ===== -->\s*<footer class="site-footer">.*?</footer>',
        NEW_FOOTER,
        content,
        count=1,
        flags=re.DOTALL
    )
    # Also handle footer without the comment
    if '<div class="container footer-inner">' in content:
        content = re.sub(
            r'<footer class="site-footer">.*?</footer>',
            NEW_FOOTER,
            content,
            count=1,
            flags=re.DOTALL
        )

    # 2. Fix back-to-top button (old: id="back-to-top" with text arrow)
    content = re.sub(
        r'<button[^>]*id="back-to-top"[^>]*>.*?</button>',
        NEW_BACK_TO_TOP,
        content,
        count=1,
        flags=re.DOTALL
    )

    # 3. Fix cookie consent privacy link (wrong relative path for recipe pages)
    content = content.replace(
        'href="privacy-policy.html" class="cookie-link"',
        'href="../privacy-policy.html" class="cookie-link"'
    )

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed:", slug + ".html")
    else:
        print("No change:", slug)

print("\nDone.")
