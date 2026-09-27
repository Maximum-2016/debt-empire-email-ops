# Architecture — Debt Empire Email System

**Wall:** MGP · **External name:** Debt Empire  
**Delivery:** Mailgun-first + Amazon SES later + bots (not Instantly)  
**Status:** Design skeleton — adapters documented, no secrets, no live sends
**Provider plan:** Mailgun is the Phase 1–2 production primary; SES is introduced in Phase 3 and can become the Phase 4 primary with Mailgun backup.

---

## 1. Goals

1. **Primary:** Lead nurture → booked discovery / enrollment calls.
2. **Same stack capacities:** client education/retention, cold/stale re-engage, partner/referral nurture.
3. **Multi-brand rotation + per-brand 10-month journeys** with contact **cycling until conversion**, then hard exit to client-edu for the winning brand only.
4. **Flexible list ingress:** Salesforce + CSV + form webhooks.
5. **Compliant US + CA** (CAN-SPAM + CASL) with hard suppression and easy STOP.

---

## 2. High-level flow

```
┌─────────────┐  ┌──────────┐  ┌──────────────┐
│ Salesforce  │  │ CSV file │  │ Form webhook │
└──────┬──────┘  └────┬─────┘  └──────┬───────┘
       │              │               │
       └──────────────┼───────────────┘
                      ▼
              ┌───────────────┐
              │  List / CRM   │  normalize → Contact 360
              │  (ATLAS)      │  consent · segments · brand affinity
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │  Email Desk   │  sequences · schedule · rail-guard
              │  (under ATLAS)│  brand identity · kill switch · caps
              └───────┬───────┘
                      ▼
         ┌────────────┴────────────┐
         ▼                         ▼
┌─────────────────┐      ┌─────────────────┐
│ Mailgun adapter │  OR  │  SES adapter    │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └────────────┬───────────┘
                      ▼
              Merchant inbox
                      │
         bounce / complaint / open / click / unsubscribe
                      ▼
              Webhooks → suppression + SF event sync
```

**Dual-adapter rule:** One primary provider at a time for production sends. Mailgun is the initial primary; SES is staged in Phase 3 and is eligible for primary only after the Phase 4 cutover gate. The other provider can be staged for failover. Never duplicate a touch to the same recipient. Adapters share the same send payload shape (`brand_id`, `to`, `subject`, `html`, `text`, `tags`, `utm`, `sequence_id`, `touch_id`).

---

## 3. Delivery adapters

### 3.1 Shared send contract

```json
{
  "brand_id": "bds",
  "from_email": "maria@mail.businessdebtsolutions.com",
  "from_name": "Maria at Business Debt Solutions",
  "reply_to": "support@businessdebtsolutions.com",
  "to": "{{email}}",
  "subject": "...",
  "text": "...",
  "html": "...",
  "tags": ["nurture", "m03", "e02"],
  "headers": {
    "List-Unsubscribe": "<mailto:unsub@...>, <https://.../u/{{token}}>",
    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
  },
  "metadata": {
    "contact_id": "...",
    "sequence_id": "nurture_v1",
    "touch_id": "nurture_m03_e02",
    "utm": "utm_source=email&utm_medium=nurture&utm_campaign=de_m03&utm_content=bds_e02"
  }
}
```

### 3.2 Mailgun

- One Mailgun account (or subaccounts) with **per-brand sending domains**.
- DNS: SPF, DKIM, DMARC on each from-domain (placeholders until Anthony provides).
- Events API / webhooks: delivered, opened, clicked, unsubscribed, complained, bounced, failed.
- Setup checklist: `delivery/adapters/mailgun.md`.

### 3.3 Amazon SES

- SES in a dedicated AWS account (or isolated IAM role) with **configuration sets per brand**.
- SNS → webhook endpoint for bounce / complaint / delivery.
- Easy DKIM + custom MAIL FROM domains per brand.
- Setup checklist: `delivery/adapters/ses.md`.

