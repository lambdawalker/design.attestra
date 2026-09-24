# Stitch brief: email onboarding and passkey setup

Read [shared auth DESIGN.md](../DESIGN.md) first. Generate responsive website views and corresponding native mobile layouts for this flow. Use the [architecture](architecture.md) for state transitions. Screen mockups are design specifications, not proof that app/web clients have been implemented. Use a neutral editable product label; avoid invented logos, legal claims, bank branding, and identity approval badges.

## One-line Stitch prompt

> Design an app-domain email signup and passkey setup for a trusted digital service. Start with one email input. Send a branded verification email, open its HTTPS link in the app or website, wait for the user to tap Verify email, issue a session, then create a platform passkey. Finish by offering identity verification or Skip for now. Use the shared DESIGN.md palette and typography; include concise recovery and accessibility states. Never show Cognito-hosted UI or treat opening the link as confirmation.

## Screens and variants

| Screen | Required visual content | Primary action | Secondary / failure states |
| --- | --- | --- | --- |
| 1. Enter email | Left-aligned heading “Start with your email”; editable email field, one-sentence delivery explanation | Continue | Invalid email inline; submission in progress; generic result if email already exists |
| 2. Check your email | Masked or fully shown address according to privacy context, link/code arrival instructions; clear way to correct email | Open email app (only if supported) or return to app | Resend after rate-limit window, change email, delayed/delivery failure copy; never assert delivery merely from HTTP 202 |
| 3. Review verification link | On the app/website domain: email being verified, action summary, optional editable code fallback. Rendering has no side effect | Verify email | Expired code → resend; mismatch → retry; link opened elsewhere; already-confirmed account → email OTP login |
| 4. Create passkey | “Protect your account with a passkey”; concise explanation of device/password-manager choice and platform prompt | Create passkey | Platform cancellation, unsupported device, retry, **Do this later** with explicit email OTP return path |
| 5. Ready for next step | Separate status rows “Email verified” and “Passkey added”; invitation to submit ID later | Continue to identity verification | Skip for now; if passkey creation was deferred, show “Passkey not added” and re-entry action instead of a success state |

## Interaction details

- Step 3 is a review screen. Trigger `POST /confirm` **only after** the explicit user action. Link scanners and the system browser's GET cannot consume the code. On 409 `confirmed_sign_in_required`, move to the email OTP login recovery state rather than looping confirmation.
- Step 4 uses the browser/native credential UI. Do not draw a fake fingerprint or passkey approval modal. Loading should say “Opening your passkey manager” and allow a clear return path if the platform prompt is dismissed.
- After `POST /passkeys/complete` succeeds, show separate email and passkey status. A user may skip identity verification without losing access to features that do not require it. Do not imply a completed identity or address check.
- On native, deep links and the web route share wording and recovery behavior. The browser fallback stays on the application domain. On desktop, the form occupies a compact left column with a restrained right side explaining security only when space permits.
- Verify on small devices, large text, keyboard-only web navigation, reduced motion, screen reader announcements, OTP paste/autofill, and an offline or slow network state. Controls must remain at least 44px high.

## Content and state checks for generated screens

1. There is exactly one primary action per screen; the recovery action is visible and text-labeled.
2. The confirmation screen never says “verified” before `/confirm` succeeds.
3. Passkey and identity outcomes are not conflated. Skipped identity is shown as a later choice, not as failure.
4. Token values, OTP values, raw error messages, and full verification URLs are never used as mock decorative text.
5. Use names like “you” and realistic editable field labels; avoid fabricated user identities or unsupported trust numbers.
