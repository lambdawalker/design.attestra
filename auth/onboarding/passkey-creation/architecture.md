# Passkey creation architecture

**Status:** The [Go onboarding baseline](https://github.com/lambdawalker/go.onboarding/tree/feat/aws-onboarding) contains passkey registration endpoints and Cognito WebAuthn configuration. The client handoff, platform integration, and end-to-end behavior still require implementation and verification.

## Boundaries

1. Email confirmation produces a usable authenticated session or takes the user through email OTP sign-in recovery. Passkey registration starts only with an authenticated account; the Cognito `sub` remains its stable account identifier.
2. On an explicit user action, call `POST /passkeys/options` with the current access token. The server gets registration options for that account and returns a challenge for the browser or native credential API. Associate the expected relying-party ID with the public web domain and native apps.
3. The OS/browser creates and protects the private credential. Send the platform result to `POST /passkeys/complete` with an authenticated session. The backend finishes registration and returns authoritative success or a recoverable error; never infer success from a dismissed system sheet.
4. Keep email-confirmed, passkey-registered, and identity-decision states separate. A cancelled, unsupported, or failed passkey can be retried later. Account access remains available through the documented email OTP route.

The client needs states for idle, fetching options, system picker, submitting, complete, cancelled, unsupported, and failed. Request fresh options for retries because challenges are short lived and bound to a registration attempt. If the app resumes after interruption, query server registration state before showing success or offering a retry. Handle session expiry through sign-in rather than reporting a device error.

Keep registration responses and authentication credentials out of analytics and logs. Credential Manager on Android, AuthenticationServices on iOS, and WebAuthn in browsers own their respective dialogs; use platform association files and origin validation for each supported client. The server retains no private key and must not treat the UI's local result as proof of completed registration.
