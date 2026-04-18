#!/usr/bin/env python3
"""Generate WordPress WXR import file from static HTML recipe pages."""
import json, re, os, glob
from datetime import datetime

RECIPES_DIR = os.path.join(os.path.dirname(__file__), 'recipes')
OUTPUT = os.path.join(os.path.dirname(__file__), 'marsrecipes-theme', 'marsrecipes-import.xml')

cat_map = {
    'beef-broccoli-stir-fry': 'beef',
    'coconut-chicken-curry': 'chicken',
    'creamy-sun-dried-tomato-pasta': 'pasta',
    'creamy-tuscan-shrimp': 'seafood',
    'crispy-baked-chicken-wings': 'chicken',
    'crispy-honey-garlic-salmon': 'seafood',
    'easy-chicken-tikka-masala': 'chicken',
    'easy-creamy-garlic-chicken': 'chicken',
    'garlic-butter-steak-bites': 'beef',
    'ground-beef-kofta-garlic-sauce': 'beef',
    'lemon-herb-sheet-pan-chicken': 'chicken',
    'one-pan-beef-shawarma-bowl': 'beef',
    'one-pan-honey-butter-chicken': 'chicken',
    'smoky-paprika-baked-salmon': 'seafood',
    'spicy-garlic-butter-shrimp': 'seafood',
}

badge_map = {
    'easy-chicken-tikka-masala': 'trending',
    'spicy-garlic-butter-shrimp': 'trending',
    'beef-broccoli-stir-fry': 'trending',
    'crispy-honey-garlic-salmon': 'quick',
    'garlic-butter-steak-bites': 'quick',
    'creamy-tuscan-shrimp': 'new',
    'one-pan-honey-butter-chicken': 'new',
    'coconut-chicken-curry': 'popular',
}

def iso_to_minutes(iso):
    m = re.search(r'PT(\d+)M', iso or '')
    return m.group(1) + ' min' if m else ''

recipes = []
for f in sorted(glob.glob(os.path.join(RECIPES_DIR, '*.html'))):
    if os.path.basename(f) == 'index.html':
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    blocks = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', content, re.DOTALL)
    recipe_data = None
    for b in blocks:
        try:
            data = json.loads(b)
            if data.get('@type') == 'Recipe':
                recipe_data = data
                break
        except Exception:
            pass
    if not recipe_data:
        continue

    slug = os.path.basename(f).replace('.html', '')
    nutrition = recipe_data.get('nutrition', {})
    ingredients = recipe_data.get('recipeIngredient', [])
    instructions = recipe_data.get('recipeInstructions', [])

    # Extract article body
    body_match = re.search(r'<div class="article-body">(.*?)</div>\s*</article>', content, re.DOTALL)
    article_body = body_match.group(1).strip() if body_match else ''
    # Fix image paths
    article_body = article_body.replace('../images/', '/wp-content/uploads/marsrecipes/')
    # Remove ad slots
    article_body = re.sub(r'<div class="ad-slot[^"]*"[^>]*>.*?</div>', '', article_body, flags=re.DOTALL)

    recipes.append({
        'name': recipe_data['name'],
        'slug': slug,
        'description': recipe_data.get('description', ''),
        'date_published': recipe_data.get('datePublished', '2026-01-01'),
        'prep_time': iso_to_minutes(recipe_data.get('prepTime', '')),
        'cook_time': iso_to_minutes(recipe_data.get('cookTime', '')),
        'total_time': iso_to_minutes(recipe_data.get('totalTime', '')),
        'servings': re.sub(r'\s*servings?', '', recipe_data.get('recipeYield', '4')),
        'calories': nutrition.get('calories', '').replace(' calories', ' kcal'),
        'difficulty': 'Easy',
        'cuisine': recipe_data.get('recipeCuisine', 'American'),
        'ingredients': '\n'.join(ingredients),
        'instructions': '\n'.join([s.get('text', '') if isinstance(s, dict) else s for s in instructions]),
        'category': cat_map.get(slug, 'chicken'),
        'badge': badge_map.get(slug, ''),
        'nutrition_calories': nutrition.get('calories', '').replace(' calories', ' kcal'),
        'nutrition_carbs': nutrition.get('carbohydrateContent', ''),
        'nutrition_protein': nutrition.get('proteinContent', ''),
        'nutrition_fat': nutrition.get('fatContent', ''),
        'nutrition_sodium': nutrition.get('sodiumContent', ''),
        'article_body': article_body,
    })
    print(f'OK: {slug} -> {recipe_data["name"]}')

print(f'\nTotal: {len(recipes)} recipes extracted')

