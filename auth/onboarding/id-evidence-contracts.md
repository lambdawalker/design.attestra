# Onboarding document contracts and boundaries

**Design contract, proposed for implementation.** [Capture](id-capture/architecture.md) and [parsing](id-parsing/architecture.md) are onboarding subfeatures. [ID validation](../../verification/id-validation/architecture.md) is independently owned and deferred. These are semantic responsibilities and proposed route families; exact JSON/OpenAPI and deployed behavior belong in the Go repository.

## Feature handoffs

| Producer | Output | Consumer and permitted interpretation |
| --- | --- | --- |
| ID capture | Account-bound ready manifest: capture ID, evidence version, policy version, required slots and pinned storage references | ID parsing may read this exact evidence. “Ready” means uploaded and file-validated. |
| ID parsing | Immutable extraction plus separately confirmed review revision, all bound to the evidence version | Onboarding may show saved document details. Future validation may consume the exact references under its own policy. |
| ID validation | Deferred | No approval, rejection, third-party request or feature authorization is emitted by capture/parsing. |

## Proposed API responsibilities

All operations require an authenticated session. Resolve the account server-side; every object reference is ownership-checked. Non-owned/absent resources use a consistent safe response. No route accepts arbitrary S3 keys/URLs or client-assigned account identity. IDs are not credentials. Responses containing personal data or signed instructions are non-cacheable.

| Proposed operation | Responsibility |
| --- | --- |
| `GET /onboarding/id/document-policy` | Enabled document types, jurisdictions, required slots, limits and policy revision |
| `POST /onboarding/id/captures` | Idempotent creation of account-bound capture/evidence version |
| `GET /onboarding/id/captures/{capture_id}` | Current state, safe slot progress, finalization outcome; no public image links |
| `POST /onboarding/id/captures/{capture_id}/uploads` | Register/replace a selected slot attempt and issue scoped instructions for declared checksum/size/type |
| `POST /onboarding/id/captures/{capture_id}/finalize` | Expected capture revision/selected upload IDs; freeze exact object versions and durably enqueue validation; return operation handle |
| `POST /onboarding/id/captures/{capture_id}/retry-finalization` | Retry a failed validation operation under service policy, preserving frozen evidence and advancing the fencing generation |
| `POST /onboarding/id/captures/{capture_id}/cancel` | Idempotent cancellation with generation fence and cleanup intent |
| `POST /onboarding/id/parses` | Idempotently enqueue parsing of an owned ready capture; server selects parser configuration |
| `POST /onboarding/id/parses/{parse_id}/retry` | Retry a failed job under server policy with a new attempt generation, fixed evidence/configuration, and stable operation key |
| `GET /onboarding/id/parses/{parse_id}` | Job state, safe error/retry metadata and result reference when available |
| `GET /onboarding/id/extractions/{extraction_id}` | Authorized extraction plus its review state/provenance |
| `POST /onboarding/id/extractions/{extraction_id}/reviews` | Save/confirm allowed corrections with expected review revision and operation key |
| `GET /onboarding/id/status` | Resume discovery: current selected capture/parse/review references for this account, never a validation approval |

The initial parsing job is normally created by the backend onboarding orchestrator from the durable capture-ready event, so app termination cannot lose the handoff. The create-parse operation applies the same rules when invoked through an authenticated client/recovery path; deduplicate the logical evidence/configuration request. Explicit reprocessing with a new approved configuration is a new job, not mutation of an old extraction.

Status discovery makes cross-device recovery possible without treating local checkpoints as authority. Renewal/retry operations are permitted only in valid server states. Failed finalization or parsing can be retried with a new operation generation under a service-returned retry policy; the original evidence binding stays fixed. The Go API must expose that action consistently rather than permitting clients to rewrite terminal state.

Mutating operations use stable operation keys scoped by account, operation type and target. Replays with the same canonical request return the same result; changed bodies conflict. Persist an operation lookup so a lost create response is recoverable by replay with the same key. Publish an idempotency retention horizon at least as long as session/retry eligibility; expired keys must not silently duplicate a still-existing logical operation. Expected revisions prevent stale slot changes, current-document promotion and review edits.

Model jobs use separate parse IDs from capture IDs. Evidence versions are server-assigned; parser attempts/configuration changes do not mutate evidence. Finalization/job creation is asynchronous (accepted + status handle); an accepted request is not completion. Documented safe errors distinguish auth expiry, conflict, rate limits, unsupported policy, missing slots, unsafe/unreadable content and transient service failure. Respect server retry timing and never expose provider diagnostics to the client.

## Current Android mock migration

The existing [Android prototype PR](https://github.com/lambdawalker/android.attestra.auth/pull/12) models a combined identity submission, binary uploads through an API, synchronous extraction, and mock provider decisions. It is a prototype, not the architectural contract for this split.

Implement the new design by separating capture and parsing gateways/state, mocking upload instructions + S3 transport + finalize/status + parse-job status, and confirming details without simulated identity approval in the onboarding flow. Keep an explicit mock-only label and isolate any retained validation demo outside these two features. Replace the echoed `extracted` submit body with server-owned extraction references and attributed corrections. Preserve session/account isolation and reconcile-before-retry behavior.

## Shared operational requirements

Retention, region, consent/purpose and supported-document/model policy are explicit production gates, not implicit defaults. Discard pending client raw bytes on exit/recreation unless encrypted resumable storage is separately designed. Deletion/cancellation prevents late job publication and queues removal of derived records/objects according to approved policy. Logs use opaque correlation IDs; no credentials, full signed URLs, images, or personal field values.
