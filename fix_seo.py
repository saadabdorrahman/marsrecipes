"""
fix_seo.py — Mars Recipes SEO fixes
1. FAQ Schema JSON-LD on all 15 recipe pages
2. Fix OG/Twitter image tags (.svg → real photo)
3. Add og:image:alt and twitter:image:alt
"""

import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

# Hero image extension per recipe (what file actually exists)
HERO_EXT = {
    "beef-broccoli-stir-fry":         "beef-broccoli-stir-fry-cooking.jpg.png",
    "coconut-chicken-curry":           "coconut-chicken-curry.jpg.png",
    "creamy-sun-dried-tomato-pasta":   "creamy-sun-dried-tomato-pasta.jpg.png",
    "easy-chicken-tikka-masala":       "easy-chicken-tikka-masala.jpg.png",
    "ground-beef-kofta-garlic-sauce":  "ground-beef-kofta-garlic-sauce.jpg.png",
    "smoky-paprika-baked-salmon":      "smoky-paprika-baked-salmon.jpg.png",
    "spicy-garlic-butter-shrimp":      "spicy-garlic-butter-shrimp.jpg.png",
    "creamy-tuscan-shrimp":            "creamy-tuscan-shrimp.jpg.png",
    "crispy-baked-chicken-wings":      "crispy-baked-chicken-wings.jpg.png",
    "crispy-honey-garlic-salmon":      "crispy-honey-garlic-salmon.jpg.png",
    "easy-creamy-garlic-chicken":      "easy-creamy-garlic-chicken.jpg.png",
    "garlic-butter-steak-bites":       "garlic-butter-steak-bites.jpg.png",
    "lemon-herb-sheet-pan-chicken":    "lemon-herb-sheet-pan-chicken.jpg.png",
    "one-pan-beef-shawarma-bowl":      "one-pan-beef-shawarma-bowl.png",
    "one-pan-honey-butter-chicken":    "one-pan-honey-butter-chicken.jpg.png",
}

def extract_faqs(content):
    """Extract (question, answer) pairs from <details class="faq-item"> elements.
    Handles both direct <p> and <div class="faq-answer"><p> wrappers."""
    faqs = []
    details_blocks = re.findall(
        r'<details[^>]*class="faq-item"[^>]*>(.*?)</details>',
        content, re.DOTALL
    )
    for block in details_blocks:
        q_match = re.search(r'<summary>(.*?)</summary>', block, re.DOTALL)
        # Try direct <p> first, then inside any <div> wrapper
        a_match = re.search(r'</summary>\s*<p>(.*?)</p>', block, re.DOTALL)
        if not a_match:
            a_match = re.search(r'</summary>.*?<p>(.*?)</p>', block, re.DOTALL)
        if q_match and a_match:
            question = re.sub(r'<[^>]+>', '', q_match.group(1)).strip()
            answer   = re.sub(r'<[^>]+>', '', a_match.group(1)).strip()
            # Collapse whitespace
            question = re.sub(r'\s+', ' ', question)
            answer   = re.sub(r'\s+', ' ', answer)
            # Escape quotes for JSON
            question = question.replace('\\', '\\\\').replace('"', '\\"')
            answer   = answer.replace('\\', '\\\\').replace('"', '\\"')
            faqs.append((question, answer))
    return faqs

def make_faq_schema(faqs):
    """Build FAQPage JSON-LD string."""
    items = []
    for q, a in faqs:
        items.append(
            '    {\n'
            '      "@type": "Question",\n'
            '      "name": "' + q + '",\n'
            '      "acceptedAnswer": {\n'
            '        "@type": "Answer",\n'
            '        "text": "' + a + '"\n'
            '      }\n'
            '    }'
        )
    return (
        '  <script type="application/ld+json">\n'
        '  {\n'
        '    "@context": "https://schema.org",\n'
        '    "@type": "FAQPage",\n'
        '    "mainEntity": [\n'
        + ',\n'.join(items) + '\n'
        '    ]\n'
        '  }\n'
        '  </script>'
    )

updated = 0
for fname in sorted(os.listdir(BASE)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    slug = fname.replace(".html", "")
    path = BASE + fname
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # ── 1. FAQ Schema ──────────────────────────────────────────
    if 'FAQPage' not in content:
        faqs = extract_faqs(content)
        if faqs:
            faq_block = make_faq_schema(faqs)
            # Insert before </head>
            content = content.replace('</head>', faq_block + '\n</head>', 1)

    # ── 2. Fix OG image (.svg → real photo) ────────────────────
    img_file = HERO_EXT.get(slug, slug + ".jpg.png")
    real_img_url = "https://www.marsrecipes.com/images/" + img_file

    # Replace .svg in og:image
    content = re.sub(
        r'(<meta property="og:image" content=")[^"]+(")',
        r'\g<1>' + real_img_url + r'\g<2>',
        content
    )
    # Replace .svg in twitter:image
    content = re.sub(
        r'(<meta name="twitter:image" content=")[^"]+(")',
        r'\g<1>' + real_img_url + r'\g<2>',
        content
    )

    # ── 3. Add og:image:alt if missing ─────────────────────────
    if 'og:image:alt' not in content:
        # Get og:title for the alt text
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', content)
        alt_text = title_match.group(1) if title_match else slug.replace("-", " ").title()
        alt_tag = '<meta property="og:image:alt" content="' + alt_text + '">'
        content = content.replace(
            '<meta property="og:image"',
            alt_tag + '\n  <meta property="og:image"',
            1
        )

    # ── 4. Add twitter:image:alt if missing ────────────────────
    if 'twitter:image:alt' not in content:
        title_match = re.search(r'<meta name="twitter:title" content="([^"]+)"', content)
        alt_text = title_match.group(1) if title_match else slug.replace("-", " ").title()
        alt_tag = '<meta name="twitter:image:alt" content="' + alt_text + '">'
        content = content.replace(
            '<meta name="twitter:image"',
            alt_tag + '\n  <meta name="twitter:image"',
            1
        )

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1
        print("Updated: " + fname)
    else:
        print("No change: " + fname)

print(f"\nDone. {updated} files updated.")
