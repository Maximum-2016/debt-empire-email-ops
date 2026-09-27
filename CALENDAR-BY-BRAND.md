# Calendar by Brand — Per-Brand 10-Month Nurture

**Wall:** MGP · **No MDA** · **No FM** · **DRY_RUN default / no live sends from this pack alone**

## Cadence (all brands)

| Phase | Timing | Emails |
|-------|--------|--------|
| Kickoff (Month 1, weeks 1–2) | Every other day: D0, D2, D4, D6, D8, D10, D12 | 7 |
| Months 2–10 | ~2 / month (month_base+5, month_base+18) | 18 |
| **Total per brand** | ~10 months | **25** |

## Brand cycle (until conversion)

Contacts are **not** locked to one brand forever. They cycle:

mrd → abr → bdn → ccc → slc → aab → spa → bds → mcb → lrl → dag → fintrilo → lsp → icd

### Conversion exit

On `booked_call` / `enrolled` / `convert_flag` for email E:
1. Stop **all** other `nurture-<brand>` enrollments for E.
2. Keep / start **client-edu** (or post-convert) for the **winning** brand only.
3. Honor global unsubscribe across every brand.

### Anti-collision

- Max **one send per email per calendar day** (no two brands same day).
- **3-day cooldown** when rotating to the next brand journey.
- Rotate after journey complete, or after kickoff + 14 idle days (ops configurable).

**Brand count:** 14 · **Emails/brand:** 25 · **Total generated:** 350

---

## Merchant Relief Desk (`nurture-mrd`)

Voice: `empathetic_ops` · Disclaimer: `settlement_non_law` · From: `desk@mail.merchantreliefdesk.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Welcome — let's name the pressure | `content/nurture-by-brand/mrd/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Urgent vs loud | `content/nurture-by-brand/mrd/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | How many advances are pulling? | `content/nurture-by-brand/mrd/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | 30-day cash if nothing changes | `content/nurture-by-brand/mrd/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Pressure-map call exists | `content/nurture-by-brand/mrd/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Desperate moves that backfire | `content/nurture-by-brand/mrd/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a pressure-map call | `content/nurture-by-brand/mrd/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Reading the ACH calendar | `content/nurture-by-brand/mrd/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Pressure-map checklist | `content/nurture-by-brand/mrd/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Pressure-map checklist | `content/nurture-by-brand/mrd/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a pressure-map call | `content/nurture-by-brand/mrd/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When calm triage isn't enough | `content/nurture-by-brand/mrd/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Pressure-map call exists | `content/nurture-by-brand/mrd/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Relief vs. settlement language | `content/nurture-by-brand/mrd/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | What we cover on a relief review | `content/nurture-by-brand/mrd/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: restaurant with three daily drafts | `content/nurture-by-brand/mrd/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Relief vs. settlement language | `content/nurture-by-brand/mrd/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | If the bank account freezes | `content/nurture-by-brand/mrd/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Desperate moves that backfire | `content/nurture-by-brand/mrd/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | What we cover on a relief review | `content/nurture-by-brand/mrd/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a pressure-map call | `content/nurture-by-brand/mrd/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Still getting hit daily? | `content/nurture-by-brand/mrd/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Pressure-map call exists | `content/nurture-by-brand/mrd/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Relief review → discovery handoff | `content/nurture-by-brand/mrd/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Still getting hit daily? | `content/nurture-by-brand/mrd/month-10/e02-trust.md` |

## ACH Breath Room (`nurture-abr`)

