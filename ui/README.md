# Debt Empire Email Ops UI

Lightweight console (stdlib Python + static HTML/JS). **MGP wall.**

## Start

```bash
cd ui
DRY_RUN=true EMAIL_UI_HOST=0.0.0.0 python3 server.py
```

Open **http://127.0.0.1:8765/** (or `$PORT`).

Deploy hosts (Render/Railway/Fly) inject `PORT`; the server honors it. Default bind is `0.0.0.0`.

Optional env: `EMAIL_UI_HOST`, `PORT` / `EMAIL_UI_PORT`, `EMAIL_PROVIDER`, `MAILGUN_*`, AWS/SES vars, `TEST_FROM_EMAIL`, `BOOKING_URL`.

## Safety

- `DRY_RUN` defaults **true**
- Live send requires keys **and** `DRY_RUN=false` **and** `confirm:true`
- See `ATLAS_PLUGIN.md` · `../TEST-WEEK.md` · `../delivery/PHASES.md`

## Static demo

`public/data/*.json` powers GitHub Pages when `/api/*` is unreachable (`app.js` fallback).
