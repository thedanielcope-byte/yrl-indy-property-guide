/* ═══════════════════════════════════════════════════════════
   Indy Property Guide — Lead Capture Forms
   Posts to GoHighLevel webhook
   ═══════════════════════════════════════════════════════════ */

(function () {
  // ── GHL WEBHOOK URL — replace this with your real URL ──
  var WEBHOOK_URL = 'https://services.leadconnectorhq.com/hooks/iOT1nopTL5CnKPq44zFI/webhook-trigger/b82bea0a-88fa-4cd5-9ad5-9fa3f05e7d50';

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
          '<p>We\'ll be in touch shortly. If you need immediate help, call <a href="tel:3172016323">317-201-6323</a>.</p>' +
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
          'Something went wrong. Please call us at 317-201-6323 or email csirealtyteam@yourrealtylink.com.';
      });
  });
})();
