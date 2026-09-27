# Delivery Phases — Debt Empire Email

**Provider preference:** Mailgun first for go-live; Amazon SES later. Both adapters remain supported throughout. **No live sends are initiated by this document.**

The system has one active production provider at a time. The inactive adapter may be configured, tested, and monitored, but it must not create duplicate customer deliveries.

## Phase 1 — Mailgun Wednesday test

**Goal:** prove the Mailgun adapter and Email Desk rail-guards with a tightly scoped test.

- Use one verified Mailgun sending domain and one approved internal seed mailbox/cohort.
- Confirm SPF, DKIM, DMARC, webhook signing, `DRY_RUN=true` behavior, suppression, unsubscribe headers, and event ingestion.
- Exercise preview, queue, send payload mapping, delivery/bounce/complaint handling, and the kill switch.
- Validate the first warm-up cap and brand identity before expanding beyond the test domain.
- The Wednesday test window is a planned gate; Anthony must explicitly approve any test send separately. This repository update sends nothing.

**Exit:** Mailgun test evidence is recorded, no rail-guard or webhook defects remain, and Anthony approves Phase 2.

## Phase 2 — Multi-domain Mailgun

**Goal:** make Mailgun the controlled primary across the approved Debt Empire brand domains.

- Verify each domain and complete SPF, DKIM, DMARC, custom tracking, and reply-to checks.
- Warm every from-domain independently; do not send the full list from a cold domain.
- Map each brand to its Mailgun domain, event stream, tags, suppression behavior, and daily/weekly caps.
- Run dry-runs and a small approved cohort per domain before increasing volume.
- Keep the SES adapter installed and schema-compatible, but inactive for production delivery.

**Exit:** all activated domains pass identity, compliance, webhook, reputation, and rollback checks at the agreed caps.

## Phase 3 — SES parallel

**Goal:** bring SES to production readiness without changing the Mailgun send path.

- Provision the SES account/region, least-privilege IAM role, verified identities, custom MAIL FROM, and configuration sets.
- Request and confirm sandbox exit before any non-verified recipient testing.
- Wire SES configuration-set events through SNS to the same idempotent Email Desk webhook and suppression store.
- Exercise the SES adapter with dry-runs and verified test identities; compare payloads, event latency, bounce/complaint mapping, and observability with Mailgun.
- If a parallel production cohort is approved, split recipients deterministically; never send the same touch to the same recipient through both providers.
- Define the rollback switch to Mailgun and record the owner, timestamp, and reason for any provider change.

**Exit:** SES passes the same compliance, event, deliverability, monitoring, cap, and rollback gates as Mailgun, with a documented cost/operations decision.

## Phase 4 — SES primary / Mailgun backup

**Goal:** cut over deliberately only after SES is proven, while retaining Mailgun as a tested backup.

- Set SES as the single primary in the provider configuration and announce the change to on-call owners.
- Keep Mailgun domains, credentials, webhooks, caps, and adapter health checks ready but disabled for normal sends.
- Migrate one approved cohort first; watch delivery, hard bounce, complaint, unsubscribe, latency, and quota signals.
- Expand only after the observation window and thresholds are met. Pause immediately on a rail-guard or reputation breach.
- Route new sends to Mailgun only through the documented rollback procedure; do not dual-send.

## Cutover checklist

### Before changing primary

- [ ] Anthony approved the change and named the change owner/on-call.
- [ ] No active incident, unexplained bounce/complaint spike, or unresolved suppression mismatch.
- [ ] SES identity/DKIM/MAIL FROM/DMARC checks pass for every activated brand.
- [ ] SES is out of sandbox, quotas are sufficient, and IAM uses the least privilege needed.
- [ ] SES configuration sets and SNS event destinations are active; SNS HTTPS subscription is confirmed and signature validation is tested.
- [ ] Bounce, complaint, unsubscribe, delivery, and provider message IDs are idempotent in the shared event store.
- [ ] Dry-run, preview, seed-recipient, kill-switch, and rollback tests pass.
- [ ] Mailgun backup path and webhook health check pass without sending a duplicate.
- [ ] Warm-up caps, cohort assignment, monitoring dashboards, and alert thresholds are recorded.

### Execute and observe

- [ ] Change one provider setting; record old/new provider, timestamp, operator, and reason.
- [ ] Send only the approved SES cohort; verify From identity, headers, tags, and event receipt.
- [ ] Monitor delivery, hard/soft bounces, complaints, unsubscribes, latency, throttling, and quota.
- [ ] Compare against the agreed Mailgun baseline during the observation window.
- [ ] Stop the cohort and roll back to Mailgun if thresholds or identity checks fail.

### After the window

- [ ] Reconcile provider events against Email Desk, suppression, and Salesforce records.
- [ ] Confirm no recipient received the same `touch_id` twice.
- [ ] Record results, costs, incidents, and the decision to expand, hold, or roll back.
- [ ] Keep Mailgun backup credentials and health checks current; re-test on a scheduled cadence.

*Phase plan v1 · 2026-09-27 ET · MGP wall · no live sends*
