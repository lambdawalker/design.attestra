# Onboarding

Onboarding has four subfeatures: email confirmation, passkey creation, ID capture, and ID parsing. The optional document flow collects and saves reviewed document data; **ID validation is a standalone feature outside onboarding**.

| Subfeature | Scope | Status / implementation |
| --- | --- | --- |
| [Email confirmation](email-confirmation/README.md) | Email proof, link/manual-code paths and recovery | [Go](https://github.com/lambdawalker/go.attestra.aws.auth), [Android](https://github.com/lambdawalker/android.attestra.auth) |
| [Passkey creation](passkey-creation/README.md) | Platform credential registration and deferral | Same implementation repositories |
| [ID capture](id-capture/README.md) | Camera/photos, direct private S3 upload and frozen evidence manifest | Architecture planned; Android mock prototype exists separately |
| [ID parsing](id-parsing/README.md) | Asynchronous vision extraction, validated JSON, attributed corrections and confirmed review | Architecture planned; model/provider selection pending evaluation |

Start with the [journey architecture](architecture.md), [flow](onboarding-flow.md), [capture/parsing contracts](id-evidence-contracts.md), and [implementation sequence](id-evidence-plan.md). [Session recovery](resume.md), [screen development order](order-of-development.md), [Stitch brief](stitch.md), and [screen references](ui-reference/README.md) cover shared behavior.

[ID validation](../../verification/id-validation/architecture.md) will consume evidence and reviewed data under a separate policy. Captured, parsed, saved, email-confirmed and passkey-registered are different outcomes; none implies validated identity.
