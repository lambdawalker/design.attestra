# Stitch brief: passkey login and email-code fallback

Read [shared auth DESIGN.md](../DESIGN.md) first. Generate responsive website views and corresponding native mobile layouts from the [login architecture](architecture.md). Login is passkey first after email entry, with email OTP as a visible fallback. Do not generate password fields, third-party social login buttons, or a Cognito-hosted redirect.

## One-line Stitch prompt

> Design a focused sign-in experience for an existing user on the app and website domain. Ask for email, offer a platform passkey prompt, and allow Use an email code instead when the prompt is cancelled or unavailable. Keep the user informed with quiet inline status, neutral account-existence wording, and a reliable recovery path. Follow the shared DESIGN.md and never claim identity or address verification from signing in.

## Screens and variants

| Screen | Required visual content | Primary action | Secondary / failure states |
| --- | --- | --- | --- |
| 1. Sign in | Heading “Sign in”; editable email field; one-line explanation of passkey | Continue with passkey | Use an email code instead; invalid email, generic service failure |
| 2. Platform passkey handoff | Non-imitative waiting state; device/password-manager prompt belongs to the OS/browser | Native/browser passkey approval | Cancel returns with email retained; challenge unavailable → email code; timed-out challenge → retry |
| 3. Check your inbox | Same email retained, clear request status and where code is entered | Continue to code | Change email; delivery/rate-limit message; do not promise delivery from a generic pre-auth response |
| 4. Enter email code | Single accessible OTP input with code autofill/paste, visible email address | Verify and sign in | Wrong/expired code inline; request a new code; preserve focus and avoid revealing account existence |
| 5. Signed in | Quiet completion and return to originally requested feature; authenticated status only | Continue | If the feature needs identity/address assurance, explain the separate next step without claiming the login fulfilled it |

## Interaction details

- Begin passkey auth through `POST /auth/passkey/start`; hand `CREDENTIAL_REQUEST_OPTIONS` to the actual browser/native credential manager. Submit its assertion with the opaque session to `POST /auth/passkey/complete`.
- On cancellation, offer **Use an email code instead**. Starting email OTP calls `POST /auth/email/start`; entering the code calls `POST /auth/email/complete` with the matching session. An expired challenge starts fresh rather than replaying an old session.
- Do not show a distinctive “email does not exist” state. Phrase recoverable failures around the action: “We couldn't finish sign-in. Try again or use an email code.”
- Use the one-accent shared design system; text states and controls communicate outcomes without constant motion. Reduced-motion and large-text variants must keep the fallback reachable.
- Desktop layout may place short security reassurance beside the form. Mobile is one column; keep the OTP form usable while the keyboard is open and every interactive target at least 44px high.

## Review checks for Stitch output

1. No password or Cognito domain appears.
2. The passkey prompt is presented as an OS/browser action, not a hand-drawn biometric approval dialog.
3. OTP fallback can be reached without completing or denying a passkey challenge.
4. Login success is not labeled identity or address verification.
5. Error, slow network, offline, cancellation, reduced-motion, and screen reader states are explicit.
