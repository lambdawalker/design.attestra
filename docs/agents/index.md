# Attestra system agent entry

Scope: current design `main`, with implementation evidence recorded in [compatibility](../compatibility.md). This repository owns requirements and cross-component contracts, not executable deployment instructions or an installable artifact.

| Task | Canonical guide | Implementation |
| --- | --- | --- |
| Understand boundaries and terminology | [Architecture](../../architecture.md), [concepts](concepts.md) | [Repository catalog](../repositories.md) |
| Implement onboarding and recovery | [Journeys](journeys.md) | [Backend agent entry](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/index.md) |
| Implement capture/parsing | [Contracts](contracts.md) | [Backend capture contract](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/id-capture.md) |
| Set up discovery/deployment | [Environment lifecycle](../../operations/environments.md) | [Backend operations](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/operations.md) |
| Match UI to real behavior | [UI semantics](ui.md) | Nearby `spec.md` files, not prototype timers |
| Evaluate compatibility or gaps | [Evidence and limitations](limitations.md) | [Ownership](../../DOCUMENTATION.md) |

Invariants: email confirmation is not identity assurance; only the confirming client receives its session; passkeys remain platform-owned; capture ready is immutable evidence, not extraction or approval; parsing does not silently invoke validation; the public environment index never contains secrets or ID data. Preserve evidence refs and state whether a claim is designed, implemented, tested, operator-reported or deferred.
