# Passkey Setup Failed

Screen ID: `passkey_setup_failed` · Parent flow: `onboarding.passkey` · Capture kind: `design-prototype`.

Status: historical visual reference; normative behavior is in [the owning flow](../../ui.md). HTML does not establish backend or device implementation. Source reference: design main before this documentation update (`bea6831`). [Evidence ledger](../../../../../docs/compatibility.md).

## Entry, actions and exit

Entry: Cancellation, timeout or registration error. Fields/actions: Try again; Do it later.

Request fresh options for retry; no passkey success until backend confirms.

Loading follows a real request; transport failure offers retry/cancel without fabricated success. Cancellation returns to the parent flow without completing it. Preserve focus after errors, accessible labels, keyboard navigation, large text, screen-reader status and reduced-motion behavior. Exact labels/appearance in [HTML source](code.html) are historical reference, not a substitute for these rules.

## Service and ownership

Read [the canonical contract](../../architecture.md) and [backend integration](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/api.md). Android owns device interaction; [its app and UI catalog](https://github.com/lambdawalker/android.attestra.auth) are the runnable implementation. These prototypes cannot prove that app renders this exact screen. Parsing/validation-specific behavior remains proposed.

## Evidence and missing states

Prototype JavaScript, external Tailwind/fonts and placeholder links are not a production service integration. Timed success transitions must not be copied into real authentication. Do not run this HTML in the docs origin with credentials. Use the flow's UI guide for missing error, recovery, permission, rotation and process-loss variants.
