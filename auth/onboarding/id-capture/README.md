# ID capture — onboarding subfeature

[Architecture](architecture.md) · [Flow](flow.md) · [AWS design](aws.md) · [UI](ui.md) · [Shared contracts](../id-evidence-contracts.md) · [Implementation sequence](../id-evidence-plan.md)

**Status: designed here and implemented in backend/Android source. Live capture is disabled by default; source implementation does not establish real-device/S3 verification.**

See [backend API and operations](https://github.com/lambdawalker/go.attestra.aws.auth/blob/main/docs/id-capture.md), [Android integration](https://github.com/lambdawalker/android.attestra.auth/blob/main/docs/identity-capture.md), and the [evidence ledger](../../../docs/compatibility.md).

ID capture obtains document photos, lets the user review them, uploads them to private S3 storage, and finalizes a complete, immutable evidence manifest. It ends at `capture.ready`. It does not extract personal fields or decide whether an identity is valid.

The next onboarding subfeature is [ID parsing](../id-parsing/README.md). [ID validation](../../../verification/id-validation/architecture.md) is a separate feature and is outside this work.

Android uses Apexfission [permissions](https://github.com/lambdawalker/android.apexfission.permissions) and [card detector](https://github.com/lambdawalker/android.apexfission.carddetector) behind a capture adapter. Detection finds a card; it does not establish its side, authenticity, or owner. Other clients implement the same capture/upload contract with their platform APIs.

Existing `ui-reference/identity_verification_*` filenames are retained for link compatibility. [UI ownership](ui.md) explains which references belong to capture, parsing, or deferred validation; historical names do not define feature boundaries.
