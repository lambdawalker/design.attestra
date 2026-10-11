# Compatibility and evidence ledger

Audit date: 2026-10-11 UTC (2026-10-10 in Ciudad Juárez). Documentation scope is `main`, not a coordinated product release.

| Area | Designed | Implemented evidence | Verification / gap |
| --- | --- | --- | --- |
| Email/passkey/sign-in/session | Onboarding/login specifications | Backend `64f4faea74e71a82795560e4b43e195d820a5242`; Android source `5e017bd2fa74edf5b2a083c72b132c1f5cbffba7` | Unit tests exist; this documentation task does not certify real-device passkeys or SES delivery |
| ID capture | Separate immutable evidence stage | Backend `capture`, `captureapi`, `awscapture`; Android capture guide | Disabled by default; real S3/device smoke gate remains required |
| ID parsing | Vision extraction + revisioned review | No production parser in reviewed backend | Model/provider and implementation pending |
| ID validation | Separate assurance feature | Deferred | Must not infer success from capture or parsing |
| Environment discovery | Shared public configuration, fenced writes | Backend `registry`, `infra-index`, operator workflows at `64f4fae` | One account/region; Android runtime discovery remains separate |
| Setup and health | Staged prerequisites/readiness and resumable operations | Backend wizard source | User reported dev and QA complete on 2026-10-10; not independently reproduced by this doc audit |
| Teardown | Environment removal distinct from index removal | Backend `teardown` and `teardown-index` at `64f4fae` | Tests/fakes and build evidence; live shared-index destruction was not executed |
| UI prototypes | Shared screen intent | Historical HTML and six PNG assets | Design-prototype only; original capture tool/source identity unknown |

## Deviations and open decisions

- Central pages previously called all capture work planned. Source capture is now implemented; parsing remains planned. Keep the normative capture/parsing boundary unchanged.
- The normative pipeline includes parsing after ready evidence. Current capture stops at ready evidence; there is no automatic parser or identity decision.
- Older combined identity mock contracts must not be used as the production capture protocol. Backend transport documentation owns current serialization.
- Cognito `PASSWORD` allowance is a provider constraint despite passwordless client UI. Strong provider-level prohibition needs a separate decision.
- Cross-account index federation and production isolation are not solved by environment naming or scoped publication alone.
- Documentation sites for this central repository and backend are added by this coordinated change, but Pages was disabled at audit time. Hosting must be enabled before advertising them as live.

## Release and documentation policy

Neither target repository had a GitHub release at audit time. This ledger is a source-review record, not a published compatibility matrix. No Android artifact version combination is certified here. Publishing repositories own their `IMPORT.md` and release catalogs; central docs link to those records rather than allocating versions.

The initial archive boundary is current-source documentation only. Historical release records must name immutable code and documentation refs, confirmed installation facts and translation/media provenance before they are advertised. Preserve existing historical design paths as historical material; they are not release-specific SDK manuals.

See the [documentation audit](documentation-audit.md) for the checks actually executed and remaining limits.
