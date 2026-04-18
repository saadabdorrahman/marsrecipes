<?php get_header(); ?>

<main id="main-content" style="padding: 6rem 0; text-align: center;">
  <div class="container" style="max-width: 600px;">
    <div style="font-size: 5rem; margin-bottom: 1rem;">🍳</div>
    <h1 style="font-size: clamp(2rem, 5vw, 3.5rem); margin-bottom: 1rem;">Oops! Recipe Not Found</h1>
    <p style="font-size: 1.1rem; opacity: 0.75; margin-bottom: 2.5rem;">
      Looks like this page got burned. Let's get you back to something delicious.
    </p>
    <a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>" class="btn" style="margin-right: 1rem;">Browse All Recipes →</a>
    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="btn btn--outline">Go Home</a>
  </div>
</main>

<?php get_footer(); ?>
