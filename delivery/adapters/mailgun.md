# Mailgun Adapter — Setup Checklist

**Wall:** MGP / Debt Empire · **No secrets in vault**

## Prerequisites
- [ ] Mailgun account (US or EU region chosen deliberately)
- [ ] At least one brand sending domain verified (start with one)
- [ ] API key stored in secret manager / env — never in git

## DNS (per brand from-domain)
- [ ] SPF includes Mailgun
- [ ] DKIM records from Mailgun dashboard
- [ ] DMARC policy (start `p=none` while monitoring)
- [ ] Optional custom tracking CNAME

## App config (env placeholders)
```
EMAIL_PROVIDER=mailgun
MAILGUN_API_KEY=           # secret
MAILGUN_DOMAIN=mail.example.com
MAILGUN_BASE_URL=https://api.mailgun.net  # or api.eu.mailgun.net
DRY_RUN=true
```

## Webhooks
- [ ] Subscribe: delivered, opened, clicked, unsubscribed, complained, permanent_fail, temporary_fail
- [ ] Endpoint: Email Desk `/webhooks/mailgun` (HMAC verify)
- [ ] Map events → suppression + SF sync

## Send sketch
`POST /v3/{domain}/messages` with from/to/subject/text/html + `o:tag` + custom vars for touch_id.

## Go-live gate
Warm-up cohort only · DRY_RUN=false · Anthony yes · complaint/bounce monitors on.
