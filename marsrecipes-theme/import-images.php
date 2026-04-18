<?php
/**
 * Mars Recipes — Image Importer
 *
 * Upload this file to your WordPress root and run it ONCE via browser:
 *   https://yourdomain.com/import-images.php
 *
 * BEFORE running:
 * 1. Upload the /images/ folder to /wp-content/uploads/marsrecipes/ via File Manager or FTP
 * 2. Make sure the theme is activated and recipes are imported
 * 3. Run this script to attach featured images to each recipe
 * 4. DELETE this file after use
 */

require_once __DIR__ . '/wp-load.php';

if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( 'Admin access required.' );
}

$upload_dir = wp_upload_dir();
$images_path = $upload_dir['basedir'] . '/marsrecipes/';
$images_url  = $upload_dir['baseurl'] . '/marsrecipes/';

// Map: recipe slug => main image filename
$image_map = [
    'beef-broccoli-stir-fry'          => 'beef-broccoli-stir-fry.jpg.png',
    'coconut-chicken-curry'           => 'coconut-chicken-curry.jpg.png',
    'creamy-sun-dried-tomato-pasta'   => 'creamy-sun-dried-tomato-pasta.jpg.png',
    'creamy-tuscan-shrimp'            => 'creamy-tuscan-shrimp.jpg.png',
    'crispy-baked-chicken-wings'      => 'crispy-baked-chicken-wings.jpg.png',
    'crispy-honey-garlic-salmon'      => 'crispy-honey-garlic-salmon.jpg.png',
    'easy-chicken-tikka-masala'       => 'easy-chicken-tikka-masala.jpg.png',
    'easy-creamy-garlic-chicken'      => 'easy-creamy-garlic-chicken.jpg.png',
    'garlic-butter-steak-bites'       => 'garlic-butter-steak-bites.jpg.png',
    'ground-beef-kofta-garlic-sauce'  => 'ground-beef-kofta-garlic-sauce.jpg.png',
    'lemon-herb-sheet-pan-chicken'    => 'lemon-herb-sheet-pan-chicken.jpg.png',
    'one-pan-beef-shawarma-bowl'      => 'one-pan-beef-shawarma-bowl.jpg.png',
    'one-pan-honey-butter-chicken'    => 'one-pan-honey-butter-chicken.jpg.png',
    'smoky-paprika-baked-salmon'      => 'smoky-paprika-baked-salmon.jpg.png',
    'spicy-garlic-butter-shrimp'      => 'spicy-garlic-butter-shrimp.jpg.png',
];

echo '<h1>Mars Recipes Image Importer</h1>';
echo '<pre>';

$recipes = get_posts([
    'post_type'      => 'recipe',
    'posts_per_page' => -1,
    'post_status'    => 'publish',
]);

if ( empty( $recipes ) ) {
    echo "No recipes found. Import recipes first via Tools > Import.\n";
    echo '</pre>';
    exit;
}

echo "Found " . count( $recipes ) . " recipes.\n\n";

require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$success = 0;
$skipped = 0;
$errors  = 0;

foreach ( $recipes as $recipe ) {
    $slug = $recipe->post_name;

    if ( ! isset( $image_map[ $slug ] ) ) {
        echo "SKIP: {$slug} — no image mapping\n";
        $skipped++;
        continue;
    }

    // Check if already has thumbnail
    if ( has_post_thumbnail( $recipe->ID ) ) {
        echo "SKIP: {$slug} — already has featured image\n";
        $skipped++;
        continue;
    }

    $filename  = $image_map[ $slug ];
    $file_path = $images_path . $filename;

    if ( ! file_exists( $file_path ) ) {
        echo "ERROR: {$slug} — file not found: {$file_path}\n";
        $errors++;
        continue;
    }

    // Create attachment
    $filetype = wp_check_filetype( $filename, null );
    $attachment = [
        'guid'           => $images_url . $filename,
        'post_mime_type' => $filetype['type'] ?: 'image/png',
        'post_title'     => sanitize_file_name( pathinfo( $filename, PATHINFO_FILENAME ) ),
        'post_content'   => '',
        'post_status'    => 'inherit',
    ];

    $attach_id = wp_insert_attachment( $attachment, $file_path, $recipe->ID );

    if ( is_wp_error( $attach_id ) ) {
        echo "ERROR: {$slug} — " . $attach_id->get_error_message() . "\n";
        $errors++;
        continue;
    }

    // Generate metadata (thumbnails)
    $attach_data = wp_generate_attachment_metadata( $attach_id, $file_path );
    wp_update_attachment_metadata( $attach_id, $attach_data );

    // Set as featured image
    set_post_thumbnail( $recipe->ID, $attach_id );

    echo "OK: {$slug} — featured image set (ID: {$attach_id})\n";
    $success++;
}

echo "\n--- DONE ---\n";
echo "Success: {$success}\n";
echo "Skipped: {$skipped}\n";
echo "Errors:  {$errors}\n";
echo "\n⚠ DELETE this file now for security!\n";
echo '</pre>';