### 3.4 Choice criteria (open decision)

| Factor | Lean Mailgun | Lean SES |
|--------|--------------|----------|
| Speed to first send | Faster UI / simpler DNS UX | Slightly more AWS plumbing |
| Cost at volume | Competitive mid | Often cheaper at high volume |
| Analytics UI | Strong built-in | Needs our dashboards / CloudWatch |
| Existing AWS | — | Better if already deep in AWS |
| ATLAS Labs today | SMTP / Resend stubs exist; either adapter is new work | Same |

Provider decision: use Mailgun for the Wednesday test and initial multi-domain go-live; introduce SES in parallel later and cut over only after the gates in `delivery/PHASES.md`. Record approval and rollback ownership in `NEXT-STEPS.md`.

---

Rollout details and the provider cutover checklist: `delivery/PHASES.md`.

## 4. Brand registry

Source of truth for runtime: `delivery/brand-registry.json`.

Each brand entry includes:

| Field | Purpose |
|-------|---------|
| `id` | Stable slug (`dag`, `bds`, `bdn`, …) |
| `display_name` | External name |
| `wall` | Always `MGP` |
| `entity_type` | `law_firm` \| `settlement_llc` \| `media` \| `proposed_skin` |
| `from_domain` | Placeholder domain |
| `from_name_pattern` | e.g. `{{first}} at Business Debt Solutions` |
| `reply_to` | Placeholder |
| `brand_url` | Site / LP base |
| `booking_url_key` | Which `{{booking_url}}` variant |
| `legal_disclaimer_key` | Law vs non-law footer block |
| `journey_ownership` | Which journeys this brand may send |
| `voice` | Short voice tag |
| `status` | `active_existing` \| `proposed_skin` \| `use_carefully` |

**Rotation policy:** Nurture sequence assigns brands per touch in `sequences.json` so consecutive emails rarely share the same from-domain. DAG reserved for legal-crisis education and formal authority touches — not every soft CTA.

---

## 5. Lists, segments, suppression

### 5.1 Ingress

| Source | Path | Notes |
|--------|------|-------|
| Salesforce | Sync sketch below | Primary CRM of record for enrolled + many leads |
| CSV | `import-schema.csv` | Bulk loads, purchased/partner lists (consent required) |
| Form webhooks | ATLAS Universal Intake | LP / quiz / booking abandoned |

### 5.2 Core segments

| Segment | Rule (sketch) | Default journey |
|---------|---------------|-----------------|
| `leads_open` | Not enrolled, has email consent, not suppressed | `nurture` |
| `leads_stale_90` | No meaningful activity ≥90d, still open | `reengage` |
| `clients_active` | Enrolled / paying / in settlement | `client-edu` |
| `partners_iso` | Partner/ISO flag | `partner` |
| `legal_tripwire` | Suit / levy / freeze signals | Prefer DAG content or pause → human |
| `suppressed` | Unsub / bounce / complaint / DND / Closed Deal | **Never send** |

### 5.3 Suppression (hard)

Never send if any of:

- Unsubscribe / STOP recorded for email channel
- Hard bounce
- Spam complaint
- ATLAS DND or Closed Deal hard-stop
- Missing or withdrawn consent (CASL-sensitive)
- Global kill switch on
- Brand identity missing (`missing_brand_identity`)

One-click List-Unsubscribe + plain-language STOP line in **every** footer.

---

## 6. Bounce / complaint webhooks

```
Provider event → Email Desk webhook →
  1. Idempotent event store
  2. Update Contact 360 (bounce_class, complaint_at, unsub_at)
  3. Add to suppression list
  4. Mirror event to Salesforce (custom object or Task / CampaignMember status)
  5. Alert ops if complaint rate or hard-bounce rate exceeds threshold
```

**Threshold sketch (tune later):** pause brand domain if complaint rate > 0.1% rolling 7d or hard bounce > 2% on a blast cohort.

