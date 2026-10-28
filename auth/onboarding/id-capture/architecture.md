# ID capture architecture

**Status: planned.** Part of [onboarding](../architecture.md); depends on an authenticated account. [Shared contracts](../id-evidence-contracts.md) define the handoff to [ID parsing](../id-parsing/architecture.md). This design supersedes the earlier combined capture/extraction/provider proposal.

## Responsibility and success condition

Capture owns document selection, camera access, photo acquisition and review, private upload, file validation, and freezing the evidence manifest. Success means every required image is present and safely decodable, with exact storage versions bound to one account and capture. It does not attest that the document is genuine or that the account holder owns it.

The client presents a backend-supplied document policy: supported document types/jurisdictions, required image slots, format/size limits, and policy version. The initial two-sided-card workflow uses `front` and `back`; do not hardcode these as universal requirements for passports or future documents. A client-supplied document type/country is a claim, not an authoritative classification. Production policy entries remain disabled until the initial document set is selected and evaluated.

## Boundaries

| Component | Owns | Must not do |
| --- | --- | --- |
| Capture adapter | Permission, camera session, crop, orientation, preview, retake, bitmap cleanup | Upload with permanent AWS credentials or declare identity validity |
| Onboarding client | Authenticated capture session, upload progress/retry, finalization, resume | Choose arbitrary S3 keys, versions, or account ownership |
| Capture API | Ownership, policy, upload authorization, state transitions, immutable manifest | Trust client completion or MIME type without validation |
| Capture worker | Decode/validate pinned images, create processing derivatives, mark ready or recapture | Start parsing incomplete images or change a frozen evidence manifest |
| ID parsing | Consume only a ready manifest | Read an unpinned latest object or mutate capture evidence |

The capture API may initially live in the Go auth repository, but use a separate domain/package and IAM permissions from email/passkey operations. Storage stays application-owned and keyed to the authenticated Cognito account; no document state belongs in Cognito attributes.

## Capture lifecycle

| State | Meaning and next actions |
| --- | --- |
| `uploading` | Session exists. Upload/replace unfinished slots, renew upload instructions, finalize, cancel, or expire. |
| `finalizing` | Server has atomically frozen exact object versions. Validate asynchronously; repeated finalization returns the same operation. |
| `ready` | All required pinned assets validated; immutable manifest is available to parsing. |
| `requires_recapture` | Permanent image/slot validation failure. Explain the affected slot; replacement starts a new capture. |
| `failed` | Infrastructure validation failure after bounded retries; a server-authorized retry revalidates the same frozen versions. |
| `cancelled` / `expired` | No further processing/publication. Start a new session if desired. |

Only the service transitions state. Retries cannot turn a ready capture back into an editable upload. `ready` evidence can later be superseded or deleted through separate lifecycle metadata; neither action rewrites its historical identity.

## Acquisition and upload

1. The authenticated client obtains policy and creates a capture with a stable idempotency key. The server binds account, capture ID, evidence version, policy version, required slots, and expiry. Lost create responses can be reconciled by that key.
2. Capture and preview each required side. Normalize orientation before stripping unnecessary EXIF metadata. Quality checks for glare, blur, missing corners and tiny text are user assistance, not authenticity checks. Keep images in protected app memory for the initial Android implementation; no gallery export or saved-state bundle.
3. For each confirmed photo, calculate SHA-256 and length. Request a short-lived upload instruction for that slot. The service allocates an opaque unique key per upload attempt and signs the necessary headers. Renew an expired instruction only after reauthenticating and checking session state.
4. Upload directly to S3 with the specified method/headers. Keep Cognito/API Authorization headers off the S3 request: the signature supplies upload authorization. Do not forward credentials or upload redirects to another host. The client can report progress and retry an unchanged photo, but server inspection establishes completion.
5. Finalize only after all required uploads appear complete. The API checks ownership and slots, resolves each registered upload to an S3 VersionId/checksum/size, and conditionally freezes that exact manifest. Missing/incomplete slots leave the session uploadable with a safe recovery response. Duplicate finalization returns the same manifest/operation.
6. A durable validation job reads those exact versions, enforces file/decode/dimension limits, and writes any normalized derivative under a worker-only prefix. Validation succeeds atomically as `ready` or records a recoverable/permanent failure. No parsing job reads an unvalidated upload.
7. Publish a durable `capture.ready` outbox event with the ready transition. A backend onboarding orchestrator requests parsing idempotently for this opted-in document flow, even if the app has closed. Capture itself has no model or provider dependency; the orchestrator owns the dependency on parsing. Resume/status can reconcile a delayed handoff.

## Immutability and races

Use S3 Versioning and pin the exact VersionId of every original and derivative. Checksums alone are not pointers. A previously issued upload URL can remain usable after finalization; a new upload may create a later S3 version, but it must not change the frozen manifest or what workers read. Client upload principals cannot delete versions or write processing results. Versions selected for finalization must be validated against the declared checksum and policy using version-specific reads.

Retakes before finalization create a new upload attempt/slot reference, so a slow old upload cannot replace a newer selection. Finalization conditionally checks the capture revision and selected upload IDs. Retakes after finalization create a new capture/evidence version. Concurrent capture sessions retain independent records; promotion to the account's current onboarding evidence uses an expected revision so an old completion cannot overwrite a newer choice.

## Recovery and privacy

Persist opaque identifiers, slot progress, and idempotency keys in account/environment-scoped protected client storage. Restore authentication before retrieving server status. For the current memory-only Android capture, process death loses unuploaded images: resume server-confirmed uploaded slots and recapture missing slots; if necessary abandon the draft and start a new capture. Do not claim transparent background upload persistence without an explicitly designed encrypted local evidence cache.

Cancellation is an authenticated, idempotent backend state transition, not merely closing the UI. Leaving the screen permits an already-finalized job to continue; expose its status on return. Cancellation/expiry fences late work from publishing and makes late uploads cleanup candidates. An issued URL is not assumed individually revocable; expiry and cleanup handle residual upload ability.

Use private encryption-protected storage, TLS, minimal access, no raw images/URLs in logs, and no document content in error text. Define consent/purpose, retention, deletion and region policy before production; see [AWS design](aws.md). Account switching clears in-memory evidence and never reuses another account's checkpoint.

## Acceptance criteria

- Cross-account create/status/finalize/upload-renewal cannot access another capture; client-supplied ownership is ignored.
- Expired URLs can be renewed without restarting completed slots; checksum mismatch, excessive size, invalid decode, and missing sides cannot reach ready.
- Delayed uploads and post-finalization overwrites do not change the evidence read by validation/parsing.
- Duplicate finalize requests and crashes after freezing do not lose validation jobs or start duplicate logical jobs.
- Rotation, process death, cancellation, and session expiry have explicit recovery without logging or persisting raw images accidentally.
- Capture-ready never grants identity assurance or unlocks restricted features.
