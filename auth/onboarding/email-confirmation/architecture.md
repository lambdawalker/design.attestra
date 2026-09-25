# Email confirmation architecture

**Status:** Proposed A+B/B+C revision. The [current Go backend](https://github.com/lambdawalker/go.onboarding/tree/feat/aws-onboarding) still uses a Cognito email code and an explicit confirmation button. This document describes the target; the [overall onboarding architecture](../architecture.md) is authoritative for cross-feature session transitions.

## Boundaries and protocol

1. The client generates cryptographically random A, retains it for this request, and sends its SHA-256 challenge with the email to `POST /signup`. The server returns an opaque `request_id` with a generic response; eligible pending signup generates independent B (link token) and six-digit C (email text).
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

**Integration decision before coding:** the existing Cognito confirmation/session handoff must be reconciled with application-owned B/C proofs. Keep any Cognito code inaccessible as a public shortcut and verify the supported server-controlled confirmation-to-session mechanism end to end. The current Custom Message Lambda cannot by itself implement the transaction protocol.
