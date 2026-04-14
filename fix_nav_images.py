"""
fix_nav_images.py
- Remove recipe-section-image figures injected inside <header> / nav area
- Re-insert the cooking image in the correct position: after the
  first </li> containing the cook_marker inside <ol class="recipe-instructions">
"""
import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

COOK_MARKERS = {
    "beef-broccoli-stir-fry":         "sauce",
    "coconut-chicken-curry":           "coconut",
    "easy-chicken-tikka-masala":       "cream",
    "ground-beef-kofta-garlic-sauce":  "garlic",
    "smoky-paprika-baked-salmon":      "paprika",
    "spicy-garlic-butter-shrimp":      "chicken broth",
}

SEO_ALTS = {
    "beef-broccoli-stir-fry":        "Beef and broccoli stir frying in wok with glossy soy garlic sauce sizzling",
    "coconut-chicken-curry":          "Coconut chicken curry simmering in Dutch oven with golden turmeric sauce",
    "easy-chicken-tikka-masala":      "Chicken tikka masala sauce simmering in skillet with cream swirl and chicken chunks",
    "ground-beef-kofta-garlic-sauce": "Beef kofta skewers searing on ridged cast iron grill pan with char marks forming",
    "smoky-paprika-baked-salmon":     "Smoky paprika salmon baking in oven with caramelized spice crust forming",
    "spicy-garlic-butter-shrimp":     "Spicy garlic butter shrimp sizzling in cast iron skillet with garlic and red pepper",
}

def make_cook_fig(slug, alt):
    return (
        "\n                  <figure class=\"recipe-section-image\" style=\"margin-top:1.25rem;\">\n"
        "                    <img src=\"../images/" + slug + "-cooking.jpg.png\"\n"
        "                         alt=\"" + alt + "\"\n"
        "                         width=\"800\" height=\"533\" loading=\"lazy\" decoding=\"async\"\n"
        "                         onerror=\"this.style.display='none'\">\n"
        "                  </figure>"
    )

for slug, cook_marker in COOK_MARKERS.items():
    path = BASE + slug + ".html"
    if not os.path.exists(path):
        print("SKIP (not found): " + slug)
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # ── Step 1: Remove ALL recipe-section-image figures from inside <header> ──
    # The site-header ends before <main>. We'll clean the first 3000 chars
    # (header area) of any injected figure.
    header_end = content.find("<main")
    if header_end == -1:
        header_end = content.find("<!-- ===== MAIN")
    if header_end == -1:
        header_end = content.find("<!-- Breadcrumb")
    if header_end == -1:
        header_end = 3000  # fallback

    head_section = content[:header_end]
    # Remove any <figure class="recipe-section-image"...>...</figure> in header area
    cleaned_head = re.sub(
        r'\n?\s*<figure class="recipe-section-image"[^>]*>.*?</figure>',
        '',
        head_section,
        flags=re.DOTALL
    )
    content = cleaned_head + content[header_end:]

    # ── Step 2: Also remove any stray figure injected directly inside <ul> nav ──
    # Pattern: </li> + figure + <li> inside first <nav> or header
    content = re.sub(
        r'(</li>)\s*\n\s*(<figure class="recipe-section-image"[^>]*>.*?</figure>)\s*\n\s*(<li)',
        r'\1\n          \3',
        content,
        flags=re.DOTALL
    )

    # ── Step 3: Re-insert cooking image in correct position ─────────────────
    # Only add if not already present in the instructions area
    instructions_start = content.find('<ol class="recipe-instructions">')
    if instructions_start == -1:
        instructions_start = content.find('<ol class="instructions-list">')
    if instructions_start == -1:
        print("No instructions OL found: " + slug)
        continue

    # Check if cooking image already exists AFTER the instructions start
    already_present = (slug + "-cooking") in content[instructions_start:]
    if already_present:
        print("Cooking image already in instructions: " + slug)
        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  -> Removed bad injection from nav")
        continue

    # Find cook_marker within the instructions section only
    instructions_section = content[instructions_start:]
    marker_pos = instructions_section.lower().find(cook_marker.lower())
    if marker_pos == -1:
        print("Cook marker '%s' not found in instructions: %s" % (cook_marker, slug))
        continue

    # Find the </li> that closes the step containing the marker
    close_li_pos = instructions_section.find("</li>", marker_pos)
    if close_li_pos == -1:
        print("No </li> after cook marker: " + slug)
        continue

    # Build and insert the figure
    alt = SEO_ALTS.get(slug, "Recipe cooking in pan")
    cook_fig = make_cook_fig(slug, alt)

    abs_insert = instructions_start + close_li_pos + 5  # after </li>
    content = content[:abs_insert] + cook_fig + content[abs_insert:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    if content != original:
        print("Fixed: " + slug + ".html")
    else:
        print("No change: " + slug + ".html")

print("\nDone.")
