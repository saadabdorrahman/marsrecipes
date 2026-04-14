"""
minify.py — Minify CSS and JS for Mars Recipes
Outputs style.min.css and main.min.js
Then updates all HTML files to reference the minified versions.
"""
import os, re, glob

BASE = "C:/Users/Hp/OneDrive/Desktop/marsrecipes claude code/"

# ── CSS Minifier ───────────────────────────────────────────────
def minify_css(src):
    # Remove /* comments */
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    # Remove line comments (shouldn't exist in CSS but just in case)
    src = re.sub(r'//[^\n]*', '', src)
    # Collapse whitespace
    src = re.sub(r'\s+', ' ', src)
    # Remove spaces around structural chars only (NOT inside selectors)
    src = re.sub(r'\s*([{}:;>~+])\s*', r'\1', src)
    # Remove spaces around commas ONLY inside property values (after : not in selectors)
    # Safe: collapse multiple spaces to one (already done above with \s+ -> ' ')
    # Remove space before { after selectors
    src = re.sub(r'\s*\{\s*', r'{', src)
    # Remove trailing semicolon before }
    src = src.replace(';}', '}')
    # Remove leading/trailing whitespace
    src = src.strip()
    return src

# ── JS Minifier (safe, conservative) ──────────────────────────
def minify_js(src):
    lines = []
    for line in src.splitlines():
        stripped = line.strip()
        # Remove single-line comments (not inside strings — conservative)
        # Only remove full-line comments to avoid breaking URLs/regex
        if stripped.startswith('//'):
            continue
        # Remove trailing inline comments only if line doesn't have string
        if '//' in stripped and '"' not in stripped and "'" not in stripped:
            stripped = stripped[:stripped.index('//')].strip()
        if stripped:
            lines.append(stripped)
    src = ' '.join(lines)
    # Collapse multiple spaces
    src = re.sub(r'  +', ' ', src)
    # Remove spaces around operators (safe cases only)
    src = re.sub(r'\s*([{}();,])\s*', r'\1', src)
    return src.strip()

# ── Read source files ──────────────────────────────────────────
css_path = BASE + "css/style.css"
js_path  = BASE + "js/main.js"
css_min_path = BASE + "css/style.min.css"
js_min_path  = BASE + "js/main.min.js"

with open(css_path, "r", encoding="utf-8") as f:
    css_src = f.read()
with open(js_path, "r", encoding="utf-8") as f:
    js_src = f.read()

css_min = minify_css(css_src)
js_min  = minify_js(js_src)

with open(css_min_path, "w", encoding="utf-8") as f:
    f.write(css_min)
with open(js_min_path, "w", encoding="utf-8") as f:
    f.write(js_min)

# Report sizes
css_orig = os.path.getsize(css_path)
css_new  = os.path.getsize(css_min_path)
js_orig  = os.path.getsize(js_path)
js_new   = os.path.getsize(js_min_path)
print("CSS: %dKB -> %dKB (%d%% reduction)" % (css_orig//1024, css_new//1024, 100-int(css_new/css_orig*100)))
print("JS:  %dKB -> %dKB (%d%% reduction)" % (js_orig//1024, js_new//1024, 100-int(js_new/js_orig*100)))

# ── Update all HTML files to use .min. versions ───────────────
html_files = glob.glob(BASE + "*.html") + glob.glob(BASE + "recipes/*.html")
updated = 0
for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Determine correct relative path (recipes/ subfolder needs ../css/)
    is_recipe = "recipes" + os.sep in path or "/recipes/" in path
    if is_recipe:
        css_ref_old = '../css/style.css'
        css_ref_new = '../css/style.min.css'
        js_ref_old  = '../js/main.js'
        js_ref_new  = '../js/main.min.js'
    else:
        css_ref_old = 'css/style.css'
        css_ref_new = 'css/style.min.css'
        js_ref_old  = 'js/main.js'
        js_ref_new  = 'js/main.min.js'

    content = content.replace(css_ref_old, css_ref_new)
    content = content.replace(js_ref_old,  js_ref_new)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1

print(f"Updated {updated} HTML files to use minified assets.")
print("Done.")
