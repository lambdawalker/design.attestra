# Stitch brief: email onboarding and passkey setup

Read [shared auth DESIGN.md](../DESIGN.md) first. Generate responsive website views and corresponding native mobile layouts for this flow. Use the [architecture](architecture.md) for state transitions. Screen mockups are design specifications, not proof that app/web clients have been implemented. Use a neutral editable product label; avoid invented logos, legal claims, bank branding, and identity approval badges.

The supplied [screen references and coverage review](ui-reference/README.md) map the updated screen variants to this flow. They are visual references; use the architecture for security and state transitions.

**Revision:** Automatic confirmation in the original signup context, with manual email-code fallback when that context is unavailable. Backend and client implementation of this revision is pending.

## One-line Stitch prompt

> Design an app-domain email signup and passkey setup for a trusted digital service. Start with one email input. Send a branded email with a verification link and a separate verification code. When the link opens in the original signup context, show a brief verifying state and automatically advance to passkey setup after the server confirms. Otherwise show an empty code field and a Verify email button; the user enters the code from that same email and submits it. Both paths reach the same Create passkey screen. Finish with identity verification or Skip for now. Use shared DESIGN.md styling, recovery and accessibility states. Never show technical token names or Cognito-hosted UI.

## Screens and variants

| Screen | Required visual content | Primary action | Secondary / failure states |
| --- | --- | --- | --- |
| 1. Enter email | Left-aligned heading “Start with your email”; editable email field and one-sentence delivery explanation | Continue | Invalid email inline; submission in progress; generic result for existing addresses |
| 2. Check your email | Address according to privacy context; instructions to open the link and keep the email's code available if asked | Open email app, only if supported | Throttled resend, change email, delayed/delivery failure copy; never assert delivery merely from HTTP 202 |
| Email template | One verification link and a separately displayed verification code; explain that the code is needed if prompted after opening the link | Verify email link | Expiry and newest-email guidance; the code is text, not embedded in the link |
| 3a. Automatic verification | “Verifying your email…” with a restrained progress state while confirmation and session exchange run; no confirmation button | Automatic transition after successful confirmation/session issuance | Timeout/error recovery; code-entry variant if local proof is stale; expiry/resend; already-confirmed account recovery |
| 3b. Enter verification code | “Verify your email”; empty labeled six-digit “Verification code” input; “Enter the code from the email you just opened.” | Verify email | Wrong code, attempt limit, expired/replaced link, throttled resend, invalid-link state |
| 4. Create passkey | “Protect your account with a passkey”; concise explanation of device/password-manager choice and platform prompt | Create passkey | Platform cancellation, unsupported device, retry, **Do this later** with email OTP return path |
| 5. Ready for next step | Separate status rows “Email verified” and “Passkey added”; invitation to submit ID later | Continue to identity verification | Skip for now; if passkey creation was deferred show “Passkey not added” and a re-entry action |

Screens 3a and 3b are alternatives selected automatically, not consecutive steps. Users do not choose an authentication mode or need to understand why a code is requested.

## One shared loading view

Use [one reusable loading layout](ui-reference/onboarding_loading/code.html) for every in-flight backend call or processing task. Preserve the title, spinner icon, and card structure, but **change the title and card text for the actual task**. The host app supplies the title, description, optional context, and accessible status; the example email text is not universal. Use the screen for email confirmation, resend requests, passkey registration, ID extraction after the plugin returns, submission of reviewed ID details, and a pending identity-provider check. The exact copy and outcome mapping are in [the UI reference inventory](ui-reference/README.md).

Never claim fixed duration or show invented percentages. The server or processing task determines success; timeout and failure lead to their relevant retry screen, while a long-running identity check may show pending with a dashboard exit. Do not show the loading screen while a person is reading, editing, or waiting for an email to arrive.

## Interaction details

- After the email link opens, the client checks for its matching retained signup secret A. With A, asynchronously send A+B to `POST /confirm` and show screen 3a until the backend returns a session or a recoverable error; do not block the UI thread or leave a permanent spinner. Without A, render screen 3b. GET/HEAD requests themselves have no confirmation side effects.
- In screen 3b, the user supplies the six-digit C while B is retained from the link. Submit B+C only after **Verify email** is activated. Support manual entry, full-code paste, leading zeros, and platform autofill as one accessible input with a six-slot presentation; filling the field never submits automatically. C is not recoverable from B and is never prefilled by a backend lookup.
- Keep the token labels A/B/C, request identifiers, hashes, provider names, and raw errors out of the product UI. The automatic screen needs no extra “Continue” button.
- Both paths advance only after the backend confirms and establishes a session. On `409 confirmed_sign_in_required`, offer email OTP sign-in recovery; do not loop confirmation. If confirmation succeeded but session exchange failed, acknowledge verified email separately from the sign-in step.
- Incorrect/stale A may transition to 3b without consuming the link. Invalid or expired B needs a new email. Resending replaces both the link and code: instruct users to open the newest email rather than combining an old link with a new code.
- Only the confirming client gets the session. Do not redirect the original waiting client based solely on polling email-verification status.
- Step 4 uses the browser/native credential UI and retains its own **Create passkey** action. Do not draw a fake biometric prompt or launch passkey creation merely because automatic email confirmation finished. Loading should say “Opening your passkey manager” and allow a return path if dismissed.
- After `POST /passkeys/complete` succeeds, show separate email and passkey status. Skipping identity verification never implies a completed identity/address check.
- Choosing ID verification hands off to the selected capture plugin. Its own flow owns camera and capture screens; the Attestra host needs launch, cancellation/error, and return-data states before the separate ID review. The plugin choice and wiring will be specified during integration.
- On native and web, use the same wording and recovery states. A link claimed by an app can use the automatic path only if that app holds the matching A. A browser fallback may require code entry even on the same physical device.
- Verify small screens, large text, keyboard navigation, reduced motion, screen-reader status announcements, OTP paste/autofill, and offline/slow-network states. Controls must remain at least 44px high.

## Content and state checks for generated screens

1. Each actionable screen has one primary action and visible recovery. Automatic verification has progress and recovery when needed, with no redundant confirmation action.
2. No “Email verified” claim appears before the server confirms. Do not show passkey setup before a usable session is available.
3. The email template includes the verification code as functional content; the manual landing screen starts empty and requires submission.
4. No technical token labels, raw secret values, full verification URLs, or provider errors are used as decorative mock text.
5. Passkey and identity outcomes are not conflated. Skipped identity is a later choice, not failure.
6. Use names like “you” and realistic editable labels; avoid fabricated identities or unsupported trust numbers.
