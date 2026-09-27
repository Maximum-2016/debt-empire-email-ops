# Bot Ops — Email Desk under ATLAS

**Recommendation:** Create an **Email Desk** coordinated by ATLAS (same fleet pattern as SEO & AEO / ISO Partner).  
**Do not** own blast sends from Telnyx Desk (voice/SMS) or HELIX CS.

## Ownership matrix

| Concern | Owner |
|---------|-------|
| Sequence schedule, brand rotation, dry-run preview | Email Desk |
| Contact 360, consent, DND, Closed Deal, kill switch | ATLAS core / rail-guard |
| Provider adapters (Mailgun/SES) | Email Desk rails |
| Voice / SMS | Telnyx / Voice Drop |
| Counsel on new copy | Human + Anthony |
| This local UI | Dev/ops sandbox → later plug into ATLAS |

## Local UI (this pack)
`ui/` is a lightweight Debt Empire ops console for registry, calendar, CSV import, enroll, dry-run preview, gated send-test, suppression stub. Default `DRY_RUN=true`. See `ui/ATLAS_PLUGIN.md` for the REST contract ATLAS can absorb.

## Hard rules
- No send unless env keys exist **and** `DRY_RUN=false`
- Never dual-brand DAG + settlement LLC as one company
- MGP wall only — no FM brands
- Idempotent `(contact_id, touch_id)` 
- Honor STOP / unsub immediately

## Proposed ATLAS routes (future)
- `POST /api/email/enroll`
- `POST /api/email/preview`
- `POST /api/email/send-test` (admin + confirm)
- `GET /api/email/brands`
- `GET /api/email/sequences/:journey`
- Webhooks under `/api/email/webhooks/{mailgun|ses}`
