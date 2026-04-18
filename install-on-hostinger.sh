#!/bin/bash
# =============================================================
#  Mars Recipes — Auto Installer for Hostinger WordPress
#  Run this ONE command in Hostinger Terminal (hPanel > Advanced > Terminal)
# =============================================================

set -e

echo ""
echo "============================================"
echo "  Mars Recipes — Auto Installer"
echo "============================================"
echo ""

# --- Detect WordPress path ---
if [ -f "$HOME/public_html/wp-config.php" ]; then
    WP_PATH="$HOME/public_html"
elif [ -f "$HOME/htdocs/wp-config.php" ]; then
    WP_PATH="$HOME/htdocs"
else
    echo "ERROR: WordPress not found. Check your installation."
    exit 1
fi

echo "[1/5] WordPress found at: $WP_PATH"

# --- Clone repo ---
TEMP_DIR="$HOME/marsrecipes-temp"
rm -rf "$TEMP_DIR"
echo "[2/5] Downloading from GitHub..."
git clone --depth 1 https://github.com/saadabdorrahman/marsrecipes.git "$TEMP_DIR"

# --- Install theme ---
echo "[3/5] Installing theme..."
rm -rf "$WP_PATH/wp-content/themes/marsrecipes-theme"
cp -r "$TEMP_DIR/marsrecipes-theme" "$WP_PATH/wp-content/themes/marsrecipes-theme"
echo "      Theme copied to wp-content/themes/marsrecipes-theme/"

# --- Upload images ---
echo "[4/5] Copying recipe images..."
mkdir -p "$WP_PATH/wp-content/uploads/marsrecipes"
cp "$TEMP_DIR"/images/*.png "$WP_PATH/wp-content/uploads/marsrecipes/" 2>/dev/null || true
cp "$TEMP_DIR"/images/*.jpg "$WP_PATH/wp-content/uploads/marsrecipes/" 2>/dev/null || true
cp "$TEMP_DIR"/images/*.svg "$WP_PATH/wp-content/uploads/marsrecipes/" 2>/dev/null || true
echo "      Images copied to wp-content/uploads/marsrecipes/"

# --- Place import-images.php in WP root ---
echo "[5/5] Placing image importer script..."
cp "$TEMP_DIR/marsrecipes-theme/import-images.php" "$WP_PATH/import-images.php"

# --- Cleanup ---
rm -rf "$TEMP_DIR"

echo ""
echo "============================================"
echo "  DONE! Now do these 3 steps:"
echo "============================================"
echo ""
echo "  STEP 1: Activate theme"
echo "    WordPress Admin > Appearance > Themes > Mars Recipes > Activate"
echo ""
echo "  STEP 2: Import recipes"
echo "    WordPress Admin > Tools > Import > WordPress > Install Now"
echo "    Then upload this file:"
echo "    $WP_PATH/wp-content/themes/marsrecipes-theme/marsrecipes-import.xml"
echo ""
echo "  STEP 3: Attach images"
echo "    Open in browser: https://YOUR-DOMAIN/import-images.php"
echo "    Then DELETE the file from File Manager after done!"
echo ""
echo "  STEP 4: Fix permalinks"
echo "    WordPress Admin > Settings > Permalinks > Post name > Save"
echo ""
echo "============================================"
