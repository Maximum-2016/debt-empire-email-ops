# Fintrilo Capacity Calendar

**Wall:** MGP · Fintrilo / Biz-Pay ISO–sales overlap (NOT FM)  
**Journey id:** `fintrilo`  
**Primary CTA:** Connect with a Liaison Officer / explore funding + payments fit  
**Cadence:** 8 emails over ~5 weeks (~D+0 → D+35)  
**ESP:** undecided — keep **DRY_RUN**; no live sends from this pack  
**Brand:** Fintrilo only on this track (do not dual-brand with DAG)

Tokens: `{{booking_url}}` · `{{brand_url}}` → https://fintrilo.com  
Research: `content/fintrilo/RESEARCH.md`

---

## CTA arc

| Phase | Touches | Emphasis |
|-------|---------|----------|
| Orient | e01–e03 | Fragmented vendors → deposit/float education → Liaison Officer role |
| Soft sell | e04–e06 | Clover/payments → funding options → combined processing+capital logic |
| Partner + close | e07–e08 | ISO/referral handoff note → soft connect CTA |

---

## Touch table

| # | Day | Id | Angle | Type |
|---|-----|----|-------|------|
| 1 | D+0 | `ft_e01` | One picture vs many vendors | Education |
| 2 | D+4 | `ft_e02` | Processor float / deposit timing | Education |
| 3 | D+9 | `ft_e03` | What Liaison Officers do | Education |
| 4 | D+14 | `ft_e04` | Clover POS / acceptance fit | Product soft sell |
| 5 | D+19 | `ft_e05` | Flex / bridge / CRE funding options | Product soft sell |
| 6 | D+24 | `ft_e06` | Fix processing before funding the leak | Product soft sell (combined) |
| 7 | D+29 | `ft_e07` | Partner/ISO handoff note | Partner-ISO |
| 8 | D+35 | `ft_e08` | Soft close — connect when ready | Soft CTA |

Content paths: `content/fintrilo/e01-fragmented.md` … `e08-connect.md`  
Wired in: `delivery/sequences.json` → `journeys.fintrilo`

---

## Enrollment notes

- Prefer contacts with Fintrilo / Biz-Pay / ISO affinity (`brand_affinity: fintrilo`) or partner segment.  
- Do **not** enroll pure legal-crisis leads here — route to DAG nurture.  
- Do **not** use for FM funding brands.  
- Suppression + consent still apply (see ARCHITECTURE / UI rail-guard).

---

## Cross-link to 10-month Debt Empire calendar

Fintrilo is a **parallel capacity track**, not a month inside `CALENDAR-10-MONTH.md`. Debt Empire settlement nurture stays on BDS/BDN/DAG/etc. Fintrilo owns unified **funding + merchant processing** education/sales for the MGP ISO-adjacent lane.

---

*Fintrilo calendar v1 · 2026-09-27 ET · DRY_RUN default*