---

## 7. Bot ownership — propose Email Desk under ATLAS

### Recommendation

**Create an Email Desk** as a fleet desk under **ATLAS** coordination (same pattern as SEO & AEO Desk / ISO Partner Desk). Do **not** put blast logic inside Telnyx Desk (voice/SMS) or HELIX CS (phone retention).

| Role | Owner |
|------|-------|
| Sequence scheduling, brand rotation, dry-run | **Email Desk** |
| Consent, Contact 360, rail-guard, kill switch | **ATLAS core** |
| Voice / SMS | Telnyx Desk / Voice Drop rail (separate) |
| Client phone retention | HELIX (out of scope for email pack) |
| Counsel gates on new copy | Human counsel + Anthony |
| Portfolio metrics | JARVIS (MGP HUD) — email KPIs can feed later |

Detail: `delivery/bot-ops.md`.

### Why not “just ATLAS Labs SMTP”?

Labs already has email dry-run / SMTP / Resend stubs. Production nurture needs: multi-brand identities, sequence engine, suppression webhooks, SF sync, warm-up — that is a desk + rail, not a lab button.

---

## 8. Salesforce sync sketch

```
SF Lead / Contact / Account
  ↔ ATLAS Contact 360 (email, consent, brand_affinity, journey_state)

Outbound (ATLAS → SF):
  - Email Sent / Opened / Clicked / Unsubscribed / Bounced (Campaign or custom Email_Event__c)
  - Journey stage (e.g. Nurture_M03)
  - Booked call (when booking webhook fires)

Inbound (SF → ATLAS):
  - New / updated leads with email + opt-in fields
  - Status changes: Enrolled → move to client-edu; Disqualified → suppress or stop nurture
  - Owner / ISO partner fields for partner track
```

**Idempotency:** `(provider_message_id)` and `(contact_id, touch_id)` unique constraints.

Level Set Partners is **SF-linked** — use carefully; prefer it for partner-adjacent or ops-aligned touches, not heavy consumer blast until Anthony clarifies positioning.

---

## 9. Compliance notes — CAN-SPAM (US) + CASL (CA)

### CAN-SPAM (US commercial email)

- Accurate from-name / from-domain (no spoofed “friend” headers).
- Non-deceptive subject lines.
- Clear identification as commercial where required; physical postal address in footer (per brand or Debt Empire HQ placeholder).
- Working unsubscribe; honor within 10 business days (we honor immediately).
- Monitor vendors (our adapters = we are the sender of record for compliance ops).

### CASL (Canada)

- Generally need **express consent** (or valid implied in narrow cases) before CEMs.
- Identify sender; provide unsubscribe.
- Keep consent records (who, when, how, what was said).
- Segment `country=CA` (or unknown) with stricter consent checks before send.

### Content red lines (Debt Empire / MGP)

- No guaranteed settlement outcomes or “erase your debt” claims.
- No fake statistics or invented case results.
- No implying a non-law brand is a law firm.
- DAG emails: attorney advertising disclaimers as required by PA / applicable rules.
- No stop-pay / “just blank the ACH” instructions in automated email.
- Never dual-brand DAG + settlement LLC as one entity.

Footers always include: physical address placeholder, STOP/unsubscribe, brand-appropriate legal disclaimer.

---

## 10. Rate limits & warm-up plan

### Warm-up (per new from-domain)

| Week | Daily cap (sketch) | Notes |
|------|--------------------|-------|
| 1 | 20–50 | Highest-engagement contacts only |
| 2 | 50–150 | Expand openers |
| 3 | 150–400 | Introduce 2nd brand domain if ready |
| 4 | 400–1,000 | Monitor bounces/complaints |
| 5+ | Scale toward list size | Stay under complaint/bounce thresholds |

Warm **each** brand domain separately. Do not point a cold domain at the full nurture list on day one.

### Steady-state rate limits (sketch)

