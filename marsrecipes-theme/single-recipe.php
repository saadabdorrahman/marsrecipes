<?php get_header(); ?>

<?php while ( have_posts() ) : the_post();

    $post_id      = get_the_ID();
    $prep_time    = mars_recipe_meta( '_recipe_prep_time' );
    $cook_time    = mars_recipe_meta( '_recipe_cook_time' );
    $total_time   = mars_recipe_meta( '_recipe_total_time' );
    $servings     = mars_recipe_meta( '_recipe_servings' );
    $calories     = mars_recipe_meta( '_recipe_calories' );
    $difficulty   = mars_recipe_meta( '_recipe_difficulty' ) ?: 'Easy';
    $cuisine      = mars_recipe_meta( '_recipe_cuisine' );
    $ingredients  = mars_recipe_meta( '_recipe_ingredients' );
    $instructions = mars_recipe_meta( '_recipe_instructions' );
    $badge        = mars_recipe_meta( '_recipe_badge' );

    // Nutrition
    $nut_calories = mars_recipe_meta( '_nutrition_calories' );
    $nut_carbs    = mars_recipe_meta( '_nutrition_carbs' );
    $nut_protein  = mars_recipe_meta( '_nutrition_protein' );
    $nut_fat      = mars_recipe_meta( '_nutrition_fat' );
    $nut_sodium   = mars_recipe_meta( '_nutrition_sodium' );

    // Categories & Tags
    $cats = get_the_terms( $post_id, 'recipe_category' );
    $cat_name = $cats && ! is_wp_error( $cats ) ? $cats[0]->name : '';
    $cat_slug = $cats && ! is_wp_error( $cats ) ? $cats[0]->slug : '';

    // Published date
    $published = get_the_date( 'F j, Y' );
    $modified  = get_the_modified_date( 'F j, Y' );

    // Permalink
    $permalink = get_permalink();

    // Schema – ISO 8601 durations (function in functions.php)
?>

<!-- ============================================================
     RECIPE SCHEMA (JSON-LD) — compatible with Rank Math
============================================================ -->
<?php
// Build ingredients array
$ing_array = array_filter( array_map( 'trim', explode( "\n", $ingredients ) ) );
$ing_json  = json_encode( array_values( $ing_array ) );

// Build instructions array
$step_lines = array_filter( array_map( 'trim', explode( "\n", $instructions ) ) );
$steps_json = [];
$i = 1;
foreach ( $step_lines as $step ) {
    $steps_json[] = [ '@type' => 'HowToStep', 'name' => 'Step ' . $i, 'text' => $step ];
    $i++;
}
?>
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": <?php echo json_encode( get_the_title() ); ?>,
  "image": [<?php echo json_encode( get_the_post_thumbnail_url( $post_id, 'full' ) ?: '' ); ?>],
  "author": {
    "@type": "Person",
    "name": "Mars",
    "url": <?php echo json_encode( home_url( '/about/' ) ); ?>
  },
  "datePublished": <?php echo json_encode( get_the_date( 'Y-m-d' ) ); ?>,
  "dateModified": <?php echo json_encode( get_the_modified_date( 'Y-m-d' ) ); ?>,
  "description": <?php echo json_encode( get_the_excerpt() ); ?>,
  "prepTime": <?php echo json_encode( marsrecipes_to_iso_duration( $prep_time ) ); ?>,
  "cookTime": <?php echo json_encode( marsrecipes_to_iso_duration( $cook_time ) ); ?>,
  "totalTime": <?php echo json_encode( marsrecipes_to_iso_duration( $total_time ) ); ?>,
  "recipeYield": <?php echo json_encode( $servings ? $servings . ' servings' : '4 servings' ); ?>,
  "recipeCategory": "Dinner",
  "recipeCuisine": <?php echo json_encode( $cuisine ?: 'American' ); ?>,
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": <?php echo json_encode( $nut_calories ?: $calories ); ?>,
    "carbohydrateContent": <?php echo json_encode( $nut_carbs ); ?>,
    "proteinContent": <?php echo json_encode( $nut_protein ); ?>,
    "fatContent": <?php echo json_encode( $nut_fat ); ?>,
    "sodiumContent": <?php echo json_encode( $nut_sodium ); ?>
  },
  "recipeIngredient": <?php echo $ing_json ?: '[]'; ?>,
  "recipeInstructions": <?php echo json_encode( $steps_json ); ?>
}
</script>

