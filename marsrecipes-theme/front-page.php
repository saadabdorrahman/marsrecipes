<?php get_header(); ?>

<!-- ============================================================
     HERO
============================================================ -->
<section class="hero" aria-label="Welcome to Mars Recipes">

  <div class="hero__glow-bg" aria-hidden="true"></div>

  <div class="container hero__layout">

    <!-- LEFT: Text -->
    <div class="hero__text">
      <div class="hero__badge">
        <span class="hero__badge-dot" aria-hidden="true"></span>
        New recipes every week
      </div>

      <h1 class="hero__headline">
        Easy 30-Minute<br>
        <span class="hero__headline-em">Dinner Recipes</span>
      </h1>

      <p class="hero__sub">
        Globally-inspired weeknight dinners — bold, simple, tested in a real home kitchen. From pan to table in 30 minutes or less.
      </p>

      <div class="hero__cta-row">
        <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>" class="hero__btn-main">Explore Recipes</a>
        <a href="<?php echo esc_url( home_url( '/recipes/category/quick/' ) ); ?>" class="hero__btn-ghost">Quick Meals</a>
      </div>

      <div class="hero__stats">
        <div class="hero__stat">
          <strong><?php echo wp_count_posts( 'recipe' )->publish; ?></strong>
          <span>Recipes</span>
        </div>
        <div class="hero__stat-sep" aria-hidden="true"></div>
        <div class="hero__stat">
          <strong>4.9 ★</strong>
          <span>Avg Rating</span>
        </div>
        <div class="hero__stat-sep" aria-hidden="true"></div>
        <div class="hero__stat">
          <strong>≤ 30</strong>
          <span>Minutes</span>
        </div>
        <div class="hero__stat-sep" aria-hidden="true"></div>
        <div class="hero__stat">
          <strong>100%</strong>
          <span>Home Tested</span>
        </div>
      </div>
    </div><!-- /.hero__text -->

    <!-- RIGHT: Hero visual cards -->
    <?php
    $hero_recipes = new WP_Query( [
        'post_type'      => 'recipe',
        'posts_per_page' => 4,
        'orderby'        => 'date',
        'order'          => 'DESC',
        'meta_key'       => '_recipe_badge',
        'meta_value'     => 'trending',
    ] );

    // Fallback: just get latest 4
    if ( ! $hero_recipes->have_posts() ) {
        $hero_recipes = new WP_Query( [
            'post_type'      => 'recipe',
            'posts_per_page' => 4,
            'orderby'        => 'date',
            'order'          => 'DESC',
        ] );
    }

    $hero_posts = [];
    if ( $hero_recipes->have_posts() ) {
        while ( $hero_recipes->have_posts() ) {
            $hero_recipes->the_post();
            $hero_posts[] = get_post();
        }
        wp_reset_postdata();
    }

    $card_classes = [ 'a', 'b', 'c', 'd' ];
    ?>
    <div class="hero__visual" aria-hidden="true">
      <div class="hero__orb"></div>
      <?php foreach ( $hero_posts as $i => $hp ) :
          $cls = $card_classes[ $i ] ?? 'a';
          $thumb_url = get_the_post_thumbnail_url( $hp->ID, 'recipe-card' );
          $is_main = ( $cls === 'a' );
      ?>
      <div class="hero__card hero__card--<?php echo $cls; ?>">
          <?php if ( $thumb_url ) : ?>
          <img src="<?php echo esc_url( $thumb_url ); ?>"
               alt="<?php echo esc_attr( get_the_title( $hp->ID ) ); ?>"
               <?php echo $is_main ? 'loading="eager" fetchpriority="high"' : 'loading="lazy"'; ?>>
          <?php endif; ?>
          <?php if ( $is_main ) : ?>
          <div class="hero__card-label">
            <span><?php echo esc_html( get_the_title( $hp->ID ) ); ?></span>
            <span class="hero__card-rating">★ 4.9</span>
          </div>
          <?php endif; ?>
      </div>
      <?php endforeach; ?>
    </div>

  </div><!-- /.hero__layout -->

  <a href="#trending-heading" class="hero-scroll-cue" aria-label="Scroll to recipes">
    <span class="hero-scroll-cue__arrow" aria-hidden="true">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </span>
  </a>
</section>

<!-- ============================================================
     TRENDING RECIPES
============================================================ -->
<section class="section" aria-labelledby="trending-heading">
  <div class="container">
    <h2 class="section-title" id="trending-heading">Trending Recipes</h2>
    <p class="section-subtitle">The hottest recipes everyone's talking about right now</p>

    <div class="grid-3">
      <?php
      $trending = new WP_Query( [
          'post_type'      => 'recipe',
          'posts_per_page' => 3,
          'meta_key'       => '_recipe_badge',
          'meta_value'     => 'trending',
          'orderby'        => 'date',
          'order'          => 'DESC',
      ] );

      // Fallback to latest 3
      if ( ! $trending->have_posts() ) {
          $trending = new WP_Query( [
              'post_type'      => 'recipe',
              'posts_per_page' => 3,
              'orderby'        => 'date',
              'order'          => 'DESC',
          ] );
      }

      if ( $trending->have_posts() ) :
          while ( $trending->have_posts() ) :
              $trending->the_post();
              echo marsrecipes_render_card( get_the_ID() );
          endwhile;
          wp_reset_postdata();
      endif;
      ?>
    </div>

    <div class="text-center" style="margin-top: 3rem;">
      <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>" class="btn btn--outline">View All Trending Recipes →</a>
    </div>
  </div>
