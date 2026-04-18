<?php get_header(); ?>

<main id="main-content" class="site-main" style="padding: 4rem 0;">
  <div class="container" style="max-width: 860px;">
    <?php while ( have_posts() ) : the_post(); ?>
      <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
        <header style="margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1.5rem;">
          <h1 style="font-size: clamp(1.8rem, 4vw, 2.8rem);"><?php the_title(); ?></h1>
        </header>
        <div class="article-body">
          <?php the_content(); ?>
        </div>
      </article>
    <?php endwhile; ?>
  </div>
</main>

<?php get_footer(); ?>
