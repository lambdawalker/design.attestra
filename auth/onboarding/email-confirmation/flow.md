# Email confirmation subflow

This diagram expands the email portion of the [overall onboarding flow](../onboarding-flow.md). A, B, and C are internal proof names; the UI never displays them. A is retained by the initiating client, B is in the link, and six-digit C appears separately in the same email.

```mermaid
flowchart TD
    S["Enter email; retain A"] --> Q["Request signup with A challenge"]
    Q --> M["Send link B and separate code C"]
    M --> D{"Use link or visible code field?"}
    D -->|Open link| L["Open verification link"]
    D -->|Code on initiating client| C1["Enter or paste C; tap Verify email"]
    C1 --> AC["Submit A+C"]
    L --> X{"Matching A here?"}
    X -->|Yes| Y["Submit A+B automatically"]
    X -->|No| Z["Enter C and tap Verify"]
    Z --> W["Submit B+C"]
    Y --> V{"Proof valid and unused?"}
    AC --> V
    W --> V
    V -->|No| R["Show code, link, or retry recovery"]
    V -->|Yes| F["Confirm email and issue session"]
    F --> H{"Session available?"}
    H -->|Yes| P["Load policy and next unmet enrollment step"]
    H -->|No| O["Email sign-in recovery"]
```

The waiting screen already contains the code field; there is no Enter verification code navigation button. Its retained A allows the initiating client to submit A+C without opening a link. Opening the link with GET or HEAD has no confirmation side effect. A link scanner without A sees only the manual-entry screen; B alone cannot spend C attempts. An email processor that reads both B and C from the message is outside this protection. Only the client that submits a valid proof can receive the session. See [architecture](architecture.md) for atomic state and recovery rules.
