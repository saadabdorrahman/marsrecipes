<?php
/**
 * Mars Recipes – functions.php
 * Theme setup, Custom Post Type, Meta Boxes, Scripts/Styles
 */

if ( ! defined( 'ABSPATH' ) ) exit;

/* =========================================================
   1. THEME SETUP
========================================================= */
function marsrecipes_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', [ 'search-form', 'comment-form', 'gallery', 'caption' ] );
    add_theme_support( 'automatic-feed-links' );
    add_theme_support( 'custom-logo', [
        'height'      => 80,
        'width'       => 200,
        'flex-height' => true,
        'flex-width'  => true,
    ] );

    register_nav_menus( [
        'primary'  => __( 'Primary Navigation', 'marsrecipes' ),
        'footer'   => __( 'Footer Navigation', 'marsrecipes' ),
    ] );

    // Set default thumbnail size for recipe cards
    set_post_thumbnail_size( 800, 600, true );
    add_image_size( 'recipe-card', 800, 1200, true );
    add_image_size( 'recipe-hero', 1200, 800, true );
}
add_action( 'after_setup_theme', 'marsrecipes_setup' );

/* =========================================================
   2. ENQUEUE SCRIPTS & STYLES
========================================================= */
function marsrecipes_enqueue() {
    // Google Fonts
    wp_enqueue_style(
        'marsrecipes-fonts',
        'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap',
        [],
        null
    );

    // Main stylesheet
    wp_enqueue_style(
        'marsrecipes-style',
        get_template_directory_uri() . '/assets/css/style.min.css',
        [ 'marsrecipes-fonts' ],
        '1.0.0'
    );

    // Main JS
    wp_enqueue_script(
        'marsrecipes-main',
        get_template_directory_uri() . '/assets/js/main.min.js',
        [],
        '1.0.0',
        true // load in footer
    );

    // Pass site URL to JS for correct search permalink generation
    wp_localize_script( 'marsrecipes-main', 'marsrecipesData', [
        'homeUrl' => esc_url( home_url( '/' ) ),
    ] );
}
add_action( 'wp_enqueue_scripts', 'marsrecipes_enqueue' );

/* =========================================================
   3. CUSTOM POST TYPE: Recipe
========================================================= */
function marsrecipes_register_cpt() {
    $labels = [
        'name'               => __( 'Recipes', 'marsrecipes' ),
        'singular_name'      => __( 'Recipe', 'marsrecipes' ),
        'add_new'            => __( 'Add New Recipe', 'marsrecipes' ),
        'add_new_item'       => __( 'Add New Recipe', 'marsrecipes' ),
        'edit_item'          => __( 'Edit Recipe', 'marsrecipes' ),
        'new_item'           => __( 'New Recipe', 'marsrecipes' ),
        'view_item'          => __( 'View Recipe', 'marsrecipes' ),
        'search_items'       => __( 'Search Recipes', 'marsrecipes' ),
        'not_found'          => __( 'No recipes found', 'marsrecipes' ),
        'not_found_in_trash' => __( 'No recipes in trash', 'marsrecipes' ),
        'menu_name'          => __( 'Recipes', 'marsrecipes' ),
    ];

    $args = [
        'labels'             => $labels,
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'menu_icon'          => 'dashicons-food',
        'query_var'          => true,
        'rewrite'            => [ 'slug' => 'recipes', 'with_front' => false ],
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'supports'           => [ 'title', 'editor', 'thumbnail', 'excerpt', 'comments', 'revisions' ],
        'show_in_rest'       => true, // Enables Gutenberg + Rank Math
    ];

    register_post_type( 'recipe', $args );
}
add_action( 'init', 'marsrecipes_register_cpt' );

/* =========================================================
   4. TAXONOMY: Recipe Category
========================================================= */
function marsrecipes_register_taxonomies() {
    // Recipe Category (Chicken, Beef, Seafood, Pasta, Quick, Vegetarian)
    register_taxonomy( 'recipe_category', 'recipe', [
        'labels'            => [
            'name'              => __( 'Recipe Categories', 'marsrecipes' ),
            'singular_name'     => __( 'Recipe Category', 'marsrecipes' ),
            'search_items'      => __( 'Search Categories', 'marsrecipes' ),
            'all_items'         => __( 'All Categories', 'marsrecipes' ),
            'edit_item'         => __( 'Edit Category', 'marsrecipes' ),
            'add_new_item'      => __( 'Add New Category', 'marsrecipes' ),
            'menu_name'         => __( 'Categories', 'marsrecipes' ),
        ],
        'hierarchical'      => true,
        'public'            => true,
        'show_ui'           => true,
        'show_in_rest'      => true,
        'rewrite'           => [ 'slug' => 'recipes/category' ],
        'show_admin_column' => true,
    ] );

    // Recipe Tag (trending, quick, viral, etc.)
    register_taxonomy( 'recipe_tag', 'recipe', [
        'labels'       => [
            'name'          => __( 'Recipe Tags', 'marsrecipes' ),
            'singular_name' => __( 'Recipe Tag', 'marsrecipes' ),
        ],
        'hierarchical' => false,
        'public'       => true,
        'show_ui'      => true,
        'show_in_rest' => true,
        'rewrite'      => [ 'slug' => 'recipes/tag' ],
    ] );
}
add_action( 'init', 'marsrecipes_register_taxonomies' );

