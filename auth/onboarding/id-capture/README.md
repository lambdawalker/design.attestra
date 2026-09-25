# ID capture

This optional subfeature starts after the account is authenticated. The selected capture plugin owns camera permission and document capture; Attestra handles its launch, cancel/error/return states, extracted data review, submission, and status. The broader [identity verification architecture](../../../verification/identity/architecture.md) defines later identity decisions. See the [onboarding architecture](../architecture.md) and [development order](../order-of-development.md) for the handoff.

| Reference | Role |
| --- | --- |
| [Start or skip](ui-reference/identity_verification_start/code.html) | Begin the optional check or visit the dashboard |
| [Document reading](ui-reference/identity_verification_reading_document/code.html) | Archived visual; implement with shared processing layout |
| [Unreadable document](ui-reference/identity_verification_document_unreadable/code.html) | Reopen the capture plugin for a retake |
| [Review details](ui-reference/identity_verification_review_details/code.html) | Correct extracted fields before submission |
| [Submission failed](ui-reference/identity_verification_submission_failed/code.html) | Reconcile status, then retry if needed |
| [Success](ui-reference/identity_verification_success/code.html) | Show only after an approved identity result |

Use the [shared processing view](../ui-reference/onboarding_loading/code.html) for document extraction, submission, and provider waits. A final unsuccessful identity decision still needs its own reference; an unreadable image is a capture error, not a provider rejection.
