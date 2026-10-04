# Returning users and session recovery

This is the shared product and integration design for returning to onboarding. See [login](../login/architecture.md) for authentication and [onboarding](architecture.md) for the one-use email proof. Exact HTTP shapes belong in the [backend reference](https://github.com/lambdawalker/go.attestra.aws.auth#return-to-onboarding-and-sign-in); platform storage and navigation details belong in the [Android guide](https://github.com/lambdawalker/android.attestra.auth#returning-after-an-unfinished-signup).

## Entry and restoration

| Available context | Next step | What it proves |
| --- | --- | --- |
| Saved session with refresh token | Refresh the session, retain the prior refresh token if no replacement is returned, then request authenticated passkey status | A successful authenticated response permits account continuation |
| Saved session without refresh token | Attempt authenticated status with the access token; require sign-in if it is no longer usable | Local storage alone is not current authentication |
| Pending email proof without a usable session | Restore the wait/recovery screen; an expired link needs an eligible resend or a fresh sign-in | Local pending state establishes only that this client started signup |
| Confirmation completed elsewhere, or local session was lost | Offer passkey sign-in or a fresh email OTP challenge | Only successful sign-in establishes a session on this device |
| No pending proof or session | Offer onboarding and existing-account sign-in | Do not use signup as a login shortcut |

The ten-minute delivered-proof lifetime is enforced by the backend. A local timestamp is only a UI hint; resend rotates the delivered proof generation and cannot be inferred from an old local timestamp alone. The client must handle the server's outcome. A `request_id`, old confirmation link, or unauthenticated status poll must never reveal passkey registration or grant a session.

The current implementation offers an explicit sign-in choice when it lacks a usable session. It does not expose an unauthenticated endpoint that decides whether an email has a passkey. `/auth/status` requires an authenticated access token. Any future automatic discovery proposal must preserve account-existence protection.

## After authentication

Check authoritative passkey status. Offer enrollment when appropriate, or continue to the optional identity step when a credential is registered. Passkey cancellation or deferral does not revoke the verified email or establish a registered credential. A transient status failure must not be interpreted as proof that the account lacks a passkey.

Confirmation that consumed the signup proof but did not deliver a usable session recovers through sign-in. Do not replay confirmation to obtain another token set. Auth challenge sessions, OTPs, refresh tokens, access tokens, and credential assertions stay out of navigation URLs and analytics.

## Welcome after ID deferral

Skipping the optional identity step opens a welcome destination with separate email, passkey, and identity status. Identity remains incomplete; skipping does not create an approval. A Verify my ID action returns to the identity entry point.

The current Android deferral is a local navigation preference, not server-owned identity state or a cross-device completion record. Restore authentication and passkey status before reusing that preference. The actual capture/provider integration remains pending; the welcome screen must not imply it has run.

## Acceptance cases

- Reopen before and after proof expiry; obey server resend decisions and use the newest link.
- Confirm on another device, then return without a local session; authenticate again without replaying the consumed proof.
- Refresh successfully when Cognito omits a replacement refresh token; retain the original token.
- Reject an expired session for authenticated status and offer sign-in without inferring account/passkey absence.
- Sign in by passkey and by fresh email OTP; continue from authenticated registration status.
- Defer identity, restart, restore the session, and return to welcome without claiming identity approval.