Voice: `grounded_ach_relief` · Disclaimer: `settlement_non_law` · From: `room@mail.achbreathroom.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Breath room for the ACH week | `content/nurture-by-brand/abr/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | NSF spiral language | `content/nurture-by-brand/abr/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Overlapping draft windows | `content/nurture-by-brand/abr/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | What drafts do to operating cash | `content/nurture-by-brand/abr/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Draft-pressure review | `content/nurture-by-brand/abr/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Moving money in ways that trigger more retries | `content/nurture-by-brand/abr/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book breath-room time | `content/nurture-by-brand/abr/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | ACH timing 101 for merchants | `content/nurture-by-brand/abr/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | This week's draft map | `content/nurture-by-brand/abr/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | This week's draft map | `content/nurture-by-brand/abr/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book breath-room time | `content/nurture-by-brand/abr/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When drafts become legal events | `content/nurture-by-brand/abr/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Draft-pressure review | `content/nurture-by-brand/abr/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Breath room vs settlement talk | `content/nurture-by-brand/abr/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | What we cover in breath-room time | `content/nurture-by-brand/abr/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: NSF week in a service business | `content/nurture-by-brand/abr/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Breath room vs settlement talk | `content/nurture-by-brand/abr/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Frozen account? Stop DIY | `content/nurture-by-brand/abr/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Moving money in ways that trigger more retries | `content/nurture-by-brand/abr/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | What we cover in breath-room time | `content/nurture-by-brand/abr/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book breath-room time | `content/nurture-by-brand/abr/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Still getting hit? | `content/nurture-by-brand/abr/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Draft-pressure review | `content/nurture-by-brand/abr/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Breath-room → discovery handoff | `content/nurture-by-brand/abr/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Still getting hit? | `content/nurture-by-brand/abr/month-10/e02-trust.md` |

## Business Debt Ninjas (`nurture-bdn`)

Voice: `education_sharp` · Disclaimer: `media_education` · From: `crew@mail.businessdebtninjas.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Ninja brief: you're not crazy | `content/nurture-by-brand/bdn/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | The mid-week balance lie | `content/nurture-by-brand/bdn/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | What “stacked” actually means | `content/nurture-by-brand/bdn/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Paying twice — the feeling vs. the math | `content/nurture-by-brand/bdn/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Read this before you stack again | `content/nurture-by-brand/bdn/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Broker culture traps | `content/nurture-by-brand/bdn/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Curious? Talk to a specialist | `content/nurture-by-brand/bdn/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Factor rate in plain English | `content/nurture-by-brand/bdn/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Urgent vs loud — a merchant drill | `content/nurture-by-brand/bdn/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Urgent vs loud — a merchant drill | `content/nurture-by-brand/bdn/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Curious? Talk to a specialist | `content/nurture-by-brand/bdn/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | How escalation often shows up | `content/nurture-by-brand/bdn/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Read this before you stack again | `content/nurture-by-brand/bdn/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement literacy without the pitch | `content/nurture-by-brand/bdn/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Myths that delay good decisions | `content/nurture-by-brand/bdn/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: broker-stacked retail | `content/nurture-by-brand/bdn/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement literacy without the pitch | `content/nurture-by-brand/bdn/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | When education ends and counsel begins | `content/nurture-by-brand/bdn/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Broker culture traps | `content/nurture-by-brand/bdn/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Myths that delay good decisions | `content/nurture-by-brand/bdn/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Curious? Talk to a specialist | `content/nurture-by-brand/bdn/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Second look without the shame | `content/nurture-by-brand/bdn/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Read this before you stack again | `content/nurture-by-brand/bdn/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Ready for a human conversation? | `content/nurture-by-brand/bdn/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Second look without the shame | `content/nurture-by-brand/bdn/month-10/e02-trust.md` |

## Cashflow Clarity Co. (`nurture-ccc`)

Voice: `diagnostic` · Disclaimer: `media_education` · From: `clarity@mail.cashflowclarityco.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Clarity before commitment | `content/nurture-by-brand/ccc/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Why your mid-week balance lies | `content/nurture-by-brand/ccc/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacking on a spreadsheet | `content/nurture-by-brand/ccc/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | True cost sketch (illustrative) | `content/nurture-by-brand/ccc/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Clarity session teaser | `content/nurture-by-brand/ccc/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Optimizing the wrong line item | `content/nurture-by-brand/ccc/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Run your clarity session | `content/nurture-by-brand/ccc/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Holdbacks and effective cost | `content/nurture-by-brand/ccc/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Weekly cash picture under hardship | `content/nurture-by-brand/ccc/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Weekly cash picture under hardship | `content/nurture-by-brand/ccc/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Run your clarity session | `content/nurture-by-brand/ccc/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When numbers say escalate | `content/nurture-by-brand/ccc/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Clarity session teaser | `content/nurture-by-brand/ccc/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Refinance vs settle — questions to ask | `content/nurture-by-brand/ccc/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Clarity → fit questions | `content/nurture-by-brand/ccc/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: clarity sheet for a multi-advance shop | `content/nurture-by-brand/ccc/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Refinance vs settle — questions to ask | `content/nurture-by-brand/ccc/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Numbers can't replace counsel | `content/nurture-by-brand/ccc/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Optimizing the wrong line item | `content/nurture-by-brand/ccc/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Clarity → fit questions | `content/nurture-by-brand/ccc/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Run your clarity session | `content/nurture-by-brand/ccc/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If prior “audits” were sales pitches | `content/nurture-by-brand/ccc/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Clarity session teaser | `content/nurture-by-brand/ccc/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Clarity session + options review | `content/nurture-by-brand/ccc/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If prior “audits” were sales pitches | `content/nurture-by-brand/ccc/month-10/e02-trust.md` |

