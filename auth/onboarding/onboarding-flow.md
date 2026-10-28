# Onboarding flow source

This is the current flow for the [onboarding architecture](architecture.md). The [legacy SVG](onboarding-flow.svg) is retained as a historical pre-split snapshot. Capture/parsing subflows have their own detailed diagrams.

```mermaid
flowchart TD
    S["Enter email; generate and retain A"] --> T["POST /signup with A challenge"]
    T --> M["Email link B and separate code C"]
    M --> L["Open app or website"]
    L --> D{"Matching A available locally?"}
    D -->|Yes| P["Automatically POST /confirm with A+B"]
    D -->|No| Q["Enter C from email; tap Verify email"]
    Q --> R["POST /confirm with B+C"]
    P --> V{"Proofs valid and unused?"}
    R --> V
    V -->|No| E["Retry, code entry, or resend"]
    V -->|Yes| F["Confirm email and exchange session"]
    F --> G{"Session available?"}
    G -->|No| O["Email OTP recovery"]
    G -->|Yes| H["Authenticated session"]
    O --> H
    H --> J["Load current policy and authenticated status"]
    J --> K{"Unmet required or offered optional step?"}
    K -->|Password enabled| W["Collect or reuse memory-only password; authenticated set"]
    K -->|Passkey enabled| X["Platform registration; server acceptance"]
    K -->|Capture enabled| C1["Capture and finalize evidence to server ready"]
    W --> J
    X --> J
    C1 --> J
    K -->|Optional skip or no remaining steps| N{"Server onboarding_complete?"}
    N -->|Yes| Z["Continue to account; no identity verification claim"]
    N -->|No| J
```

Password may be collected with email but is submitted only after verification; loss of process or cross-device confirmation requires re-entry. Disabled enrollment is omitted. Optional skips are local choices, never substitutes for required durable facts. ID parsing/review can follow ready capture independently; capture is not identity verification. See [policy](policy.md).
