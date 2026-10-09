# ID capture UI

[Capture flow](flow.md) · [Parsing UI](../id-parsing/ui.md) · [Shared layout](../stitch.md)

| Screen | Responsibility and action |
| --- | --- |
| Capture introduction | Optional document submission; explain purpose and supported types. Start or return to account. Do not promise identity verification. |
| Permission and camera | Apexfission permissions/detector integration on Android. Show required side, framing/glare guidance, cancel and Settings recovery. |
| Photo preview | Confirm the requested side and visible details; use photo or retake. |
| Upload progress | Real transferred-byte progress per slot, retry/renewal, and a safe exit. Never invent parsing percentages. |
| Finalizing | Shared processing view: “Preparing your document.” Long-running work becomes resumable pending status. |
| Capture failure | Distinguish missing upload/network failures from invalid images; preserve completed slot state where policy permits. |
| Capture ready | Advance to parsing/status; never show an identity-approved badge. |

Historical references remain at their existing paths. The [start view](ui-reference/identity_verification_start/code.html) provides layout only; replace its verification wording for capture. The [submission-failed view](ui-reference/identity_verification_submission_failed/code.html) can inform upload/finalize recovery, with task-specific copy and status reconciliation.

The [review-details](ui-reference/identity_verification_review_details/code.html), [reading-document](ui-reference/identity_verification_reading_document/code.html), and [unreadable-document](ui-reference/identity_verification_document_unreadable/code.html) references are now owned conceptually by ID parsing. The [identity-success reference](ui-reference/identity_verification_success/code.html) belongs only to the deferred standalone ID-validation feature. File location is historical, not ownership.

Camera/preview/upload/pending variants need dedicated designs before visual acceptance. This architecture change does not claim new mockups exist. Keep accessibility, screen-reader status, permission denial, rotation, and process-loss recovery in the implementation acceptance checklist.