## Stack Literacy Co. (`nurture-slc`)

Voice: `teacher_literacy` · Disclaimer: `media_education` · From: `literacy@mail.stackliteracyco.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Stack Literacy — class is open | `content/nurture-by-brand/slc/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | The “paying twice” feeling | `content/nurture-by-brand/slc/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacking mechanics literacy | `content/nurture-by-brand/slc/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Literacy on effective cost | `content/nurture-by-brand/slc/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Literacy session teaser | `content/nurture-by-brand/slc/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Renewal language that hides a stack | `content/nurture-by-brand/slc/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a literacy session | `content/nurture-by-brand/slc/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Holds, splits, and stack entries | `content/nurture-by-brand/slc/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Literacy under cash stress | `content/nurture-by-brand/slc/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Literacy under cash stress | `content/nurture-by-brand/slc/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a literacy session | `content/nurture-by-brand/slc/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When literacy isn't enough | `content/nurture-by-brand/slc/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Literacy session teaser | `content/nurture-by-brand/slc/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement words merchants confuse | `content/nurture-by-brand/slc/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Literacy → options review | `content/nurture-by-brand/slc/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: stack literacy for a multi-advance shop | `content/nurture-by-brand/slc/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement words merchants confuse | `content/nurture-by-brand/slc/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Contract words that imply PG heat | `content/nurture-by-brand/slc/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Renewal language that hides a stack | `content/nurture-by-brand/slc/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Literacy → options review | `content/nurture-by-brand/slc/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a literacy session | `content/nurture-by-brand/slc/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If education was just a sales funnel before | `content/nurture-by-brand/slc/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Literacy session teaser | `content/nurture-by-brand/slc/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Literacy + options review | `content/nurture-by-brand/slc/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If education was just a sales funnel before | `content/nurture-by-brand/slc/month-10/e02-trust.md` |

## Advance Alternatives Brief (`nurture-aab`)

