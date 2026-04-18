<?php get_header(); ?>

<main id="main-content" style="padding: 4rem 0;">
  <div class="container">
    <header style="text-align: center; margin-bottom: 3rem;">
      <h1 class="section-title">
        <?php if ( have_posts() ) : ?>
          Search results for: "<?php echo esc_html( get_search_query() ); ?>"
        <?php else : ?>
          No results for "<?php echo esc_html( get_search_query() ); ?>"
        <?php endif; ?>
      </h1>

      <!-- Search form -->
      <form class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>" method="get" style="max-width: 480px; margin: 1.5rem auto 0; display: flex; gap: 0.5rem;">
        <input type="search" name="s" value="<?php echo esc_attr( get_search_query() ); ?>"
               class="search-bar__input" placeholder="Search recipes…" style="flex:1;">
        <button type="submit" class="btn">Search</button>
      </form>
    </header>

    <?php if ( have_posts() ) : ?>
    <div class="grid-3">
      <?php while ( have_posts() ) : the_post();
          if ( get_post_type() === 'recipe' ) {
              echo marsrecipes_render_card( get_the_ID() );
          } else { ?>
          <article <?php post_class( 'recipe-card' ); ?>>
            <div class="recipe-card__body">
              <h2 class="recipe-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
              <p class="recipe-card__excerpt"><?php the_excerpt(); ?></p>
            </div>
          </article>
          <?php }
      endwhile; ?>
    </div>

    <div style="margin-top: 3rem; text-align: center;">
      <?php the_posts_pagination( [ 'prev_text' => '← Previous', 'next_text' => 'Next →' ] ); ?>
    </div>

    <?php else : ?>
    <div style="text-align:center; padding: 3rem;">
      <p style="font-size: 1.1rem; opacity:0.75; margin-bottom: 2rem;">
        No recipes matched your search. Try a different keyword.
      </p>
      <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>" class="btn">Browse All Recipes →</a>
    </div>
    <?php endif; ?>
  </div>
</main>

<?php get_footer(); ?>
