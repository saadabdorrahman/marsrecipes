<?php get_header(); ?>

<main id="main-content" style="padding: 4rem 0;">
  <div class="container">
    <div class="grid-3">
      <?php
      if ( have_posts() ) :
          while ( have_posts() ) : the_post();
              if ( get_post_type() === 'recipe' ) {
                  echo marsrecipes_render_card( get_the_ID() );
              } else { ?>
              <article id="post-<?php the_ID(); ?>" <?php post_class( 'recipe-card' ); ?>>
                <?php if ( has_post_thumbnail() ) : ?>
                <a href="<?php the_permalink(); ?>" class="recipe-card__image-link">
                  <?php the_post_thumbnail( 'recipe-card', [ 'class' => 'recipe-card__image' ] ); ?>
                </a>
                <?php endif; ?>
                <div class="recipe-card__body">
                  <h2 class="recipe-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                  <p class="recipe-card__excerpt"><?php the_excerpt(); ?></p>
                </div>
              </article>
              <?php }
          endwhile;
      else : ?>
          <p style="grid-column:1/-1; text-align:center; padding:3rem;">
            Nothing found. <a href="<?php echo esc_url( home_url( '/' ) ); ?>">Go home →</a>
          </p>
      <?php endif; ?>
    </div>

    <!-- Pagination -->
    <div style="margin-top: 3rem; text-align: center;">
      <?php the_posts_pagination( [ 'prev_text' => '← Previous', 'next_text' => 'Next →' ] ); ?>
    </div>
  </div>
</main>

<?php get_footer(); ?>
