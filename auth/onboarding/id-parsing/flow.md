# ID parsing flow

```mermaid
flowchart TD
    A["Ready immutable capture"] --> B["Create or reconcile parse job"]
    B --> C["Queue and invoke vision model"]
    C --> D{"Output usable?"}
    D -->|Transient failure| E["Bounded retry; then failed status"]
    E -->|Retry permitted| C
    D -->|Unreadable evidence| F["Recapture through ID capture"]
    D -->|Structured extraction| G["Review fields and warnings"]
    G --> H["Save attributed corrections"]
    H --> I{"Revision matches?"}
    I -->|No| J["Resolve concurrent edits"]
    J --> G
    I -->|Yes| K["Confirm document details"]
    K --> L["Continue onboarding or account"]
    B -->|Leave while pending| M["Resume by saved job ID"]
    M --> G
```

Resume always retrieves current job status first; the diagram's resume-to-review edge applies only when extraction succeeded. A failed or pending job resumes its corresponding state. Confirming document details does not invoke ID validation or imply verified identity.
