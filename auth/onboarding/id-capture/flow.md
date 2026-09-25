# ID capture subflow

This expands the optional identity branch of the [overall onboarding flow](../onboarding-flow.md). Camera capture belongs to the selected plugin; the application owns the surrounding screens and recorded decisions.

```mermaid
flowchart TD
    S["Authenticated account"] --> C{"Start identity check?"}
    C -->|Skip| D["Continue to dashboard"]
    C -->|Start| P["Launch capture plugin"]
    P --> X{"Capture returned?"}
    X -->|Cancel or error| R["Retry capture or leave"]
    X -->|Yes| E["Process document"]
    E --> L{"Readable?"}
    L -->|No| U["Retake unreadable document"]
    U --> P
    L -->|Yes| V["Review and correct fields"]
    V --> Q["Submit evidence"]
    Q --> T{"Submission accepted?"}
    T -->|No| F["Reconcile; retry if needed"]
    T -->|Yes| W["Wait for identity decision"]
    W --> O{"Decision?"}
    O -->|Approved| A["Show approved result"]
    O -->|Pending| H["Show pending status; check later"]
    O -->|Unsuccessful| N["Show result and next action"]
```

An accepted upload or readable document does not mean identity approval. The separate automated report and external provider decision follow the [identity architecture](../../../verification/identity/architecture.md). “Unsuccessful” needs a dedicated screen and policy-specific retry or support action; see [UI](ui.md).