<main class="recipe-page" id="main-content">
  <div class="container">

    <!-- Breadcrumb -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">Recipes</a>
      <?php if ( $cat_name ) : ?>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="<?php echo esc_url( home_url( '/recipes/category/' . $cat_slug . '/' ) ); ?>"><?php echo esc_html( $cat_name ); ?></a>
      <?php endif; ?>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page"><?php the_title(); ?></span>
    </nav>

    <!-- Jump Bar -->
    <div class="jump-bar">
      <a href="#recipe-card" class="btn btn--jump">↓ Jump to Recipe</a>
      <a href="#" class="btn btn--ghost btn--print" onclick="window.print(); return false;">🖨 Print</a>
    </div>

    <div class="recipe-page-layout">
      <article>

        <!-- Hero Image -->
        <?php if ( has_post_thumbnail() ) : ?>
        <div class="recipe-hero-image">
          <?php the_post_thumbnail( 'recipe-hero', [
              'loading'        => 'eager',
              'fetchpriority'  => 'high',
          ] ); ?>
        </div>
        <?php endif; ?>

        <!-- Article Header -->
        <header class="recipe-article-header">
          <h1><?php the_title(); ?></h1>

          <div class="article-meta">
            <span>By <span class="author">Mars</span></span>
            <span>Published <?php echo esc_html( $published ); ?></span>
            <?php if ( $modified !== $published ) : ?>
            <span>Updated <?php echo esc_html( $modified ); ?></span>
            <?php endif; ?>
          </div>

          <!-- Share Bar -->
          <div class="share-bar" aria-label="Share this recipe">
            <a href="https://pinterest.com/pin/create/button/?url=<?php echo urlencode( $permalink ); ?>&media=<?php echo urlencode( get_the_post_thumbnail_url( $post_id, 'full' ) ); ?>&description=<?php echo urlencode( get_the_title() ); ?>"
               class="share-btn share-btn--pinterest" target="_blank" rel="noopener" aria-label="Save to Pinterest">
              📌 Save to Pinterest
            </a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=<?php echo urlencode( $permalink ); ?>"
               class="share-btn share-btn--facebook" target="_blank" rel="noopener" aria-label="Share on Facebook">
              Share
            </a>
            <button class="share-btn share-btn--copy" type="button" aria-label="Copy link" onclick="navigator.clipboard.writeText('<?php echo esc_js( $permalink ); ?>').then(()=>this.textContent='✓ Copied!')">
              🔗 Copy Link
            </button>
          </div>
        </header>

        <!-- Article Body -->
        <div class="article-body">

          <?php the_content(); ?>

          <!-- ============================================================
               RECIPE CARD BLOCK
          ============================================================ -->
          <div id="recipe-card" class="recipe-card-block">
            <div class="recipe-card-block-header">
              <h2><?php the_title(); ?></h2>
              <p><?php echo esc_html( get_the_excerpt() ); ?></p>

              <!-- Meta Strip -->
              <div class="recipe-meta-strip" role="list">
                <?php if ( $prep_time ) : ?>
                <div class="recipe-meta-strip__item" role="listitem">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span class="recipe-meta-strip__label">Prep</span>
                  <span class="recipe-meta-strip__value"><?php echo esc_html( $prep_time ); ?></span>
                </div>
                <?php endif; ?>
                <?php if ( $cook_time ) : ?>
                <div class="recipe-meta-strip__item" role="listitem">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span class="recipe-meta-strip__label">Cook</span>
                  <span class="recipe-meta-strip__value"><?php echo esc_html( $cook_time ); ?></span>
                </div>
                <?php endif; ?>
                <?php if ( $total_time ) : ?>
                <div class="recipe-meta-strip__item" role="listitem">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span class="recipe-meta-strip__label">Total</span>
                  <span class="recipe-meta-strip__value"><?php echo esc_html( $total_time ); ?></span>
                </div>
                <?php endif; ?>
                <?php if ( $servings ) : ?>
                <div class="recipe-meta-strip__item" role="listitem">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                  <span class="recipe-meta-strip__label">Serves</span>
                  <span class="recipe-meta-strip__value"><?php echo esc_html( $servings ); ?></span>
                </div>
                <?php endif; ?>
                <?php if ( $calories ) : ?>
                <div class="recipe-meta-strip__item" role="listitem">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M12 6v6l4 2"/></svg>
                  <span class="recipe-meta-strip__label">Calories</span>
                  <span class="recipe-meta-strip__value"><?php echo esc_html( $calories ); ?></span>
                </div>
                <?php endif; ?>
              </div>

              <div class="recipe-card-actions">
                <button class="btn btn--print" onclick="window.print()" type="button">🖨 Print Recipe</button>
                <a href="https://pinterest.com/pin/create/button/?url=<?php echo urlencode( $permalink ); ?>&media=<?php echo urlencode( get_the_post_thumbnail_url( $post_id, 'full' ) ); ?>&description=<?php echo urlencode( get_the_title() ); ?>"
                   class="btn btn--pinterest" target="_blank" rel="noopener">📌 Save to Pinterest</a>
              </div>
            </div>

            <!-- Ingredients -->
            <?php if ( $ingredients ) : ?>
            <section class="recipe-ingredients" id="ingredients">
              <h3>Ingredients</h3>
              <ul class="ingredient-list">
                <?php
                $ing_lines = array_filter( array_map( 'trim', explode( "\n", $ingredients ) ) );
                foreach ( $ing_lines as $ing ) : ?>
                <li><?php echo esc_html( $ing ); ?></li>
                <?php endforeach; ?>
              </ul>
            </section>
            <?php endif; ?>

            <!-- Instructions -->
            <?php if ( $instructions ) : ?>
            <section class="recipe-instructions" id="instructions">
              <h3>Instructions</h3>
              <ol class="instruction-list">
                <?php
                $step_lines_render = array_filter( array_map( 'trim', explode( "\n", $instructions ) ) );
                $step_num = 1;
                foreach ( $step_lines_render as $step ) : ?>
                <li>
                  <div class="step-number"><?php echo $step_num; ?></div>
                  <div class="step-text"><?php echo esc_html( $step ); ?></div>
                </li>
                <?php $step_num++; endforeach; ?>
              </ol>
            </section>
            <?php endif; ?>

            <!-- Nutrition -->
            <?php if ( $nut_calories || $nut_protein || $nut_carbs || $nut_fat ) : ?>
            <section class="recipe-nutrition" id="nutrition">
              <h3>Nutrition (per serving)</h3>
              <div class="nutrition-grid">
                <?php if ( $nut_calories ) : ?><div class="nutrition-item"><span class="nutrition-value"><?php echo esc_html( $nut_calories ); ?></span><span class="nutrition-label">Calories</span></div><?php endif; ?>
                <?php if ( $nut_protein ) : ?><div class="nutrition-item"><span class="nutrition-value"><?php echo esc_html( $nut_protein ); ?></span><span class="nutrition-label">Protein</span></div><?php endif; ?>
                <?php if ( $nut_carbs ) : ?><div class="nutrition-item"><span class="nutrition-value"><?php echo esc_html( $nut_carbs ); ?></span><span class="nutrition-label">Carbs</span></div><?php endif; ?>
                <?php if ( $nut_fat ) : ?><div class="nutrition-item"><span class="nutrition-value"><?php echo esc_html( $nut_fat ); ?></span><span class="nutrition-label">Fat</span></div><?php endif; ?>
                <?php if ( $nut_sodium ) : ?><div class="nutrition-item"><span class="nutrition-value"><?php echo esc_html( $nut_sodium ); ?></span><span class="nutrition-label">Sodium</span></div><?php endif; ?>
              </div>
            </section>
            <?php endif; ?>

          </div><!-- /#recipe-card -->

        </div><!-- /.article-body -->

      </article><!-- end article -->
    </div><!-- /.recipe-page-layout -->

    <!-- ============================================================
         RELATED RECIPES
    ============================================================ -->
    <?php if ( $cat_slug ) :
        $related = new WP_Query( [
            'post_type'      => 'recipe',
            'posts_per_page' => 3,
            'post__not_in'   => [ $post_id ],
            'tax_query'      => [
                [ 'taxonomy' => 'recipe_category', 'field' => 'slug', 'terms' => $cat_slug ],
            ],
            'orderby'        => 'rand',
        ] );
        if ( $related->have_posts() ) : ?>
    <section class="section" aria-labelledby="related-heading" style="margin-top: 4rem;">
      <h2 class="section-title" id="related-heading">More <?php echo esc_html( $cat_name ); ?> Recipes</h2>
      <div class="grid-3">
        <?php while ( $related->have_posts() ) : $related->the_post();
            echo marsrecipes_render_card( get_the_ID() );
        endwhile; wp_reset_postdata(); ?>
      </div>
    </section>
    <?php endif; endif; ?>

  </div><!-- /.container -->
</main>

<?php endwhile; ?>

<?php get_footer(); ?>
