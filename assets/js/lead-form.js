/* ═══════════════════════════════════════════════════════════
   Indy Property Guide — Lead Capture Forms
   Posts to the Nomad Systems CRM capture-lead endpoint (Supabase)

   Bot/spam guard, layered:
   1. Cloudflare Turnstile — a verified human-proof token sent with the lead; the
      server rejects any YRL lead without a valid token. This is the real defense.
   2. Honeypot + interaction trap (below) — cheap client-side backstop.
   Dropped/failed submissions show the normal success UI so bots don't retry.
   ═══════════════════════════════════════════════════════════ */

(function () {
  var WEBHOOK_URL = 'https://wdvolamasztetwpitbwg.supabase.co/functions/v1/capture-lead';
  var TS_SITEKEY = '0x4AAAAAAFBn_J2vobl7Yrk7';
  var HP_NAME = 'contact_time_pref';
  var MIN_MS = 1500;

  // ── Load the Turnstile API (once) + render a widget in each lead form ──
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
    try {
      form.__tsId = window.turnstile.render(holder, { sitekey: TS_SITEKEY, action: 'lead' });
    } catch (e) { /* leave __tsId unset; guarded below */ }
  }
  function renderAllWidgets() {
    if (!window.turnstile) return;
    var forms = document.querySelectorAll('form.ipg-lead-form');
    for (var i = 0; i < forms.length; i++) renderWidget(forms[i]);
  }
  // Turnstile loads async — render as soon as it's ready.
  var tsPoll = setInterval(function () {
    if (window.turnstile) { clearInterval(tsPoll); renderAllWidgets(); }
  }, 250);
  setTimeout(function () { clearInterval(tsPoll); }, 20000);

  function successHTML() {
    return '<div class="form-success">' +
      '<span class="form-success-icon">✓</span>' +
      '<strong>Thank you!</strong>' +
      '<p>We\'ll be in touch shortly. If you need immediate help, call <a href="tel:3179977404">317-997-7404</a>.</p>' +
      '</div>';
  }

  function armForm(form) {
    if (form.__armed) return;
    form.__armed = true;
    form.__loadedAt = Date.now();
    form.__interacted = false;
    var hp = document.createElement('input');
    hp.type = 'text'; hp.name = HP_NAME; hp.tabIndex = -1;
    hp.setAttribute('autocomplete', 'off'); hp.setAttribute('aria-hidden', 'true');
    hp.style.cssText = 'position:absolute!important;left:-9999px!important;top:auto;width:1px;height:1px;overflow:hidden;opacity:0;';
    form.appendChild(hp);
    form.addEventListener('focusin', function () { form.__interacted = true; }, true);
    form.addEventListener('input', function () { form.__interacted = true; }, true);
    renderWidget(form);
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
    armForm(form);

    var btn = form.querySelector('button[type="submit"]');
    var originalText = btn ? btn.textContent : '';

    // Client-side backstop: honeypot + interaction trap.
    var hpEl = form.querySelector('[name="' + HP_NAME + '"]');
    if ((hpEl && hpEl.value.trim() !== '') ||
        (form.__loadedAt && Date.now() - form.__loadedAt < MIN_MS) ||
        !form.__interacted) {
      form.innerHTML = successHTML();
      return;
    }

    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

    var data = {};
    var inputs = form.querySelectorAll('input, select, textarea');
    for (var i = 0; i < inputs.length; i++) {
      var el = inputs[i];
      if (el.name && el.name !== HP_NAME) data[el.name] = el.value;
    }
    // Turnstile token (verified server-side).
    var token = (window.turnstile && form.__tsId != null) ? window.turnstile.getResponse(form.__tsId) : '';
    data['cf-turnstile-response'] = token || '';
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
        if (window.turnstile && form.__tsId != null) { try { window.turnstile.reset(form.__tsId); } catch (e) {} }
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
