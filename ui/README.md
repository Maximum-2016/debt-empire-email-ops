# Debt Empire Email Ops UI

Lightweight local console (stdlib Python + static HTML/JS). MGP wall.

## Start

```bash
cd /workspace/ai-hub/vault/mgp/email-empire/ui
DRY_RUN=true python3 server.py
```

Open **http://127.0.0.1:8765/**

Optional env: `EMAIL_UI_HOST`, `EMAIL_UI_PORT` (default `8765`), `EMAIL_PROVIDER`, `MAILGUN_*`, AWS/SES vars, `TEST_FROM_EMAIL`, `BOOKING_URL`.

## Safety

- `DRY_RUN` defaults true
- Live send requires keys **and** `DRY_RUN=false` **and** `confirm:true`
- See `ATLAS_PLUGIN.md` for API contract · `../TEST-WEEK.md` for the week plan
