<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo( 'charset' ); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- DNS Prefetch -->
  <link rel="dns-prefetch" href="https://www.googletagmanager.com">
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">

  <!-- Favicons -->
  <link rel="icon" type="image/x-icon" href="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/apple-touch-icon.png">

  <!-- Font preconnect for performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<!-- ============================================================
     HEADER
============================================================ -->
<header class="site-header" role="banner" data-glass>
  <div class="container header-inner">

    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="logo" aria-label="<?php bloginfo( 'name' ); ?> – Home">
      <img src="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/favicon-192x192.png" class="logo-icon" alt="" width="38" height="38">
      <span class="logo-text"><span>Mars</span> Recipes</span>
    </a>

    <nav class="nav-primary" aria-label="Main navigation">
      <ul>
        <li><a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">Recipes</a></li>
        <li><a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About</a></li>
        <li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a></li>
      </ul>
    </nav>

    <button class="search-btn" id="searchToggle" aria-label="Search recipes" aria-expanded="false">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <span class="search-btn-label">Search</span>
    </button>

    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-mobile" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>

  <!-- Search Bar (hidden by default, toggled via JS) -->
  <div id="searchBar" class="search-bar" aria-hidden="true" role="search">
    <form class="search-bar__form" action="<?php echo esc_url( home_url( '/' ) ); ?>" method="get">
      <input
        type="search"
        name="s"
        class="search-bar__input"
        placeholder="Search recipes…"
        aria-label="Search recipes"
        value="<?php echo get_search_query(); ?>"
      >
      <button type="submit" class="search-bar__submit" aria-label="Submit search">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
      </button>
    </form>
  </div>

  <!-- Mobile Navigation -->
  <nav id="nav-mobile" class="nav-mobile" aria-hidden="true" aria-label="Mobile navigation">
    <ul>
      <li><a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">All Recipes</a></li>
      <li><a href="<?php echo esc_url( home_url( '/recipes/category/chicken/' ) ); ?>">Chicken</a></li>
      <li><a href="<?php echo esc_url( home_url( '/recipes/category/beef/' ) ); ?>">Beef</a></li>
      <li><a href="<?php echo esc_url( home_url( '/recipes/category/seafood/' ) ); ?>">Seafood</a></li>
      <li><a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About</a></li>
      <li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a></li>
    </ul>
  </nav>

  <!-- Category Strip -->
  <nav class="header-cats" aria-label="Browse by category">
    <div class="header-cats-inner">
      <ul>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/chicken/' ) ); ?>">🍗 Chicken</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/beef/' ) ); ?>">🥩 Beef</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/seafood/' ) ); ?>">🦐 Seafood</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/pasta/' ) ); ?>">🍝 Pasta</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/quick/' ) ); ?>">⚡ Quick Meals</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/vegetarian/' ) ); ?>">🥗 Vegetarian</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">✦ All Recipes</a></li>
      </ul>
    </div>
  </nav>

</header>
