# ID capture and ID parsing implementation sequence

**Architecture plan only.** No backend deployment, Android changes or model selection is included in this document change. [Contracts](id-evidence-contracts.md) · [Capture](id-capture/architecture.md) · [Parsing](id-parsing/architecture.md).

## 1. Contract and policy fixtures

Define versioned document policy, capture manifest, parse job, extraction and review contracts in the Go repository. Confirm initial document types/jurisdictions, required slots, extraction fields and measurable accuracy targets. Use a synthetic two-sided-card fixture for development while production entries stay disabled. Establish operation keys, expected revisions, safe errors and account-scoped resume discovery.

Deliverable: shared contract fixtures covering success, partial uploads, expired instructions, malformed images, partial extraction, conflicts and processing failures. The Android mock reproduces these semantics, including delayed status transitions; no production model or deployment is needed.

## 2. Capture vertical slice

Implement private versioned evidence storage, ownership checks, scoped upload instructions, per-slot progress, exact-version finalization, transactional job intent and file-validation worker. Exercise camera permission/preview/retake in Android and direct upload through the replaceable transport. Final result is capture-ready only.

Gate: cross-account denial; upload expiry/renewal; checksum/size/decode limits; late overwrite and late retake races; duplicate finalize; outbox failure; cancellation/process restart. Prove pinned versions remain available even when noncurrent.

## 3. Parsing vertical slice with deterministic adapter

Implement job creation/status, queue/lease/fencing, synthetic model adapter, schema validation, immutable extraction and revisioned review. Android supports pending/leave/resume, warnings, correction attribution, conflict recovery and “Document details saved.” No validation/provider approval in this slice.

Gate: duplicate delivery, model timeout/refusal/malformed JSON, missing/ambiguous fields, stale workers, deletion during inference, two-device review conflicts, lost responses and reparse invalidating confirmation. Verify limits on retries and calls.

## 4. Real vision adapter and evaluation

Choose provider/model/region after benchmarking representative permitted samples. Pin prompt/schema/preprocessing/model versions and record field-level accuracy, unsupported/null behavior, latency and cost. Validate structured-output support and image limits using the selected endpoint, not assumed provider-wide capabilities. Review input/output logging, data retention/training and inference routing. Enable production document policies only when their release criteria pass.

Gate: no hallucinated completion of missing text in the acceptance corpus; report measured error/recapture rates rather than promising zero real-world errors. Include adversarial printed instructions, small text, accents, multiple names, leading zeros, ambiguous dates and front/back disagreement.

## 5. Operational readiness

Test queue/DLQ recovery, concurrency/rate budgets, orphan cleanup, referenced-version retention, deletion fences, account switching, auth expiry and real devices. Set numeric release thresholds and retention schedules before rollout. Verify that neither capture nor parsing changes Cognito assurance or grants restricted features.

## Deferred separate feature

ID validation receives immutable evidence/extraction/confirmed-review references when designed later. Authenticity, account-holder binding, selfie/liveness, third-party providers, approval/rejection, appeals and feature gating are not blockers for the mock capture/parsing slices and are not implemented by them.