/* =========================================================
   5. META BOXES: Recipe Details
========================================================= */
function marsrecipes_add_meta_boxes() {
    add_meta_box(
        'marsrecipes_details',
        __( '🍳 Recipe Details', 'marsrecipes' ),
        'marsrecipes_details_callback',
        'recipe',
        'normal',
        'high'
    );

    add_meta_box(
        'marsrecipes_nutrition',
        __( '🥗 Nutrition Information', 'marsrecipes' ),
        'marsrecipes_nutrition_callback',
        'recipe',
        'normal',
        'default'
    );

    add_meta_box(
        'marsrecipes_badge',
        __( '🏷️ Recipe Badge', 'marsrecipes' ),
        'marsrecipes_badge_callback',
        'recipe',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'marsrecipes_add_meta_boxes' );

function marsrecipes_details_callback( $post ) {
    wp_nonce_field( 'marsrecipes_save_meta', 'marsrecipes_nonce' );

    $prep_time    = get_post_meta( $post->ID, '_recipe_prep_time', true );
    $cook_time    = get_post_meta( $post->ID, '_recipe_cook_time', true );
    $total_time   = get_post_meta( $post->ID, '_recipe_total_time', true );
    $servings     = get_post_meta( $post->ID, '_recipe_servings', true );
    $calories     = get_post_meta( $post->ID, '_recipe_calories', true );
    $difficulty   = get_post_meta( $post->ID, '_recipe_difficulty', true );
    $cuisine      = get_post_meta( $post->ID, '_recipe_cuisine', true );
    $ingredients  = get_post_meta( $post->ID, '_recipe_ingredients', true );
    $instructions = get_post_meta( $post->ID, '_recipe_instructions', true );

    ?>
    <style>
        .mars-meta-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
        .mars-meta-field label { display: block; font-weight: 600; margin-bottom: 4px; font-size: 12px; color: #555; text-transform: uppercase; }
        .mars-meta-field input, .mars-meta-field select { width: 100%; padding: 6px 8px; border: 1px solid #ddd; border-radius: 4px; }
        .mars-meta-field--full { grid-column: 1 / -1; }
        .mars-meta-field textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; font-size: 13px; }
        .mars-meta-hint { font-size: 11px; color: #888; margin-top: 3px; }
    </style>
    <div class="mars-meta-grid">
        <div class="mars-meta-field">
            <label><?php _e( 'Prep Time', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_prep_time" value="<?php echo esc_attr( $prep_time ); ?>" placeholder="e.g. 10 min">
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Cook Time', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_cook_time" value="<?php echo esc_attr( $cook_time ); ?>" placeholder="e.g. 20 min">
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Total Time', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_total_time" value="<?php echo esc_attr( $total_time ); ?>" placeholder="e.g. 30 min">
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Servings', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_servings" value="<?php echo esc_attr( $servings ); ?>" placeholder="e.g. 4">
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Calories', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_calories" value="<?php echo esc_attr( $calories ); ?>" placeholder="e.g. 480 kcal">
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Difficulty', 'marsrecipes' ); ?></label>
            <select name="_recipe_difficulty">
                <option value="Easy" <?php selected( $difficulty, 'Easy' ); ?>>Easy</option>
                <option value="Medium" <?php selected( $difficulty, 'Medium' ); ?>>Medium</option>
                <option value="Hard" <?php selected( $difficulty, 'Hard' ); ?>>Hard</option>
            </select>
        </div>
        <div class="mars-meta-field">
            <label><?php _e( 'Cuisine', 'marsrecipes' ); ?></label>
            <input type="text" name="_recipe_cuisine" value="<?php echo esc_attr( $cuisine ); ?>" placeholder="e.g. American, Italian">
        </div>
        <div class="mars-meta-field--full">
            <label><?php _e( 'Ingredients (one per line)', 'marsrecipes' ); ?></label>
            <textarea name="_recipe_ingredients" rows="8" placeholder="4 boneless skinless chicken thighs&#10;1 tablespoon olive oil&#10;6 cloves garlic, minced"><?php echo esc_textarea( $ingredients ); ?></textarea>
            <p class="mars-meta-hint">Enter each ingredient on a new line</p>
        </div>
        <div class="mars-meta-field--full">
            <label><?php _e( 'Instructions (one step per line)', 'marsrecipes' ); ?></label>
            <textarea name="_recipe_instructions" rows="10" placeholder="Season the chicken generously with salt and pepper.&#10;Heat oil in a large skillet over medium-high heat."><?php echo esc_textarea( $instructions ); ?></textarea>
            <p class="mars-meta-hint">Each line = one step. Will be numbered automatically.</p>
        </div>
    </div>
    <?php
}

function marsrecipes_nutrition_callback( $post ) {
    $calories  = get_post_meta( $post->ID, '_nutrition_calories', true );
    $carbs     = get_post_meta( $post->ID, '_nutrition_carbs', true );
    $protein   = get_post_meta( $post->ID, '_nutrition_protein', true );
    $fat       = get_post_meta( $post->ID, '_nutrition_fat', true );
    $sodium    = get_post_meta( $post->ID, '_nutrition_sodium', true );
    ?>
    <style>
        .mars-nutrition-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
    </style>
    <div class="mars-nutrition-grid">
        <?php
        $fields = [
            '_nutrition_calories' => [ 'Calories', $calories, 'e.g. 480' ],
            '_nutrition_carbs'    => [ 'Carbs (g)', $carbs, 'e.g. 6g' ],
            '_nutrition_protein'  => [ 'Protein (g)', $protein, 'e.g. 38g' ],
            '_nutrition_fat'      => [ 'Fat (g)', $fat, 'e.g. 32g' ],
            '_nutrition_sodium'   => [ 'Sodium (mg)', $sodium, 'e.g. 520mg' ],
        ];
        foreach ( $fields as $key => $data ) : ?>
            <div class="mars-meta-field">
                <label><?php echo esc_html( $data[0] ); ?></label>
                <input type="text" name="<?php echo esc_attr( $key ); ?>" value="<?php echo esc_attr( $data[1] ); ?>" placeholder="<?php echo esc_attr( $data[2] ); ?>">
            </div>
        <?php endforeach; ?>
    </div>
    <?php
}

function marsrecipes_badge_callback( $post ) {
    $badge = get_post_meta( $post->ID, '_recipe_badge', true );
    ?>
    <label><?php _e( 'Badge', 'marsrecipes' ); ?></label>
    <select name="_recipe_badge" style="width:100%; margin-top:4px;">
        <option value="" <?php selected( $badge, '' ); ?>>— None —</option>
        <option value="trending" <?php selected( $badge, 'trending' ); ?>>🔥 Trending</option>
        <option value="quick" <?php selected( $badge, 'quick' ); ?>>⚡ Quick</option>
        <option value="viral" <?php selected( $badge, 'viral' ); ?>>🚀 Viral</option>
        <option value="new" <?php selected( $badge, 'new' ); ?>>✨ New</option>
        <option value="popular" <?php selected( $badge, 'popular' ); ?>>⭐ Popular</option>
    </select>
    <?php
}

/* =========================================================
   6. SAVE META BOX DATA
========================================================= */
function marsrecipes_save_meta( $post_id ) {
    if ( ! isset( $_POST['marsrecipes_nonce'] ) ) return;
    if ( ! wp_verify_nonce( $_POST['marsrecipes_nonce'], 'marsrecipes_save_meta' ) ) return;
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
    if ( ! current_user_can( 'edit_post', $post_id ) ) return;

    $fields = [
        '_recipe_prep_time', '_recipe_cook_time', '_recipe_total_time',
        '_recipe_servings', '_recipe_calories', '_recipe_difficulty',
        '_recipe_cuisine', '_recipe_ingredients', '_recipe_instructions',
        '_recipe_badge',
        '_nutrition_calories', '_nutrition_carbs', '_nutrition_protein',
        '_nutrition_fat', '_nutrition_sodium',
    ];

    foreach ( $fields as $field ) {
        if ( isset( $_POST[ $field ] ) ) {
            update_post_meta( $post_id, $field, sanitize_textarea_field( $_POST[ $field ] ) );
        }
    }
}
add_action( 'save_post_recipe', 'marsrecipes_save_meta' );

/* =========================================================
   7. HELPER: Get recipe meta shortcut
========================================================= */
function mars_recipe_meta( $key, $post_id = null ) {
    if ( ! $post_id ) $post_id = get_the_ID();
    return get_post_meta( $post_id, $key, true );
}

/* =========================================================
   8. RECIPE CARD HTML helper
========================================================= */
function marsrecipes_render_card( $post_id ) {
    $title      = get_the_title( $post_id );
    $permalink  = get_permalink( $post_id );
    $thumb      = get_the_post_thumbnail( $post_id, 'recipe-card', [ 'class' => 'recipe-card__image', 'loading' => 'lazy' ] );
    $excerpt    = get_the_excerpt( $post_id );
    $total_time = mars_recipe_meta( '_recipe_total_time', $post_id );
    $difficulty = mars_recipe_meta( '_recipe_difficulty', $post_id ) ?: 'Easy';
    $badge      = mars_recipe_meta( '_recipe_badge', $post_id );
    $categories = get_the_terms( $post_id, 'recipe_category' );
    $cat_name   = $categories && ! is_wp_error( $categories ) ? $categories[0]->name : '';

    $badge_html = '';
    if ( $badge === 'trending' ) $badge_html = '<span class="recipe-badge recipe-badge--hot">🔥 Trending</span>';
    elseif ( $badge === 'quick' ) $badge_html = '<span class="recipe-badge recipe-badge--quick">⚡ ' . esc_html( $total_time ) . '</span>';
    elseif ( $badge === 'viral' ) $badge_html = '<span class="recipe-badge recipe-badge--viral">🚀 Viral</span>';
    elseif ( $badge === 'new' ) $badge_html = '<span class="recipe-badge recipe-badge--new">✨ New</span>';

    $cat_time = trim( $cat_name . ( $total_time ? ' · ' . $total_time : '' ), ' · ' );

    ob_start(); ?>
    <article class="recipe-card" data-category="<?php echo esc_attr( strtolower( $cat_name ) ); ?>">
        <a href="<?php echo esc_url( $permalink ); ?>" class="recipe-card__image-link">
            <?php echo $badge_html; ?>
            <?php echo $thumb; ?>
            <?php if ( $cat_time ) : ?>
            <span class="recipe-card__category"><?php echo esc_html( $cat_time ); ?></span>
            <?php endif; ?>
        </a>
        <div class="recipe-card__body">
            <div class="recipe-card__meta">
                <?php if ( $total_time ) : ?>
                <span class="recipe-card__time">⏱ <?php echo esc_html( $total_time ); ?></span>
                <?php endif; ?>
                <span class="recipe-card__difficulty"><?php echo esc_html( $difficulty ); ?></span>
            </div>
            <h3 class="recipe-card__title"><a href="<?php echo esc_url( $permalink ); ?>"><?php echo esc_html( $title ); ?></a></h3>
            <?php if ( $excerpt ) : ?>
            <p class="recipe-card__excerpt"><?php echo esc_html( $excerpt ); ?></p>
            <?php endif; ?>
        </div>
    </article>
    <?php return ob_get_clean();
}

/* =========================================================
   9. RANK MATH COMPATIBILITY
========================================================= */
// Tell Rank Math about our CPT
add_filter( 'rank_math/sitemap/post_type', function( $post_types ) {
    $post_types[] = 'recipe';
    return $post_types;
} );

// Provide structured data hints to Rank Math
add_filter( 'rank_math/recipe/post_type', function() {
    return 'recipe';
} );

/* =========================================================
   10. FLUSH REWRITE RULES ON ACTIVATION
========================================================= */
function marsrecipes_flush_rewrites() {
    marsrecipes_register_cpt();
    marsrecipes_register_taxonomies();
    flush_rewrite_rules();
}
add_action( 'after_switch_theme', 'marsrecipes_flush_rewrites' );

/* =========================================================
   11. SEARCH — include recipes in search results
========================================================= */
add_filter( 'pre_get_posts', function( $query ) {
    if ( ! is_admin() && $query->is_main_query() ) {
        if ( $query->is_search() ) {
            $query->set( 'post_type', [ 'post', 'recipe', 'page' ] );
        }
        if ( $query->is_home() || $query->is_front_page() ) {
            // homepage handled by front-page.php
        }
    }
    return $query;
} );

/* =========================================================
   12. EXCERPT LENGTH
========================================================= */
add_filter( 'excerpt_length', function() { return 25; } );
add_filter( 'excerpt_more', function() { return '…'; } );

/* =========================================================
   13. ISO 8601 DURATION HELPER (for Recipe Schema)
========================================================= */
function marsrecipes_to_iso_duration( $str ) {
    preg_match( '/(\d+)/', $str, $m );
    return isset( $m[1] ) ? 'PT' . $m[1] . 'M' : '';
}
