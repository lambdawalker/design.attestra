# Onboarding UI references

Screens are grouped under [email confirmation](../email-confirmation/README.md), [passkey creation](../passkey-creation/README.md), [ID capture](../id-capture/README.md), and [ID parsing](../id-parsing/README.md). The loading view and logo are shared. Some parsing references retain historical paths beneath id-capture.

These are visual HTML prototypes from the supplied onboarding archives. The six original PNGs remain for reference; the latest ZIP includes some empty image placeholders and screenshots with sample identity data, so its corrected views are included as HTML only. Prefer the HTML for revised wording. None of these prototypes performs a real backend request, passkey registration, or identity decision. Use the [architecture](../architecture.md) for security and transitions and the [Stitch brief](../stitch.md) for the shared visual and loading states.

| Screen | Textual specification | Role |
| --- | --- | --- |
| Email verification - start | [Spec](../email-confirmation/ui-reference/email_verification_start/spec.md) | Entry and generic signup response |
| Email verification - wait | [Spec](../email-confirmation/ui-reference/email_verification_wait/spec.md) | Waiting for a link; resend or change email |
| Email verification - manual code input | [Spec](../email-confirmation/ui-reference/email_verification_manual_code_input/spec.md) | Empty six-digit fallback form when local signup context is unavailable |
| Email verification - incorrect code | [Spec](../email-confirmation/ui-reference/email_verification_incorrect_code/spec.md) | Correct and retry the entered code |
| Email verification - attempt limit | [Spec](../email-confirmation/ui-reference/email_verification_attempt_limit/spec.md) | Request a new email when permitted; show server cooldown when limited |
| Email verification - unusable link | [Spec](../email-confirmation/ui-reference/email_verification_link_unusable/spec.md) | Request a new email; never retry the expired/replaced link |
| Onboarding - processing | [Spec](onboarding_loading/spec.md) | One reusable wait view for all active backend and processing work |
| Passkey setup - start | [Spec](../passkey-creation/ui-reference/passkey_setup_start/spec.md) | Start platform passkey setup |
| Passkey setup - failed | [Spec](../passkey-creation/ui-reference/passkey_setup_failed/spec.md) | Retry or continue without a passkey |
| Passkey setup - unsupported device | [Spec](../passkey-creation/ui-reference/passkey_setup_unsupported_device/spec.md) | Continue without a passkey; recheck only if capability changes |
| Identity verification - start | [Spec](../id-capture/ui-reference/identity_verification_start/spec.md) | Historical start layout; current capture entry or account exit |
| Identity verification - review details | [Spec](../id-capture/ui-reference/identity_verification_review_details/spec.md) | Parsing-owned review after asynchronous extraction |
| Identity verification - submission failed | [Spec](../id-capture/ui-reference/identity_verification_submission_failed/spec.md) | Historical failure layout; use task-specific capture/review recovery |
| Identity verification - unreadable document | [Spec](../id-capture/ui-reference/identity_verification_document_unreadable/spec.md) | Parsing-owned unreadable outcome; return to capture |
| Identity verification - success | [Spec](../id-capture/ui-reference/identity_verification_success/spec.md) | Deferred standalone ID-validation reference; never capture/parsing success |

The earlier [ID processing reference](../id-capture/ui-reference/identity_verification_reading_document/spec.md) remains as an archived visual example. Implement its wait state with the shared loading view above. Source HTML uses some remote assets and demo click handlers; replace them in production. The [logo](logo.svg) is a reference asset.

## Shared loading view

Use the same title, spinner icon, and card layout whenever the app is waiting on the backend or a processing task. **Change the title, card text, optional context row, and screen-reader status according to the active task.** The host sets `loading-title`, `loading-description`, `loading-help`, and `loading-icon` on the reusable view; the default email wording is just one example. Do not claim a fixed duration or invent a completion percentage. Show a retry or recovery action if the operation fails or times out. A task result, rather than animation, decides when to navigate.

| Active task | Title | Card text | Completion or recovery |
| --- | --- | --- | --- |
| Email confirmation with A+B or submitted B+C | Verifying your email | We are confirming your email. This may take a moment. | Only proceed to passkey setup after the authenticated session is available. If confirmation completed without a session, use email sign-in recovery. |
| Request a new confirmation email | Requesting another email | We are processing your request. | Give a neutral response; respect resend limits and advise opening the newest email. |
| Start passkey registration | Opening your passkey manager | Follow your device or password manager to create a passkey. | Return to setup on cancellation; display passkey success only after server registration. |
| Finish passkey registration | Saving your passkey | We are adding this passkey to your account. | Show “Passkey added” only after the server confirms completion. |
| Finalize uploaded capture | Preparing your document | We are preparing your uploaded photos. | Ready evidence enters parsing; invalid images require recapture. |
| Parse ready evidence | Reading your document | We are extracting details for you to review. | Show review after validated extraction, or pending/recapture/retry as appropriate. |
| Save reviewed details | Saving your document details | We are saving your corrections. | Reconcile the exact review revision; completion is details saved, not identity approved. |
| Standalone ID validation | Deferred from onboarding | Historical provider-wait reference only. | Do not invoke or show this state as part of capture/parsing. |

Show loading only for genuine in-flight work. Do not display it while a person is reading instructions or editing a field. Do not freeze the UI thread. Avoid a permanent spinner: each task needs a bounded timeout or pending state with a safe path away. Treat retry actions as new user actions and respect transaction limits.

## Coverage and outstanding variants

- The email template is still needed: link B and separate six-digit C, expiration guidance, and no C in the link or preview.
- Identity success/failure variants belong to deferred ID validation. Capture/parsing need photo preview, upload recovery, long-running pending, partial extraction, review conflict and details-saved variants. The supplied unreadable screen is a parsing recapture outcome, not identity rejection.
- Capture owns permissions/photos and S3 evidence finalization. Parsing owns extraction, field review and saved corrections. The host coordinates the subfeatures and resume behavior; see their current UI pages.
- Incorrect code, exhausted code attempts, expired link, save interruption, and passkey interruption are separate recoveries. Failed C attempts are limited per generation and across resends; a resend cannot bypass an account-level cooldown. Never promise a fixed 24-hour wait unless returned by the backend.
- Only the client that completes A+B or B+C confirmation receives a session. The “Change email address” action on the waiting screen must not sign in a different device by polling status.
- Passkey and identity checks are separate from email verification. “Do this later” preserves the account; passkey deferral uses the documented email sign-in route. Show a passkey success row only when the backend confirms registration.
