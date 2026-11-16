# ID capture UI

[Capture flow](flow.md) · [Parsing UI](../id-parsing/ui.md) · [Shared layout](../stitch.md)

| Screen | Responsibility and action |
| --- | --- |
| Capture introduction | Policy-controlled document submission; explain purpose and supported types. Offer skip only when optional; required capture blocks onboarding completion. Do not promise identity verification. |
| Permission and camera | The live host uses `IdentityCameraAfterDisclosure` only after the capture policy/disclosure check. Request Android permission directly if needed. Preserve denial, explicit retry/cancel, Settings recovery, grant recheck and no-camera handling. The standalone `IdentityCamera` entry remains explanation-first. |
| Photo preview | Confirm the requested side and visible details; use photo or retake. |
| Upload progress | Real transferred-byte progress per slot, retry/renewal, and a safe exit. Never invent parsing percentages. |
| Finalizing | Shared processing view: “Preparing your document.” Long-running work becomes resumable pending status. |
| Capture failure | Distinguish missing upload/network failures from invalid images; preserve completed slot state where policy permits. |
| Capture ready | Advance to parsing/status; never show an identity-approved badge. |

Historical references remain at their existing paths. The [start view](ui-reference/identity_verification_start/code.html) provides layout only; replace its verification wording for capture. The [submission-failed view](ui-reference/identity_verification_submission_failed/code.html) can inform upload/finalize recovery, with task-specific copy and status reconciliation.

The [review-details](ui-reference/identity_verification_review_details/code.html), [reading-document](ui-reference/identity_verification_reading_document/code.html), and [unreadable-document](ui-reference/identity_verification_document_unreadable/code.html) references are now owned conceptually by ID parsing. The [identity-success reference](ui-reference/identity_verification_success/code.html) belongs only to the deferred standalone ID-validation feature. File location is historical, not ownership.

Android owns executable previews and reviewed screenshot baselines for implemented states, including permission recovery. Historical central mockups are not replacements for those references. Keep accessibility, screen-reader status, permission denial, rotation, and process-loss recovery in the implementation acceptance checklist.

Only the attempt marker survives recreation; the actual OS grant is rechecked. Request on a resumed lifecycle, avoid duplicate requests, and never request access during processing or saved-details review. Native dialog dismissal, rotation during the prompt and manufacturer-specific denial behavior still need real-device smoke tests. See [Android PR #80](https://github.com/lambdawalker/android.apexfission.auth/pull/80).
