# Passkey creation UI

Use the [shared design brief](../stitch.md) and the existing screen structure: title, icon, explanatory card, and primary action. The platform owns credential selection, biometric prompts, and system permissions; do not recreate those dialogs in app UI.

| Screen | When to show it | Actions |
| --- | --- | --- |
| [Start](ui-reference/passkey_setup_start/code.html) | After email confirmation yields an authenticated session | Create passkey opens the platform flow; Do it later continues with email sign-in available. |
| [Failed or cancelled](ui-reference/passkey_setup_failed/code.html) | Credential picker cancels, times out, or server rejects completion | Try again requests fresh options; Do it later continues. Distinguish cancellation from a saved passkey. |
| [Unsupported device](ui-reference/passkey_setup_unsupported_device/code.html) | Capability check or platform API reports unavailable | Recheck support where useful, or continue with email sign-in. |

Use the [shared loading screen](../ui-reference/onboarding_loading/code.html) for live waits, changing its title and card text to match the task: “Opening your passkey manager” while fetching options and “Saving your passkey” while completing registration. Leave the loading screen on a timeout or error and offer a retry. A later sign-in can offer passkey setup again; skipping is not an identity-check result. Support accessible labels, focus return after the system sheet, reduced motion, and recovery after app backgrounding.
