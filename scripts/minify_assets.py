#!/usr/bin/env python3
"""
minify_assets.py — Minify CSS and JS for Mars Recipes.

Portable replacement for the legacy minify.py (which hardcodes a Windows
path). Regenerates css/style.min.css and js/main.min.js from their sources,
then rewrites any HTML file still referencing the unminified assets.

    python3 scripts/minify_assets.py
"""
import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def minify_css(src):
    # Remove /* comments */
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.DOTALL)
    src = re.sub(r"//[^\n]*", "", src)
    # Collapse whitespace
    src = re.sub(r"\s+", " ", src)
    # Remove spaces around structural chars only (NOT inside selectors)
    src = re.sub(r"\s*([{}:;>~+])\s*", r"\1", src)
    src = re.sub(r"\s*\{\s*", r"{", src)
    # Remove trailing semicolon before }
    src = src.replace(";}", "}")
    return src.strip()


def minify_js(src):
    """Conservative JS minifier: strips comments and collapses whitespace."""
    lines = []
    for line in src.splitlines():
        stripped = line.strip()
        # Only remove full-line comments to avoid breaking URLs/regex
        if stripped.startswith("//"):
            continue
        if "//" in stripped and '"' not in stripped and "'" not in stripped:
            stripped = stripped[: stripped.index("//")].strip()
        if stripped:
            lines.append(stripped)
    src = " ".join(lines)
    src = re.sub(r"  +", " ", src)
    src = re.sub(r"\s*([{}();,])\s*", r"\1", src)
    return src.strip()


def main():
    css_path = os.path.join(BASE, "css", "style.css")
    js_path = os.path.join(BASE, "js", "main.js")
    css_min_path = os.path.join(BASE, "css", "style.min.css")
    js_min_path = os.path.join(BASE, "js", "main.min.js")

    with open(css_path, "r", encoding="utf-8") as f:
        css_src = f.read()
    with open(js_path, "r", encoding="utf-8") as f:
        js_src = f.read()

    css_min = minify_css(css_src)
    js_min = minify_js(js_src)

    with open(css_min_path, "w", encoding="utf-8") as f:
        f.write(css_min)
    with open(js_min_path, "w", encoding="utf-8") as f:
        f.write(js_min)

    css_orig = os.path.getsize(css_path)
    css_new = os.path.getsize(css_min_path)
    js_orig = os.path.getsize(js_path)
    js_new = os.path.getsize(js_min_path)
    print("CSS: %dKB -> %dKB (%d%% reduction)" % (css_orig // 1024, css_new // 1024, 100 - int(css_new / css_orig * 100)))
    print("JS:  %dKB -> %dKB (%d%% reduction)" % (js_orig // 1024, js_new // 1024, 100 - int(js_new / js_orig * 100)))

    # Rewrite any HTML file still pointing at unminified assets
    html_files = glob.glob(os.path.join(BASE, "*.html")) + glob.glob(
        os.path.join(BASE, "recipes", "*.html")
    )
    updated = 0
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        is_recipe = os.sep + "recipes" + os.sep in path or "/recipes/" in path
        prefix = "../" if is_recipe else ""
        content = content.replace(f'{prefix}css/style.css"', f'{prefix}css/style.min.css"')
        content = content.replace(f'{prefix}js/main.js"', f'{prefix}js/main.min.js"')

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            updated += 1

    print(f"Updated {updated} HTML files to use minified assets.")
    print("Done.")


if __name__ == "__main__":
    main()
