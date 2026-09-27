# ATLAS Plugin Contract — Debt Empire Email UI

**Wall:** MGP / Debt Empire only · **Never FM** · **MDA is dead**  
**Umbrella:** Debt Empire  
**Arm:** `email-marketing` · **Contract version:** 2.0  
**Purpose:** Local ops UI + REST JSON API that ATLAS Email Desk mounts as the Email arm.  
**Provider plan:** Mailgun-first for Phase 1–2 go-live; SES is a Phase 3+ option and may become primary only after the documented cutover gate, with Mailgun backup.

Base URL (local): `http://127.0.0.1:8765`  
Hosted: Render / Railway (when deployed) — ATLAS must call a **running** server.  
**GitHub Pages demo is read-only** — brands/calendars only; no enroll/pause/convert.

---

## Auth (local)

None (localhost sandbox). ATLAS production must wrap with `atlas_session` / bot Bearer + rail-guard.

---

## ATLAS Email Desk action map

| ATLAS action | Meaning | HTTP |
|--------------|---------|------|
| `email.enroll` | Enroll contact into a brand journey or `brand-cycle` | `POST /api/enroll` or `POST /api/atlas/email/enroll` |
| `email.pause` | Pause active enrollment(s) | `POST /api/pause` or `POST /api/atlas/email/pause` |
| `email.resume` | Resume paused enrollment(s) | `POST /api/resume` or `POST /api/atlas/email/resume` |
| `email.convert` | Conversion exit (`booked_call` \| `enrolled` \| `convert_flag`) | `POST /api/convert` or `POST /api/atlas/email/convert` |
| `email.cycle_advance` | Rotate to next brand in cycle | `POST /api/cycle/advance` or `POST /api/atlas/email/cycle/advance` |
| `email.status` | Full ATLAS-facing status for one email | `GET/POST /api/status` or `/api/atlas/email/status` |

Handoff for day-to-day ATLAS use: `docs/ATLAS-EMAIL-ARM.md`.

---

## Endpoints

### Health / discovery

| Method | Path | Response |
|--------|------|----------|
| GET | `/api/health` | `{ ok, wall, umbrella, dry_run, provider, time }` |
| GET | `/api/atlas/email/health` | Same + `{ arm: "email-marketing", version: "2.0" }` |

### Catalog

| Method | Path | Body / query | Response |
|--------|------|--------------|----------|
| GET | `/api/brands` | — | Brand registry JSON |
| GET | `/api/sequences` | — | All journeys + touches |
| GET | `/api/sequences/:journey` | — | One journey |
| GET | `/api/calendar` | — | Journeys with brand objects expanded |
| GET | `/api/calendars` | — | Index of per-brand calendars |
| GET | `/api/calendars/:brandId` | — | One brand calendar (SoT) |
| POST | `/api/campaigns/generate` | `{ brand_id }` or `{ all:true }` | Build/update `nurture-<brand>` + stubs. No live sends. |
| GET | `/api/brand-cycle` | — | Cycle order, rules, conversion_exit |

### Contacts / enrollments

| Method | Path | Body / query | Response |
|--------|------|--------------|----------|
| GET | `/api/contacts` | — | `{ contacts }` |
| POST | `/api/contacts/import` | `{ csv_text }` or `{ rows }` | `{ added, updated, total }` |
| POST | `/api/contacts/seed` | `{}` | Loads seed CSV |
| GET | `/api/enrollments` | — | `{ enrollments }` |

### Email arm ops (Step 2)

| Method | Path | Body / query | Response |
|--------|------|--------------|----------|
| POST | `/api/enroll` | `{ emails?, segment?, journey, cohort?, start_day_offset?, cycle_index? }` | Enroll. `journey:"brand-cycle"` starts per-brand cycle. |
| POST | `/api/pause` | `{ email, journey?, reason? }` | Pause active → `paused` + `paused_at` + optional `pause_reason`. Omit `journey` → all active for email. **404** if none match. |
| POST | `/api/resume` | `{ email, journey? }` | Resume `paused` → `active` + `resumed_at`. Clears `pause_reason`. **403** if suppressed. Does **not** resume `stopped_converted` / `converted` / `rotated`. |
| POST | `/api/convert` | `{ email, winning_brand, trigger: booked_call\|enrolled\|convert_flag, cohort? }` | Stop sibling nurtures; enroll `client-edu`. |
| POST | `/api/cycle/advance` | `{ email, cohort? }` | Rotate to next brand (`rotated` prior). Blocked if converted/suppressed. |
| GET or POST | `/api/status` | `?email=` or `{ email }` | Stable ATLAS status shape (below). |

