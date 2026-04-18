<?php get_header(); ?>

<main id="main-content" class="recipe-archive-page">
  <div class="container" style="padding-top: 3rem;">

    <!-- Archive Header -->
    <header class="archive-header" style="text-align: center; margin-bottom: 3rem;">
      <?php if ( is_tax( 'recipe_category' ) ) :
          $term = get_queried_object();
      ?>
        <h1 class="section-title"><?php echo esc_html( $term->name ); ?> Recipes</h1>
        <?php if ( $term->description ) : ?>
        <p class="section-subtitle"><?php echo esc_html( $term->description ); ?></p>
        <?php endif; ?>
      <?php else : ?>
        <h1 class="section-title">All Recipes</h1>
        <p class="section-subtitle">Every recipe, tested in a real home kitchen</p>
      <?php endif; ?>
    </header>

    <!-- Category Filter -->
    <?php if ( ! is_tax() ) : ?>
    <nav class="recipe-filter" aria-label="Filter by category" style="margin-bottom: 2.5rem; text-align: center;">
      <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>"
         class="btn btn--filter <?php echo ! is_tax() ? 'active' : ''; ?>" style="margin: 0.25rem;">
        All
      </a>
      <?php
      $cats = get_terms( [ 'taxonomy' => 'recipe_category', 'hide_empty' => true ] );
      if ( $cats && ! is_wp_error( $cats ) ) :
          foreach ( $cats as $cat ) : ?>
          <a href="<?php echo esc_url( get_term_link( $cat ) ); ?>"
             class="btn btn--filter" style="margin: 0.25rem;">
            <?php echo esc_html( $cat->name ); ?>
            <span style="opacity:0.6; font-size:0.85em;">(<?php echo $cat->count; ?>)</span>
          </a>
      <?php endforeach; endif; ?>
    </nav>
    <?php endif; ?>

    <!-- Recipe Grid -->
    <div class="grid-3">
      <?php
      if ( have_posts() ) :
          while ( have_posts() ) :
              the_post();
              echo marsrecipes_render_card( get_the_ID() );
          endwhile;
      else : ?>
          <p style="grid-column: 1/-1; text-align: center; padding: 3rem;">
            No recipes found in this category yet. <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">Browse all recipes →</a>
          </p>
      <?php endif; ?>
    </div>

    <!-- Pagination -->
    <?php if ( $GLOBALS['wp_query']->max_num_pages > 1 ) : ?>
    <nav class="pagination" aria-label="Recipes pagination" style="margin-top: 3rem; text-align: center;">
      <?php
      echo paginate_links( [
          'prev_text' => '← Previous',
          'next_text' => 'Next →',
          'type'      => 'list',
      ] );
      ?>
    </nav>
    <?php endif; ?>

  </div>
</main>

<?php get_footer(); ?>
