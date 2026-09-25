# Attestra design and planning

This repository is the central home for product flows, architecture decisions, and screen design briefs across Attestra code repositories. A feature can own subfeatures. Implementation belongs in its respective code repository; links to code and deployment instructions remain there.

| Feature | Architecture | Stitch screen spec | Implementation |
| --- | --- | --- | --- |
| Auth / onboarding | [Email confirmation and passkey creation](auth/onboarding/architecture.md) | [Onboarding](auth/onboarding/stitch.md) | [go.onboarding](https://github.com/lambdawalker/go.onboarding/pull/1) baseline draft; A+B / B+C confirmation revision pending |
| Auth / login | [Passkey login and email OTP fallback](auth/login/architecture.md) | [Login](auth/login/stitch.md) | [go.onboarding](https://github.com/lambdawalker/go.onboarding/pull/1) draft PR |
| Verification / identity | [AI auto report and third-party check](verification/identity/architecture.md) | Pending policy/provider choices | Architecture proposed |
| Verification / address | [AI auto report, third-party check, and expiry](verification/address/architecture.md) | Pending policy/provider choices | Architecture proposed |

Auth screens share the [Stitch design system](auth/DESIGN.md). [Onboarding](auth/onboarding/README.md) is divided into email confirmation, passkey creation, and ID capture; its [screen index](auth/onboarding/ui-reference/README.md) links the mockups. The onboarding [Mermaid source](auth/onboarding/onboarding-flow.md) is separate from its SVG rendering in the architecture. The [original AWS onboarding implementation plan](auth/onboarding/history/2026-09-24-aws-onboarding.md) is retained as history; its initial TypeScript/Node approach was subsequently converted to Go.

For the current API and deployment instructions, see the [go.onboarding code repository](https://github.com/lambdawalker/go.onboarding/tree/feat/aws-onboarding).
