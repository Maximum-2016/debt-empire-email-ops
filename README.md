# Debt Empire Email Marketing System

**Wall:** MGP only — never FM  
**External brand preference:** prefer **"Debt Empire"** over "MGP" in brand-facing copy  
**Owner:** Anthony Nocera  
**Status:** Design + content pack (no live sends)
**Provider plan:** Mailgun-first go-live; Amazon SES later (parallel adapter, then primary with Mailgun backup)  
**Created:** 2026-09-27 ET

---

## What this is

A complete multi-brand email nurture and retention system for the Debt Empire / MGP portfolio. Primary goal is **lead nurture → booked discovery / enrollment calls**. The same delivery stack also runs client education/retention, cold/stale re-engage, and partner/referral nurture — as modes of one system, not separate products.

Delivery is **Mailgun-first** for go-live, with Amazon SES as the later-phase provider; both adapters remain available through ATLAS / Email Desk. **Not Instantly.** Domains and API keys are placeholders until Anthony supplies them.

## Walls (hard rules)

| Rule | Detail |
|------|--------|
| Wall | **MGP only.** Do not touch FM vault, FM brands, or Funding Metrics / Wolf & Cohen surfaces. |
| External wording | Prefer **"Debt Empire"** when speaking to merchants/partners. Use "MGP" / "Maximum Growth Partners" only in internal ops docs. |
| Dual-brand | Never present DAG Law + a settlement LLC as "the same company" in one flight. Rotate brands across touches; warm-transfer legal tripwires to DAG. |
| Secrets | No API keys, DNS secrets, or list PII in this folder. Placeholders only. |
| Sends | This pack is content + architecture. **No emails are sent from these files.** |

## Folder map

```
email-empire/
├── README.md                 ← you are here
├── ARCHITECTURE.md           ← SES/Mailgun, brand registry, suppression, bots, compliance
├── BRAND_KIT.md              ← existing + invented skins, voices, disclaimers
├── CALENDAR-10-MONTH.md      ← Month 1–10 themes, cadence, brand rotation, CTA arc
├── CALENDAR-FINTRILO.md      ← Fintrilo capacity track (parallel)
├── NEXT-STEPS.md             ← what Anthony must provide before go-live
├── content/
│   ├── nurture/              ← shared multi-brand 10-month (kept)
│   ├── nurture-by-brand/     ← per-brand 10-month (25 emails each; primary)
│   ├── client-edu/           ← 6-email enrolled-client / post-convert track
│   ├── reengage/             ← 5-email cold/stale track
│   ├── partner/              ← 5-email ISO/referral track
│   └── fintrilo/             ← Fintrilo capacity (8 emails + RESEARCH.md)
├── CALENDAR-BY-BRAND.md      ← per-brand calendars + cycle / conversion exit
├── scripts/
│   ├── generate_nurture_by_brand.py        ← seeds calendars + content + journeys
│   └── generate_campaign_from_calendar.py  ← calendar → nurture-<brand> (SoT path)
└── delivery/
    ├── PHASES.md              ← Mailgun-first → SES-later rollout and cutover checklist
    ├── brand-registry.json
    ├── brand-cycle.json       ← cycle order + conversion exit machine config
    ├── brand-calendars.json   ← map of brand_id → calendar file
    ├── calendars/             ← **source of truth** per-brand sequence calendars
    │   ├── <brandId>.json
    │   └── index.json
    ├── sequences.json         ← generated nurture-<brandId> journeys + brand_cycle
    ├── import-schema.csv
    ├── bot-ops.md
    └── adapters/
        ├── mailgun.md
        └── ses.md
```

## How to run (when wired)

1. Anthony supplies domains and DNS; follow `delivery/PHASES.md`: Mailgun is the Phase 1–2 primary, SES is introduced in Phase 3, and may become primary in Phase 4 (see `NEXT-STEPS.md`).
2. Ops loads `delivery/brand-registry.json` into ATLAS brand tenancy + Email Desk.
3. Lists land via Salesforce sync, CSV import (`import-schema.csv`), or form webhooks.
4. Edit `delivery/calendars/<brandId>.json` (SoT), then generate the campaign (`POST /api/campaigns/generate` or the script). `sequences.json` journeys + content stubs are **outputs** of the calendar.
5. Email Desk (proposed under ATLAS) owns queue → adapter → send → webhook handling. Rail-guard: consent, suppression, brand identity, kill switch, weekly caps.
6. **Dry-run first.** No blast without counsel + Anthony yes.

