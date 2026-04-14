import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

# Map slug -> real image extension for Pinterest
IMG_EXT = {
    "beef-broccoli-stir-fry":         "jpg.png",   # no hero, will use -cooking
    "coconut-chicken-curry":           "jpg.png",
    "creamy-sun-dried-tomato-pasta":   "jpg.png",
    "easy-chicken-tikka-masala":       "jpg.png",
    "ground-beef-kofta-garlic-sauce":  "jpg.png",
    "smoky-paprika-baked-salmon":      "jpg.png",
    "spicy-garlic-butter-shrimp":      "jpg.png",
    "creamy-tuscan-shrimp":            "jpg.png",
    "crispy-baked-chicken-wings":      "jpg.png",
    "crispy-honey-garlic-salmon":      "jpg.png",
    "easy-creamy-garlic-chicken":      "jpg.png",
    "garlic-butter-steak-bites":       "jpg.png",
    "lemon-herb-sheet-pan-chicken":    "jpg.png",
    "one-pan-beef-shawarma-bowl":      "png",
    "one-pan-honey-butter-chicken":    "jpg.png",
}

# For beef-broccoli there's no hero so use the cooking image
PINTEREST_IMG = {
    "beef-broccoli-stir-fry": "https://marsrecipes.com/images/beef-broccoli-stir-fry-cooking.jpg.png",
}

for fname in os.listdir(BASE):
    if not fname.endswith(".html"):
        continue
    slug = fname.replace(".html", "")
    path = BASE + fname
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # 1. Fix Pinterest image URL from .svg to real photo
    ext = IMG_EXT.get(slug, "jpg.png")
    if slug in PINTEREST_IMG:
        new_img = PINTEREST_IMG[slug]
    else:
        new_img = f"https://marsrecipes.com/images/{slug}.{ext}"

    # Replace .svg in Pinterest media param
    content = re.sub(
        r'(pinterest\.com/pin/create/button/\?[^"]*&media=https://[^&"]+)\.svg',
        lambda m: m.group(0).replace(".svg", f".{ext}"),
        content
    )

    # 2. Add Facebook share button after Copy Link button (if not already there)
    fb_share_url = f"https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fmarsrecipes.com%2Frecipes%2F{slug}.html"

    if 'btn-facebook' not in content:
        old_copy = '<button class="btn btn-outline btn-copy-link"'
        new_copy = f'<a href="{fb_share_url}" target="_blank" rel="noopener" class="btn btn-facebook" aria-label="Share on Facebook">&#x1F4C4; Share</a>\n          <button class="btn btn-outline btn-copy-link"'
        content = content.replace(old_copy, new_copy, 1)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated: " + fname)
    else:
        print("No change: " + fname)

print("Done.")
