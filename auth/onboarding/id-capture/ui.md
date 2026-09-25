# ID capture UI

Keep the [shared design brief](../stitch.md): title, icon, explanatory card, fields when needed, and a clear primary action. The selected plugin controls camera instructions, document framing, permission prompts, and its own capture screens. The app presents these surrounding views.

| Screen | When to show it | Action and meaning |
| --- | --- | --- |
| [Start or skip](ui-reference/identity_verification_start/code.html) | Authenticated account arrives at optional check | Start identity check launches the plugin; Skip goes to the dashboard. |
| [Document reading](ui-reference/identity_verification_reading_document/code.html) | Archived visual after capture | Use the shared loading screen for actual extraction; this reference is not a second dedicated loading implementation. |
| [Unreadable document](ui-reference/identity_verification_document_unreadable/code.html) | Extraction cannot read the capture | Retake reopens the plugin; offer a way to leave and continue later. This is not a failed identity decision. |
| [Review details](ui-reference/identity_verification_review_details/code.html) | Extracted fields are available | Edit inaccurate fields and submit; label corrections separately from extracted text. |
| [Submission failed](ui-reference/identity_verification_submission_failed/code.html) | Server could not establish accepted submission | Check existing status first, then Retry submission if still needed; do not duplicate evidence silently. |
| [Success](ui-reference/identity_verification_success/code.html) | Authoritative identity policy reports approval | Continue to dashboard; never show this after capture or OCR alone. |

The final **identity unsuccessful** result has no approved mockup yet. Add a dedicated screen with reason text allowed by policy, a retry action only when permitted, and support/exit guidance. Keep provider rejection distinct from unreadable capture and transient submission failure. Pending or inconclusive decisions also need an accessible route from the dashboard to check status rather than an indefinite blocking loader.

Reuse [onboarding loading](../ui-reference/onboarding_loading/code.html) and change its title and card text for each wait: “Reading your document,” “Submitting your information,” or “Checking your identity.” Exit a loading view when processing becomes long-running, report an error, or move to the pending status view. Do not display unmasked document content in errors, notifications, or analytics.
