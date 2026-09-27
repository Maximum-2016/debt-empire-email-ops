# Amazon SES Adapter — Phase 3+ Setup Checklist

**Wall:** MGP / Debt Empire · **Provider plan:** Mailgun primary first; SES later in parallel, then SES primary with Mailgun backup · **No secrets in vault**

SES is already supported by the shared adapter contract, but it is not the Phase 1 go-live provider. Complete this checklist during Phase 3 and use `delivery/PHASES.md` for the cutover gate.

## 1. Account, region, and IAM

- [ ] Use a dedicated AWS account or an isolated production environment; choose one SES region deliberately and keep identities/configuration sets in that region.
- [ ] Prefer an instance/task role or workload identity over long-lived access keys. Store any unavoidable credentials in the secret manager, never in git or this vault.
- [ ] Create a least-privilege send role. Scope sending to the selected region and approved SES identities where the deployment supports identity restrictions.
- [ ] Allow only the actions required by the adapter, typically `ses:SendEmail` and `ses:SendRawEmail`; add `ses:GetSendQuota` / `ses:GetAccount` only for health and quota checks.
- [ ] Keep administrative actions (identity verification, configuration-set changes, production-access requests, suppression review) in a separate operator role; do not grant them to the runtime sender.
- [ ] Log role assumption and SES API calls in CloudTrail; alert on unexpected region, role, identity, or volume.
- [ ] Confirm the runtime role cannot read unrelated S3, SNS, Secrets Manager, or customer data.

## 2. Sandbox exit and sending identity

- [ ] Verify every from-domain or address used by the activated brand in the chosen SES region.
- [ ] Enable Easy DKIM and publish all CNAME records; configure a custom MAIL FROM subdomain with SPF and matching MX records.
- [ ] Publish DMARC for each from-domain. Start with monitoring (`p=none`) while validating alignment, then tighten under the approved deliverability policy.
- [ ] While in the SES sandbox, send only to verified recipients and keep the test identity list explicit.
- [ ] Request production access (sandbox exit) with the intended use case, website, consent model, expected volume, warm-up plan, and bounce/complaint controls.
- [ ] Confirm the approved daily sending quota and per-second rate; implement backoff for throttling and keep ATLAS caps lower than the AWS quota.
- [ ] Re-check production access after identity, region, or volume changes. Sandbox exit is regional and does not automatically cover another AWS region.

## 3. Configuration sets and message metadata

- [ ] Create a configuration set for each brand, or a documented shared set with brand-level dimensions, rather than relying on an implicit default.
- [ ] Add event destinations for sends, deliveries, rejects, bounces, complaints, and rendering failures as applicable. Use CloudWatch for operational metrics and SNS for Email Desk events.
- [ ] Use message tags for `brand_id`, `journey`, `sequence_id`, and `touch_id`; do not put email addresses or other unnecessary PII in tags.
- [ ] Keep configuration-set names and tag keys stable across Mailgun and SES so dashboards and reconciliation remain provider-neutral.
- [ ] Include `ConfigurationSetName` on every `SendEmail` / `SendRawEmail` call and record the returned SES `MessageId`.
- [ ] Test that configuration-set event publishing fails visibly rather than silently dropping feedback.

## 4. SNS bounce, complaint, and delivery pipeline

- [ ] Create an SNS topic per environment (or a documented per-brand layout) and subscribe the Email Desk HTTPS endpoint, `/webhooks/ses`.
- [ ] Confirm the HTTPS subscription and validate SNS signatures against the official SNS certificate chain before accepting events.
- [ ] Handle `SubscriptionConfirmation` safely, then accept SES notifications only for the expected topic/region.
- [ ] Parse SES notification types `Bounce`, `Complaint`, and `Delivery`; retain the SES `messageId`, event timestamp, recipient, feedback type, and configuration-set dimensions needed for reconciliation.
- [ ] Treat permanent bounces and complaints as immediate global suppression events. Classify transient bounces separately with bounded retry/backoff; never retry a complaint or hard bounce.
- [ ] Make event handling idempotent on provider message/event identifiers and preserve the raw event needed for audit without storing unnecessary message content.
- [ ] Return success only after durable processing. Configure SNS retries and a dead-letter path/alert for repeated webhook failures; monitor delivery lag and dropped-event counts.
- [ ] Verify that SNS feedback updates Contact 360, Salesforce, the shared suppression list, and the Email Desk alert path just as Mailgun events do.

## 5. App configuration (env placeholders)

```dotenv
EMAIL_PROVIDER=ses                 # Phase 3 test; Phase 4 primary only after cutover gate
AWS_REGION=us-east-1               # use the approved SES region
AWS_ROLE_ARN=                      # prefer workload/instance role; do not commit credentials
AWS_ACCESS_KEY_ID=                 # secret only if a role is unavailable
AWS_SECRET_ACCESS_KEY=             # secret only if a role is unavailable
SES_CONFIGURATION_SET=debt-empire-default
SES_SNS_TOPIC_ARN=                 # secret/config-store value as appropriate
DRY_RUN=true
```

The local UI also recognizes `AWS_PROFILE` or `SES_READY=1` as a readiness hint. That hint is not proof of sandbox exit, IAM correctness, or production approval.

## 6. Send sketch

Use `SendEmail` or `SendRawEmail` with the shared payload, the appropriate `ConfigurationSetName`, and `DefaultEmailTags` / message tags for `journey`, `sequence_id`, `touch_id`, and `brand_id`. Preserve `List-Unsubscribe` and `List-Unsubscribe-Post` headers in the raw message where required.

## 7. Cost and operating trade-offs vs Mailgun

- **SES economics:** SES is commonly priced as a low per-message/per-1,000-message service, with separate charges possible for data, dedicated IPs, Virtual Deliverability Manager, CloudWatch, SNS, and other AWS services. Verify current regional pricing before approval; do not treat a headline send rate as total cost.
- **Mailgun economics:** Mailgun generally bundles a more operationally friendly sending/events experience into a plan with monthly volume tiers, included quotas, and overage/feature charges that vary by plan and region. Verify the current contract/pricing before comparing.
- **Practical trade:** SES may win on raw high-volume send cost, while Mailgun usually reduces AWS plumbing and provides a faster dashboard/webhook workflow. SES adds IAM, sandbox/quota management, SNS/CloudWatch operations, and deliverability ownership.
- Compare total cost of ownership: provider fees, AWS event/monitoring charges, engineering/on-call time, deliverability tooling, dedicated IP needs, and migration/rollback complexity—not only cents per message.
- Record the measured cost per delivered 1,000 messages and event/ops overhead during Phase 3 before authorizing Phase 4.

## 8. Go-live gate

SES is eligible for primary only after the Phase 3 evidence and the `delivery/PHASES.md` cutover checklist pass: sandbox exit, identity alignment, least-privilege IAM, configuration-set/SNS feedback, suppression parity, warm-up cohort, quota headroom, monitoring, rollback to Mailgun, and Anthony's explicit approval. Keep `DRY_RUN=true` until that approval; this documentation change performs no sends.
