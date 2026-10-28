# ID validation — standalone feature

**Status: deferred; boundary definition only.** This is a feature of its own, not an onboarding subfeature. No validation architecture or provider selection is being implemented in the capture/parsing plan.

Onboarding owns [ID capture](../../auth/onboarding/id-capture/README.md) and [ID parsing](../../auth/onboarding/id-parsing/README.md). Capture produces immutable private evidence; parsing produces an immutable extraction and a separately confirmed review revision. Neither output means identity approval.

When designed, ID validation may consume those exact account-bound references under its own purpose, eligibility and retention policy. It owns authenticity checks, any account-holder binding/selfie/liveness, external provider decisions, assurance policy, allowed retries/appeals and restricted-feature authorization. Its state remains independent from capture, parsing, email confirmation and passkey registration.

Do not automatically start validation after parsing or copy parsing success into validation status. Do not decide whether an automated report or a third-party approval is mandatory in this scope. A changed capture/extraction/review must not silently inherit a previous validation decision.

The [historical combined proposal](history/2026-10-08-combined-identity-proposal.md) preserves earlier ideas about separate automated/provider tracks for later review; they are not a finalized validation design.
