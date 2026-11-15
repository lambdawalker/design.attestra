# Onboarding flow source

This is the current flow for the [onboarding architecture](architecture.md). The [legacy SVG](onboarding-flow.svg) is retained as a historical pre-split snapshot. Capture/parsing subflows have their own detailed diagrams.

```mermaid
flowchart TD
    S["Enter email; generate and retain A"] --> T["POST /signup with A challenge"]
    T --> M["Email link B and separate code C"]
    M --> W0["One waiting screen with visible code entry"]
    W0 -->|Open link| L["Open app or website"]
    W0 -->|Type or paste code| AC["Explicitly POST /confirm with A+C"]
    L --> D{"Matching A available locally?"}
    D -->|Yes| P["Automatically POST /confirm with A+B"]
    D -->|No| Q["Enter C from email; tap Verify email"]
    Q --> R["POST /confirm with B+C"]
    P --> V{"Proofs valid and unused?"}
    AC --> V
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
    K -->|Capture enabled| C0["Review purpose, retention and camera disclosure"]
    C0 --> C2["Native permission dialog if needed; capture and review photos"]
    C2 --> C1["Finalize evidence; extract or enter data manually"]
    C1 --> C3["Save and continue; require matching server-reviewed data"]
    W --> J
    X --> J
    C3 --> J
    K -->|Optional skip or no remaining steps| N{"Server onboarding_complete?"}
    N -->|Yes| Z["Continue to account; no identity verification claim"]
    N -->|No| J
```

Password may be collected with email but is submitted only after verification; loss of process or cross-device confirmation requires re-entry. Disabled enrollment is omitted. Optional skips are local choices, never substitutes for required durable facts. ID parsing/review can follow ready capture independently; capture is not identity verification. See [policy](policy.md).

After an acknowledged review save, Android returns automatically to account-status routing; no additional Done action is required. Review ID details opens the saved form directly. Existing processing and saved records do not request camera permission. The standalone camera entry retains its explanation-first behavior.
