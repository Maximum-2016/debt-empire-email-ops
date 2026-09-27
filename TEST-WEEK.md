# Test Week Checklist — Debt Empire Email

**Goal:** Anthony can exercise the system **this week**.  
**Default:** dry-run (no DNS required).  
**Live test:** needs one verified domain + API key + `DRY_RUN=false`.  
**Wall:** MGP · never FM · no Instantly

Times below are **ET** (America/New_York).

---

## Pre-flight (Sunday / whenever you start)

- [ ] Open pack: `/workspace/ai-hub/vault/mgp/email-empire/`
- [ ] Skim `README.md`, `BRAND_KIT.md`, `NEXT-STEPS.md`
- [ ] Start UI:
  ```bash
  cd /workspace/ai-hub/vault/mgp/email-empire/ui
  DRY_RUN=true python3 server.py
  ```
- [ ] Browser: **http://127.0.0.1:8765/**
- [ ] Confirm header shows `DRY_RUN=True` and provider keys=no (expected)

---

## Day 1 — Orient (dry-run only)

- [ ] **Brands** tab: confirm **10 brands** (6 existing incl. Fintrilo + 4 proposed)
- [ ] **Sequence calendar**: nurture shows 31 touches; side tracks 6 / 5 / 5; **fintrilo** shows 8
- [ ] **CSV import** → **Load seed fake contacts** (5 fakes)
- [ ] **Dry-run preview**: journey `nurture`, touch `nurture_m01_e01`, email `alex.merchant@example.com`
- [ ] Confirm subject/body tokens render (`{{first_name}}` → Alex, etc.)
- [ ] Preview DAG touch (`nurture_m04_e02` or calendar day ~87) — formal disclaimer present in source

**Pass:** Previews render; no email left the building.

---

## Day 2 — Enroll + suppression

- [ ] **Enroll cohort**: segment `leads_open` → journey `nurture`, cohort `test-week`
- [ ] Enroll `sam.enrolled@example.com` on `client-edu`
- [ ] Enroll `casey.iso@example.com` on `partner`
- [ ] **Suppression**: suppress `jordan.owner@example.com`
- [ ] Try enroll Jordan on `reengage` — should skip / not enroll
- [ ] Preview + send-test toward a suppressed address → expect blocked/403 or skip

**Pass:** Cohort list looks right; suppression sticks.

---

## Day 3 — Full dry-run “send me one test email” path

- [ ] On **Send test** tab:
  - To: **Anthony’s real inbox** (for subject line visibility in log — still dry-run)
  - Journey: `nurture`
  - Touch: `nurture_m01_e01` (or leave default first touch)
  - Check **confirm**
  - Click Send
- [ ] Expect response **DRY-RUN (not sent)** and a send-log row with `[DRY-RUN]` subject prefix
- [ ] Repeat for brands: BDS (`nurture_m01_e04`), DAG (`nurture_m04_e02`), proposed MRD (`nurture_m01_e01`)

**Pass:** Log shows dry-runs only; inbox receives **nothing** (correct).

---

## Day 4 — Provider choice + DNS homework (no blast)

Pick **Mailgun or SES**. For **one** domain you control (even a scratch subdomain):

### If Mailgun
- [ ] Create account / domain `mail.<yourdomain>`
- [ ] Add SPF + DKIM (+ DMARC p=none)
- [ ] Wait until Mailgun shows verified
- [ ] Put keys in **shell env only** (not vault files):
  ```bash
  export EMAIL_PROVIDER=mailgun
  export MAILGUN_API_KEY='…'          # secret form / password manager
  export MAILGUN_DOMAIN='mail.yourdomain.com'
  export TEST_FROM_EMAIL='test@mail.yourdomain.com'
  export TEST_FROM_NAME='Debt Empire Test'
  export DRY_RUN=true                 # keep true until Day 5
  python3 server.py
  ```

### If SES
- [ ] Verify domain (Easy DKIM) in AWS SES
- [ ] Leave sandbox **or** only send to verified emails
- [ ] Export AWS creds / profile; `pip install boto3` if needed
- [ ] `EMAIL_PROVIDER=ses DRY_RUN=true python3 server.py`

**Pass:** `/api/health` shows `keys_present: true` while still `dry_run: true`.

---

## Day 5 — Single live test (optional, gated)

**Only if** Day 4 verified + Anthony explicitly wants live:

```bash
export DRY_RUN=false
# keys still set
python3 server.py
```

- [ ] Send test **to Anthony only**
- [ ] Touch: short nurture email
- [ ] Confirm arrives from verified domain
- [ ] Click List-Unsubscribe / note footer STOP (placeholder URL ok if not wired)
- [ ] Set `DRY_RUN=true` again immediately after

**Fail conditions:** any second recipient, any full cohort, any FM brand, any Instantly.

---


## Optional — Fintrilo dry-run (any day)

Fintrilo is an **existing MGP-adjacent** capacity (not a proposed skin). ESP still undecided — stay on `DRY_RUN=true`.

- [ ] Brands tab: Fintrilo card shows `active_existing` · `merchant_finance` · domain `fintrilo.com`
- [ ] Calendar → journey **fintrilo**: 8 touches (ft_e01 … ft_e08)
- [ ] Dry-run preview: journey `fintrilo`, touch `ft_e01`, any seed contact
- [ ] Spot-check `ft_e04` (Clover) + `ft_e07` (partner/ISO) — confirm non-law disclaimer token
- [ ] Send-test (still dry-run) for `ft_e08` toward Anthony inbox address in log only
- [ ] Confirm **no** live send; subject in send_log prefixed `[DRY-RUN]`

**Pass:** Fintrilo appears in UI brands + sequences; dry-run only.

---
## Day 6–7 — Content spot-check + decisions

- [ ] Skim Month 3 + Month 8 nurture copy for CTA tone
- [ ] Decide which **proposed skins** to actually buy domains for
- [ ] Note Fintrilo uses **existing** fintrilo.com — DNS for `mail.fintrilo.com` still placeholder
- [ ] Decide Mailgun vs SES as primary
- [ ] Supply booking link placeholder → real URL (`BOOKING_URL`)
- [ ] Postal address for footers
- [ ] Counsel glance at one DAG template

---

## Seed contacts (fake)

| Email | Role |
|-------|------|
| alex.merchant@example.com | Lead nurture |
| jordan.owner@example.com | Stale / reengage (use for suppress tests) |
| sam.enrolled@example.com | Client-edu |
| casey.iso@example.com | Partner |
| riley.ca@example.com | CA lead (CASL-sensitive flag in notes) |

Source: `ui/seed/fake-contacts.csv` (from `delivery/import-schema.csv`).

---

## What Anthony needs by Wednesday for a live test

1. **Provider pick:** Mailgun **or** SES  
2. **One verified sending domain** (DNS done)  
3. **API key / AWS creds** via secure channel — not chat vault files  
4. **From-address** on that domain (`TEST_FROM_EMAIL`)  
5. **Anthony inbox** as the only live recipient  
6. Explicit **yes** to set `DRY_RUN=false` for one message  

Nice-to-have by Wednesday: real `BOOKING_URL`, postal address line, which proposed brand (if any) to put on the from-name for the test.

---

*Test-week v1.1 · 2026-09-27 ET · MGP wall · Fintrilo optional dry-run*
