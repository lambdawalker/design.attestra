# Email confirmation UI

Follow the [shared design brief](../stitch.md) and [screen index](../ui-reference/README.md). Keep the title, icon, explanatory card, input, and primary action consistent across these views. The [shared loading view](../ui-reference/onboarding_loading/code.html) supplies the wait state while a request is actually in flight; set its title and card text to “Verifying your email” or “Requesting another email” as appropriate.

| Screen | When to show it | Primary action and recovery |
| --- | --- | --- |
| [Start](ui-reference/email_verification_start/code.html) | New signup intent | Enter email; Continue sends a generic request. Inline invalid-address error. |
| [Wait](ui-reference/email_verification_wait/code.html) | Signup request returned | Open the latest email; throttled Resend email and Change email address. A generic response does not guarantee delivery. |
| [Manual code](ui-reference/email_verification_manual_code_input/code.html) | Link opened without matching local A | One empty, accessible six-digit input displayed as six slots. Paste/autofill fills it; only Verify email submits B+C. |
| [Incorrect code](ui-reference/email_verification_incorrect_code/code.html) | Backend rejected C for this B | Keep B and the editable input; show server-provided attempts remaining, Try again, and throttled resend. |
| [Attempt limit](ui-reference/email_verification_attempt_limit/code.html) | Current generation cannot accept more C attempts | Disable code submission. Request a new email only when the server allows it; show its actual cooldown. |
| [Unusable link](ui-reference/email_verification_link_unusable/code.html) | B is expired, replaced, malformed, or missing | Request a new email and open its latest link; never retry the unusable B. |

The automatic A+B path goes from the link straight to the shared loading view and then passkey creation after the server returns a session. There is no extra Verify tap. If confirmation succeeds but session exchange fails, show **Email verified** and route to email sign-in recovery; do not replay the consumed confirmation. If a previously completed link opens without this client's session, offer sign-in. Never infer a session from status polling on another device.

The verification email template is still to be designed: display the link containing B and a separate six-digit C, including expiry and newest-email guidance. Neither C nor A belongs in a URL, HTML landing page, or decorative example. All screens need keyboard, large text, screen-reader announcements, offline/timeout, and reduced-motion variants.