Voice: `skeptical_educator` · Disclaimer: `media_education` · From: `brief@mail.advancealternativesbrief.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Before you take another advance | `content/nurture-by-brand/aab/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Quick capital fog | `content/nurture-by-brand/aab/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Why “one more” feels rational | `content/nurture-by-brand/aab/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Cost of the next advance (illustrative) | `content/nurture-by-brand/aab/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Fund vs wait vs other path | `content/nurture-by-brand/aab/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Signing under NSF panic | `content/nurture-by-brand/aab/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book an alternatives brief | `content/nurture-by-brand/aab/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Reading a hard-money offer | `content/nurture-by-brand/aab/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Is this a capital problem or an ACH problem? | `content/nurture-by-brand/aab/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Is this a capital problem or an ACH problem? | `content/nurture-by-brand/aab/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book an alternatives brief | `content/nurture-by-brand/aab/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When another advance won't fix escalation | `content/nurture-by-brand/aab/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Fund vs wait vs other path | `content/nurture-by-brand/aab/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Refinance vs stack vs settle — question set | `content/nurture-by-brand/aab/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Decision checklist before any new capital | `content/nurture-by-brand/aab/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: owner offered a “save” refinance | `content/nurture-by-brand/aab/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Refinance vs stack vs settle — question set | `content/nurture-by-brand/aab/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Contracts that quietly add PG heat | `content/nurture-by-brand/aab/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Signing under NSF panic | `content/nurture-by-brand/aab/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Decision checklist before any new capital | `content/nurture-by-brand/aab/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book an alternatives brief | `content/nurture-by-brand/aab/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If the last broker oversold ease | `content/nurture-by-brand/aab/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Fund vs wait vs other path | `content/nurture-by-brand/aab/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Alternatives brief → options handoff | `content/nurture-by-brand/aab/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If the last broker oversold ease | `content/nurture-by-brand/aab/month-10/e02-trust.md` |

## Settlement Path Advisors (`nurture-spa`)

Voice: `steady_guide` · Disclaimer: `settlement_non_law` · From: `path@mail.settlementpathadvisors.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Path, not panic | `content/nurture-by-brand/spa/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Pressure without a map | `content/nurture-by-brand/spa/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacked path checkpoints | `content/nurture-by-brand/spa/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Tradeoffs on the path | `content/nurture-by-brand/spa/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Options map teaser | `content/nurture-by-brand/spa/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Skipping checkpoints | `content/nurture-by-brand/spa/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a path review | `content/nurture-by-brand/spa/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | How settlement paths are often sequenced | `content/nurture-by-brand/spa/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Path vs. crisis fork | `content/nurture-by-brand/spa/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Path vs. crisis fork | `content/nurture-by-brand/spa/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a path review | `content/nurture-by-brand/spa/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | Path checkpoints under creditor heat | `content/nurture-by-brand/spa/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Options map teaser | `content/nurture-by-brand/spa/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | What settlement is — and isn't | `content/nurture-by-brand/spa/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Readiness checklist | `content/nurture-by-brand/spa/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: path review for a service business | `content/nurture-by-brand/spa/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | What settlement is — and isn't | `content/nurture-by-brand/spa/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Legal fork on the path | `content/nurture-by-brand/spa/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Skipping checkpoints | `content/nurture-by-brand/spa/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Readiness checklist | `content/nurture-by-brand/spa/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a path review | `content/nurture-by-brand/spa/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Burned before? Trust rebuild | `content/nurture-by-brand/spa/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Options map teaser | `content/nurture-by-brand/spa/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Enrollment-adjacent path review | `content/nurture-by-brand/spa/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Burned before? Trust rebuild | `content/nurture-by-brand/spa/month-10/e02-trust.md` |

## Business Debt Solutions (`nurture-bds`)

