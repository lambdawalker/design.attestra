# Persistent authentication tasks

Status: persistent sign-in, inline passkey recovery, and optional account actions are merged in Android source at `659d208fd933cea97bb448b8581bfc6532b57be4`; the distinct successful-completion callback and demo handoff are proposed on branch `feat/onboarding-completion-handoff-20261115`. This contract does not assert publication or deployment. It builds on the [onboarding journey](onboarding/architecture.md) and [returning login](login/architecture.md). This document supersedes their separate loading/error destinations and repeated optional-onboarding offers for the updated Android host; security requirements and platform consent remain unchanged. Legacy exported screen functions and custom policy routing may remain for source compatibility.

## Returning sign-in

One task surface owns the selected method, recipient, input, request progress, and recovery. Choosing email code or password changes the active form within that surface. Preserve the email address when moving from account creation to returning sign-in. A contextual recovery notice appears beside usable sign-in actions, not on an extra page requiring another Continue tap.

| Event | Required behavior |
| --- | --- |
| Send code | Explicit action. Keep the recipient visible while pending; show the code form only after a challenge is returned. |
| Submit code/password | Explicit action. Keep the form visible, disable edits and duplicate submissions while pending, and show progress in context. |
| Temporary connection/service failure | Retain the input in transient memory and offer an explicit retry. Do not report the credential as incorrect when transport failed. |
| Rejected credential/code | Inline validation and correction. Retain the editable input; do not silently send another code or claim success. |
| Throttled request | Inline feedback and a bounded countdown, respecting numeric server Retry-After where supplied. Server enforcement remains authoritative. |
| Resend | Explicit action with a local cooldown. Clear the old code only when a new challenge is received. A failed resend does not guarantee that the server left the older challenge valid. |
| Choose another method or edit recipient | Clear code, password, and challenge; retain the email where appropriate. |
| Exit, account/environment replacement, or disposal | Clear transient credentials; abandon late results so they cannot persist a session or navigate the new task. |
| Successful authentication | Clear transient credentials, persist only the normal authenticated session through the host, then obtain server account status. |

Codes and passwords must not be serialized into saved-instance state, disk, logs, analytics, or previews containing real data. Memory retention is limited to the current UI owner; rotation/process death is not promised to preserve secret input. Cancellation propagates without being reclassified as a wrong credential. Paste and email one-time-code autofill remain available, but never submit automatically. Unknown failures use safe generic copy, not provider response bodies.

A current coroutine may finish a network operation after the user exits. Its result must be fenced from the new owner and cannot save an abandoned session. UI duplicate guards complement, not replace, backend authentication and attempt limits.

## Passkey setup

The same Secure your account screen displays ready, opening-provider, saving, checking-status, cancelled, unsupported, and retryable-failure states. Android Credential Manager still opens only after an explicit Create passkey action. There is no separate cancellation/error page.

Cancellation is informational and offers retry. Unsupported devices offer a clear recovery action without claiming that setup succeeded. Required passkeys cannot be skipped locally. Optional passkeys expose Do this later, with account setup still governed by server status.

A successful provider response is not a successful registration: the backend must acknowledge the credential. After acknowledgement, retrying an interrupted account-status check must read status, not open the provider or submit the credential again. If status still does not report the registered passkey, remain in a status-recovery state rather than claiming completion. Exiting while the provider is open prevents a later result from being submitted by the abandoned task.

## Optional setup and completion

The updated host routes missing required password, passkey, and ID-capture steps first. When those facts are satisfied, it still requires `onboarding_complete` from the backend. Optional steps do not block that completion or create a repeated sequence of Skip actions.

The completed account view exposes Add passkey, Add password, and Add ID only for permitted, incomplete optional steps. Already saved ID details remain directly reviewable. Disabled steps have no add action. An explicit account action opens the corresponding task; it does not weaken validation or server permission checks. Policies that deliberately place password collection beside signup email retain that configured input, including its optional status.

The library can preserve the legacy optional-offer `OnboardingPolicy.next` API for existing custom hosts. The updated bundled host uses required-only routing plus server-confirmed account actions. This is an intentional live-host interaction change, not a backend contract or credential-policy change.

A completed account view exposes a dedicated successful-onboarding handoff that is distinct from cancel/back/defer. The success action is reachable only after required steps and backend `onboarding_complete` have produced the completed account destination; it must not be emitted from authentication, capture, or local UI state alone. Back/cancel continues through the existing exit/defer integration. Consumers that do not adopt the dedicated callback may retain the legacy exit behavior. Neither path may label email/passkey completion or saved document data as identity validation.

## Acceptance evidence

Required regressions: connection failure retains code/password; incorrect code differs from transport failure; repeated taps start one request; resend cooldown and challenge rotation remain explicit; abandoning an operation cannot write a late session; passkey cancellation does not save; status retry after acknowledged registration does not recreate a passkey; all required/optional/disabled policy combinations preserve required steps and backend completion.

UI coverage includes light/dark method choice, code entry, verification, connection recovery, password retry, passkey cancellation/unsupported/status recovery, completed account actions, and narrow/large-font code entry. Device checks must still cover keyboard accessibility, actual provider cancellation, background/rotation, and live backend error classification. Rendered previews and mocked transport tests do not establish those device/service guarantees.

The current provider adapter may map provider refresh failures to HTTP 401; the Android client cannot infer an outage that the server has classified as an expired session. Record that limitation rather than bypassing reauthentication.
