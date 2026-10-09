# ID parsing AWS design

**Planned.** [Architecture](architecture.md) defines behavior; [capture AWS](../id-capture/aws.md) owns evidence storage. No model/provider is declared production-ready by this plan.

| Component | Responsibility |
| --- | --- |
| Authenticated Go API | Create/get parse jobs, retrieve safe extraction, save/confirm review revisions |
| DynamoDB parsing/review records | Immutable result identity, operation keys, job states/leases, review revisions and current selection |
| Transactional outbox + dispatcher | Atomically persist job creation and dispatch intent; sweep undispatched intent for recovery |
| SQS parse queue + DLQ | Backpressure, retry delivery, operational isolation from capture validation |
| Parsing worker | Fetch pinned evidence, invoke model adapter, validate output, conditionally store result |
| Vision model adapter | Provider-specific images, schema support, errors, timeouts and usage accounting |

Amazon Bedrock is an initial integration candidate to keep invocation under AWS service roles. Keep the adapter replaceable and select an actual vision-capable model/region only after checking supported images, structured output, data handling and measured accuracy for the enabled document set. A provider without native schema enforcement still requires the same backend validator; JSON-only prompting is not equivalent to constrained output. A non-AWS provider requires reviewed credential storage, network egress, retention and regional processing policy.

The worker has scoped read access to ready evidence versions, model invocation rights for approved models, and write access only to its parsing records/results. It has no user-management, email, arbitrary URL-fetch or validation-approval capability. Keep S3/model service region and any cross-region inference routing within the approved data residency policy.

Configure queue visibility, worker timeout, lease renewal and model timeout together. Expired leases can be reclaimed with a new fencing generation; prior workers cannot publish. Never tie worker lifetime to an Android HTTP request. Provider throttling obeys bounded backoff/concurrency limits; a DLQ and stuck-job sweep expose terminal failures with safe retry actions. A deletion/cancellation fence must be checked again before publishing results, even if a provider call could not be cancelled.

Record operational metrics for queue age, duration, model usage/cost, throttles, retry counts, recapture rate and schema failures. Use opaque correlation IDs; do not log prompts, image bodies, signed URLs, extracted fields or corrections. Bedrock invocation logging can copy input images/documents into S3 when configured; review and disable inappropriate body/image logging rather than assuming evidence lives in only one bucket.

Retain confirmed extraction/review data only under the approved policy. Deletion covers original/derived images, S3 versions, extraction records, optional raw responses, backups/replicas where applicable, and any provider-side retention obligations. Cleanup must fence active jobs so deleted evidence cannot be recreated by late results. Lifecycle policies complement application deletion; they do not replace authorization or an auditable deletion workflow.

## References

- [Bedrock structured outputs](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)
- [Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [Textract AnalyzeID scope](https://docs.aws.amazon.com/ai/responsible-ai/textract-analyzeid/overview.html): potential benchmark for supported US documents, not assumed coverage for other jurisdictions.
