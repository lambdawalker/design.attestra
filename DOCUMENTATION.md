# Documentation ownership

Every maintained explanation has one owner. Other repositories link to that explanation; a short orientation sentence is welcome, but do not copy a protocol, flow, runbook, or configuration procedure.

| Subject | Canonical home |
| --- | --- |
| System architecture, trust boundaries, module interactions, shared requirements and decisions | `design.attestra` |
| User journeys, recovery rules, screen specifications, identity/address policy | Feature folders in `design.attestra` |
| Go package structure, exact request/response serialization, implementation limits and provider adapters | `go.attestra.aws.auth` |
| Backend build, Lambda packaging, Pulumi deployment, AWS/SES/DNS setup and operational gotchas | `go.attestra.aws.auth` |
| Android modules, Gradle/build/install instructions, Ktor adapters, storage, Credential Manager, App Links and device troubleshooting | `android.attestra.auth` |
| Historical module implementation plans | The corresponding implementation repository, clearly labeled historical |

## Editing rules

1. Change shared behavior, security requirements, or component responsibilities in the design repository. Link the module implementation change to the relevant design page.
2. Change executable commands, code paths, concrete configuration, wire serialization, diagnostics, and module-specific limitations next to the code they describe. Link back to the relevant architecture and flow.
3. A discovered platform constraint may affect both: record the incident/workaround in the module and the resulting system decision in design. These are different explanations; do not copy the troubleshooting steps into design.
4. Keep source implementation status separate from deployed/tested readiness. A route in code is not evidence of a working production deployment. Module READMEs own detailed current capabilities and test instructions.
5. Link to `main` for current guidance. Use a commit permalink when discussing historical evidence. A pinned design submodule is a versioned reference, not a second editable design source.
6. When moving an established page, retain a short redirect if existing links may depend on it. Do not keep two full copies. Archives must not masquerade as current instructions.
7. Review relative paths and cross-repository anchors with documentation changes. Preserve implementation gotchas when removing duplicated prose.

## Starting points

- [System architecture](architecture.md)
- [Onboarding](auth/onboarding/README.md), [session recovery](auth/onboarding/resume.md), and [login](auth/login/architecture.md)
- [Backend implementation and operations](https://github.com/lambdawalker/go.attestra.aws.auth)
- [Android implementation and device setup](https://github.com/lambdawalker/android.attestra.auth)