# --- Build WXR XML ---
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
post_id = 100

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<rss version="2.0"')
lines.append('  xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"')
lines.append('  xmlns:content="http://purl.org/rss/1.0/modules/content/"')
lines.append('  xmlns:wfw="http://wellformedweb.org/CommentAPI/"')
lines.append('  xmlns:dc="http://purl.org/dc/elements/1.1/"')
lines.append('  xmlns:wp="http://wordpress.org/export/1.2/"')
lines.append('>')
lines.append('<channel>')
lines.append('  <title>Mars Recipes</title>')
lines.append('  <link>https://www.marsrecipes.com</link>')
lines.append('  <description>Easy weeknight dinner recipes in 30 minutes or less</description>')
lines.append('  <language>en-US</language>')
lines.append('  <wp:wxr_version>1.2</wp:wxr_version>')
lines.append('  <wp:base_site_url>https://www.marsrecipes.com</wp:base_site_url>')
lines.append('  <wp:base_blog_url>https://www.marsrecipes.com</wp:base_blog_url>')
lines.append('')

# Taxonomy terms
cats = [
    (1, 'chicken', 'Chicken'),
    (2, 'beef', 'Beef'),
    (3, 'seafood', 'Seafood'),
    (4, 'pasta', 'Pasta'),
    (5, 'quick', 'Quick Meals'),
    (6, 'vegetarian', 'Vegetarian'),
]
for tid, tslug, tname in cats:
    lines.append(f'  <wp:term>')
    lines.append(f'    <wp:term_id>{tid}</wp:term_id>')
    lines.append(f'    <wp:term_taxonomy>recipe_category</wp:term_taxonomy>')
    lines.append(f'    <wp:term_slug>{tslug}</wp:term_slug>')
    lines.append(f'    <wp:term_name><![CDATA[{tname}]]></wp:term_name>')
    lines.append(f'  </wp:term>')

# Recipe items
for r in recipes:
    post_id += 1
    pub = r['date_published'] + ' 12:00:00'
    cat_label = r['category'].capitalize()

    meta_fields = [
        ('_recipe_prep_time', r['prep_time']),
        ('_recipe_cook_time', r['cook_time']),
        ('_recipe_total_time', r['total_time']),
        ('_recipe_servings', r['servings']),
        ('_recipe_calories', r['calories']),
        ('_recipe_difficulty', r['difficulty']),
        ('_recipe_cuisine', r['cuisine']),
        ('_recipe_ingredients', r['ingredients']),
        ('_recipe_instructions', r['instructions']),
        ('_recipe_badge', r['badge']),
        ('_nutrition_calories', r['nutrition_calories']),
        ('_nutrition_carbs', r['nutrition_carbs']),
        ('_nutrition_protein', r['nutrition_protein']),
        ('_nutrition_fat', r['nutrition_fat']),
        ('_nutrition_sodium', r['nutrition_sodium']),
    ]

    lines.append('')
    lines.append('  <item>')
    lines.append(f'    <title><![CDATA[{r["name"]}]]></title>')
    lines.append(f'    <link>https://www.marsrecipes.com/recipes/{r["slug"]}/</link>')
    lines.append(f'    <pubDate>{pub}</pubDate>')
    lines.append(f'    <dc:creator><![CDATA[mars]]></dc:creator>')
    lines.append(f'    <description><![CDATA[{r["description"]}]]></description>')
    lines.append(f'    <content:encoded><![CDATA[{r["article_body"]}]]></content:encoded>')
    lines.append(f'    <excerpt:encoded><![CDATA[{r["description"]}]]></excerpt:encoded>')
    lines.append(f'    <wp:post_id>{post_id}</wp:post_id>')
    lines.append(f'    <wp:post_date>{pub}</wp:post_date>')
    lines.append(f'    <wp:post_date_gmt>{pub}</wp:post_date_gmt>')
    lines.append(f'    <wp:post_modified>{now}</wp:post_modified>')
    lines.append(f'    <wp:post_modified_gmt>{now}</wp:post_modified_gmt>')
    lines.append(f'    <wp:comment_status>open</wp:comment_status>')
    lines.append(f'    <wp:ping_status>closed</wp:ping_status>')
    lines.append(f'    <wp:post_name>{r["slug"]}</wp:post_name>')
    lines.append(f'    <wp:status>publish</wp:status>')
    lines.append(f'    <wp:post_type>recipe</wp:post_type>')
    lines.append(f'    <category domain="recipe_category" nicename="{r["category"]}"><![CDATA[{cat_label}]]></category>')
    for mk, mv in meta_fields:
        lines.append(f'    <wp:postmeta><wp:meta_key>{mk}</wp:meta_key><wp:meta_value><![CDATA[{mv}]]></wp:meta_value></wp:postmeta>')
    lines.append('  </item>')

lines.append('')
lines.append('</channel>')
lines.append('</rss>')

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'\nWXR import file created: {OUTPUT}')
print(f'Contains {len(recipes)} recipes with full metadata + content')
