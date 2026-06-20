(function () {
  var GHL_WEBHOOK = 'https://services.leadconnectorhq.com/hooks/iOT1nopTL5CnKPq44zFI/webhook-trigger/90f523ba-dd26-4946-ab3d-5b036540af8a';

  var VALUATION_API = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/property-valuation';

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

    var btn = form.querySelector('button[type="submit"]');
    var originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Analyzing your property…';

    var data = {};
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].name) data[inputs[i].name] = inputs[i].value;
    }
    data.source_url = window.location.href;
    data.submitted_at = new Date().toISOString();

    // Auto-append Indiana if no state detected
    if (data.address && !/\b[A-Z]{2}\b/.test(data.address) && !/indiana/i.test(data.address)) {
      data.address = data.address.replace(/,?\s*$/, '') + ', IN';
    }

    // Send to GHL in background (don't wait for it)
    fetch(GHL_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
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
        errEl.textContent = 'We couldn\'t find data for that address. Please double-check and try again, or call 317-201-6323 for a personalized CMA.';
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