Voice: `direct_merchant` · Disclaimer: `settlement_non_law` · From: `maria@mail.businessdebtsolutions.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Welcome from Business Debt Solutions | `content/nurture-by-brand/bds/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Daily ACH is eating the week | `content/nurture-by-brand/bds/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacked advances, one bank account | `content/nurture-by-brand/bds/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Sketching true cost (illustrative) | `content/nurture-by-brand/bds/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Discovery exists when you're ready | `content/nurture-by-brand/bds/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Don't ghost funders in a panic | `content/nurture-by-brand/bds/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | A discovery call — only when you're ready | `content/nurture-by-brand/bds/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Factor rate in merchant English | `content/nurture-by-brand/bds/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Stabilize core ops first | `content/nurture-by-brand/bds/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Stabilize core ops first | `content/nurture-by-brand/bds/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | A discovery call — only when you're ready | `content/nurture-by-brand/bds/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When funders turn up the heat | `content/nurture-by-brand/bds/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Discovery exists when you're ready | `content/nurture-by-brand/bds/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | What settlement is — and isn't | `content/nurture-by-brand/bds/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Fit questions before enrollment | `content/nurture-by-brand/bds/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: multi-advance retail stack | `content/nurture-by-brand/bds/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | What settlement is — and isn't | `content/nurture-by-brand/bds/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | If a suit shows up, pause and get counsel | `content/nurture-by-brand/bds/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Don't ghost funders in a panic | `content/nurture-by-brand/bds/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Fit questions before enrollment | `content/nurture-by-brand/bds/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | A discovery call — only when you're ready | `content/nurture-by-brand/bds/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If you've been burned before | `content/nurture-by-brand/bds/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Discovery exists when you're ready | `content/nurture-by-brand/bds/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Enrollment-oriented discovery | `content/nurture-by-brand/bds/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If you've been burned before | `content/nurture-by-brand/bds/month-10/e02-trust.md` |

## Merchant Crisis Brief (`nurture-mcb`)

Voice: `urgent_calm_triage` · Disclaimer: `settlement_non_law` · From: `crisis@mail.merchantcrisisbrief.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Crisis Brief — this week’s fire | `content/nurture-by-brand/mcb/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Urgent vs loud in a crisis window | `content/nurture-by-brand/mcb/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacked drafts in a crisis week | `content/nurture-by-brand/mcb/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Cost of waiting 72 more hours | `content/nurture-by-brand/mcb/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Crisis brief booking | `content/nurture-by-brand/mcb/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Panic communications | `content/nurture-by-brand/mcb/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a crisis brief | `content/nurture-by-brand/mcb/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Crisis ≠ mechanics class | `content/nurture-by-brand/mcb/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | 72-hour plan | `content/nurture-by-brand/mcb/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | 72-hour plan | `content/nurture-by-brand/mcb/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a crisis brief | `content/nurture-by-brand/mcb/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | Legal tripwire → DAG | `content/nurture-by-brand/mcb/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Crisis brief booking | `content/nurture-by-brand/mcb/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | After the fire: literacy later | `content/nurture-by-brand/mcb/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | What triage needs from you | `content/nurture-by-brand/mcb/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: owner with suit threat this week | `content/nurture-by-brand/mcb/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | After the fire: literacy later | `content/nurture-by-brand/mcb/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Account freeze / levy language | `content/nurture-by-brand/mcb/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Panic communications | `content/nurture-by-brand/mcb/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | What triage needs from you | `content/nurture-by-brand/mcb/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a crisis brief | `content/nurture-by-brand/mcb/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If last “help” vanished in a crisis | `content/nurture-by-brand/mcb/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Crisis brief booking | `content/nurture-by-brand/mcb/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Crisis brief → next stable step | `content/nurture-by-brand/mcb/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If last “help” vanished in a crisis | `content/nurture-by-brand/mcb/month-10/e02-trust.md` |

## Ledger Reset Lab (`nurture-lrl`)

