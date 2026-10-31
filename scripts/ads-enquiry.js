/* Sends website enquiries to the ADS OS inbox (in addition to the existing email / WhatsApp flow).
   It calls one narrow database function that can only add an enquiry to the inbox; it cannot read
   any data. If ADS OS can't be reached, the form still works exactly as before. */
(function () {
  var ADS_OS = {
    url: "https://ixsdayxmutyjavcoqqoe.supabase.co/rest/v1/rpc/submit_web_enquiry",
    key: "sb_publishable_F7omKTyj60mA_RrbNI1vSA_KmUJhLnV" // publishable key: safe to be public
  };
  var started = Date.now();

  function addHoneypot(form) {
    if (form.querySelector('input[name="website"]')) return;
    var wrap = document.createElement("div");
    wrap.setAttribute("aria-hidden", "true");
    wrap.style.cssText = "position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden";
    wrap.innerHTML = '<label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(wrap);
  }
  function val(form, sel) { var el = form.querySelector(sel); return el ? String(el.value || "").trim() : ""; }

  // Returns a promise that always resolves (true = saved to ADS OS), within ~2.5 s at most.
  window.sendToAdsOs = function (form, data) {
    data.website = val(form, 'input[name="website"]');
    data.elapsed_ms = Date.now() - started;
    data.page = location.pathname;
    var timer = new Promise(function (res) { setTimeout(function () { res(false); }, 2500); });
    var req = fetch(ADS_OS.url, {
      method: "POST", keepalive: true, mode: "cors",
      headers: { "Content-Type": "application/json", "apikey": ADS_OS.key },
      body: JSON.stringify({ payload: data })
    }).then(function (r) { return r.ok; }).catch(function () { return false; });
    return Promise.race([req, timer]);
  };

  document.addEventListener("DOMContentLoaded", function () {
    // Contact form (still emails via Formspree after saving to ADS OS)
    var contact = document.querySelector('form[action*="formspree.io"]');
    if (contact) {
      addHoneypot(contact);
      var sending = false;
      contact.addEventListener("submit", function (e) {
        if (sending) return;
        if (!contact.checkValidity()) return;
        e.preventDefault(); sending = true;
        var btn = contact.querySelector('[type="submit"]'); if (btn) { btn.disabled = true; btn.textContent = document.documentElement.lang === "bn" ? "পাঠানো হচ্ছে…" : "SENDING…"; }
        window.sendToAdsOs(contact, {
          form: "contact", name: val(contact, "#name"), email: val(contact, "#email"), phone: val(contact, "#phone"),
          project_type: val(contact, "#project-type"), package: val(contact, "#package-dropdown"), message: val(contact, "#message")
        }).then(function () { HTMLFormElement.prototype.submit.call(contact); });
      });
    }
    // Consultation form (still opens WhatsApp; the ADS OS save runs alongside)
    var consult = document.getElementById("consultationForm");
    if (consult) {
      addHoneypot(consult);
      consult.addEventListener("submit", function () {
        window.sendToAdsOs(consult, {
          form: "consultation", name: val(consult, "#fullname"), phone: val(consult, "#whatsapp"), location: val(consult, "#location"),
          project_type: val(consult, "#ptype"), mode: val(consult, "#mode"), preferred_date: val(consult, "#date"), slot: val(consult, "#time")
        });
      }, true);
    }
  });
})();
