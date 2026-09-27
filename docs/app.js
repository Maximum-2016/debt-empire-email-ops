
async function populateJourneySelects() {
  const seq = await api("/api/sequences");
  const keys = Object.keys(seq.journeys).sort((a, b) => {
    const rank = (j) => j.startsWith("nurture-") ? 0 : j === "nurture" ? 1 : 2;
    return rank(a) - rank(b) || a.localeCompare(b);
  });
  const opts = [`<option value="brand-cycle">brand-cycle (meta — start rotation)</option>`]
    .concat(keys.map((j) => `<option value="${j}">${j} (${seq.journeys[j].touches.length})</option>`))
    .join("");
  for (const id of ["enroll-journey", "prev-journey", "send-journey"]) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = opts;
  }
}

/* Debt Empire Email Ops UI — MGP wall */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

function msg(el, text, kind = "info") {
  el.innerHTML = `<div class="msg ${kind}">${escapeHtml(text)}</div>`;
}
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

/* Tabs */
$$(".tabs button").forEach((btn) => {
  btn.addEventListener("click", () => {
    $$(".tabs button").forEach((b) => b.classList.remove("active"));
    $$(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    $(`#tab-${btn.dataset.tab}`).classList.add("active");
  });
});

async function loadHealth() {
  const h = await api("/api/health");
  const el = $("#health");
  const keys = h.provider.keys_present;
  el.textContent = `DRY_RUN=${h.dry_run} · ${h.provider.provider} keys=${keys ? "yes" : "no"}`;
  el.className = "status " + (h.dry_run || !keys ? "warn" : "ok");
}

async function renderBrands() {
  const data = await api("/api/brands");
  const root = $("#tab-brands");
  root.innerHTML = `<h2>Brand registry</h2><p class="lead">Umbrella: <strong>${escapeHtml(data.umbrella_external)}</strong> · Wall: ${escapeHtml(data.wall)}</p><div class="grid" id="brand-grid"></div>`;
  const grid = $("#brand-grid");
  for (const b of data.brands) {
    const badge =
      b.entity_type === "law_firm" ? "law" :
      b.status === "proposed_skin" ? "proposed" :
      b.status === "use_carefully" ? "careful" : "";
    grid.innerHTML += `<article class="card">
      <h3>${escapeHtml(b.display_name)}</h3>
      <div class="meta">
        <span class="badge ${badge}">${escapeHtml(b.status)}</span>
        <span class="badge">${escapeHtml(b.entity_type)}</span>
        <div><code>${escapeHtml(b.id)}</code> · ${escapeHtml(b.domain)}</div>
        <div>From: ${escapeHtml(b.from_email)}</div>
        <div>Voice: ${escapeHtml(b.voice)}</div>
        <div>Journeys: ${(b.journey_ownership || []).map(escapeHtml).join(", ")}</div>
        <div>${escapeHtml(b.notes || "")}</div>
      </div>
    </article>`;
  }
}

async function renderCalendar() {
  const data = await api("/api/calendar");
  const root = $("#tab-calendar");
  const journeys = Object.keys(data.journeys).sort((a, b) => {
    const rank = (j) => j.startsWith("nurture-") ? 0 : j === "nurture" ? 1 : 2;
    return rank(a) - rank(b) || a.localeCompare(b);
  });
  root.innerHTML = `<h2>Sequence calendar</h2>
    <p class="lead">10-month nurture + side tracks. Offsets in days from enrollment.</p>
    <div class="journey-tabs" id="jtabs"></div>
    <div class="card" style="overflow:auto"><table><thead><tr>
      <th>Day</th><th>Touch</th><th>Brand</th><th>Subject</th><th>Content</th>
    </tr></thead><tbody id="cal-body"></tbody></table></div>`;
  const jtabs = $("#jtabs");
  let current = "nurture";
  function paint(jid) {
    current = jid;
    $$("#jtabs button").forEach((b) => b.classList.toggle("active", b.dataset.j === jid));
    const body = $("#cal-body");
    body.innerHTML = "";
    for (const t of data.journeys[jid].touches) {
      const bn = t.brand ? t.brand.display_name : t.brand_id;
      body.innerHTML += `<tr>
        <td><code>D+${t.offset_days}</code></td>
        <td><code>${escapeHtml(t.id)}</code></td>
        <td>${escapeHtml(bn)}</td>
        <td>${escapeHtml(t.subject)}</td>
        <td><code>${escapeHtml(t.content_path)}</code></td>
      </tr>`;
    }
  }
  journeys.forEach((j) => {
    const b = document.createElement("button");
    b.className = "ghost";
    b.dataset.j = j;
    b.textContent = `${j} (${data.journeys[j].touches.length})`;
    b.onclick = () => paint(j);
    jtabs.appendChild(b);
  });
  paint(current);
}

function renderImport() {
  const root = $("#tab-import");
  root.innerHTML = `<h2>CSV contact import</h2>
    <p class="lead">Columns match <code>delivery/import-schema.csv</code>. Seed loads 5 fake contacts.</p>
    <div class="row">
      <div><button class="primary" id="btn-seed">Load seed fake contacts</button>
      <button class="ghost" id="btn-reload-contacts">Refresh list</button></div>
    </div>
    <label>Paste CSV</label>
    <textarea id="csv-text" placeholder="email,first_name,..."></textarea>
    <button class="primary" id="btn-import">Import CSV</button>
    <div id="import-msg"></div>
    <div class="card" style="margin-top:1rem;overflow:auto"><table>
      <thead><tr><th>Email</th><th>Name</th><th>Business</th><th>Segment</th><th>Journey</th></tr></thead>
      <tbody id="contact-body"></tbody>
    </table></div>`;
  $("#btn-seed").onclick = async () => {
    try {
      const r = await api("/api/contacts/seed", { method: "POST", body: "{}" });
      msg($("#import-msg"), `Seeded/updated · added ${r.added}, updated ${r.updated}, total ${r.total}`, "ok");
      loadContactsTable();
    } catch (e) { msg($("#import-msg"), e.message, "err"); }
  };
  $("#btn-import").onclick = async () => {
    try {
      const r = await api("/api/contacts/import", {
        method: "POST",
        body: JSON.stringify({ csv_text: $("#csv-text").value }),
      });
      msg($("#import-msg"), `Imported · added ${r.added}, updated ${r.updated}, total ${r.total}`, "ok");
      loadContactsTable();
    } catch (e) { msg($("#import-msg"), e.message, "err"); }
  };
  $("#btn-reload-contacts").onclick = loadContactsTable;
  loadContactsTable();
}

async function loadContactsTable() {
  const data = await api("/api/contacts");
  const body = $("#contact-body");
  if (!body) return;
  body.innerHTML = data.contacts.map((c) => `<tr>
    <td>${escapeHtml(c.email)}</td>
    <td>${escapeHtml(c.first_name)} ${escapeHtml(c.last_name || "")}</td>
    <td>${escapeHtml(c.business_name || "")}</td>
    <td>${escapeHtml(c.segment || "")}</td>
    <td>${escapeHtml(c.journey || "")}</td>
  </tr>`).join("") || `<tr><td colspan="5">No contacts yet</td></tr>`;
}

function renderEnroll() {
  const root = $("#tab-enroll");
  root.innerHTML = `<h2>Enroll test cohort</h2>
    <p class="lead">Attaches contacts to a journey. Suppressed emails are skipped.</p>
    <div class="row">
      <div><label>Journey</label>
        <select id="enroll-journey">
          <option value="nurture">nurture</option>
          <option value="client-edu">client-edu</option>
          <option value="reengage">reengage</option>
          <option value="partner">partner</option>
        </select></div>
      <div><label>Cohort name</label><input id="enroll-cohort" value="test-week" /></div>
      <div><label>Or segment</label>
        <select id="enroll-segment">
          <option value="">(use emails below)</option>
          <option>leads_open</option>
          <option>leads_stale_90</option>
          <option>clients_active</option>
          <option>partners_iso</option>
        </select></div>
    </div>
    <label>Emails (comma or newline)</label>
    <textarea id="enroll-emails" placeholder="alex.merchant@example.com"></textarea>
    <button class="primary" id="btn-enroll">Enroll</button>
    <div id="enroll-msg"></div>
    <div class="card" style="margin-top:1rem;overflow:auto"><table>
      <thead><tr><th>Cohort</th><th>Email</th><th>Journey</th><th>Enrolled</th></tr></thead>
      <tbody id="enroll-body"></tbody>
    </table></div>`;
  $("#btn-enroll").onclick = async () => {
    const emails = $("#enroll-emails").value.split(/[\s,]+/).map((s) => s.trim()).filter(Boolean);
    try {
      const r = await api("/api/enroll", {
        method: "POST",
        body: JSON.stringify({
          journey: $("#enroll-journey").value,
          cohort: $("#enroll-cohort").value,
          segment: $("#enroll-segment").value || undefined,
          emails,
        }),
      });
      msg($("#enroll-msg"), `Enrolled ${r.count} contact(s)`, "ok");
      loadEnrollments();
    } catch (e) { msg($("#enroll-msg"), e.message, "err"); }
  };
  loadEnrollments();
}

async function loadEnrollments() {
  const data = await api("/api/enrollments");
  const body = $("#enroll-body");
  if (!body) return;
  body.innerHTML = data.enrollments.map((e) => `<tr>
    <td>${escapeHtml(e.cohort)}</td><td>${escapeHtml(e.email)}</td>
    <td>${escapeHtml(e.journey)}</td><td>${escapeHtml(e.enrolled_at)}</td>
  </tr>`).join("") || `<tr><td colspan="4">None yet</td></tr>`;
}

async function renderPreview() {
  const seq = await api("/api/sequences");
  const root = $("#tab-preview");
  root.innerHTML = `<h2>Dry-run preview</h2>
    <p class="lead">See which email / brand / day fires — no send.</p>
    <div class="row">
      <div><label>Journey</label><select id="prev-journey"></select></div>
      <div><label>Touch</label><select id="prev-touch"></select></div>
      <div><label>Or day offset</label><input id="prev-day" type="number" placeholder="e.g. 12" /></div>
      <div><label>Contact email</label><input id="prev-email" placeholder="alex.merchant@example.com" /></div>
    </div>
    <button class="primary" id="btn-preview">Preview</button>
    <div id="prev-meta" class="msg info" style="display:none"></div>
    <h3 style="margin-top:1rem">Subject</h3>
    <div id="prev-subject" class="card"></div>
    <h3 style="margin-top:1rem">Body</h3>
    <div id="prev-body" class="preview-box"></div>`;
  const jsel = $("#prev-journey");
  Object.keys(seq.journeys).forEach((j) => {
    jsel.innerHTML += `<option value="${j}">${j}</option>`;
  });
  function fillTouches() {
    const j = jsel.value;
    const tsel = $("#prev-touch");
    tsel.innerHTML = seq.journeys[j].touches.map((t) =>
      `<option value="${t.id}">D+${t.offset_days} · ${t.id} · ${escapeHtml(t.subject)}</option>`
    ).join("");
  }
  jsel.onchange = fillTouches;
  fillTouches();
  $("#btn-preview").onclick = async () => {
    const dayVal = $("#prev-day").value;
    const payload = {
      journey: jsel.value,
      touch_id: dayVal === "" ? $("#prev-touch").value : undefined,
      day: dayVal === "" ? undefined : Number(dayVal),
      email: $("#prev-email").value || undefined,
    };
    try {
      const p = await api("/api/preview", { method: "POST", body: JSON.stringify(payload) });
      const meta = $("#prev-meta");
      meta.style.display = "block";
      meta.className = "msg info";
      meta.textContent = `Day D+${p.day_offset} · ${p.brand.display_name} · from ${p.from_name} <${p.from_email}> · suppressed=${p.suppressed}`;
      $("#prev-subject").textContent = p.subject;
      $("#prev-body").textContent = p.body;
    } catch (e) {
      msg($("#prev-meta"), e.message, "err");
      $("#prev-meta").style.display = "block";
    }
  };
}

function renderSend() {
  const root = $("#tab-send");
  root.innerHTML = `<h2>Send test</h2>
    <p class="lead">Gated. Default <code>DRY_RUN=true</code> logs only. Live requires provider keys <em>and</em> <code>DRY_RUN=false</code>.</p>
    <div class="row">
      <div><label>To (your inbox)</label><input id="send-to" placeholder="you@example.com" /></div>
      <div><label>Journey</label>
        <select id="send-journey"><option>nurture</option><option>client-edu</option><option>reengage</option><option>partner</option></select>
      </div>
      <div><label>Touch id (optional)</label><input id="send-touch" placeholder="nurture_m01_e01" /></div>
    </div>
    <label><input type="checkbox" id="send-confirm" /> I confirm this is an intentional test</label>
    <div>
      <button class="primary" id="btn-send">Send / dry-run test</button>
    </div>
    <div id="send-msg"></div>
    <h3 style="margin-top:1rem">Send log</h3>
    <div class="card" style="overflow:auto"><table>
      <thead><tr><th>At</th><th>To</th><th>Subject</th><th>Mode</th></tr></thead>
      <tbody id="send-log-body"></tbody>
    </table></div>`;
  $("#btn-send").onclick = async () => {
    try {
      const r = await api("/api/send-test", {
        method: "POST",
        body: JSON.stringify({
          to: $("#send-to").value,
          journey: $("#send-journey").value,
          touch_id: $("#send-touch").value || undefined,
          confirm: $("#send-confirm").checked,
        }),
      });
      const mode = r.dry_run ? "DRY-RUN (not sent)" : r.sent ? "SENT" : "FAILED";
      msg($("#send-msg"), `${mode} · ${JSON.stringify(r.detail)}`, r.dry_run || r.sent ? "ok" : "err");
      loadSendLog();
    } catch (e) { msg($("#send-msg"), e.message, "err"); }
  };
  loadSendLog();
}

async function loadSendLog() {
  const data = await api("/api/send-log");
  const body = $("#send-log-body");
  if (!body) return;
  body.innerHTML = data.log.slice().reverse().map((e) => `<tr>
    <td>${escapeHtml(e.at)}</td><td>${escapeHtml(e.to)}</td>
    <td>${escapeHtml(e.subject)}</td>
    <td>${e.dry_run ? "dry-run" : "live"}</td>
  </tr>`).join("") || `<tr><td colspan="4">Empty</td></tr>`;
}

function renderSuppress() {
  const root = $("#tab-suppress");
  root.innerHTML = `<h2>Suppression stub</h2>
    <p class="lead">Manual suppress / unsuppress for local tests. Live webhooks will write here later.</p>
    <div class="row">
      <div><label>Email</label><input id="sup-email" /></div>
      <div><label>Reason</label><input id="sup-reason" value="manual" /></div>
    </div>
    <button class="danger" id="btn-sup">Suppress</button>
    <button class="ghost" id="btn-unsup">Remove suppression</button>
    <div id="sup-msg"></div>
    <div class="card" style="margin-top:1rem;overflow:auto"><table>
      <thead><tr><th>Email</th><th>Reason</th><th>At</th></tr></thead>
      <tbody id="sup-body"></tbody>
    </table></div>`;
  $("#btn-sup").onclick = async () => {
    try {
      await api("/api/suppressions", { method: "POST", body: JSON.stringify({ email: $("#sup-email").value, reason: $("#sup-reason").value }) });
      msg($("#sup-msg"), "Suppressed", "ok"); loadSup();
    } catch (e) { msg($("#sup-msg"), e.message, "err"); }
  };
  $("#btn-unsup").onclick = async () => {
    try {
      await api("/api/suppressions/remove", { method: "POST", body: JSON.stringify({ email: $("#sup-email").value }) });
      msg($("#sup-msg"), "Removed", "ok"); loadSup();
    } catch (e) { msg($("#sup-msg"), e.message, "err"); }
  };
  loadSup();
}

async function loadSup() {
  const data = await api("/api/suppressions");
  const body = $("#sup-body");
  if (!body) return;
  body.innerHTML = data.suppressions.map((s) => `<tr>
    <td>${escapeHtml(s.email)}</td><td>${escapeHtml(s.reason)}</td><td>${escapeHtml(s.at)}</td>
  </tr>`).join("") || `<tr><td colspan="3">None</td></tr>`;
}

async function boot() {
  await loadHealth();
  await renderBrands();
  await renderCalendar();
  renderImport();
  renderEnroll();
  await renderPreview();
  renderSend();
  renderSuppress();
}
boot().catch((e) => {
  $("#health").textContent = "API error: " + e.message;
  $("#health").className = "status warn";
});
