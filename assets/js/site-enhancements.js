(function() {
  'use strict';

  // ═══════════════════════════════════════════════
  // STICKY BOTTOM BAR CTA
  // ═══════════════════════════════════════════════
  function initStickyBar() {
    if (document.querySelector('.sticky-cta-bar')) return;

    var dismissed = sessionStorage.getItem('stickyBarDismissed');
    if (dismissed) return;

    var bar = document.createElement('div');
    bar.className = 'sticky-cta-bar';
    bar.innerHTML =
      '<div class="sticky-cta-inner">' +
        '<span class="sticky-cta-text">Ready to buy or sell in Indianapolis? Talk to a local expert — <strong>no obligation.</strong></span>' +
        '<div class="sticky-cta-actions">' +
          '<a href="/schedule/" class="sticky-btn sticky-btn-primary">Schedule a Free Consultation</a>' +
          '<a href="tel:3172016323" class="sticky-btn sticky-btn-phone">📞 317-201-6323</a>' +
        '</div>' +
        '<button class="sticky-cta-close" aria-label="Close">&times;</button>' +
      '</div>';

    document.body.appendChild(bar);

    // Show after 5 seconds of scrolling (user engaged)
    var shown = false;
    function showBar() {
      if (shown) return;
      if (window.scrollY > 400) {
        shown = true;
        bar.classList.add('visible');
        window.removeEventListener('scroll', showBar);
      }
    }
    window.addEventListener('scroll', showBar, { passive: true });

    bar.querySelector('.sticky-cta-close').addEventListener('click', function() {
      bar.classList.remove('visible');
      bar.classList.add('dismissed');
      sessionStorage.setItem('stickyBarDismissed', '1');
    });
  }

  // ═══════════════════════════════════════════════
  // EXIT-INTENT POPUP
  // ═══════════════════════════════════════════════
  function initExitPopup() {
    if (sessionStorage.getItem('exitPopupShown')) return;

    var overlay = document.createElement('div');
    overlay.className = 'exit-popup-overlay';
    overlay.innerHTML =
      '<div class="exit-popup">' +
        '<button class="exit-popup-close" aria-label="Close">&times;</button>' +
        '<div class="exit-popup-content">' +
          '<h2>Wait — Grab a Free Guide Before You Go</h2>' +
          '<p>Download a free checklist and get expert tips for your next move in Indianapolis.</p>' +
          '<div class="exit-popup-cards">' +
            '<a href="/resources/buyer-checklist/" class="exit-card">' +
              '<span class="exit-card-icon">📋</span>' +
              '<span class="exit-card-label">Buying a Home?</span>' +
              '<span class="exit-card-action">Free Buyer Checklist →</span>' +
            '</a>' +
            '<a href="/resources/seller-guide/" class="exit-card">' +
              '<span class="exit-card-icon">📦</span>' +
              '<span class="exit-card-label">Selling a Home?</span>' +
              '<span class="exit-card-action">Free Seller Prep Guide →</span>' +
            '</a>' +
          '</div>' +
          '<div class="exit-popup-alt">' +
            '<a href="/schedule/" class="exit-phone">Or <strong>schedule a free consultation</strong> — no obligation</a>' +
          '</div>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    function showPopup() {
      if (sessionStorage.getItem('exitPopupShown')) return;
      overlay.classList.add('visible');
      sessionStorage.setItem('exitPopupShown', '1');
      document.removeEventListener('mouseout', handleMouseOut);
    }

    function closePopup() {
      overlay.classList.remove('visible');
    }

    // Desktop: mouse leaves viewport from top
    function handleMouseOut(e) {
      if (e.clientY <= 0 && e.relatedTarget == null) {
        showPopup();
      }
    }

    // Only attach after user has been on page 15 seconds
    setTimeout(function() {
      document.addEventListener('mouseout', handleMouseOut);
    }, 15000);

    // Close handlers
    overlay.querySelector('.exit-popup-close').addEventListener('click', closePopup);
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closePopup();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closePopup();
    });
  }

  // ═══════════════════════════════════════════════
  // BLOG POST INLINE CTA UPGRADES
  // ═══════════════════════════════════════════════
  function initBlogInlineCTAs() {
    // Only run on blog post pages
    if (window.location.pathname.indexOf('/blog/') === -1) return;
    if (window.location.pathname === '/blog/' || window.location.pathname === '/blog') return;

    var h2s = document.querySelectorAll('.service-wrap h2, .post-content h2, article h2');
    if (h2s.length < 4) return;

    // Insert an inline CTA after the 3rd H2's content section
    var targetH2 = h2s[2];
    var nextEl = targetH2.nextElementSibling;
    while (nextEl && nextEl.tagName !== 'H2' && nextEl.tagName !== 'DIV') {
      nextEl = nextEl.nextElementSibling;
    }

    if (!nextEl) return;

    // Don't double-insert
    if (document.querySelector('.blog-inline-cta')) return;

    var isSeller = /sell|valuation|staging|price|expired|fsbo|closing.cost.*seller/i.test(document.title);
    var scheduleUrl = isSeller ? '/schedule/seller-consultation/' : '/schedule/buyer-consultation/';
    var scheduleLabel = isSeller ? 'Free Seller Consultation' : 'Free Buyer Consultation';

    var cta = document.createElement('div');
    cta.className = 'blog-inline-cta';
    cta.innerHTML =
      '<div class="blog-inline-cta-inner">' +
        '<p class="blog-inline-cta-text">💬 <strong>Have questions?</strong> Talk to a local Indianapolis agent — no pressure, no obligation.</p>' +
        '<div class="blog-inline-cta-buttons">' +
          '<a href="' + scheduleUrl + '" class="btn btn-primary">Schedule a ' + scheduleLabel + '</a>' +
          '<a href="tel:3172016323" class="btn btn-outline">Call 317-201-6323</a>' +
        '</div>' +
      '</div>';

    nextEl.parentNode.insertBefore(cta, nextEl);
  }

  // ═══════════════════════════════════════════════
  // INIT
  // ═══════════════════════════════════════════════
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initStickyBar();
      initExitPopup();
      initBlogInlineCTAs();
    });
  } else {
    initStickyBar();
    initExitPopup();
    initBlogInlineCTAs();
  }
})();
