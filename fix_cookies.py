"""
fix_cookies.py — Add cookie consent banner HTML to all site pages
The CSS goes into style.css and the JS logic goes into main.js
"""
import os, glob

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/"

BANNER_HTML = '''
<!-- ============================================================
     Cookie Consent Banner (GDPR / CCPA)
============================================================ -->
<div id="cookieConsent" class="cookie-consent" role="dialog" aria-labelledby="cookieTitle" aria-describedby="cookieDesc" hidden>
  <div class="cookie-consent__inner">
    <div class="cookie-consent__text">
      <p id="cookieTitle"><strong>We use cookies</strong></p>
      <p id="cookieDesc">We use cookies to analyze traffic and improve your experience. By clicking "Accept", you consent to our use of cookies. <a href="privacy-policy.html" class="cookie-link">Privacy Policy</a></p>
    </div>
    <div class="cookie-consent__actions">
      <button id="cookieDecline" class="cookie-btn cookie-btn--decline">Decline</button>
      <button id="cookieAccept" class="cookie-btn cookie-btn--accept">Accept</button>
    </div>
  </div>
</div>'''

# All HTML files in root + recipes/
html_files = (
    glob.glob(BASE + "*.html") +
    glob.glob(BASE + "recipes/*.html")
)

updated = 0
for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "cookieConsent" in content:
        print("Skip (already has banner): " + os.path.basename(path))
        continue
    # Insert just before </body>
    if "</body>" not in content:
        print("Skip (no </body>): " + os.path.basename(path))
        continue
    content = content.replace("</body>", BANNER_HTML + "\n</body>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    updated += 1
    print("Updated: " + os.path.basename(path))

print(f"\nDone. {updated} files updated.")
