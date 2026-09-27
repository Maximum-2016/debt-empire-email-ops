# Debt Empire Email Ops

**Wall:** MGP only — never FM  
**External brand:** prefer **"Debt Empire"** over "MGP" in merchant-facing copy  
**Owner:** Anthony Nocera (GitHub: Maximum-2016)  
**Provider plan:** **Mailgun-first** go-live · Amazon SES later (parallel adapter)  
**Default:** `DRY_RUN=true` — no live sends unless keys exist **and** `DRY_RUN=false`

This repo is the public publish pack for the Debt Empire multi-brand email nurture system (content + delivery design + ops UI). **API keys are never committed.** Live Mailgun/SES sends require secrets set in your host environment only.

---

## Quick links

| Surface | How |
|---------|-----|
| **Static demo (GitHub Pages)** | Read-only UI — brands + sequence calendar from snapped JSON (no Python) |
| **Local / deployable UI** | `cd ui && DRY_RUN=true python3 server.py` → binds `0.0.0.0`, honors `PORT` |
| **Docker** | `docker build -t debt-empire-email-ops . && docker run -p 8765:8765 debt-empire-email-ops` |

---

## Walls (hard rules)

| Rule | Detail |
|------|--------|
| Wall | **MGP only.** Do not touch FM vault, FM brands, or Funding Metrics surfaces. |
| External wording | Prefer **"Debt Empire"** externally. Use "MGP" only in internal ops docs. |
| Secrets | No API keys, DNS secrets, 2FA codes, or list PII in this repo. Placeholders only. |
| Sends | Default is dry-run. Live send needs provider keys **and** `DRY_RUN=false` **and** UI `confirm:true`. |

---

## Folder map

```
debt-empire-email-ops/
├── README.md                 ← you are here
├── ARCHITECTURE.md
├── BRAND_KIT.md
├── CALENDAR-10-MONTH.md
├── CALENDAR-FINTRILO.md
├── NEXT-STEPS.md
├── TEST-WEEK.md
├── Dockerfile / Procfile     ← Render / Railway / Fly
├── docs/                     ← GitHub Pages static demo (ui/public snapshot)
├── content/                  ← nurture, client-edu, reengage, partner, fintrilo, skins
├── delivery/
│   ├── PHASES.md             ← Mailgun-first → SES-later
│   ├── brand-registry.json
│   ├── sequences.json
│   └── adapters/
└── ui/
    ├── server.py             ← stdlib HTTP API + static file server
    ├── public/               ← SPA (falls back to public/data/*.json if /api fails)
    └── seed/fake-contacts.csv
```

---

## Run locally

```bash
cd ui
DRY_RUN=true EMAIL_UI_HOST=0.0.0.0 python3 server.py
```

Open **http://127.0.0.1:8765/** (or the `PORT` your host assigns).

Env knobs: `PORT` / `EMAIL_UI_PORT`, `EMAIL_UI_HOST` (default `0.0.0.0`), `EMAIL_PROVIDER` (`mailgun`|`ses`), `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, AWS/SES vars, `BOOKING_URL`, `UNSUB_URL`, `TEST_FROM_EMAIL`.

**Never put those keys in git.** Set them on Render/Railway/Fly (or your shell) only.

---

## Deploy (Render / Railway / Fly)

- Binds `0.0.0.0` and reads `PORT` automatically.
- `Procfile`: `web: cd ui && DRY_RUN=true python3 server.py`
- Or build the included `Dockerfile`.
- Keep `DRY_RUN=true` until you intentionally go live with Mailgun keys.

---

## Static GitHub Pages demo

The `docs/` folder is a copy of `ui/public` plus snapped `data/brands.json`, `sequences.json`, `calendar.json`.  
`app.js` tries `/api/*` first; if that fails (as on Pages), it loads the static JSON — **read-only** brands + calendar. Import / enroll / send need the Python server.

Enable Pages: **Settings → Pages → Source: Deploy from a branch → `main` / `/docs`**.

---

## Journeys

| Journey | Audience | Cadence |
|---------|----------|---------|
| `nurture` | Leads | ~2–4 / month over 10 months |
| `client-edu` | Enrolled clients | 6 emails over ~6–8 weeks |
| `reengage` | Cold / stale | 5 emails over ~3–4 weeks |
| `partner` | ISOs / referral partners | 5 emails over ~5–6 weeks |
| `fintrilo` | SMB + ISO overlap | 8 emails over ~5 weeks |
| `new-skins-batch2` | Pilot proposed skins | 15 emails over ~26 days |

---

## Status

Design + content pack + ops sandbox UI. **No live sends from this repo.**  
See `delivery/PHASES.md` and `NEXT-STEPS.md` before go-live.

*Debt Empire email pack · MGP wall · Mailgun-first / SES-later · DRY_RUN default*
