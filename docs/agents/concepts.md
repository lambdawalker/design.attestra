# Components and terminology

The [system architecture](../../architecture.md) owns trust boundaries. Android owns interaction, permission/camera lifecycle, protected client state and native credential operations. The Go API owns proof validation, Cognito orchestration and private evidence capture. AWS services implement storage, delivery, account identity and asynchronous work.

A **proof** authorizes email confirmation under the onboarding protocol. A **session** authorizes authenticated requests. An **evidence manifest** pins exact S3 versions. A **parse result** is extracted data with provenance. A **review** records user corrections. A **validation decision** is an independent assurance result. None of these is interchangeable.

The **environment index** publishes public client configuration. Its configuration hash identifies configuration content; it does not identify deployed code, certify health or authenticate a mobile user. Local deployment receipts coordinate writes and recovery; they are not user sessions.

The [catalog](../repositories.md) records source owners and known documentation availability. Follow exact implementation guides for configuration, APIs and platform limitations. Central specifications do not allocate library release numbers.
