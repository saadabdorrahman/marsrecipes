import os, re

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/recipes/"

AVAILABLE = {
    "beef-broccoli-stir-fry":         {"hero": False, "ingredients": False, "cooking": True,  "serving": True},
    "coconut-chicken-curry":           {"hero": True,  "ingredients": True,  "cooking": True,  "serving": True},
    "creamy-sun-dried-tomato-pasta":   {"hero": True,  "ingredients": True,  "cooking": True,  "serving": False},
    "easy-chicken-tikka-masala":       {"hero": True,  "ingredients": True,  "cooking": True,  "serving": True},
    "ground-beef-kofta-garlic-sauce":  {"hero": True,  "ingredients": True,  "cooking": True,  "serving": False},
    "smoky-paprika-baked-salmon":      {"hero": True,  "ingredients": True,  "cooking": True,  "serving": True},
    "spicy-garlic-butter-shrimp":      {"hero": False, "ingredients": True,  "cooking": True,  "serving": True},
}

SEO_ALTS = {
    "beef-broccoli-stir-fry": {
        "cooking": "Beef and broccoli stir frying in wok with glossy soy garlic sauce sizzling",
        "serving": "Beef and broccoli stir fry served over steamed jasmine rice in white bowl",
    },
    "coconut-chicken-curry": {
        "hero": "Creamy coconut chicken curry in golden turmeric sauce served with fluffy basmati rice",
        "ingredients": "All ingredients for coconut chicken curry on white marble countertop",
        "cooking": "Coconut chicken curry simmering in Dutch oven with golden turmeric sauce",
        "serving": "Coconut chicken curry served in white bowl over basmati rice with cilantro and lime",
    },
    "creamy-sun-dried-tomato-pasta": {
        "hero": "Creamy sun-dried tomato pasta with Parmesan, fresh basil and al dente pappardelle",
        "ingredients": "All ingredients for creamy sun-dried tomato pasta on white quartz surface",
        "cooking": "Sun-dried tomato cream sauce simmering in stainless pan with garlic and basil",
    },
    "easy-chicken-tikka-masala": {
        "hero": "Easy chicken tikka masala in rich orange cream sauce with tender chicken and fresh cilantro",
        "ingredients": "All ingredients for chicken tikka masala on white marble countertop",
        "cooking": "Chicken tikka masala sauce simmering in skillet with cream swirl and chicken chunks",
        "serving": "Chicken tikka masala served in white bowl with garlic naan and basmati rice",
    },
    "ground-beef-kofta-garlic-sauce": {
        "hero": "Ground beef kofta skewers with dark grill marks served with creamy white garlic sauce",
        "ingredients": "All ingredients for ground beef kofta with garlic sauce on white quartz",
        "cooking": "Beef kofta skewers searing on ridged cast iron grill pan with char marks forming",
    },
    "smoky-paprika-baked-salmon": {
        "hero": "Smoky paprika baked salmon fillets with caramelized spice crust and fresh dill",
        "ingredients": "All ingredients for smoky paprika baked salmon on white marble countertop",
        "cooking": "Smoky paprika salmon baking in oven with caramelized spice crust forming",
        "serving": "Smoky paprika salmon plated over herbed quinoa with lemon wedge and dill",
    },
    "spicy-garlic-butter-shrimp": {
        "ingredients": "All ingredients for spicy garlic butter shrimp on white quartz countertop",
        "cooking": "Spicy garlic butter shrimp sizzling in cast iron skillet with garlic and red pepper",
        "serving": "Spicy garlic butter shrimp served over jasmine rice with fresh parsley and lemon",
    },
}

COOK_MARKERS = {
    "beef-broccoli-stir-fry":        "sauce",
    "coconut-chicken-curry":         "coconut",
    "creamy-sun-dried-tomato-pasta": "melted",
    "easy-chicken-tikka-masala":     "cream",
    "ground-beef-kofta-garlic-sauce":"garlic",
    "smoky-paprika-baked-salmon":    "paprika",
    "spicy-garlic-butter-shrimp":    "chicken broth",
}