- Per brand domain: start ~500–2,000/day after warm-up; raise with reputation.
- Per contact: **kickoff** every other day for 14 days (D0–D12), then ~2 / month months 2–10 on the *current* brand; never two brands same calendar day.
- Global kill switch + weekly send caps in rail-guard (ATLAS pattern).

---

## 11. Tokens used in content

| Token | Meaning |
|-------|---------|
| `{{first_name}}` | Contact first name (fallback “there”) |
| `{{business_name}}` | Merchant DBA / legal name |
| `{{booking_url}}` | Brand-appropriate booking link |
| `{{brand_url}}` | Brand site / LP |
| `{{unsub_url}}` | One-click unsubscribe |
| `{{postal_address}}` | CAN-SPAM address block |
| `{{brand_disclaimer}}` | Law vs non-law disclaimer block |

UTM pattern:  
`utm_source=email&utm_medium={{journey}}&utm_campaign=de_{{month_or_track}}&utm_content={{brand}}_{{touch}}`

---


## 11b. Per-brand journeys + contact brand cycle (until conversion)

Primary nurture is no longer only the shared rotating `nurture` journey. Each active brand (except **MDA — dead**) has:

- Journey id: `nurture-<brandId>`
- Content: `content/nurture-by-brand/<brandId>/month-01…10/`
- Cadence: **kickoff** D0, D2, D4, D6, D8, D10, D12 (7 emails), then **months 2–10** at 2 emails/month → **25 emails/brand**
- **Sequence calendar (source of truth):** `delivery/calendars/<brandId>.json` (index: `delivery/calendars/index.json` · map: `delivery/brand-calendars.json`)
- **Campaign generation:** edit the brand calendar, then `POST /api/campaigns/generate` `{ "brand_id" }` (or `scripts/generate_campaign_from_calendar.py`) → builds/updates `nurture-<brandId>` in `sequences.json` + content stubs if missing
- Human-readable calendar: `CALENDAR-BY-BRAND.md` · cycle machine config: `delivery/brand-cycle.json` + `sequences.json` → `brand_cycle`

### Cycle order

Contacts are **cycled through brand campaigns** — not locked to one brand forever:

`mrd → abr → bdn → ccc → slc → aab → spa → bds → mcb → lrl → dag → fintrilo → lsp → icd`

(Ops may start mid-order via `cycle_index`. **mda excluded.**)

### Rotation rules

| Rule | Detail |
|------|--------|
| Same-day collision | **Forbidden** — max one send per email per calendar day across all brands |
| Cooldown on switch | **3 days** after last touch of brand A before brand B kickoff |
| When to rotate | Journey complete, **or** kickoff done + 14 idle days (configurable) |
| Shared `nurture` | Kept as optional multi-brand rotation; per-brand journeys are primary |

### Conversion exit (hard stop)

Triggers on contact: `booked_call` · `enrolled` · `convert_flag` (explicit).

On conversion for email **E** under winning brand **W**:

1. Set all other `nurture-*` enrollments for **E** → `status: stopped_converted`.
2. Do **not** start the next brand in the cycle.
3. Hand **E** to **`client-edu`** (post-convert track) attributed to **W** (or brand-appropriate client-edu content).
4. Global unsubscribe still stops everything.

Demo/API: `POST /api/enroll` with `journey: "brand-cycle"` starts cycle; `POST /api/convert` with `{email, winning_brand, trigger}` applies exit; `POST /api/campaigns/generate` `{brand_id}` rebuilds the nurture journey from that brand's calendar. See `ui/ATLAS_PLUGIN.md`.

## 12. What is intentionally out of scope

- Instantly or any cold-email SaaS “unlimited inbox” product
- FM / Funding Metrics brands
- Live sends from this vault pack
- Real EIN / entity filings for proposed skins
- SMS/voice copy (separate rails)

---

*Architecture v1.4 · 2026-09-27 ET · MGP wall · calendar-per-brand → generate campaign*
