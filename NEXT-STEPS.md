# Next Steps — What Anthony Must Provide

**Before any live send.** This pack is content + architecture only.

---

## 1. Domains & DNS (per brand you activate)

For each sending brand:

- [ ] Confirm root domain ownership / access
- [ ] Choose subdomain for mail (suggested: `mail.<branddomain>`)
- [ ] Add SPF, DKIM, DMARC when provider is chosen
- [ ] Confirm public web URL for `{{brand_url}}`
- [ ] Confirm or create booking link(s) for `{{booking_url}}`
- [ ] Physical postal address for CAN-SPAM footers (per entity or HQ)

**New skins** (Merchant Relief Desk, Cashflow Clarity Co., Settlement Path Advisors, Ledger Reset Lab):  
Decide adopt / rename / drop. If adopt: register domains (or map to existing), decide DBA vs redirect-only skin. **Do not treat vault names as filed entities.**

---

## 2. Provider rollout + keys (secure form later)

**Preference:** Mailgun-first for the Wednesday test and initial go-live; Amazon SES later (Phase 3 parallel validation, Phase 4 optional primary with Mailgun backup). See `delivery/PHASES.md`.

Initial primary (Phases 1–2):

- [ ] **Mailgun** — verify one domain for the Wednesday test, then approve multi-domain rollout

Later provider (Phase 3+):

- [ ] **Amazon SES** — provision and validate in parallel; do not cut over before the phase gates

Then (via secure form / secret store — **never paste into vault chat files**):

- [ ] API keys / SMTP creds
- [ ] Webhook signing secrets
- [ ] AWS account/role if SES
- [ ] From-address allowlist per brand

See `delivery/adapters/mailgun.md` and `delivery/adapters/ses.md`.

---

## 3. List & CRM

- [ ] Salesforce export or sync credentials path (ops-owned)
- [ ] Consent field mapping (express/implied, source, timestamp) — critical for CASL
- [ ] CSV of seed leads matching `delivery/import-schema.csv`
- [ ] Suppression list export (unsubs, bounces, DND)
- [ ] Segment rules sign-off (`leads_open`, `clients_active`, `partners_iso`, …)
- [ ] Level Set Partners: clarify consumer vs partner-only use

---

## 4. Booking & tracking

- [ ] Canonical discovery/enrollment booking URL(s) — possibly per brand
- [ ] UTM conventions approved (defaults in ARCHITECTURE.md)
- [ ] Thank-you / booked webhook → ATLAS / SF
- [ ] Optional: calendar seats / round-robin owners

---

## 5. Counsel & compliance

- [ ] Counsel review of DAG templates (attorney advertising)
- [ ] Sign-off on non-law disclaimers
- [ ] CASL process for CA recipients
- [ ] Kill-switch owner + on-call
- [ ] Warm-up cohort selection (engaged contacts first)

---

## 6. Bot / desk ownership

- [ ] Approve **Email Desk under ATLAS** (recommended) vs alternate
- [ ] Rail-guard caps (daily/weekly per brand)
- [ ] Who may press “go live” (Anthony only initially recommended)

---

## 7. Open product decisions (summary)

1. Approve the Mailgun-first / SES-later rollout and Phase 4 cutover owner  
2. Which proposed skins to actually stand up (domains)  
3. Level Set Partners consumer policy  
4. Single global booking link vs per-brand links  
5. Postal address(es) per legal entity  
6. Whether umbrella “Debt Empire network” line is allowed in footers  

---

*No sends until the above are satisfied and Anthony says yes.*
