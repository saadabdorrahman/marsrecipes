/**
 * MarsRecipes.com – Main JavaScript
 * Vanilla JS, zero dependencies, IIFE pattern
 */
(function () {
  'use strict';

  /* ----------------------------------------------------------------
     1. Mobile Navigation
  ---------------------------------------------------------------- */
  function initMobileNav() {
    var toggle = document.querySelector('.nav-toggle, .hamburger');
    var mobileNav = document.getElementById('nav-mobile') || document.getElementById('main-nav');
    if (!toggle || !mobileNav) return;

    toggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.contains('is-open');
      if (isOpen) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });

    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !mobileNav.contains(e.target)) {
        closeMobileNav();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMobileNav();
    });

    function openMobileNav() {
      mobileNav.classList.add('is-open');
      mobileNav.removeAttribute('aria-hidden');
      toggle.setAttribute('aria-expanded', 'true');
    }

    function closeMobileNav() {
      mobileNav.classList.remove('is-open');
      mobileNav.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
    }
  }

  /* ----------------------------------------------------------------
     2. Sticky Header
  ---------------------------------------------------------------- */
  function initStickyHeader() {
    var header = document.querySelector('.site-header');
    if (!header) return;

    window.addEventListener('scroll', function () {
      if (window.scrollY > 80) {
        header.classList.add('is-sticky');
      } else {
        header.classList.remove('is-sticky');
      }
    }, { passive: true });
  }

  /* ----------------------------------------------------------------
     3. Ingredient Checker (localStorage persistence)
     Supports both .ingredient-check checkboxes and #recipe-ingredients checkboxes
  ---------------------------------------------------------------- */
  function initIngredientChecker() {
    var slug = window.location.pathname.replace(/[^a-z0-9-]/gi, '-').replace(/-+/g, '-').replace(/^-|-$/g, '') || 'recipe';

    // Standard ingredient-check style
    var checkboxes = document.querySelectorAll('.ingredient-check');
    checkboxes.forEach(function (cb, i) {
      var key = 'mr_ingredient_' + slug + '_' + i;
      if (localStorage.getItem(key) === '1') cb.checked = true;
      cb.addEventListener('change', function () {
        localStorage.setItem(key, cb.checked ? '1' : '0');
      });
    });

    // Recipe card block style (#recipe-ingredients)
    var recipeIngList = document.getElementById('recipe-ingredients');
    if (recipeIngList) {
      var riCheckboxes = recipeIngList.querySelectorAll('input[type="checkbox"]');
      riCheckboxes.forEach(function (cb, i) {
        var key = 'mr_ri_' + slug + '_' + i;
        if (localStorage.getItem(key) === '1') cb.checked = true;
        cb.addEventListener('change', function () {
          localStorage.setItem(key, cb.checked ? '1' : '0');
        });
      });
    }

    // Clear all button
    var clearBtn = document.getElementById('clearIngredients');
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        checkboxes.forEach(function (cb, i) {
          cb.checked = false;
          localStorage.removeItem('mr_ingredient_' + slug + '_' + i);
        });
        if (recipeIngList) {
          recipeIngList.querySelectorAll('input[type="checkbox"]').forEach(function (cb, i) {
            cb.checked = false;
            localStorage.removeItem('mr_ri_' + slug + '_' + i);
          });
        }
      });
    }
  }

  /* ----------------------------------------------------------------
     4. Servings Adjuster
     Supports both data-action buttons (original) and id-based buttons (recipe pages)
  ---------------------------------------------------------------- */
  function initServingsAdjuster() {
    // Original pattern: data-action buttons inside .servings-adjuster
    var adjusters = document.querySelectorAll('.servings-adjuster');
    adjusters.forEach(function (adjuster) {
      var decreaseBtn = adjuster.querySelector('[data-action="decrease"]');
      var increaseBtn = adjuster.querySelector('[data-action="increase"]');
      var display = adjuster.querySelector('.servings-display');
      var ingredientsList = adjuster.closest('.recipe-ingredients, .recipe-card-block');

      if (!decreaseBtn || !increaseBtn || !display) return;

      var currentServings = parseInt(adjuster.dataset.servings || '4', 10);
      var originalServings = currentServings;

      function updateServings(newServings) {
        if (newServings < 1) return;
        currentServings = newServings;
        display.textContent = currentServings + (currentServings === 1 ? ' serving' : ' servings');
        if (ingredientsList) {
          ingredientsList.querySelectorAll('.ingredient-amount[data-original]').forEach(function (amt) {
            var original = parseFloat(amt.dataset.original);
            if (!isNaN(original)) amt.textContent = formatAmount((original / originalServings) * currentServings);
          });
        }
      }

      decreaseBtn.addEventListener('click', function () { updateServings(currentServings - 1); });
      increaseBtn.addEventListener('click', function () { updateServings(currentServings + 1); });
    });

    // Recipe page pattern: #servings-minus / #servings-plus / #servings-input / .qty[data-original]
    var minusBtn = document.getElementById('servings-minus');
    var plusBtn  = document.getElementById('servings-plus');
    var input    = document.getElementById('servings-input');
    var display2 = document.getElementById('servings-display');

    if (minusBtn && plusBtn && input) {
      var originalServings = parseInt(input.value, 10) || 4;

      function scaleIngredients(newVal) {
        if (newVal < 1) return;
        input.value = newVal;
        if (display2) display2.textContent = newVal;
        document.querySelectorAll('.qty[data-original]').forEach(function (el) {
          var orig = parseFloat(el.dataset.original);
          if (!isNaN(orig)) el.textContent = formatAmount((orig / originalServings) * newVal);
        });
      }

      minusBtn.addEventListener('click', function () { scaleIngredients(parseInt(input.value, 10) - 1); });
      plusBtn.addEventListener('click',  function () { scaleIngredients(parseInt(input.value, 10) + 1); });
      input.addEventListener('change',   function () { scaleIngredients(parseInt(input.value, 10) || originalServings); });
    }

    function formatAmount(num) {
      var fractions = { 0.25: '¼', 0.5: '½', 0.75: '¾', 0.33: '⅓', 0.67: '⅔' };
      var whole = Math.floor(num);
      var decimal = Math.round((num - whole) * 100) / 100;
      if (whole === 0) return fractions[decimal] || num.toFixed(1);
      if (decimal === 0) return whole.toString();
      return whole + (fractions[decimal] ? fractions[decimal] : '+' + decimal.toFixed(1));
    }
  }

  /* ----------------------------------------------------------------
     5. Back to Top Button
     Supports id="backToTop" and id="back-to-top"
  ---------------------------------------------------------------- */
  function initBackToTop() {
    var btn = document.getElementById('backToTop') || document.getElementById('back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', function () {
      if (window.scrollY > 500) {
        btn.classList.add('is-visible');
      } else {
        btn.classList.remove('is-visible');
      }
    }, { passive: true });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ----------------------------------------------------------------
     6. Newsletter Form
  ---------------------------------------------------------------- */
  function initNewsletterForm() {
    document.querySelectorAll('.newsletter-form').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var emailInput = form.querySelector('input[type="email"]');
        var feedback = form.nextElementSibling;
        if (!emailInput) return;

        var email = emailInput.value.trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          showMsg(form, 'Please enter a valid email address.', 'error');
          return;
        }
        showMsg(form, "Thanks! You're on the list. Check your inbox soon!", 'success');
        emailInput.value = '';
      });
    });

    function showMsg(form, msg, type) {
      var fb = form.querySelector('.newsletter-feedback') || form.nextElementSibling;
      if (!fb) return;
      fb.textContent = msg;
      fb.className = 'newsletter-feedback form-feedback ' + type;
    }
  }

  /* ----------------------------------------------------------------
     7. Contact Form
  ---------------------------------------------------------------- */
  function initContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var feedback = document.querySelector('.form-feedback');
      var name = form.querySelector('#name');
      var email = form.querySelector('#email');
      var message = form.querySelector('#message');

      if (!name || !name.value.trim()) { showFeedback(feedback, 'Please enter your name.', 'error'); return; }
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { showFeedback(feedback, 'Please enter a valid email address.', 'error'); return; }
      if (!message || !message.value.trim()) { showFeedback(feedback, 'Please write a message before sending.', 'error'); return; }

      showFeedback(feedback, "Message sent! We'll get back to you within 2 business days.", 'success');
      form.reset();
    });

    function showFeedback(el, msg, type) {
      if (!el) return;
      el.textContent = msg;
      el.className = 'form-feedback ' + type;
      el.style.display = 'block';
    }
  }

  /* ----------------------------------------------------------------
     8. Active Nav Link
  ---------------------------------------------------------------- */
  function initActiveNavLink() {
    var path = window.location.pathname;
    document.querySelectorAll('.nav-primary a, .nav-mobile a, .main-nav a').forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      if (path === href || (href !== '/' && href !== '../' && path.indexOf(href.replace('../', '/')) !== -1)) {
        link.classList.add('is-active');
      }
    });
  }

  /* ----------------------------------------------------------------
     9. Recipe Filter (recipes listing page)
     Supports space-separated multi-category: data-category="chicken quick"
  ---------------------------------------------------------------- */
  function initRecipeFilter() {
    var filterBtns = document.querySelectorAll('.filter-btn');
    var recipeCards = document.querySelectorAll('.recipe-card[data-category]');
    if (!filterBtns.length || !recipeCards.length) return;

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var category = btn.dataset.filter;

        filterBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');

        recipeCards.forEach(function (card) {
          var cats = (card.dataset.category || '').split(' ');
          var show = category === 'all' || cats.indexOf(category) !== -1;
          card.style.display = show ? '' : 'none';
          if (show) card.removeAttribute('hidden');
          else card.setAttribute('hidden', '');
        });
      });
    });

    // Handle ?category= URL param on load
    var params = new URLSearchParams(window.location.search);
    var cat = params.get('category') || params.get('filter');
    if (cat) {
      var matchBtn = document.querySelector('.filter-btn[data-filter="' + cat + '"]');
      if (matchBtn) matchBtn.click();
    }
  }

  /* ----------------------------------------------------------------
     10. Copy Link Button
     Supports both .share-btn--copy and .btn-copy-link
  ---------------------------------------------------------------- */
  function initCopyLink() {
    var copyBtn = document.querySelector('.share-btn--copy, .btn-copy-link');
    if (!copyBtn) return;

    copyBtn.addEventListener('click', function () {
      var url = copyBtn.dataset.url || window.location.href;
      var originalText = copyBtn.innerHTML;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          copyBtn.innerHTML = '✓ Copied!';
          setTimeout(function () { copyBtn.innerHTML = originalText; }, 2000);
        }).catch(fallbackCopy);
      } else {
        fallbackCopy();
      }

      function fallbackCopy() {
        var ta = document.createElement('textarea');
        ta.value = url;
        ta.style.cssText = 'position:fixed;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        copyBtn.innerHTML = '✓ Copied!';
        setTimeout(function () { copyBtn.innerHTML = originalText; }, 2000);
      }
    });
  }

  /* ----------------------------------------------------------------
     11. Smooth Scroll (jump-to-recipe and all anchor links)
  ---------------------------------------------------------------- */
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href^="#"]');
      if (!link) return;
      var target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      var headerOffset = 80;
      var top = target.getBoundingClientRect().top + window.scrollY - headerOffset;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  }

  /* ----------------------------------------------------------------
     12. Search Overlay
  ---------------------------------------------------------------- */
  function initSearch() {
    var toggleBtn = document.getElementById('searchToggle');
    if (!toggleBtn) return;

    // Determine path prefix based on current page location
    var pathname = window.location.pathname.replace(/\\/g, '/');
    var isInRecipes = pathname.indexOf('/recipes/') !== -1 ||
                      (pathname.lastIndexOf('/') > 0 && pathname.indexOf('recipes') !== -1 &&
                       !pathname.match(/\/recipes\/?$/));
    var prefix = isInRecipes ? '' : 'recipes/';

    var RECIPES = [
      { title: 'Easy Creamy Garlic Chicken',         time: '30 min', cat: 'Chicken', file: 'easy-creamy-garlic-chicken.html' },
      { title: 'One-Pan Beef Shawarma Bowl',         time: '35 min', cat: 'Beef',    file: 'one-pan-beef-shawarma-bowl.html' },
      { title: 'Spicy Garlic Butter Shrimp',         time: '10 min', cat: 'Seafood', file: 'spicy-garlic-butter-shrimp.html' },
      { title: 'Crispy Honey Garlic Salmon',         time: '25 min', cat: 'Seafood', file: 'crispy-honey-garlic-salmon.html' },
      { title: 'One-Pan Honey Butter Chicken',       time: '30 min', cat: 'Chicken', file: 'one-pan-honey-butter-chicken.html' },
      { title: 'Garlic Butter Steak Bites',          time: '15 min', cat: 'Beef',    file: 'garlic-butter-steak-bites.html' },
      { title: 'Creamy Tuscan Shrimp',               time: '20 min', cat: 'Seafood', file: 'creamy-tuscan-shrimp.html' },
      { title: 'Lemon Herb Sheet Pan Chicken',       time: '45 min', cat: 'Chicken', file: 'lemon-herb-sheet-pan-chicken.html' },
      { title: 'Crispy Baked Chicken Wings',         time: '50 min', cat: 'Chicken', file: 'crispy-baked-chicken-wings.html' },
      { title: 'Ground Beef Kofta with Garlic Sauce',time: '30 min', cat: 'Beef',    file: 'ground-beef-kofta-garlic-sauce.html' },
      { title: 'Coconut Chicken Curry',              time: '35 min', cat: 'Chicken', file: 'coconut-chicken-curry.html' },
      { title: 'Creamy Sun-Dried Tomato Pasta',      time: '25 min', cat: 'Pasta',   file: 'creamy-sun-dried-tomato-pasta.html' },
      { title: 'Beef & Broccoli Stir Fry',           time: '20 min', cat: 'Beef',    file: 'beef-broccoli-stir-fry.html' },
      { title: 'Smoky Paprika Baked Salmon',         time: '25 min', cat: 'Seafood', file: 'smoky-paprika-baked-salmon.html' },
      { title: 'Easy Chicken Tikka Masala',          time: '40 min', cat: 'Chicken', file: 'easy-chicken-tikka-masala.html' }
    ];

    // Build overlay and inject into <body>
    var overlay = document.createElement('div');
    overlay.id = 'searchOverlay';
    overlay.className = 'search-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Search recipes');
    overlay.innerHTML =
      '<div class="search-overlay__inner">' +
        '<span class="search-overlay__label">Search Recipes</span>' +
        '<div class="search-overlay__input-wrap">' +
          '<svg class="search-overlay__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>' +
          '<input class="search-overlay__input" id="searchInput" type="search" placeholder="Search a recipe or ingredient…" autocomplete="off" spellcheck="false" aria-label="Search recipes">' +
          '<button class="search-overlay__close" id="searchClose" aria-label="Close search">✕</button>' +
        '</div>' +
        '<div class="search-overlay__results" id="searchResults" role="listbox" aria-label="Search results"></div>' +
        '<div class="search-overlay__hint">' +
          '<span class="search-overlay__hint-item"><kbd>↑↓</kbd> Navigate</span>' +
          '<span class="search-overlay__hint-item"><kbd>↵</kbd> Open</span>' +
          '<span class="search-overlay__hint-item"><kbd>Esc</kbd> Close</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(overlay);

    var input    = document.getElementById('searchInput');
    var results  = document.getElementById('searchResults');
    var closeBtn = document.getElementById('searchClose');
    var focusIdx = -1;

    function openSearch() {
      overlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      toggleBtn.setAttribute('aria-expanded', 'true');
      setTimeout(function () { input.focus(); }, 40);
      renderResults('');
    }

    function closeSearch() {
      overlay.classList.remove('is-open');
      document.body.style.overflow = '';
      input.value = '';
      results.innerHTML = '';
      focusIdx = -1;
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.focus();
    }

    function escHtml(s) {
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }

    function highlight(text, q) {
      if (!q) return text;
      var i = text.toLowerCase().indexOf(q);
      if (i === -1) return text;
      return text.slice(0, i) +
        '<mark style="background:rgba(212,168,83,0.45);color:inherit;border-radius:2px;">' +
        text.slice(i, i + q.length) + '</mark>' +
        text.slice(i + q.length);
    }

    function renderResults(raw) {
      var q = raw.trim().toLowerCase();
      var list = q === '' ? RECIPES : RECIPES.filter(function (r) {
        return r.title.toLowerCase().indexOf(q) !== -1 ||
               r.cat.toLowerCase().indexOf(q) !== -1;
      });

      if (!list.length) {
        results.innerHTML = '<p class="search-overlay__empty">No recipes found for "<strong>' + escHtml(q) + '</strong>". Try another keyword.</p>';
        return;
      }

      results.innerHTML = list.map(function (r, i) {
        return '<a class="search-result-item" href="' + prefix + r.file + '" role="option" tabindex="-1" data-idx="' + i + '">' +
          '<span class="search-result__icon" aria-hidden="true">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M3 12h18M3 18h12"/></svg>' +
          '</span>' +
          '<span class="search-result__title">' + highlight(r.title, q) + '</span>' +
          '<span class="search-result__meta">' + escHtml(r.time) + '</span>' +
        '</a>';
      }).join('');
      focusIdx = -1;
    }

    function moveFocus(dir) {
      var items = results.querySelectorAll('.search-result-item');
      if (!items.length) return;
      items.forEach(function (el) { el.classList.remove('is-focused'); });
      focusIdx = (focusIdx + dir + items.length) % items.length;
      items[focusIdx].classList.add('is-focused');
      items[focusIdx].scrollIntoView({ block: 'nearest' });
    }

    toggleBtn.addEventListener('click', function () {
      overlay.classList.contains('is-open') ? closeSearch() : openSearch();
    });

    closeBtn.addEventListener('click', closeSearch);

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSearch();
    });

    input.addEventListener('input', function () {
      renderResults(input.value);
    });

    document.addEventListener('keydown', function (e) {
      if (!overlay.classList.contains('is-open')) {
        // Open on Ctrl+K / Cmd+K from anywhere
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
        return;
      }
      if (e.key === 'Escape')    { closeSearch(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); moveFocus(1); return; }
      if (e.key === 'ArrowUp')   { e.preventDefault(); moveFocus(-1); return; }
      if (e.key === 'Enter') {
        var focused = results.querySelector('.search-result-item.is-focused');
        if (focused) { closeSearch(); window.location.href = focused.href; }
      }
    });
  }

  /* ----------------------------------------------------------------
     13. Glass Header — homepage only
  ---------------------------------------------------------------- */
  function initGlassHeader() {
    var header = document.querySelector('.site-header[data-glass]');
    if (!header) return;
    document.body.classList.add('has-glass-header');
  }

  /* ----------------------------------------------------------------
     Count-up animation for trust strip numbers
  ---------------------------------------------------------------- */
  function animateCount(el, target, duration) {
    var start = 0;
    var startTime = null;
    var isFloat = String(target).indexOf('.') !== -1;
    var end = parseFloat(target);
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3);
      var current = start + (end - start) * ease;
      el.textContent = isFloat ? current.toFixed(1) : Math.floor(current);
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = isFloat ? end.toFixed(1) : end;
    }
    requestAnimationFrame(step);
  }

  function initTrustCounters() {
    var items = document.querySelectorAll('.trust-item__num[data-count]');
    if (!items.length) return;
    var observed = false;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !observed) {
          observed = true;
          items.forEach(function (el) {
            animateCount(el, el.getAttribute('data-count'), 1400);
          });
          observer.disconnect();
        }
      });
    }, { threshold: 0.4 });
    observer.observe(items[0].closest('.trust-strip') || items[0]);
  }

  /* ----------------------------------------------------------------
     Reviewer Avatar Colors
     Assigns a unique gradient color (1-8) to each avatar based on
     the letter's char code so the same person always gets same color
  ---------------------------------------------------------------- */
  function initAvatarColors() {
    var avatars = document.querySelectorAll('.reviewer-avatar');
    if (!avatars.length) return;
    // Sequential assignment so adjacent reviewers always differ
    var seq = [1, 3, 5, 2, 7, 4, 6, 8];
    avatars.forEach(function (el, i) {
      el.setAttribute('data-color', String(seq[i % seq.length]));
    });
  }

  /* ----------------------------------------------------------------
     Cookie Consent Banner
  ---------------------------------------------------------------- */
  function initCookieConsent() {
    var banner = document.getElementById('cookieConsent');
    if (!banner) return;

    var consent = localStorage.getItem('mars_cookie_consent');
    if (consent) return; // already decided

    // Show banner after short delay
    banner.removeAttribute('hidden');
    setTimeout(function () { banner.classList.add('is-visible'); }, 300);

    document.getElementById('cookieAccept').addEventListener('click', function () {
      localStorage.setItem('mars_cookie_consent', 'accepted');
      hideBanner();
    });

    document.getElementById('cookieDecline').addEventListener('click', function () {
      localStorage.setItem('mars_cookie_consent', 'declined');
      hideBanner();
    });

    function hideBanner() {
      banner.classList.remove('is-visible');
      setTimeout(function () { banner.setAttribute('hidden', ''); }, 400);
    }
  }

  /* ----------------------------------------------------------------
     Init
  ---------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    initMobileNav();
    initStickyHeader();
    initIngredientChecker();
    initServingsAdjuster();
    initBackToTop();
    initNewsletterForm();
    initContactForm();
    initActiveNavLink();
    initRecipeFilter();
    initCopyLink();
    initSmoothScroll();
    initSearch();
    initGlassHeader();
    initTrustCounters();
    initCookieConsent();
    initAvatarColors();
    initReviewForm();
  });

  /* ----------------------------------------------------------------
     Review Form – interactive stars + localStorage persistence
  ---------------------------------------------------------------- */
  function initReviewForm() {
    var form = document.getElementById('reviewForm');
    if (!form) return;

    var stars = document.querySelectorAll('.rf-star');
    var ratingInput = document.getElementById('rfRating');
    var selectedRating = 0;

    // Highlight stars up to hovered index
    function litStars(n) {
      stars.forEach(function (s, i) {
        s.classList.toggle('is-lit', i < n);
      });
    }

    stars.forEach(function (star) {
      star.addEventListener('mouseover', function () {
        litStars(parseInt(this.dataset.v));
      });
      star.addEventListener('click', function () {
        selectedRating = parseInt(this.dataset.v);
        ratingInput.value = selectedRating;
        stars.forEach(function (s, i) {
          s.classList.toggle('is-active', i < selectedRating);
          s.classList.remove('is-lit');
        });
      });
    });

    var starsWrap = document.getElementById('rfStars');
    if (starsWrap) {
      starsWrap.addEventListener('mouseleave', function () {
        litStars(0);
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (selectedRating === 0) {
        alert('Please select a star rating before submitting.');
        return;
      }
      var name = (document.getElementById('rfName').value || '').trim();
      var comment = (document.getElementById('rfComment').value || '').trim();
      if (!name || !comment) return;

      // Sanitise plain text (no HTML injection)
      var rev = {
        name: name.slice(0, 60),
        rating: selectedRating,
        comment: comment.slice(0, 800),
        date: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
      };

      var key = 'mars_reviews_' + location.pathname;
      var stored = JSON.parse(localStorage.getItem(key) || '[]');
      stored.push(rev);
      localStorage.setItem(key, JSON.stringify(stored));

      renderReview(rev);
      form.hidden = true;
      var ok = document.getElementById('rfSuccess');
      if (ok) ok.hidden = false;
    });

    loadStoredReviews();
  }

  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function starsHtml(n) {
    var s = '';
    for (var i = 1; i <= 5; i++) s += i <= n ? '★' : '☆';
    return s;
  }

  function renderReview(r) {
    var list = document.querySelector('.reviews-list');
    if (!list) return;
    var art = document.createElement('article');
    art.className = 'review-card';
    art.innerHTML =
      '<div class="review-header">' +
        '<div class="reviewer-avatar" style="background:linear-gradient(135deg,#C0522B,#E8845E)">' + esc(r.name.charAt(0).toUpperCase()) + '</div>' +
        '<div class="reviewer-info">' +
          '<span class="reviewer-name">' + esc(r.name) + '</span>' +
          '<span class="review-date">' + esc(r.date) + '</span>' +
        '</div>' +
        '<span class="review-stars" aria-label="' + r.rating + ' out of 5 stars">' + starsHtml(r.rating) + '</span>' +
      '</div>' +
      '<p class="review-text">' + esc(r.comment) + '</p>';
    list.appendChild(art);
  }

  function loadStoredReviews() {
    var key = 'mars_reviews_' + location.pathname;
    var stored = JSON.parse(localStorage.getItem(key) || '[]');
    stored.forEach(function (r) { renderReview(r); });
  }

})();
