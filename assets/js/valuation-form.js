(function () {
  var LEAD_CAPTURE = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead';

  var VALUATION_API = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/property-valuation';

  // ── Bot/spam guard: Cloudflare Turnstile (verified server-side) + honeypot backstop ──
  var TS_SITEKEY = '0x4AAAAAAFBn_J2vobl7Yrk7';
  var HP_NAME = 'contact_time_pref';
  var MIN_MS = 1500;
  (function loadTurnstile() {
    if (window.turnstile || document.getElementById('cf-ts-api')) return;
    var s = document.createElement('script');
    s.id = 'cf-ts-api';
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    s.async = true; s.defer = true;
    (document.head || document.documentElement).appendChild(s);
  })();
  function renderWidget(form) {
    if (form.__tsId != null || !window.turnstile) return;
    var holder = document.createElement('div');
    holder.className = 'cf-turnstile-holder';
    holder.style.margin = '12px 0';
    var btn = form.querySelector('button[type="submit"]');
    if (btn) form.insertBefore(holder, btn); else form.appendChild(holder);
    try { form.__tsId = window.turnstile.render(holder, { sitekey: TS_SITEKEY, action: 'valuation' }); }
    catch (e) {}
  }
  var tsPoll = setInterval(function () {
    if (window.turnstile) {
      clearInterval(tsPoll);
      var fs = document.querySelectorAll('form.ipg-valuation-form');
      for (var i = 0; i < fs.length; i++) renderWidget(fs[i]);
    }
  }, 250);
  setTimeout(function () { clearInterval(tsPoll); }, 20000);
  function armForm(form) {
    if (form.__armed) return;
    form.__armed = true;
    form.__loadedAt = Date.now();
    form.__interacted = false;
    var hp = document.createElement('input');
    hp.type = 'text'; hp.name = HP_NAME; hp.tabIndex = -1;
    hp.setAttribute('autocomplete', 'off'); hp.setAttribute('aria-hidden', 'true');
    hp.style.cssText = 'position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden;opacity:0;';
    form.appendChild(hp);
    form.addEventListener('focusin', function () { form.__interacted = true; }, true);
    form.addEventListener('input', function () { form.__interacted = true; }, true);
    renderWidget(form);
  }
  function armAll() {
    var fs = document.querySelectorAll('form.ipg-valuation-form');
    for (var i = 0; i < fs.length; i++) armForm(fs[i]);
  }
  if (document.readyState !== 'loading') armAll();
  else document.addEventListener('DOMContentLoaded', armAll);
  function isBot(form) {
    var hpEl = form.querySelector('[name="' + HP_NAME + '"]');
    return (hpEl && hpEl.value.trim() !== '') ||
           (form.__loadedAt && Date.now() - form.__loadedAt < MIN_MS) ||
           !form.__interacted;
  }

  function fmt(n) {
    if (n == null) return 'N/A';
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function fmtDate(d) {
    if (!d) return '';
    return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.classList.contains('ipg-valuation-form')) return;
    e.preventDefault();
    armForm(form);
    if (isBot(form)) { return; } // silently drop bot submissions — nothing sent to CRM or API

    var btn = form.querySelector('button[type="submit"]');
    var originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Analyzing your property…';

    var data = {};
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].name && inputs[i].name !== HP_NAME) data[inputs[i].name] = inputs[i].value;
    }
    data.source_url = window.location.href;
    data.submitted_at = new Date().toISOString();

    // Auto-append Indiana if no state detected
    if (data.address && !/\b[A-Z]{2}\b/.test(data.address) && !/indiana/i.test(data.address)) {
      data.address = data.address.replace(/,?\s*$/, '') + ', IN';
    }

    // Capture the lead in the CRM in the background (don't wait for it)
    var tsToken = (window.turnstile && form.__tsId != null) ? window.turnstile.getResponse(form.__tsId) : '';
    fetch(LEAD_CAPTURE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        business: 'yrl',
        name: data.name,
        email: data.email,
        phone: data.phone,
        message: 'Home valuation request: ' + (data.address || ''),
        source: data.source || 'home-valuation',
        tags: data.tags || 'valuation-lead',
        source_page: data.source_page || 'home-valuation',
        'cf-turnstile-response': tsToken || ''
      })
    }).catch(function () {});

    // Send to valuation API
    fetch(VALUATION_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address: data.address,
        email: data.email,
        name: data.name,
        phone: data.phone,
        source_page: data.source_page
      })
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        return res.json();
      })
      .then(function (result) {
        if (!result.success) throw new Error(result.error || 'Valuation failed');
        showResults(result, data.address);
        form.style.display = 'none';
      })
      .catch(function (err) {
        btn.disabled = false;
        btn.textContent = originalText;
        var errEl = form.querySelector('.form-error');
        if (!errEl) {
          errEl = document.createElement('p');
          errEl.className = 'form-error';
          form.appendChild(errEl);
        }
        errEl.textContent = 'We couldn\'t find data for that address. Please double-check and try again, or call 317-997-7404 for a personalized CMA.';
      });
  });

  function showResults(r, address) {
    var container = document.getElementById('valuation-results');
    if (!container) return;

    document.getElementById('val-estimate').textContent = fmt(r.estimate);
    document.getElementById('val-range').textContent = 'Estimated Range: ' + fmt(Math.max(0, r.rangeLow || 0)) + ' — ' + fmt(r.rangeHigh);
    document.getElementById('val-address-display').textContent = r.address || address;

    // Property details
    var detailsEl = document.getElementById('val-details');
    var details = [
      { label: 'Bedrooms', value: r.bedrooms || '—' },
      { label: 'Bathrooms', value: r.bathrooms || '—' },
      { label: 'Sq Ft', value: r.squareFootage ? r.squareFootage.toLocaleString() : '—' },
      { label: 'Year Built', value: r.yearBuilt || '—' },
      { label: 'Type', value: r.propertyType || '—' },
      { label: 'Comps Found', value: r.comparables || 0 }
    ];
    detailsEl.innerHTML = details.map(function (d) {
      return '<div class="val-detail-item"><div class="val-detail-label">' + d.label + '</div><div class="val-detail-value">' + d.value + '</div></div>';
    }).join('');

    // Comparable sales
    if (r.comparableDetails && r.comparableDetails.length > 0) {
      var compsSection = document.getElementById('val-comps-section');
      var compsList = document.getElementById('val-comps-list');
      compsSection.style.display = 'block';
      compsList.innerHTML = r.comparableDetails.map(function (c) {
        var meta = [
          c.bedrooms ? c.bedrooms + ' bed' : '',
          c.bathrooms ? c.bathrooms + ' bath' : '',
          c.squareFootage ? c.squareFootage.toLocaleString() + ' sqft' : '',
          c.yearBuilt ? 'Built ' + c.yearBuilt : '',
          c.status || '',
          c.distance != null ? c.distance.toFixed(2) + ' mi' : ''
        ].filter(Boolean).join(' · ');
        return '<div class="comp-card"><span class="comp-address">' + (c.address || '') + '</span><span class="comp-price">' + fmt(c.price) + '</span><div class="comp-meta">' + meta + '</div></div>';
      }).join('');
    }

    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
