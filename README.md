# Attestra design and planning

This repository is the central index for Attestra product flows, architecture decisions, API behavior, and screen design across code repositories. Start with a feature below, then follow the implementation links for setup, deployment, and platform-specific debugging.

| Feature | Architecture | Stitch screen spec | Implementation |
| --- | --- | --- | --- |
| Auth / onboarding | [Journey](auth/onboarding/architecture.md) and [subfeatures](auth/onboarding/README.md) | [Onboarding](auth/onboarding/stitch.md) | [Go backend](https://github.com/lambdawalker/go.attestra.aws.auth), [Android app](https://github.com/lambdawalker/android.attestra.auth); passkey and ID capture backend work is pending |
| Auth / login | [Passkey login and email OTP fallback](auth/login/architecture.md) | [Login](auth/login/stitch.md) | Planned in [go.attestra.aws.auth](https://github.com/lambdawalker/go.attestra.aws.auth) |
| Verification / identity | [AI auto report and third-party check](verification/identity/architecture.md) | Pending policy/provider choices | Architecture proposed |
| Verification / address | [AI auto report, third-party check, and expiry](verification/address/architecture.md) | Pending policy/provider choices | Architecture proposed |

Auth screens share the [Stitch design system](auth/DESIGN.md). [Onboarding](auth/onboarding/README.md) is divided into email confirmation, passkey creation, and ID capture; its [screen index](auth/onboarding/ui-reference/README.md) links the mockups. The onboarding [Mermaid source](auth/onboarding/onboarding-flow.md) is separate from its SVG rendering in the architecture. The [original AWS onboarding implementation plan](auth/onboarding/history/2026-09-24-aws-onboarding.md) is retained as history; its initial TypeScript/Node approach was subsequently converted to Go.

## Where information lives

| Question | Source of truth |
| --- | --- |
| What does a user see, and how does the flow work across platforms? | The feature's `ui.md`, `flow.md`, and `architecture.md` here |
| What AWS services implement the feature, and where are the trust boundaries? | The feature's `aws.md` here |
| How do I deploy, configure SES/DNS, find stack outputs, or troubleshoot a Lambda? | [Go auth README](https://github.com/lambdawalker/go.attestra.aws.auth/blob/main/README.md) and its [read-only debug scripts](https://github.com/lambdawalker/go.attestra.aws.auth/tree/main/debug) |
| How do I build and configure the Android client or test deep links? | [Android auth repository](https://github.com/lambdawalker/android.attestra.auth) |
| How do I build and configure the iOS client or universal links? | Future iOS repository (link when created) |

For onboarding, begin at the [journey index](auth/onboarding/README.md), then follow the subfeature pages. Implementation repositories own their executable instructions so configuration and code change together. Link to those instructions from the relevant feature rather than copying commands into this repository.