Voice: `workshop` · Disclaimer: `media_education` · From: `lab@mail.ledgerresetlab.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Lab open — experiment before you lock | `content/nurture-by-brand/lrl/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Ledger under ACH stress | `content/nurture-by-brand/lrl/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacking as a lab problem | `content/nurture-by-brand/lrl/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Scenario cost without fake stats | `content/nurture-by-brand/lrl/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Reset session teaser | `content/nurture-by-brand/lrl/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Locking a plan on day-one emotion | `content/nurture-by-brand/lrl/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a lab walkthrough | `content/nurture-by-brand/lrl/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Modeling factor cost in scenarios | `content/nurture-by-brand/lrl/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Scenario A status quo vs B structured path | `content/nurture-by-brand/lrl/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Scenario A status quo vs B structured path | `content/nurture-by-brand/lrl/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a lab walkthrough | `content/nurture-by-brand/lrl/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When the lab says pause for counsel | `content/nurture-by-brand/lrl/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Reset session teaser | `content/nurture-by-brand/lrl/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement as a ledger redesign | `content/nurture-by-brand/lrl/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Which scenario are you ready to test? | `content/nurture-by-brand/lrl/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: multi-advance restaurant lab | `content/nurture-by-brand/lrl/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement as a ledger redesign | `content/nurture-by-brand/lrl/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | PG risk in the model | `content/nurture-by-brand/lrl/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Locking a plan on day-one emotion | `content/nurture-by-brand/lrl/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Which scenario are you ready to test? | `content/nurture-by-brand/lrl/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a lab walkthrough | `content/nurture-by-brand/lrl/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Prior plans that ignored the ledger | `content/nurture-by-brand/lrl/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Reset session teaser | `content/nurture-by-brand/lrl/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Lab walkthrough → human decision | `content/nurture-by-brand/lrl/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Prior plans that ignored the ledger | `content/nurture-by-brand/lrl/month-10/e02-trust.md` |

## DAG Law (`nurture-dag`)

Voice: `formal_authority` · Disclaimer: `law_firm` · From: `education@mail.daglaw.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | A measured introduction from DAG Law | `content/nurture-by-brand/dag/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | When pressure becomes a legal question | `content/nurture-by-brand/dag/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stacked obligations — informational overview | `content/nurture-by-brand/dag/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Cost is not only the factor rate | `content/nurture-by-brand/dag/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Counsel vs. non-counsel paths | `content/nurture-by-brand/dag/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Panic replies that can hurt your position | `content/nurture-by-brand/dag/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Consultation when the facts warrant it | `content/nurture-by-brand/dag/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | MCA contracts — what counsel often reviews | `content/nurture-by-brand/dag/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Urgent legal events vs. loud collection noise | `content/nurture-by-brand/dag/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Urgent legal events vs. loud collection noise | `content/nurture-by-brand/dag/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Consultation when the facts warrant it | `content/nurture-by-brand/dag/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | How escalation often appears in the file | `content/nurture-by-brand/dag/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Counsel vs. non-counsel paths | `content/nurture-by-brand/dag/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement talk vs. legal strategy | `content/nurture-by-brand/dag/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | What to bring to a consultation | `content/nurture-by-brand/dag/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: owner with PG + active suit risk | `content/nurture-by-brand/dag/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement talk vs. legal strategy | `content/nurture-by-brand/dag/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Personal guaranty — informational overview | `content/nurture-by-brand/dag/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Panic replies that can hurt your position | `content/nurture-by-brand/dag/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | What to bring to a consultation | `content/nurture-by-brand/dag/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Consultation when the facts warrant it | `content/nurture-by-brand/dag/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Burned by aggressive collectors? | `content/nurture-by-brand/dag/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Counsel vs. non-counsel paths | `content/nurture-by-brand/dag/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | If legal pressure is active, talk to counsel | `content/nurture-by-brand/dag/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Burned by aggressive collectors? | `content/nurture-by-brand/dag/month-10/e02-trust.md` |

## Fintrilo (`nurture-fintrilo`)

