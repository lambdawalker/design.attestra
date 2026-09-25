# Passkey creation

[Subflow](flow.md) · [UI](ui.md) · [Architecture](architecture.md) · [AWS strategy](aws.md)

This subfeature begins only after email confirmation yields an authenticated session. The browser or operating system supplies its credential picker. A passkey is shown as added only after the server confirms registration; cancellation or deferral leaves email confirmed. See the [onboarding architecture](../architecture.md) and [development order](../order-of-development.md).

| Reference | Role |
| --- | --- |
| [Start](ui-reference/passkey_setup_start/code.html) | Explain the benefit and start platform setup |
| [Failed or cancelled](ui-reference/passkey_setup_failed/code.html) | Retry or do it later |
| [Unsupported device](ui-reference/passkey_setup_unsupported_device/code.html) | Continue without a passkey or recheck support |

Use the [shared processing view](../ui-reference/onboarding_loading/code.html) while saving a returned credential. A deferred passkey uses the documented email sign-in route.