SERVE_MARKERS = {
    "beef-broccoli-stir-fry":        "<h2>Serving Suggestions</h2>",
    "coconut-chicken-curry":         "<h2>Serving Suggestions</h2>",
    "easy-chicken-tikka-masala":     "<h2>Serving Suggestions</h2>",
    "smoky-paprika-baked-salmon":    "<h2>Serving Suggestions</h2>",
}

for slug, avail in AVAILABLE.items():
    fname = slug + ".html"
    path = BASE + fname
    if not os.path.exists(path):
        print("MISSING: " + fname)
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    alts = SEO_ALTS.get(slug, {})

    # 1. Update hero image (SVG -> jpg.png)
    if avail["hero"]:
        old_src = 'src="../images/' + slug + '.svg"'
        new_src = 'src="../images/' + slug + '.jpg.png"'
        content = content.replace(old_src, new_src)
        old_jld = '"image": ["https://marsrecipes.com/images/' + slug + '.svg"]'
        new_jld = '"image": ["https://marsrecipes.com/images/' + slug + '.jpg.png"]'
        content = content.replace(old_jld, new_jld)

    # 2. Add ingredients image after <h3>Ingredients</h3>
    if avail["ingredients"] and (slug + "-ingredients") not in content:
        ing_fig = (
            "\n              <figure class=\"recipe-section-image\">\n"
            "                <img src=\"../images/" + slug + "-ingredients.jpg.png\"\n"
            "                     alt=\"" + alts.get("ingredients", "Recipe ingredients on white marble") + "\"\n"
            "                     width=\"800\" height=\"533\" loading=\"lazy\" decoding=\"async\"\n"
            "                     onerror=\"this.style.display='none'\">\n"
            "              </figure>"
        )
        content = content.replace("<h3>Ingredients</h3>", "<h3>Ingredients</h3>" + ing_fig, 1)

    # 3. Add cooking image after first </li> following cook_marker
    if avail["cooking"] and (slug + "-cooking") not in content:
        cook_marker = COOK_MARKERS.get(slug, "")
        cook_fig = (
            "\n                  <figure class=\"recipe-section-image\" style=\"margin-top:1.25rem;\">\n"
            "                    <img src=\"../images/" + slug + "-cooking.jpg.png\"\n"
            "                         alt=\"" + alts.get("cooking", "Recipe cooking in pan") + "\"\n"
            "                         width=\"800\" height=\"533\" loading=\"lazy\" decoding=\"async\"\n"
            "                         onerror=\"this.style.display='none'\">\n"
            "                  </figure>"
        )
        if cook_marker and cook_marker in content:
            idx = content.find(cook_marker)
            close_li = content.find("</li>", idx)
            if close_li != -1:
                content = content[:close_li+5] + cook_fig + content[close_li+5:]

    # 4. Add serving image after serve_marker
    serve_marker = SERVE_MARKERS.get(slug, "")
    if avail["serving"] and (slug + "-serving") not in content and serve_marker and serve_marker in content:
        serve_fig = (
            "\n          <figure class=\"recipe-section-image\">\n"
            "            <img src=\"../images/" + slug + "-serving.jpg.png\"\n"
            "                 alt=\"" + alts.get("serving", "Recipe plated and ready to serve") + "\"\n"
            "                 width=\"800\" height=\"533\" loading=\"lazy\" decoding=\"async\"\n"
            "                 onerror=\"this.style.display='none'\">\n"
            "          </figure>"
        )
        idx = content.find(serve_marker)
        end_line = content.find("\n", idx)
        content = content[:end_line+1] + serve_fig + content[end_line+1:]

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated: " + fname)
    else:
        print("No change: " + fname)

print("Done.")
