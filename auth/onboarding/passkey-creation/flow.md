# Passkey creation subflow

This expands the passkey branch of the [overall onboarding flow](../onboarding-flow.md). A confirmed email and authenticated session are prerequisites.

```mermaid
flowchart TD
    S["Authenticated account"] --> I["Explain passkey; tap Continue"]
    I --> O["Request registration options"]
    O --> D{"Device supports passkeys?"}
    D -->|No| U["Unsupported device; use email sign-in"]
    D -->|Yes| P["Open platform credential picker"]
    P --> C{"Credential returned?"}
    C -->|No| R["Retry or defer setup"]
    C -->|Yes| F["Submit registration result"]
    F --> V{"Server confirms registration?"}
    V -->|No| R
    V -->|Yes| N["Continue to optional ID capture"]
```

Cancellation leaves email confirmed and passkey registration incomplete. The client shows success only after the registration completion response; neither opening the platform picker nor receiving a local credential proves server registration. See [architecture](architecture.md).
