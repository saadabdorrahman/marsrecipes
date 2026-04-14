"""
fix_all_svgs.py
Replace every recipe .svg image reference with the real food photo.
Works on all HTML files in both /recipes/ and root directory.
"""
import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/"
DIRS = [BASE, BASE + "recipes/"]

# SVG slug -> real image file (relative to /images/)
IMG_MAP = {
    "beef-broccoli-stir-fry":        "beef-broccoli-stir-fry-cooking.jpg.png",
    "coconut-chicken-curry":          "coconut-chicken-curry.jpg.png",
    "creamy-sun-dried-tomato-pasta":  "creamy-sun-dried-tomato-pasta.jpg.png",
    "creamy-tuscan-shrimp":           "creamy-tuscan-shrimp.jpg.png",
    "crispy-baked-chicken-wings":     "crispy-baked-chicken-wings.jpg.png",
    "crispy-honey-garlic-salmon":     "crispy-honey-garlic-salmon.jpg.png",
    "easy-chicken-tikka-masala":      "easy-chicken-tikka-masala.jpg.png",
    "easy-creamy-garlic-chicken":     "easy-creamy-garlic-chicken.jpg.png",
    "garlic-butter-steak-bites":      "garlic-butter-steak-bites.jpg.png",
    "ground-beef-kofta-garlic-sauce": "ground-beef-kofta-garlic-sauce.jpg.png",
    "lemon-herb-sheet-pan-chicken":   "lemon-herb-sheet-pan-chicken.jpg.png",
    "one-pan-beef-shawarma-bowl":     "one-pan-beef-shawarma-bowl.png",
    "one-pan-honey-butter-chicken":   "one-pan-honey-butter-chicken.jpg.png",
    "smoky-paprika-baked-salmon":     "smoky-paprika-baked-salmon.jpg.png",
    "spicy-garlic-butter-shrimp":     "spicy-garlic-butter-shrimp.jpg.png",
}

total = 0
for d in DIRS:
    for fname in os.listdir(d):
        if not fname.endswith(".html"):
            continue
        path = d + fname
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        # 1. Replace src="../images/SLUG.svg" and src="images/SLUG.svg"
        for slug, real_img in IMG_MAP.items():
            # Both relative paths (../images/ for recipe pages, images/ for root)
            content = content.replace(
                '../images/' + slug + '.svg',
                '../images/' + real_img
            )
            content = content.replace(
                'images/' + slug + '.svg',
                'images/' + real_img
            )

        # 2. Fix onerror handlers that fall back to .svg files
        # e.g. onerror="this.src='../images/SLUG.svg'; this.onerror=null;"
        content = re.sub(
            r"onerror=\"this\.src='[^']*\.svg';?\s*this\.onerror=null;?\"",
            "onerror=\"this.style.display='none'\"",
            content
        )
        # Also fix: onerror="this.onerror=null;this.src='../images/SLUG.svg';"
        content = re.sub(
            r"onerror=\"this\.onerror=null;this\.src='[^']*\.svg';?\"",
            "onerror=\"this.style.display='none'\"",
            content
        )

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            total += 1
            print("Fixed:", fname)

print(f"\nDone. {total} files updated.")
