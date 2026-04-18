<!-- ============================================================
     NEWSLETTER
============================================================ -->
<section class="newsletter-section" aria-labelledby="newsletter-heading">
  <div class="container">
    <h2 id="newsletter-heading">Get New Recipes Every Week</h2>
    <p>Join thousands of home cooks who get fresh recipes, kitchen tips,<br>and seasonal meal ideas delivered straight to their inbox.</p>
    <form class="newsletter-form" novalidate>
      <input type="email" placeholder="Enter your email address" aria-label="Email address" required>
      <button type="submit" class="btn">Subscribe Free →</button>
    </form>
    <p class="newsletter-note">No spam, ever. Unsubscribe anytime.</p>
    <div class="newsletter-feedback" aria-live="polite"></div>
  </div>
</section>

<!-- ============================================================
     FOOTER
============================================================ -->
<footer class="site-footer" role="contentinfo">
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="<?php echo esc_url( get_template_directory_uri() ); ?>/assets/images/favicon-192x192.png" class="logo-icon" alt="" width="44" height="44">
      <span class="logo-text"><span>Mars</span> Recipes</span>
      <p>Easy, delicious recipes for busy weeknights. From our kitchen to yours — tested, trusted, and always family-friendly.</p>
      <div class="footer-social">
        <a href="https://www.pinterest.com/saadabdorrahman/pie/" class="social-link" aria-label="Pinterest" target="_blank" rel="noopener">P</a>
        <a href="https://www.facebook.com/profile.php?id=61569030950569" class="social-link" aria-label="Facebook" target="_blank" rel="noopener">f</a>
      </div>
    </div>

    <div class="footer-nav">
      <h3>Recipes</h3>
      <ul>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/chicken/' ) ); ?>">Chicken</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/beef/' ) ); ?>">Beef</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/seafood/' ) ); ?>">Seafood</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/pasta/' ) ); ?>">Pasta</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/quick/' ) ); ?>">Quick Meals</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/category/vegetarian/' ) ); ?>">Vegetarian</a></li>
      </ul>
    </div>

    <div class="footer-nav">
      <h3>Site</h3>
      <ul>
        <li><a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About Us</a></li>
        <li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a></li>
        <li><a href="<?php echo esc_url( home_url( '/recipes/' ) ); ?>">All Recipes</a></li>
      </ul>
    </div>

    <div class="footer-nav">
      <h3>Legal</h3>
      <ul>
        <li><a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">Privacy Policy</a></li>
        <li><a href="<?php echo esc_url( home_url( '/disclaimer/' ) ); ?>">Disclaimer</a></li>
        <li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Advertise</a></li>
      </ul>
    </div>
  </div>

  <div class="footer-bottom">
    <p>© <?php echo date( 'Y' ); ?> Mars Recipes · All rights reserved ·
      <a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>" style="color:rgba(255,255,255,0.45)">Privacy</a> ·
      <a href="<?php echo esc_url( home_url( '/disclaimer/' ) ); ?>" style="color:rgba(255,255,255,0.45)">Disclaimer</a>
    </p>
  </div>
</footer>

<!-- Back to Top -->
<button class="back-to-top" id="backToTop" aria-label="Back to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <polyline points="18 15 12 9 6 15"></polyline>
  </svg>
</button>

<!-- Cookie Consent Banner (GDPR / CCPA) -->
<div id="cookieConsent" class="cookie-consent" role="dialog" aria-labelledby="cookieTitle" aria-describedby="cookieDesc" hidden>
  <div class="cookie-consent__inner">
    <div class="cookie-consent__text">
      <p id="cookieTitle"><strong>We use cookies</strong></p>
      <p id="cookieDesc">We use cookies to analyze traffic and improve your experience. By clicking "Accept", you consent to our use of cookies.
        <a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>" class="cookie-link">Privacy Policy</a>
      </p>
    </div>
    <div class="cookie-consent__actions">
      <button id="cookieDecline" class="cookie-btn cookie-btn--decline">Decline</button>
      <button id="cookieAccept" class="cookie-btn cookie-btn--accept">Accept</button>
    </div>
  </div>
</div>

<?php wp_footer(); ?>
</body>
</html>