Voice: `consultative_b2b` · Disclaimer: `merchant_finance` · From: `liaison@mail.fintrilo.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | One picture beats three vendors | `content/nurture-by-brand/fintrilo/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | Fragmented vendors, fragmented cash | `content/nurture-by-brand/fintrilo/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Processing float vs. advance pulls | `content/nurture-by-brand/fintrilo/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Cost of sprawl | `content/nurture-by-brand/fintrilo/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Liaison Officer conversation | `content/nurture-by-brand/fintrilo/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Buying another tool instead of a plan | `content/nurture-by-brand/fintrilo/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Connect with a Liaison Officer | `content/nurture-by-brand/fintrilo/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | Funding options without fog | `content/nurture-by-brand/fintrilo/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Stabilize payments rails while cash is tight | `content/nurture-by-brand/fintrilo/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Stabilize payments rails while cash is tight | `content/nurture-by-brand/fintrilo/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Connect with a Liaison Officer | `content/nurture-by-brand/fintrilo/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | When capital talk must pause for legal | `content/nurture-by-brand/fintrilo/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Liaison Officer conversation | `content/nurture-by-brand/fintrilo/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Optimization vs. settlement lanes | `content/nurture-by-brand/fintrilo/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | What a liaison session covers | `content/nurture-by-brand/fintrilo/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: retail needing Clover + capital clarity | `content/nurture-by-brand/fintrilo/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Optimization vs. settlement lanes | `content/nurture-by-brand/fintrilo/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Debt-relief interest ≠ legal advice | `content/nurture-by-brand/fintrilo/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Buying another tool instead of a plan | `content/nurture-by-brand/fintrilo/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | What a liaison session covers | `content/nurture-by-brand/fintrilo/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Connect with a Liaison Officer | `content/nurture-by-brand/fintrilo/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | If prior funders overpromised | `content/nurture-by-brand/fintrilo/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Liaison Officer conversation | `content/nurture-by-brand/fintrilo/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Explore funding + payments fit | `content/nurture-by-brand/fintrilo/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | If prior funders overpromised | `content/nurture-by-brand/fintrilo/month-10/e02-trust.md` |

## Level Set Partners (`nurture-lsp`)

Voice: `b2b_partner` · Disclaimer: `partner` · From: `partners@mail.levelsetpartners.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | Level Set — partner orientation | `content/nurture-by-brand/lsp/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | When your merchant's ACH stress hits you | `content/nurture-by-brand/lsp/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stack signals partners should spot | `content/nurture-by-brand/lsp/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | True cost talk for partner desks | `content/nurture-by-brand/lsp/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Referral paths that stay clean | `content/nurture-by-brand/lsp/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Handoffs that damage trust | `content/nurture-by-brand/lsp/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Connect on next steps | `content/nurture-by-brand/lsp/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | MCA mechanics partners must explain fairly | `content/nurture-by-brand/lsp/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Partner triage checklist | `content/nurture-by-brand/lsp/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Partner triage checklist | `content/nurture-by-brand/lsp/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Connect on next steps | `content/nurture-by-brand/lsp/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | Escalation signals in partner pipelines | `content/nurture-by-brand/lsp/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Referral paths that stay clean | `content/nurture-by-brand/lsp/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement vs funding — partner script hygiene | `content/nurture-by-brand/lsp/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Align before you enroll a referral | `content/nurture-by-brand/lsp/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: ISO caught between funder and merchant | `content/nurture-by-brand/lsp/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement vs funding — partner script hygiene | `content/nurture-by-brand/lsp/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Legal tripwires — stop and route | `content/nurture-by-brand/lsp/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Handoffs that damage trust | `content/nurture-by-brand/lsp/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Align before you enroll a referral | `content/nurture-by-brand/lsp/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Connect on next steps | `content/nurture-by-brand/lsp/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Repairing a burned referral | `content/nurture-by-brand/lsp/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Referral paths that stay clean | `content/nurture-by-brand/lsp/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Partner sync + merchant handoff | `content/nurture-by-brand/lsp/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Repairing a burned referral | `content/nurture-by-brand/lsp/month-10/e02-trust.md` |

## ISO Care Desk (`nurture-icd`)

