# ID capture AWS design

**Planned infrastructure; not a deployment claim.** [Architecture](architecture.md) · [Shared contracts](../id-evidence-contracts.md). Pulumi configuration and exact IAM policies belong in the Go implementation repository.

## Components

| Service | Responsibility |
| --- | --- |
| Authenticated API Gateway + Go Lambda handlers | Policy, capture creation/status, upload authorization, finalization, cancellation |
| Private S3 evidence bucket with Versioning | Original uploads and normalized derivatives; separate upload and worker-only prefixes |
| DynamoDB capture records | Account ownership, policy/version, selected upload attempts, pinned manifest, revision, operation state and expiry |
| DynamoDB transactional outbox + dispatcher | Durable job intent written with the finalizing transition |
| SQS validation queue + dead-letter queue | Bounded retries and backpressure for image validation |
| Go validation worker | Exact-version download, safe decoding, limits, derivative creation, conditional ready/failure publication |

The outbox record and capture state change commit in one DynamoDB transaction, both when scheduling validation and when publishing the ready handoff. A dispatcher forwards pending work to SQS; marking dispatched is retryable and consumers deduplicate. Use a pending-outbox sweep to recover missed dispatches rather than depending solely on stream retention. S3 notifications are optional reconciliation signals, not the authority for complete document sets. They may be duplicated or out of order.

## Upload constraints

Presigned SigV4 PUT is the initial mobile transport. Sign the exact key, content type, checksum and required encryption headers. A starting proposal is five-minute URLs, 24-hour unfinished capture sessions, JPEG only, at most 4 MiB per slot and 20 megapixels after decoding; make these server policy values and verify them with device/model benchmarks before enabling production. Limits on format and decoded pixels are enforced by the worker, not trusted from metadata. Presigned PUT does not provide the same policy range mechanism as POST; if a hard pre-ingest content-length range is required, use a presigned POST policy or another upload control in the implementation. Always enforce measured stored size before processing and apply upload/account budgets.

Bucket requirements: Block Public Access, disabled ACL-based ownership, encryption at rest, TLS-only access, Versioning, and narrowly scoped IAM. Prefer a dedicated customer-managed KMS key when audit/access-control requirements justify it; model the worker/upload role permissions and key lifecycle together. Never put account emails or ID numbers in object paths. Clients receive upload instructions, not AWS keys or read/list privileges. Treat signed URLs as secrets and redact query strings from network instrumentation.

## Freeze before parsing

Finalization selects only registered upload keys, pins their VersionIds, and records checksum/size. Subsequent reads, validation and derivative generation use those exact versions. Only worker roles write derivatives; record their version/checksum and transformation version. Enforce checksum/length binding and validate decoded image content. A rewritten latest version is irrelevant to a frozen manifest.

Do not blindly expire noncurrent versions: a pinned version can become noncurrent after a late signed PUT. Retention/deletion must respect the manifest's referenced versions. A scheduled cleanup reconciles abandoned uploads, late uploads after cancellation/expiry, unused derivatives, and object versions no longer retained under policy. DynamoDB TTL is a cleanup aid, not an exact-time authorization boundary or evidence deletion guarantee.

## IAM and operational boundaries

- Upload signer: authenticate account; authorize specific upload operations; no document download API by default.
- Validation worker: read selected original versions and write derivatives; no Cognito mutations or unrestricted bucket access.
- Parsing worker: read validated/pinned processing assets only, through its scoped service role.
- Cleanup worker: narrowly scoped delete/version permissions after checking retention and active-job references.
- Support access: separate audited role and explicit purpose; no public evidence links.

Bind jobs to capture ID, evidence version and operation generation. Retry transient S3/KMS/worker failures with backoff; permanent unsafe/unsupported images require recapture. Conditional writes/leases prevent stale workers committing after cancellation or a newer generation. A sweeper detects stuck finalization and outbox/queue failures. Logs contain opaque request/job IDs and coarse outcomes, not image bytes, OCR fields, object URLs, or tokens.

## References

- [S3 presigned URL semantics and checksums](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- [S3 notification delivery and ordering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html)
- [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
