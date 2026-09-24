# Onboarding flow source

This Mermaid source corresponds to the [rendered SVG](onboarding-flow.svg) embedded in the [onboarding architecture](architecture.md). Update both representations when the flow changes.

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
    H --> J["Create platform passkey"]
    J --> K["POST /passkeys/complete"]
    K --> N["Invite identity check or skip"]
```