Voice: `b2b_partner_ops` · Disclaimer: `partner` · From: `partners@mail.isocaredesk.com`

| # | Day | Month | Slot | Subject | Path |
|---|-----|-------|------|---------|------|
| 1 | D0 | 1 | welcome | ISO Care Desk — handoff hygiene | `content/nurture-by-brand/icd/month-01/e01-welcome.md` |
| 2 | D2 | 1 | pain | When your funded merchant starts drowning | `content/nurture-by-brand/icd/month-01/e02-pain.md` |
| 3 | D4 | 1 | stack | Stack signals on the ISO desk | `content/nurture-by-brand/icd/month-01/e03-stack.md` |
| 4 | D6 | 1 | cost | Cost of a messy handoff | `content/nurture-by-brand/icd/month-01/e04-cost.md` |
| 5 | D8 | 1 | options | Handoff brief request | `content/nurture-by-brand/icd/month-01/e05-options.md` |
| 6 | D10 | 1 | mistakes | Promising settlement outcomes as an ISO | `content/nurture-by-brand/icd/month-01/e06-mistakes.md` |
| 7 | D12 | 1 | soft_cta | Book a partner sync | `content/nurture-by-brand/icd/month-01/e07-soft_cta.md` |
| 8 | D35 | 2 | mechanics | What to explain fairly about MCA cost | `content/nurture-by-brand/icd/month-02/e01-mechanics.md` |
| 9 | D48 | 2 | triage | Distress checklist for ISOs | `content/nurture-by-brand/icd/month-02/e02-triage.md` |
| 10 | D65 | 3 | triage | Distress checklist for ISOs | `content/nurture-by-brand/icd/month-03/e01-triage.md` |
| 11 | D78 | 3 | soft_cta | Book a partner sync | `content/nurture-by-brand/icd/month-03/e02-soft_cta.md` |
| 12 | D95 | 4 | escalation | Escalation without burning the funder | `content/nurture-by-brand/icd/month-04/e01-escalation.md` |
| 13 | D108 | 4 | options | Handoff brief request | `content/nurture-by-brand/icd/month-04/e02-options.md` |
| 14 | D125 | 5 | literacy | Settlement lane vs funding lane | `content/nurture-by-brand/icd/month-05/e01-literacy.md` |
| 15 | D138 | 5 | readiness | Clean referral packet | `content/nurture-by-brand/icd/month-05/e02-readiness.md` |
| 16 | D155 | 6 | scenarios | Composite: ISO between funder and stressed merchant | `content/nurture-by-brand/icd/month-06/e01-scenarios.md` |
| 17 | D168 | 6 | literacy | Settlement lane vs funding lane | `content/nurture-by-brand/icd/month-06/e02-literacy.md` |
| 18 | D185 | 7 | risk | Legal tripwires — you are not counsel | `content/nurture-by-brand/icd/month-07/e01-risk.md` |
| 19 | D198 | 7 | mistakes | Promising settlement outcomes as an ISO | `content/nurture-by-brand/icd/month-07/e02-mistakes.md` |
| 20 | D215 | 8 | readiness | Clean referral packet | `content/nurture-by-brand/icd/month-08/e01-readiness.md` |
| 21 | D228 | 8 | soft_cta | Book a partner sync | `content/nurture-by-brand/icd/month-08/e02-soft_cta.md` |
| 22 | D245 | 9 | trust | Repairing partner trust after a bad transfer | `content/nurture-by-brand/icd/month-09/e01-trust.md` |
| 23 | D258 | 9 | options | Handoff brief request | `content/nurture-by-brand/icd/month-09/e02-options.md` |
| 24 | D275 | 10 | commit | Partner sync + care handoff | `content/nurture-by-brand/icd/month-10/e01-commit.md` |
| 25 | D288 | 10 | trust | Repairing partner trust after a bad transfer | `content/nurture-by-brand/icd/month-10/e02-trust.md` |

