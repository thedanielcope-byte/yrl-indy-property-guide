/* ═══════════════════════════════════════════════════════════
   Indy Property Guide — Lead Capture Forms
   Posts to the Nomad Systems CRM capture-lead endpoint (Supabase)
   ═══════════════════════════════════════════════════════════ */

(function () {
  // ── CRM capture-lead endpoint (Supabase Edge Function) ──
  var WEBHOOK_URL = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead';

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.classList.contains('ipg-lead-form')) return;
    e.preventDefault();

    var btn = form.querySelector('button[type="submit"]');
    var originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Sending…';

    var data = {};
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      var el = inputs[i];
      if (el.name) data[el.name] = el.value;
    }
    data.source_url = window.location.href;
    data.submitted_at = new Date().toISOString();
    data.business = 'yrl';
    data.source = data.source || 'indypropertyguide';
    data.tags = data.tags || 'real-estate-lead';

    fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.innerHTML =
          '<div class="form-success">' +
          '<span class="form-success-icon">✓</span>' +
          '<strong>Thank you!</strong>' +
          '<p>We\'ll be in touch shortly. If you need immediate help, call <a href="tel:3179977404">317-997-7404</a>.</p>' +
          '</div>';
      })
      .catch(function () {
        btn.disabled = false;
        btn.textContent = originalText;
        var err = form.querySelector('.form-error');
        if (!err) {
          err = document.createElement('p');
          err.className = 'form-error';
          form.appendChild(err);
        }
        err.textContent =
          'Something went wrong. Please call us at 317-997-7404 or email info@yourrealtylink.com.';
      });
  });
})();
