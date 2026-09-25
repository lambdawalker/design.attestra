# Onboarding UI references

These are visual HTML prototypes from the supplied onboarding archives. The six original PNGs remain for reference; the latest ZIP includes some empty image placeholders and screenshots with sample identity data, so its corrected views are included as HTML only. Prefer the HTML for revised wording. None of these prototypes performs a real backend request, passkey registration, or identity decision. Use the [architecture](../architecture.md) for security and transitions and the [Stitch brief](../stitch.md) for the shared visual and loading states.

| Screen | HTML | Role |
| --- | --- | --- |
| Start with your email | [Open](start_with_your_email/code.html) | Entry and generic signup response |
| Check your email | [Open](confirm_verification/code.html) | Waiting for a link; resend or change email |
| Complete email verification | [Open](complete_email_verification/code.html) | Empty six-digit fallback form when local signup context is unavailable |
| Incorrect confirmation code | [Open](email_code_incorrect/code.html) | Correct and retry the entered code |
| Too many code attempts | [Open](email_verification_attempts_exhausted/code.html) | Request a new email when permitted; show server cooldown when limited |
| Confirmation link unusable | [Open](confirmation_link_unusable/code.html) | Request a new email; never retry the expired/replaced link |
| Shared loading | [Open](processing_verification/code.html) | One reusable wait view for all active backend and processing work |
| Create passkey | [Open](create_passkey/code.html) | Start platform passkey setup |
| Passkey setup interrupted | [Open](passkey_setup_retry/code.html) | Retry or continue without a passkey |
| Passkeys unavailable | [Open](passkey_setup_unsupported_device/code.html) | Continue without a passkey; recheck only if capability changes |
| Ready for next step | [Open](ready_for_next_step/code.html) | Optional identity check or dashboard |
| Review ID details | [Open](verify_id_details/code.html) | Correct extracted details after the capture plugin returns |
| ID submission interrupted | [Open](error_saving_id_details/code.html) | Retry the submission or leave for dashboard |
| Document images unreadable | [Open](id_document_unreadable/code.html) | Reopen plugin to retake images |
| Identity check complete | [Open](identity_check_success/code.html) | Show a completed identity result only when returned by the identity service |

The earlier [ID processing reference](processing_id_document/code.html) remains as an archived visual example. Implement its wait state with the shared loading view above. Source HTML uses some remote assets and demo click handlers; replace them in production. The [logo](logo.svg) is a reference asset.

## Shared loading view

Use the same title, spinner icon, and card layout whenever the app is waiting on the backend or a processing task. **Change the title, card text, optional context row, and screen-reader status according to the active task.** The host sets `loading-title`, `loading-description`, `loading-help`, and `loading-icon` on the reusable view; the default email wording is just one example. Do not claim a fixed duration or invent a completion percentage. Show a retry or recovery action if the operation fails or times out. A task result, rather than animation, decides when to navigate.

| Active task | Title | Card text | Completion or recovery |
| --- | --- | --- | --- |
| Email confirmation with A+B or submitted B+C | Verifying your email | We are confirming your email. This may take a moment. | Only proceed to passkey setup after the authenticated session is available. If confirmation completed without a session, use email sign-in recovery. |
| Request a new confirmation email | Requesting another email | We are processing your request. | Give a neutral response; respect resend limits and advise opening the newest email. |
| Start passkey registration | Opening your passkey manager | Follow your device or password manager to create a passkey. | Return to setup on cancellation; display passkey success only after server registration. |
| Finish passkey registration | Saving your passkey | We are adding this passkey to your account. | Show “Passkey added” only after the server confirms completion. |
| Return from ID capture plugin | Reading your document | We are extracting details for you to review. | Open ID review after extraction; offer plugin retake/recovery if unreadable. This is not an identity decision. |
| Submit reviewed ID details | Submitting your ID details | We are sending your reviewed details for an identity check. | Avoid duplicate submissions; on timeout reconcile server state before retrying. |
| Wait for identity provider | Checking your identity | Your details have been submitted. We will show the result when it is available. | If processing continues, show pending with a dashboard exit. Approval or failure comes from the actual provider result. |

Show loading only for genuine in-flight work. Do not display it while a person is reading instructions or editing a field. Do not freeze the UI thread. Avoid a permanent spinner: each task needs a bounded timeout or pending state with a safe path away. Treat retry actions as new user actions and respect transaction limits.

## Coverage and outstanding variants

- The email template is still needed: link B and separate six-digit C, expiration guidance, and no C in the link or preview.
- The new identity success view is valid only after the identity service approves. A **final unsuccessful identity decision** still needs its own result variant with a dashboard exit and retry only if permitted. The supplied “Document images unreadable” screen is a capture retry, not that decision. The shared loading view covers in-progress checks.
- The capture plugin owns camera permissions, front/back capture, and quality flow. Attestra handles plugin launch, cancel/error, return data, and the review and result screens.
- Incorrect code, exhausted code attempts, expired link, save interruption, and passkey interruption are separate recoveries. Failed C attempts are limited per generation and across resends; a resend cannot bypass an account-level cooldown. Never promise a fixed 24-hour wait unless returned by the backend.
- Only the client that completes A+B or B+C confirmation receives a session. The “Change email address” action on the waiting screen must not sign in a different device by polling status.
- Passkey and identity checks are separate from email verification. “Do this later” preserves the account; passkey deferral uses the documented email sign-in route. Show a passkey success row only when the backend confirms registration.
