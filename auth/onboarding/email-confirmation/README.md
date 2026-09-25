# Email confirmation

[Subflow](flow.md) · [UI](ui.md) · [Architecture](architecture.md) · [AWS strategy](aws.md)

This subfeature covers email entry, waiting for the message, and confirming the address with A+B in the initiating client or B+C when the original client context is unavailable. The link alone never confirms the address. The [onboarding architecture](../architecture.md) owns the protocol and session recovery rules; the [development order](../order-of-development.md) gives implementation sequence.

| Reference | Role |
| --- | --- |
| [Start](ui-reference/email_verification_start/code.html) | Enter an email and request signup |
| [Wait](ui-reference/email_verification_wait/code.html) | Open the email, resend, or change address |
| [Manual code input](ui-reference/email_verification_manual_code_input/code.html) | Enter the six-digit code after opening the link without A |
| [Incorrect code](ui-reference/email_verification_incorrect_code/code.html) | Correct and retry a code |
| [Attempt limit](ui-reference/email_verification_attempt_limit/code.html) | Recover within backend retry limits |
| [Unusable link](ui-reference/email_verification_link_unusable/code.html) | Request a new link and code |

Use the [shared processing view](../ui-reference/onboarding_loading/code.html) while confirmation or resend is in flight. The verification email template is still missing; it must contain link B and a separately displayed six-digit C.
