# Onboarding screen development order

Follow the four subfeature folders: [email confirmation](email-confirmation/README.md), [passkey creation](passkey-creation/README.md), [ID capture](id-capture/README.md), and [ID parsing](id-parsing/README.md). Shared layout and loading belong to the overall onboarding flow.

This is a design dependency sequence, not an outstanding-task or deployment checklist. Current implementation details belong in the [Android](https://github.com/lambdawalker/android.attestra.auth) and [Go](https://github.com/lambdawalker/go.attestra.aws.auth) repositories.

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

## 4. Optional ID capture

13. Build the optional Add your ID / Skip entry and document-type policy selection.
14. Integrate permission, camera, per-side preview and retake; preserve host cancel/error navigation.
15. Add direct S3 upload progress, instruction renewal and status reconciliation for missing slots.
16. Finalize and show preparing/pending status until the frozen evidence is ready; invalid images route to recapture.

## 5. ID parsing

17. Create/reconcile an asynchronous parse job for ready evidence. Support bounded waiting and leave/resume.
18. Build review of extracted fields, missing/ambiguous warnings, user corrections and recapture.
19. Save/confirm a revision with conflict and lost-response recovery. End at Document details saved, then continue to account.

The detailed backend/client sequence and acceptance gates are in the [document pipeline plan](id-evidence-plan.md). ID-validation provider checks, approval/rejection screens and restricted-feature gating are outside these slices. Historical identity-success mockups are not parsing-success screens.

## Completion checks

- Test the A+B and B+C paths on the web and native clients, including opening the link on another device.
- Verify that fetching a link alone cannot confirm an email, and that a code cannot confirm without its matching link.
- Test wrong codes, exhausted attempts, expired or replaced links, resends, network timeouts, and confirmation without a recoverable session.
- Test passkey success, cancellation, failure, unsupported devices, and deferral.
- Test capture cancellation/retakes, incomplete uploads, URL expiry, frozen-version races, unreadable parsing, model failures, corrected details, uncertain writes, pending recovery and revision conflicts.
- Confirm that skipping passkey setup or document submission does not falsely mark either complete; capture/parsing must never mark identity validated.
