# Onboarding screen development order

Follow the three subfeature folders: [email confirmation](email-confirmation/README.md), [passkey creation](passkey-creation/README.md), and [ID capture](id-capture/README.md). Shared layout and loading belong to the overall onboarding flow.

Build the screens in vertical slices so each completed stage can be exercised from its entry point through success and recovery. The HTML mockups are visual references; the architecture defines the actual state transitions.

## 1. Shared foundations

1. Implement the shared layout, accessible fields, status messages, and navigation.
2. Implement [Onboarding - processing](ui-reference/onboarding_loading/code.html) once. Supply its title, icon, card text, and accessible status from the active task. Use it only while work is in progress; every use needs a success transition and a timeout or failure path.

## 2. Email confirmation

3. Build [Email verification - start](email-confirmation/ui-reference/email_verification_start/code.html), including validation, submission, and the neutral response for addresses that may already exist.
4. Build [Email verification - wait](email-confirmation/ui-reference/email_verification_wait/code.html), including resend limits and change-email navigation.
5. Create the verification email template with link B and a separate six-digit code C. This is required to exercise the screens that follow.
6. Handle the opened link:
    - With matching local A, show the shared processing screen and submit A+B automatically.
    - Without A, show [Email verification - manual code input](email-confirmation/ui-reference/email_verification_manual_code_input/code.html). Submit B+C only when the user activates Verify email.
7. Add [incorrect code](email-confirmation/ui-reference/email_verification_incorrect_code/code.html), [attempt limit](email-confirmation/ui-reference/email_verification_attempt_limit/code.html), and [unusable link](email-confirmation/ui-reference/email_verification_link_unusable/code.html). A replacement email supplies a new link and code; old and new values cannot be combined.
8. Advance only after confirmation **and** an authenticated session are available. If the email was confirmed but session creation failed, route to email sign-in recovery.

## 3. Passkey creation

9. Build [Passkey setup - start](passkey-creation/ui-reference/passkey_setup_start/code.html) and invoke the browser or platform credential UI from its Create passkey action.
10. Use the shared processing screen while saving the returned passkey registration. Show “Passkey added” only after the server confirms it.
11. Add [Passkey setup - failed](passkey-creation/ui-reference/passkey_setup_failed/code.html) with Try again and Do this later.
12. Add [Passkey setup - unsupported device](passkey-creation/ui-reference/passkey_setup_unsupported_device/code.html). Allow deferral and the documented email sign-in path; recheck support only when the device environment changes.

## 4. Optional ID capture and identity check

13. Build [Identity verification - start](id-capture/ui-reference/identity_verification_start/code.html), with separate email and passkey statuses, Start identity check, and Skip for now.
14. Integrate the selected capture plugin. It owns camera permission, document capture, and its internal retry screens. Handle launch, cancellation, errors, and returned data in Attestra.
15. Use the shared processing screen to read the returned images. For unreadable images, show [Identity verification - unreadable document](id-capture/ui-reference/identity_verification_document_unreadable/code.html) and reopen the plugin on retry.
16. Build [Identity verification - review details](id-capture/ui-reference/identity_verification_review_details/code.html). Let the user correct extracted data before submission; extraction is not an identity decision.
17. Use the shared processing screen for submission. On interruption, show [Identity verification - submission failed](id-capture/ui-reference/identity_verification_submission_failed/code.html). Check the server outcome before retrying an uncertain submission.
18. Use the shared processing screen or a persistent pending state while the identity provider decides. Show [Identity verification - success](id-capture/ui-reference/identity_verification_success/code.html) only after an approved result.
19. Design and build the **final unsuccessful identity decision** variant. It remains missing from the references. Provide a dashboard exit and a retry only when the provider permits one. The unreadable-document screen is a capture error, not this decision.

## Completion checks

- Test the A+B and B+C paths on the web and native clients, including opening the link on another device.
- Verify that fetching a link alone cannot confirm an email, and that a code cannot confirm without its matching link.
- Test wrong codes, exhausted attempts, expired or replaced links, resends, network timeouts, and confirmation without a recoverable session.
- Test passkey success, cancellation, failure, unsupported devices, and deferral.
- Test identity plugin cancellation, unreadable images, corrected details, uncertain submissions, pending results, approval, and unsuccessful decisions.
- Confirm that skipping passkey setup or identity verification does not falsely mark either step complete.
