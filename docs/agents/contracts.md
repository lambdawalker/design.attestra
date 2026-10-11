# Contract ownership and integration

| Contract | Owner | Exact representation |
| --- | --- | --- |
| Email proof rules, transitions and privacy | [Onboarding design](../../auth/onboarding/architecture.md) | [Backend HTTP/source](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/api.md) |
| Capture/parsing separation and references | [Evidence contracts](../../auth/onboarding/id-evidence-contracts.md) | Capture: [backend contract](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/id-capture.md); parsing wire API remains proposed |
| Public environment discovery | [Environment architecture](../../operations/environments.md) | [Registry guide](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/environment-index.md), `registry/registry.go` |
| Android build-time settings | Backend exporter and Android Gradle consumer | [Integration guide](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/integration.md) |
| UI state semantics | Feature `ui.md` and nearby `spec.md` | [Screen directory](../../auth/onboarding/ui-reference/README.md) |

Formal evidence design stays at its established path. Do not relocate it into an implementation merely because capture now exists. Conversely, do not copy operational limits or JSON types here and maintain a second schema. A proposed central endpoint is not evidence that a deployed route exists.

When changing a contract, identify affected backend, Android and central pages/tests. Coordinate commits with explicit transition status; repository commits are not atomic. Keep old valid links. Source/development compatibility is separate from released artifact compatibility. There is no confirmed system-wide release matrix in this revision.
