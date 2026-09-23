/* ═══════════════════════════════════════════════════════════
   Indy Property Guide — Lead Capture Forms
   Posts to the Nomad Systems CRM capture-lead endpoint (Supabase)

   Bot/spam guard (client-side, zero friction for real users):
   - Honeypot: a hidden field bots fill but humans never see. If filled → drop.
   - Interaction trap: real users focus/type in a field before submitting;
     a submit with no prior interaction (or within ~1.5s of load) → drop.
   Dropped submissions show the normal success UI so bots don't retry, but nothing
   is sent to the CRM. The honeypot value is never included in the payload.
   ═══════════════════════════════════════════════════════════ */

(function () {
  // ── CRM capture-lead endpoint (Supabase Edge Function) ──
  var WEBHOOK_URL = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead';
  var HP_NAME = 'contact_time_pref';   // honeypot field name (innocuous, bot-attractive)
  var MIN_MS = 1500;                    // submits faster than this after load are bots

  function successHTML() {
    return '<div class="form-success">' +
      '<span class="form-success-icon">✓</span>' +
      '<strong>Thank you!</strong>' +
      '<p>We\'ll be in touch shortly. If you need immediate help, call <a href="tel:3179977404">317-997-7404</a>.</p>' +
      '</div>';
  }

  // Arm each lead form: inject the honeypot, stamp load time, track interaction.
  function armForm(form) {
    if (form.__armed) return;
    form.__armed = true;
    form.__loadedAt = Date.now();
    form.__interacted = false;

    var hp = document.createElement('input');
    hp.type = 'text';
    hp.name = HP_NAME;
    hp.tabIndex = -1;
    hp.setAttribute('autocomplete', 'off');
    hp.setAttribute('aria-hidden', 'true');
    // Off-screen rather than display:none (some bots skip display:none fields).
    hp.style.cssText = 'position:absolute!important;left:-9999px!important;top:auto;width:1px;height:1px;overflow:hidden;opacity:0;';
    form.appendChild(hp);

    form.addEventListener('focusin', function () { form.__interacted = true; }, true);
    form.addEventListener('input', function () { form.__interacted = true; }, true);
  }

  function armAll() {
    var forms = document.querySelectorAll('form.ipg-lead-form');
    for (var i = 0; i < forms.length; i++) armForm(forms[i]);
  }
  if (document.readyState !== 'loading') armAll();
  else document.addEventListener('DOMContentLoaded', armAll);

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.classList.contains('ipg-lead-form')) return;
    e.preventDefault();
    armForm(form); // in case it was added after load

    var btn = form.querySelector('button[type="submit"]');
    var originalText = btn ? btn.textContent : '';

    // ── Bot checks ──
    var hpEl = form.querySelector('[name="' + HP_NAME + '"]');
    var honeypotTripped = hpEl && hpEl.value.trim() !== '';
    var tooFast = form.__loadedAt && (Date.now() - form.__loadedAt < MIN_MS);
    var noInteraction = !form.__interacted;
    if (honeypotTripped || tooFast || noInteraction) {
      // Silently drop: show success so the bot doesn't retry, but send nothing.
      form.innerHTML = successHTML();
      return;
    }

    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

    var data = {};
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      var el = inputs[i];
      if (el.name && el.name !== HP_NAME) data[el.name] = el.value; // never send the honeypot
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
        form.innerHTML = successHTML();
      })
      .catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = originalText; }
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
