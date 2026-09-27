# ATLAS Email Arm — Handoff

**Wall:** Debt Empire / MGP only · never FM · **MDA is dead**  
**Arm id:** `email-marketing` · **Contract:** `ui/ATLAS_PLUGIN.md` v2.0  
**Repo:** https://github.com/Maximum-2016/debt-empire-email-ops  
**Server:** `ui/server.py` (stdlib) · default `DRY_RUN=true`

---

## Base URL

| Environment | Base URL |
|-------------|----------|
| Local | `http://127.0.0.1:8765` |
| Hosted (Render / Railway) | `https://<DEPLOYED_HOST>` ← replace when live |

**GitHub Pages is read-only.** Do not call enroll/pause/convert against Pages — ATLAS must hit a running Python server.

---

## Action → endpoint

| ATLAS action | Method | Path (prefer alias) | Body / query |
|--------------|--------|---------------------|--------------|
| `email.enroll` | POST | `/api/atlas/email/enroll` | `{ "emails": ["…"], "journey": "brand-cycle"\|"nurture-<id>", "cohort"?: "…" }` |
| `email.pause` | POST | `/api/atlas/email/pause` | `{ "email": "…", "journey"?: "nurture-bds", "reason"?: "…" }` |
| `email.resume` | POST | `/api/atlas/email/resume` | `{ "email": "…", "journey"?: "…" }` |
| `email.convert` | POST | `/api/atlas/email/convert` | `{ "email": "…", "winning_brand": "bds", "trigger": "booked_call"\|"enrolled"\|"convert_flag" }` |
| `email.cycle_advance` | POST | `/api/atlas/email/cycle/advance` | `{ "email": "…" }` |
| `email.status` | GET/POST | `/api/atlas/email/status` | `?email=` or `{ "email": "…" }` |
| health | GET | `/api/atlas/email/health` | — → includes `{ arm, version: "2.0" }` |

Original `/api/*` paths work the same (no alias prefix).

---

## Example curls

### Enroll into brand-cycle

```bash
curl -sS -X POST "$BASE/api/atlas/email/enroll" \
  -H 'Content-Type: application/json' \
  -d '{"emails":["alex.merchant@example.com"],"journey":"brand-cycle","cohort":"atlas-demo"}'
```

### Status

```bash
curl -sS "$BASE/api/atlas/email/status?email=alex.merchant@example.com"
# or
curl -sS -X POST "$BASE/api/atlas/email/status" \
  -H 'Content-Type: application/json' \
  -d '{"email":"alex.merchant@example.com"}'
```

### Pause / resume / convert

```bash
curl -sS -X POST "$BASE/api/atlas/email/pause" \
  -H 'Content-Type: application/json' \
  -d '{"email":"alex.merchant@example.com","reason":"ops hold"}'

curl -sS -X POST "$BASE/api/atlas/email/resume" \
  -H 'Content-Type: application/json' \
  -d '{"email":"alex.merchant@example.com"}'

curl -sS -X POST "$BASE/api/atlas/email/convert" \
  -H 'Content-Type: application/json' \
  -d '{"email":"alex.merchant@example.com","winning_brand":"mrd","trigger":"booked_call"}'
```

---

## Safety rules (always)

1. **DRY_RUN defaults true** — no live Mailgun/SES send without keys **and** `DRY_RUN=false` **and** `confirm:true` on send-test.
2. **Suppressed contacts** → 403 on resume / send; enroll skips them.
3. **No MDA** — refuse generate/convert with `mda`.
4. **Terminal statuses** (`converted`, `stopped_converted`, `rotated`) are never resumed.
5. **Never invent Mailgun keys** or blast from this arm without Anthony approval.
6. Prefer **Debt Empire** wording externally; MGP is internal wall only.

---

## How ATLAS should use this day to day

1. **Health-check** the arm (`GET /api/atlas/email/health`) before desk work.
2. **Status first** for any contact ATLAS is about to touch — read `next_actions`, `active` / `paused`, `brand_cycle`.
3. **Enroll** leads with `journey: "brand-cycle"` (or a specific `nurture-<brand>` when affinity is known).
4. **Pause** on ops holds, DND windows, or manual review; **resume** when clear (not if suppressed).
5. On booked call / enrollment / convert flag → **`email.convert`** with `winning_brand` (stops siblings, starts `client-edu`).
6. If a brand track completes without convert → **`email.cycle_advance`** (marks prior `rotated`, enrolls next brand).
7. Treat Pages / static demo as browse-only; all mutations go to the running server.

Status `next_actions` is the shortlist of safe ops for that contact — ATLAS should not invent actions outside that list without a human override.

---

*Debt Empire Email arm handoff · MGP wall · 2026-09-27 ET*