### ATLAS bridge aliases

Thin mirrors of the same handlers (prefer these when mounting the Email arm):

| Method | Path |
|--------|------|
| POST | `/api/atlas/email/enroll` |
| POST | `/api/atlas/email/pause` |
| POST | `/api/atlas/email/resume` |
| POST | `/api/atlas/email/convert` |
| POST | `/api/atlas/email/cycle/advance` |
| GET or POST | `/api/atlas/email/status` |
| GET | `/api/atlas/email/health` |

Original `/api/*` paths remain fully supported.

### Preview / send / suppressions

| Method | Path | Notes |
|--------|------|-------|
| POST | `/api/preview` | Rendered subject/body — no send |
| POST | `/api/send-test` | Requires `confirm:true`; respects DRY_RUN + keys |
| GET | `/api/send-log` | Local send/dry-run log |
| GET/POST | `/api/suppressions` | List / add |
| POST | `/api/suppressions/remove` | Remove |

---

## `/api/status` response shape (stable)

```json
{
  "email": "alex@example.com",
  "suppressed": false,
  "contact": { },
  "active": [ { "journey": "nurture-mrd", "brand_id": "mrd", "status": "active", "...": "..." } ],
  "paused": [],
  "history": [],
  "brand_cycle": {
    "order": ["mrd", "abr", "..."],
    "current_brand": "mrd",
    "converted": false,
    "winning_brand": null
  },
  "dry_run": true,
  "provider": "mailgun",
  "next_actions": ["enroll", "pause", "convert", "cycle_advance"]
}
```

- `brand_id` is inferred from `nurture-<id>` / `winning_brand` / enrollment fields when missing.
- `history` = non-active terminal rows: `converted` / `rotated` / `stopped_converted`.
- `next_actions` lists only ops that make sense given state (never includes resume of terminal statuses).

---

## Provider selection

`EMAIL_PROVIDER` defaults to `mailgun`. If a UI picker is added, keep **Mailgun** selected by default and label SES **Amazon SES (phase 3+)**. Do not bypass phase gates, dry-run, caps, or Anthony approval.

See `delivery/PHASES.md` and `delivery/adapters/ses.md`.

## Send safety contract

1. `DRY_RUN` defaults **true**.  
2. Live send only if `DRY_RUN=false` **and** provider keys present.  
3. `confirm:true` required on `/api/send-test`.  
4. Suppressed emails → 403 (including resume).  
5. Optional overrides: `TEST_FROM_EMAIL`, `TEST_FROM_NAME`, `BOOKING_URL`, `UNSUB_URL`, `POSTAL_ADDRESS`.

---

## ATLAS absorption

```
ATLAS Email Desk
  ├── brands package     ← brand-registry.json
  ├── sequences engine   ← sequences.json + content/
  ├── intake             ← CSV / SF / webhooks
  ├── rail-guard         ← consent, DND, caps, kill switch
  └── adapters           ← mailgun (primary) | ses (phase 3+)
```

Prefer mounting via `/api/atlas/email/*`. Keep payload shapes stable.

**Pages demo = read-only.** ATLAS must call a running `ui/server.py` (local or hosted).

---

## UI screens ↔ API

| Screen | APIs |
|--------|------|
| Brands | GET `/api/brands`, calendars, POST `/api/campaigns/generate` |
| Sequence calendar | GET `/api/calendar`, `/api/calendars` |
| CSV import | POST `/api/contacts/import`, `/seed` |
| Enroll cohort | POST `/api/enroll` + Pause/Resume buttons → `/api/pause` `/api/resume` |
| Dry-run preview | POST `/api/preview` |
| Send test | POST `/api/send-test` |
| Suppression | GET/POST suppressions |

---

## Brand cycle + conversion exit

- Per-brand **calendars** are SoT: `delivery/calendars/<brandId>.json` → generate `nurture-<brandId>`.
- Meta enroll: `journey: "brand-cycle"` + optional `cycle_index`.
- **No MDA.** Same-day multi-brand send forbidden. 3-day cooldown on switch (ops).
- On convert: siblings → `stopped_converted`; winning brand → `client-edu`.
- Mailgun-first · `DRY_RUN` default · no live sends without keys + `DRY_RUN=false` + confirm.

---

*Contract v2.0 · 2026-09-27 ET · ATLAS Email arm (pause / resume / status / aliases)*
