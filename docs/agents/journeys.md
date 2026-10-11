# Journeys and failure recovery

Start at [onboarding](../../auth/onboarding/README.md). [Email confirmation](../../auth/onboarding/email-confirmation/flow.md) uses local proof A plus emailed B, or B plus separately displayed manual code C. A link fetch must not confirm an account. Generic signup acceptance does not prove delivery. Resend invalidates old material under server budgets. A lost successful confirmation response goes to sign-in recovery, not proof replay.

[Passkey creation](../../auth/onboarding/passkey-creation/flow.md) begins only with an authenticated session. The platform owns the credential picker/private key. Cancellation and unsupported devices retain email sign-in as the fallback. [Login](../../auth/login/architecture.md) and [resume](../../auth/onboarding/resume.md) are separate from initial confirmation.

[Capture](../../auth/onboarding/id-capture/flow.md) acquires photos, uploads to private S3 and freezes an exact-version manifest. Retry uncertain operations using the same operation identity and reconcile status. File validation can yield ready, recapture, failure, cancellation or expiry. [Parsing](../../auth/onboarding/id-parsing/flow.md) is the designed next feature: asynchronous model extraction, bounded JSON validation and revisioned review. It is not implemented by the current backend capture feature.

[ID validation](../../verification/id-validation/architecture.md) remains a separate deferred feature. A “details saved” or “capture ready” screen must never imply an identity-approved outcome. [Address verification](../../verification/address/architecture.md) has separate policy/provider decisions.

Implementation integration: [backend HTTP guide](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/api.md), [Android capture guide](https://raw.githubusercontent.com/lambdawalker/android.attestra.auth/main/docs/identity-capture.md), and [capture HTTP contract](https://raw.githubusercontent.com/lambdawalker/android.attestra.auth/main/docs/identity/http-contract.md). These guides change independently; consult the evidence ledger before claiming compatibility.
