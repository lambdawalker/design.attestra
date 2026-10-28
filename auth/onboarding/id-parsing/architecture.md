# ID parsing architecture

**Status: planned onboarding subfeature.** [Capture](../id-capture/architecture.md) provides immutable evidence; [data model](data-model.md) defines extraction/review semantics. ID validation is outside this pipeline.

## Responsibility and boundary

The parsing service extracts what is visible, normalizes only unambiguous values, validates a versioned JSON shape and field rules, and stores source values separately from user corrections. It cannot certify authenticity, document ownership, identity validity or eligibility for restricted features. Do not call the extraction result an `autoReport` approval; that term belongs to the previous validation proposal.

The client never calls the model directly, receives provider credentials, or supplies a URL for a worker to fetch. A job references an authorized ready capture ID and evidence version. The backend resolves storage references internally. The model cannot select another account's evidence or update account identity attributes.

## Flow and execution

1. The backend onboarding orchestrator consumes the durable capture-ready event and creates a parse job with an idempotency key for that evidence/configuration. The opted-in capture flow authorizes this parsing handoff; it does not authorize validation. Persist job and dispatch intent atomically. The same logical request returns its existing job; explicit reprocessing creates a new attempt only when server policy permits.
2. Pin a parser configuration version containing provider/model identifier, prompt, image preprocessing and schema versions. Job metadata holds these trusted values; model-generated metadata is not authoritative.
3. A queued worker obtains a conditional lease and checks cancellation, evidence availability and lifecycle policy. Fetch the precise original/derivative versions from the manifest, verify integrity, and label required sides in the model request.
4. Invoke a vision-capable model with extraction-only instructions and schema-constrained output where supported. Treat printed text as data, never as commands. Disable tools, external browsing and untrusted URL retrieval for this task. The model's response is untrusted input even when schema-constrained.
5. Enforce response size/schema, field lengths, supported types, nullable missing values and normalization rules. Bound malformed-output retries. Unreadable images or ambiguous critical content return recapture/review outcomes rather than invented facts.
6. Persist the immutable extraction and its provenance, then conditionally publish a successful result using the lease/generation. A stale worker cannot overwrite a newer attempt or current capture pointer. Publish after verifying the capture is still eligible; deletion/cancellation fences late results.
7. The authenticated client fetches status/result, displays fields and warnings, and submits corrections with the expected extraction and review revisions. The backend loads the original extraction itself; it does not trust an `extracted` object echoed by Android.
8. Confirm the review revision and return “Document details saved.” Save correction attribution and original values separately. This finishes the optional document-data portion of onboarding, with no call to ID validation in this iteration.

## Separate state tracks

| Record | States | Meaning |
| --- | --- | --- |
| Parse job | `queued`, `running`, `succeeded`, `requires_recapture`, `failed`, `cancelled` | `succeeded` means usable, schema-validated extraction exists, possibly with field warnings. |
| Review | `not_started`, `draft`, `confirmed` | Confirmation belongs to an exact extraction/review revision; it is not a parse-job state or identity decision. |

Availability/deletion/supersession is tracked separately from immutable historical outcomes. A new model version or new capture does not inherit an old review confirmation. Only the explicitly selected current capture/result can advance the current onboarding document step. A reparse of identical evidence still creates a new extraction identity and requires fresh review if promoted.

## Errors and retry policy

- Rate limits, network interruptions and temporary provider errors: bounded exponential backoff with jitter; a DLQ/failed state after the budget. Respect provider retry instructions and per-account/model concurrency budgets.
- Syntactically invalid JSON, schema mismatch, refusal or truncated output: safe typed failure; optionally one controlled repeat under policy. Never loop indefinitely trying to repair output or fabricate missing data.
- Unreadable/unsupported images: `requires_recapture` or a supported-document guidance error. Do not retry the same unreadable image endlessly.
- Partial extraction: allow review where required fields can be supplied/corrected under policy; clearly distinguish user-supplied values from extracted ones. Contradictions remain warnings requiring resolution, not silent model reconciliation.
- Lost job-create/review-save response: reconcile by stable operation key/revision; do not start a second paid job or overwrite another device's edits blindly.
- Worker crash after provider invocation: at-least-once execution can cause another paid invocation if no durable result exists. Guarantee one authoritative result through conditional publication; do not promise exactly-once provider billing without provider idempotency support.

Use bounded request timeouts. The API returns a job handle rather than keeping a mobile request open for model inference. Foreground clients poll with backoff/server hints and a bounded active wait, then show “Still processing; return later.” Re-entry retrieves the same job. Push notifications, if added later, contain no personal fields or evidence URLs.

## Privacy and evaluation

Keep evidence reads server-side. A provider adapter can send bytes or use supported scoped storage access; never make the bucket public merely because a model accepts image URLs. Approve provider retention/training terms, region/routing and data-processing purpose before enabling real documents. Model input/output and image logging are disabled/redacted unless an explicit reviewed retention/access policy permits them.

Evaluate with permitted representative samples for each enabled document type, jurisdiction, language and capture condition. Track exact-match accuracy by field, missing/ambiguous handling, hallucinated values, cross-side contradictions, recapture rates, latency and cost. Include accents, multiple surnames, leading zeros, glare and low-light samples. Schema validity is measured separately from factual accuracy. Model-reported confidence is not a calibrated approval threshold. No production model/policy is selected solely from an attractive demo.

## Acceptance criteria

- Only account-owned ready evidence can start/read a job; caller-supplied storage paths and model configuration cannot bypass policy.
- Duplicate dispatch, concurrent workers, cancellation, deletion and stale completions publish at most one applicable result.
- Missing text yields explicit null/reason; document numbers retain leading zeros; ambiguous dates are not guessed.
- Embedded instructions in images cannot trigger tools, change the schema, select other evidence, or influence account authorization.
- Corrections remain separate; stale review revisions fail with conflict; original extraction cannot be replaced by a client payload.
- Jobs and confirmed reviews resume after app restart; parsing completion never sets validation status to approved.