Until keys and lists exist, treat this folder as the **source of truth for copy, brand skins, and ops design**.

## Journeys (same system)

| Journey | Audience | Cadence | Primary CTA |
|---------|----------|---------|-------------|
| `nurture-<brandId>` | Leads on one brand skin | Kickoff D0–D12 EOD; then 2/mo months 2–10 (**25**/brand) | Book discovery/enrollment call |
| `brand-cycle` (meta) | Leads cycling brands until convert | Same cadence per brand; 3-day cooldown on switch; **no two brands same day** | Rotate order in `brand-cycle.json` |
| `nurture` | Shared multi-brand (optional) | ~2–4 / month over 10 months | Book discovery/enrollment call |
| `client-edu` | **Post-convert** / enrolled clients | 6 emails over ~6–8 weeks | Portal / check-in / education |
| `reengage` | Cold / stale / unconverted | 5 emails over ~3–4 weeks | Soft re-book or reply |
| `partner` | ISOs / referral partners | 5 emails over ~5–6 weeks | Refer a merchant / partner portal |
| `fintrilo` | SMB + ISO/Biz-Pay overlap (MGP) | 8 emails over ~5 weeks | Liaison Officer connect / funding+payments |
| `new-skins-batch2` | Pilot lists for batch2 proposed skins | 15 emails over ~26 days | Brand-skin education / soft discovery (proposed_only) |

**Conversion exit:** on `booked_call` / `enrolled` / `convert_flag` → stop all other brand nurtures for that email; hand to `client-edu` for the winning brand only. **No MDA.**

## Brand skins (summary)

**Existing (MGP wall):** DAG Law, Business Debt Solutions, Business Debt Ninjas, Level Set Partners (careful / SF-linked), **Fintrilo** (merchant finance / Biz-Pay ISO overlap — not a proposed skin).

**New (proposed skins / DBA candidates — not filed entities):**
- Batch 1: Merchant Relief Desk, Cashflow Clarity Co., Settlement Path Advisors, Ledger Reset Lab.
- Batch 2: Advance Alternatives Brief, ACH Breath Room, ISO Care Desk, Merchant Crisis Brief, Stack Literacy Co. (`content/new-skins-batch2/` · journey `new-skins-batch2`).

Full detail: `BRAND_KIT.md`.

## Related vault / ops

- ATLAS overview: `/workspace/ai-hub/vault/mgp/atlas/`
- Walls: `/workspace/ai-hub/WALLS.md`
- Telnyx notes: `/workspace/ai-hub/vault/mgp/refs/TELNYX.md`
- Portfolio analytics (MGP HUD): `mgp-portfolio-analytics.md`

---

*Debt Empire email pack · MGP wall · calendar-per-brand → generate campaign · no live sends*

## Local UI (ops sandbox)

```bash
cd /workspace/ai-hub/vault/mgp/email-empire/ui
DRY_RUN=true python3 server.py
```

→ **http://127.0.0.1:8765/**  
API contract for ATLAS: `ui/ATLAS_PLUGIN.md` (v2.0 — pause/resume/status + `/api/atlas/email/*`)  
ATLAS Email arm handoff: `docs/ATLAS-EMAIL-ARM.md`  
This-week test plan: `TEST-WEEK.md`


## Public repo / GitHub Pages

This directory is the publish copy pushed to `Maximum-2016/debt-empire-email-ops`.

| Surface | What |
|---------|------|
| **Static demo (GitHub Pages)** | Read-only UI — brands + sequence calendar from snapped JSON (no Python) |
| **Python ops UI** | `ui/server.py` — enroll, preview, dry-run test send (Mailgun-first, `DRY_RUN` default) |

```
docs/                     ← GitHub Pages static demo (ui/public snapshot)
ui/public/data/*.json     ← sequences (incl. nurture-<brand>), brands, calendar + calendars/
delivery/calendars/       ← per-brand sequence calendars (SoT) → generate campaign
delivery/brand-cycle.json ← cycle order + conversion exit
content/nurture-by-brand/ ← 14 brands × 25 emails
```

Enable Pages: **Settings → Pages → Source: Deploy from a branch → `main` / `/docs`**.

Demo URL: https://maximum-2016.github.io/debt-empire-email-ops/

**Conversion exit / brand cycle** documented in `ARCHITECTURE.md` §11b and `CALENDAR-BY-BRAND.md`.
