# Onboarding UI references and coverage

These six screen mockups and their HTML prototypes come from the supplied `onboarding_design.zip`. They are design references, not production views or evidence that the backend or clients implement the flow. The [architecture](../architecture.md) defines confirmation and session behavior; the [Stitch brief](../stitch.md) defines intended UI states. Source HTML contains placeholder content and external fonts, scripts, and images, so reuse requires local assets and production behavior.

| Supplied screen | Reference files | Intended place in the flow | Coverage |
| --- | --- | --- | --- |
| Start with your email | [Image](start_with_your_email/screen.png) · [HTML](start_with_your_email/code.html) | Email entry and signup | Main view present; invalid/submitting and generic result need state designs |
| Check your inbox | [Image](confirm_verification/screen.png) · [HTML](confirm_verification/code.html) | Await the email link | Main view present; resend cooldown, edit email, delayed delivery, and safe status copy need variants |
| Complete email verification | [Image](complete_email_verification/screen.png) · [HTML](complete_email_verification/code.html) | Manual B+C path after opening the link without A | Six-digit input matches the requirement; explanatory copy and mismatch/expiry/attempt-limit variants need design |
| Protect your account with a passkey | [Image](create_passkey/screen.png) · [HTML](create_passkey/code.html) | After an authenticated confirmation session | Main view present; cancellation, unsupported device, retry, and deferral need variants |
| Confirm your ID | [Image](ready_for_next_step/screen.png) · [HTML](ready_for_next_step/code.html) | Choice after email and passkey setup | Continue/skip view present; completed email/passkey statuses and deferred-passkey state need variants |
| Review Extracted ID Data | [Image](verify_id_details/screen.png) · [HTML](verify_id_details/code.html) | Identity verification after the capture plugin returns; this is a separate optional continuation | Review view present; host plugin handoff and submission/result states need design |

The supplied [logo](logo.svg) is a reference asset. The HTML prototypes use some remotely hosted images and fonts and should not be copied into an authentication page without replacing external dependencies.

## Pending screens and integration

1. **Verification email template:** Show the clickable link containing B and a separately printed six-digit C. The email must explain that C may be requested after opening the link; C must never appear in the link or previewable landing-page content. Include expiry and resend wording. The user will supply this missing design.
2. **Automatic verification:** When the link opens in the initiating client with A, show “Verifying your email…” while A+B and the session exchange run asynchronously, then advance to passkey setup after success. Provide a failure/timeout action that can fall back to manual entry or resend. There is no separate confirmation tap on this path. The user will supply this missing screen.
3. **ID capture plugin handoff:** “Scan government ID” launches the selected plugin, which provides its own permission, camera, front/back capture, and quality flow. The host needs launch/cancel/error/return states and a defined data handoff before the supplied ID review. No custom Attestra capture screen is required; plugin integration is forthcoming. This is an optional identity continuation, not completion of email onboarding.

## Needed variants and corrections in supplied views

- **Manual verification:** The mockup's six-digit presentation is now the requirement. The screen is used when A is unavailable after a link containing B has opened; replace “if your link didn't open automatically” with this situation. Keep one accessible code input with a segmented six-slot presentation, paste/autofill, and an empty initial value. Show expired/replaced link, wrong code, attempt limit, and resend states. Only the explicit Verify action submits B+C.
- **Check inbox:** “Check verification status” must never grant a session or passkey setup based only on observing that another device confirmed the email. If retained, it can only update local informational state and instruct sign-in on this device. A generic signup 202 must not assert that an email was definitely sent. Provide resend cooldown and change-email actions.
- **Passkey:** The mockup has no visible “Do this later” path, while the architecture supports deferral and email OTP return. The platform credential picker is owned by the OS/browser; show retry and deferral after cancel or unsupported device. Do not show “Passkey added” until `POST /passkeys/complete` succeeds.
- **Ready for next step:** Add explicit “Email verified” and “Passkey added” status rows (or “Passkey not added” when deferred). The mockup claims ID scanning is required for specific signing and notice features; keep such claims conditional on a documented feature policy, while preserving “Skip for now” for account onboarding.
- **ID review:** The screen assumes a completed front/back scan supplied by the capture plugin. Use a separate identity verification progress indicator; its “5/5” label implies the review is part of mandatory onboarding. The sample identity and document data are placeholders. Do not imply that editing OCR output alone verifies the identity or that an address has been verified. Confirmed edits should be submitted to the actual identity verification workflow and receive an explicit result or pending state.
- **Design system:** These mockups use Attestra branding, a dark blue palette, and Inter. The existing [shared auth DESIGN.md](../../DESIGN.md) still specifies neutral branding, zinc/teal, and Geist. Treat the mockups as a proposed visual direction until the shared system is intentionally reconciled for onboarding and login together. Avoid unsupported legal or cryptographic claims in visible copy.

## Coverage boundary

The six supplied files represent primary views. The user will provide the missing email template and automatic verification view. Error/recovery variants, the capture plugin handoff, and identity verification outcome remain integration/design work. “Email confirmed,” “passkey registered,” and “identity verified” are separate backend outcomes. A person can skip the optional identity continuation without changing their authenticated account.
