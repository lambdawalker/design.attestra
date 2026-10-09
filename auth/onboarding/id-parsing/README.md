# ID parsing — onboarding subfeature

[Architecture](architecture.md) · [Flow](flow.md) · [AWS design](aws.md) · [JSON data design](data-model.md) · [UI](ui.md) · [Shared contracts](../id-evidence-contracts.md) · [Implementation sequence](../id-evidence-plan.md)

**Status: architecture planned.** Parsing consumes ready evidence from [ID capture](../id-capture/README.md), sends the pinned images to a vision-capable model through a backend adapter, validates structured JSON, and lets the user review/correct it. Completion means a confirmed document-data revision, not verified identity.

Authenticity, selfie/liveness, third-party checks and assurance decisions belong to [ID validation](../../../verification/id-validation/architecture.md), a separate feature deferred from this plan.
