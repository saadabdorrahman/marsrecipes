<?php
/**
 * Plugin Name:       Mars Connect
 * Plugin URI:        https://github.com/saadabdorrahman/marsrecipes
 * Description:       Companion plugin for the mars-assistant automation: exposes recipe meta over the REST API and adds a status endpoint so Claude can publish recipes (live or draft) remotely.
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Mars Recipes
 * License:           GPL-2.0-or-later
 * Text Domain:       mars-connect
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Recipe meta keys written by the marsrecipes theme / WXR importer.
 * Underscore-prefixed meta is protected by default, so each key needs an
 * explicit REST registration with an edit-capability auth callback.
 */
function mars_connect_meta_keys() {
	return array(
		'_recipe_prep_time',
		'_recipe_cook_time',
		'_recipe_total_time',
		'_recipe_servings',
		'_recipe_calories',
		'_recipe_difficulty',
		'_recipe_cuisine',
		'_recipe_ingredients',
		'_recipe_instructions',
		'_recipe_badge',
		'_nutrition_calories',
		'_nutrition_carbs',
		'_nutrition_protein',
		'_nutrition_fat',
		'_nutrition_sodium',
	);
}

/**
 * Expose recipe meta in the REST API so POST /wp-json/wp/v2/recipe can set it.
 */
function mars_connect_register_meta() {
	foreach ( mars_connect_meta_keys() as $key ) {
		register_post_meta(
			'recipe',
			$key,
			array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				'auth_callback' => function () {
					return current_user_can( 'edit_posts' );
				},
			)
		);
	}
}
add_action( 'init', 'mars_connect_register_meta' );

/**
 * GET /wp-json/mars-connect/v1/status — lightweight health check used by the
 * /publish command before attempting a REST publish. Public, read-only,
 * exposes only non-sensitive counts.
 */
function mars_connect_register_routes() {
	register_rest_route(
		'mars-connect/v1',
		'/status',
		array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function () {
				$counts = wp_count_posts( 'recipe' );
				return array(
					'plugin'    => 'mars-connect',
					'version'   => '1.0.0',
					'theme'     => wp_get_theme()->get( 'Name' ),
					'recipes'   => array(
						'publish' => isset( $counts->publish ) ? (int) $counts->publish : 0,
						'draft'   => isset( $counts->draft ) ? (int) $counts->draft : 0,
					),
					'rest_cpt'  => (bool) get_post_type_object( 'recipe' ),
					'timestamp' => gmdate( 'c' ),
				);
			},
		)
	);
}
add_action( 'rest_api_init', 'mars_connect_register_routes' );