</section>

<!-- AD SLOT -->
<div class="container">
  <div class="ad-slot ad-slot--leaderboard" aria-hidden="true">
    <span class="ad-slot--placeholder-text">Advertisement</span>
  </div>
</div>

<!-- ============================================================
     ALL RECIPES GRID
============================================================ -->
<section class="section" aria-labelledby="all-recipes-heading">
  <div class="container">
    <h2 class="section-title" id="all-recipes-heading">All Recipes</h2>
    <p class="section-subtitle">Every recipe, tested in a real kitchen</p>

    <div class="grid-3">
      <?php
      $all_recipes = new WP_Query( [
          'post_type'      => 'recipe',
          'posts_per_page' => 6,
          'orderby'        => 'date',
          'order'          => 'DESC',
          'meta_query'     => [
              [
                  'key'     => '_recipe_badge',
                  'value'   => 'trending',
                  'compare' => '!=',
              ],
          ],
      ] );

      if ( ! $all_recipes->have_posts() ) {
          $all_recipes = new WP_Query( [
              'post_type'      => 'recipe',
              'posts_per_page' => 6,
              'orderby'        => 'date',
              'order'          => 'DESC',
              'offset'         => 3,
          ] );
      }

      if ( $all_recipes->have_posts() ) :
          while ( $all_recipes->have_posts() ) :
              $all_recipes->the_post();
              echo marsrecipes_render_card( get_the_ID() );
          endwhile;
          wp_reset_postdata();
      endif;
      ?>
    </div>

    <div class="text-center" style="margin-top: 3rem;">
      <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>" class="btn btn--outline">View All <?php echo wp_count_posts( 'recipe' )->publish; ?> Recipes →</a>
    </div>
  </div>
</section>

<!-- ============================================================
     QUICK MEALS (≤ 20 min)
============================================================ -->
<section class="section" aria-labelledby="quick-heading">
  <div class="container">
    <h2 class="section-title" id="quick-heading">Ready in 20 Minutes or Less</h2>
    <p class="section-subtitle">When dinner needs to happen <em>right now</em></p>

    <div class="grid-3">
      <?php
      $quick = new WP_Query( [
          'post_type'      => 'recipe',
          'posts_per_page' => 3,
          'tax_query'      => [
              [
                  'taxonomy' => 'recipe_category',
                  'field'    => 'slug',
                  'terms'    => 'quick',
              ],
          ],
          'orderby'        => 'date',
          'order'          => 'DESC',
      ] );

      if ( $quick->have_posts() ) :
          while ( $quick->have_posts() ) :
              $quick->the_post();
              echo marsrecipes_render_card( get_the_ID() );
          endwhile;
          wp_reset_postdata();
      endif;
      ?>
    </div>
  </div>
</section>

<!-- ============================================================
     BROWSE BY CATEGORY
============================================================ -->
<section class="section section--alt" aria-labelledby="categories-heading">
  <div class="container">
    <h2 class="section-title" id="categories-heading">Browse by Category</h2>

    <div class="category-grid">
      <?php
      $categories = [
          [ 'slug' => 'chicken',    'label' => '🍗 Chicken',    'emoji' => '🍗' ],
          [ 'slug' => 'beef',       'label' => '🥩 Beef',       'emoji' => '🥩' ],
          [ 'slug' => 'seafood',    'label' => '🦐 Seafood',    'emoji' => '🦐' ],
          [ 'slug' => 'pasta',      'label' => '🍝 Pasta',      'emoji' => '🍝' ],
          [ 'slug' => 'quick',      'label' => '⚡ Quick Meals', 'emoji' => '⚡' ],
          [ 'slug' => 'vegetarian', 'label' => '🥗 Vegetarian', 'emoji' => '🥗' ],
      ];

      foreach ( $categories as $cat ) :
          $term = get_term_by( 'slug', $cat['slug'], 'recipe_category' );
          $count = $term ? $term->count : 0;
          $cat_url = home_url( '/recipes/category/' . $cat['slug'] . '/' );

          // Get a recipe image for the category
          $cat_query = new WP_Query( [
              'post_type'      => 'recipe',
              'posts_per_page' => 1,
              'tax_query'      => [
                  [ 'taxonomy' => 'recipe_category', 'field' => 'slug', 'terms' => $cat['slug'] ],
              ],
          ] );
          $thumb_url = '';
          if ( $cat_query->have_posts() ) {
              $cat_query->the_post();
              $thumb_url = get_the_post_thumbnail_url( get_the_ID(), 'medium_large' );
              wp_reset_postdata();
          }
          ?>
          <a href="<?php echo esc_url( $cat_url ); ?>" class="category-tile">
            <?php if ( $thumb_url ) : ?>
            <img decoding="async" src="<?php echo esc_url( $thumb_url ); ?>"
                 alt="<?php echo esc_attr( $cat['label'] ); ?>" width="400" height="300" loading="lazy">
            <?php endif; ?>
            <span class="category-tile__name">
              <?php echo esc_html( $cat['label'] ); ?>
              <span class="category-tile__count"><?php echo $count; ?> recipe<?php echo $count !== 1 ? 's' : ''; ?></span>
            </span>
          </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php get_footer(); ?>
