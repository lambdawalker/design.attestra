# Email confirmation architecture

**Status:** Implemented as an email API and Pulumi stack in [go.attestra.aws.auth](https://github.com/lambdawalker/go.attestra.aws.auth); client routing, deployment, and live integration checks remain. The [overall onboarding architecture](../architecture.md) describes cross-feature session transitions.

## Boundaries and protocol

1. The client generates cryptographically random A, retains it for this request, and sends its SHA-256 challenge with the email to `POST /signup`. The server returns an opaque `request_id` with a generic response; an eligible pending transaction generates independent B (link token) and six-digit C (email text). Cognito user creation occurs after the proof is claimed.
2. The server binds normalized email, `request_id`, challenge, B digest, keyed C digest, expiry, resend generation, failed-attempt budgets, and transaction state. The confirming request must contain B plus **exactly one** matching A or C. B alone and C alone are insufficient.
3. The link route reads B without mutating server state. With matching local A, the client submits A+B automatically; otherwise it renders an empty code field and submits B+C only after an explicit Verify action.
4. The backend atomically claims a valid, unused transaction before provider side effects. Confirmation and session issuance are tracked separately for retries, races, and partial failures. Only the successful confirming client receives tokens.
5. A confirmed account without a usable session uses email OTP sign-in recovery. Passkey creation requires that session; email confirmation never asserts passkey or identity approval.

## State and policy

| State | Allowed transition |
| --- | --- |
| Pending | Confirm with matching A+B or B+C; resend rotates B and C while preserving the A challenge and request ID |
| Confirming | One claimant performs provider confirmation/session exchange; competitors receive safe in-progress/already-used results |
| Confirmed, session issued | Return the session only to the confirming request; clear pending client A and secrets |
| Confirmed, session unavailable | Return a stable sign-in-required result; never replay confirmation |
| Expired/replaced/attempt-limited | Deny old proofs; offer permitted resend or sign-in without account enumeration |

Initial policy: ten minutes per B/C generation, at most five incorrect C attempts per generation, and an account-level budget across resends. Check expiry explicitly on every read and write. Resend cannot reset a broader cooldown. Store C as a keyed digest because six decimal digits are easy to brute-force from an unkeyed hash. Strip B from browser navigation after capture; avoid third-party resources and raw URL logging on the landing page. Native apps keep A in protected pending storage; website storage must survive the link opening a new tab without placing A in the URL.

**Cognito handoff:** After a valid proof, the API creates a passwordless email-verified user with `AdminCreateUser` and suppresses the default invitation. A one-use server grant is checked by Cognito custom-challenge Lambda triggers before Cognito returns tokens to the confirming request. If account creation succeeds but token issuance fails, return the sign-in-required outcome and use email OTP recovery. The custom challenge and account-creation path require end-to-end verification in a nonproduction AWS stack.
