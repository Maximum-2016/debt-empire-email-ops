# ATLAS Plugin Contract — Debt Empire Email UI

**Wall:** MGP only · **Umbrella:** Debt Empire  
**Purpose:** Local ops UI + REST-ish JSON API that ATLAS Email Desk can absorb later.
**Provider plan:** Mailgun-first for Phase 1–2 go-live; SES is a Phase 3+ option and may become primary only after the documented cutover gate, with Mailgun backup.

Base URL (local): `http://127.0.0.1:8765`

---

## Auth (local)

None (localhost sandbox). ATLAS production must wrap with `atlas_session` / bot Bearer + rail-guard.

---

## Endpoints

| Method | Path | Body / query | Response |
|--------|------|--------------|----------|
| GET | `/api/health` | — | `{ ok, wall, umbrella, dry_run, provider:{provider,keys_present,dry_run}, time }` |
| GET | `/api/brands` | — | Brand registry JSON (`delivery/brand-registry.json`) |
| GET | `/api/sequences` | — | All journeys + touches |
| GET | `/api/sequences/:journey` | — | One journey |
| GET | `/api/calendar` | — | Journeys with brand objects expanded |
| GET | `/api/contacts` | — | `{ contacts: [...] }` |
| POST | `/api/contacts/import` | `{ csv_text }` or `{ rows:[{...}] }` | `{ added, updated, total }` |
| POST | `/api/contacts/seed` | `{}` | Loads `ui/seed/fake-contacts.csv` |
| GET | `/api/enrollments` | — | `{ enrollments }` |

| GET | `/api/brand-cycle` | — | Cycle order, rules, conversion_exit, journeys_present |
| POST | `/api/enroll` | `{ emails?, segment?, journey, cohort?, start_day_offset?, cycle_index? }` | Enroll. Use `journey:"brand-cycle"` to start/continue per-brand cycle (`nurture-<brand>`). |
| POST | `/api/cycle/advance` | `{ email, cohort? }` | Rotate contact to next brand in order (blocked if converted/suppressed). Marks prior nurture as `rotated`. |
| POST | `/api/convert` | `{ email, winning_brand, trigger: booked_call\|enrolled\|convert_flag, cohort? }` | **Conversion exit:** stop all other brand nurtures; enroll `client-edu` for winning brand only. |

| POST | `/api/preview` | `{ journey, touch_id?, day?, email?, first_name?, business_name? }` | Rendered subject/body + brand + day_offset |
| POST | `/api/send-test` | `{ to, journey?, touch_id?, day?, confirm:true, first_name?, business_name? }` | `{ sent, dry_run, detail, payload_meta }` |
| GET | `/api/send-log` | — | Local send/dry-run log |
| GET | `/api/suppressions` | — | `{ suppressions }` |
| POST | `/api/suppressions` | `{ email, reason? }` | Updated list |
| POST | `/api/suppressions/remove` | `{ email }` | Updated list |

---

## Provider selection

The local UI currently has no interactive provider picker. `EMAIL_PROVIDER` defaults to `mailgun` in `ui/server.py`, so Mailgun is the safe default for the Wednesday test and initial go-live. If a picker is added, keep **Mailgun** selected by default and label the SES option **Amazon SES (phase 3+)**; do not allow a UI choice to bypass the phase gates, dry-run, caps, or Anthony approval.

See `delivery/PHASES.md` for the rollout and `delivery/adapters/ses.md` for SES IAM, sandbox, configuration-set, SNS, and cost requirements.

## Send safety contract

1. `DRY_RUN` defaults **true**.  
2. Live send only if `DRY_RUN=false` **and** provider keys present (`MAILGUN_API_KEY`+`MAILGUN_DOMAIN` or SES creds).  
3. `confirm:true` required on `/api/send-test`.  
4. Suppressed emails → 403.  
5. Optional overrides: `TEST_FROM_EMAIL`, `TEST_FROM_NAME`, `BOOKING_URL`, `UNSUB_URL`, `POSTAL_ADDRESS`.

---

## ATLAS absorption sketch

```
ATLAS Email Desk
  ├── brands package     ← brand-registry.json
  ├── sequences engine   ← sequences.json + content/
  ├── intake             ← CSV / SF / webhooks (same columns as import-schema)
  ├── rail-guard         ← consent, DND, caps, kill switch, brand identity
  └── adapters           ← mailgun (primary first) | ses (phase 3+)
```

Map local `/api/*` to `/api/email/*` under ATLAS bridge. Keep payload shapes stable.

---

## UI screens ↔ API

| Screen | APIs |
|--------|------|
| Brands | GET `/api/brands` |
| Sequence calendar | GET `/api/calendar` |
| CSV import | POST `/api/contacts/import`, `/seed` |
| Enroll cohort | POST `/api/enroll` |
| Dry-run preview | POST `/api/preview` |
| Send test | POST `/api/send-test` |
| Suppression | GET/POST suppressions |

---

*Contract v1 · 2026-09-27 ET*


## Brand cycle + conversion exit

- Per-brand journeys: `nurture-<brandId>` (25 touches: kickoff D0–D12, then months 2–10 × 2).
- Meta enroll: `journey: "brand-cycle"` + optional `cycle_index`.
- Order / rules: `delivery/brand-cycle.json` and `sequences.json` → `brand_cycle`.
- **No MDA.** Same-day multi-brand send forbidden. 3-day cooldown on switch (ops).
- On convert: siblings → `stopped_converted`; winning brand → `client-edu`.
- Mailgun-first · `DRY_RUN` default · no live sends without keys + `DRY_RUN=false` + confirm.

