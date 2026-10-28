# UI semantics and evidence

Use the [screen index](../../auth/onboarding/ui-reference/README.md) and the `spec.md` next to each HTML reference. Screen IDs remain the established directory names. A spec gives entry/exit, fields/actions, visible states, accessibility requirements, service ownership and known prototype limitations.

HTML prototypes are design references, not running backend integrations. Timers, buttons or success banners do not establish email delivery, session issuance, passkey registration or identity decisions. The site links HTML as source rather than executing it in the documentation origin. Existing PNGs are labeled `design-prototype`; their original renderer/source hashes are unavailable. They are retained historical references, not newly verified implementation screenshots.

The [capture manifest](../screenshots/manifest.json) records provenance limits and source locations. No production-app capture is claimed. New accepted captures need synthetic data, a controlled renderer/configuration, explicit source identity and visual review. Do not silently replace historical images during a site build.

Email manual code entry requires one accessible six-digit field with paste/autofill. Loading states reflect actual in-flight tasks and have timeout/recovery behavior. Passkey dialogs belong to the operating system. Capture photo preview/upload and parsing review need additional variants listed in the feature UI specifications; a historical identity-success screen belongs to deferred validation, never capture success.
