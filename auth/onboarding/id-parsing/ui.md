# ID parsing UI

Use the [shared onboarding design](../stitch.md) and [processing view](../ui-reference/onboarding_loading/code.html).

| View | Copy/action and boundary |
| --- | --- |
| Queued/running | “Reading your document.” Give a leave/resume option; switch to pending after bounded foreground waiting. |
| Long-running pending | “Your document is still processing.” Check status or return to account; do not promise a duration. |
| Unreadable | Identify affected side where available; start a new capture. No identity rejection wording. |
| Technical failure | Safe failure text with server-permitted retry; reconcile before creating new work. |
| Review | Display extracted fields, missing/ambiguous values, cross-side warnings and clearly attributed edits. Allow recapture. |
| Save conflict | Preserve unsaved local edits, load the current review revision, and ask the user to resolve differences. |
| Confirmed | “Document details saved.” Continue onboarding/account; no verified badge or identity-success screen. |

The existing [review details](../id-capture/ui-reference/identity_verification_review_details/code.html), [unreadable](../id-capture/ui-reference/identity_verification_document_unreadable/code.html), and [reading](../id-capture/ui-reference/identity_verification_reading_document/code.html) HTML files are layout references retained at historical paths. Their identity-oriented labels are superseded by this page. Dedicated partial-extraction, pending, conflict and saved-details variants remain UI work.

Do not imply the model saw user-supplied values. Preserve raw text where useful for resolving ambiguity, but avoid unnecessary full document-number exposure outside focused review. Error messages, notifications, analytics and background previews contain no document content. Mock runs must show synthetic extraction and never masquerade as a real parsed ID.
