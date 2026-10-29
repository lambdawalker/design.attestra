# Compatibility and evidence ledger

Audit date: 2026-10-11 UTC (2026-10-10 in Ciudad Juárez). Documentation scope is `main`, not a coordinated product release.

| Area | Designed | Implemented evidence | Verification / gap |
| --- | --- | --- | --- |
| Email/passkey/sign-in/session | Onboarding/login specifications | Backend `64f4faea74e71a82795560e4b43e195d820a5242`; Android source `5e017bd2fa74edf5b2a083c72b132c1f5cbffba7` | Unit tests exist; this documentation task does not certify real-device passkeys or SES delivery |
| ID capture | Separate immutable evidence stage | Backend `capture`, `captureapi`, `awscapture`; Android capture guide | Disabled by default; real S3/device smoke gate remains required |
| ID parsing | Vision extraction + revisioned review | Backend `9d9f87685589a1cf307341c8b788221a1b45535c`; Android `dfd5159bcacc8c3536720849470e415d956c67ad` | Automatic extraction, revisioned review and failed-extraction manual entry implemented; cloud accuracy/device smoke checks remain |
| ID validation | Separate assurance feature | Deferred | Must not infer success from capture or parsing |
| Environment discovery | Shared public configuration, fenced writes | Backend `registry`, `infra-index`, operator workflows at `64f4fae` | One account/region; Android runtime discovery remains separate |
| Setup and health | Staged prerequisites/readiness and resumable operations | Backend wizard source | User reported dev and QA complete on 2026-10-10; not independently reproduced by this doc audit |
| Teardown | Environment removal distinct from index removal | Backend `teardown` and `teardown-index` at `64f4fae` | Tests/fakes and build evidence; live shared-index destruction was not executed |
| UI prototypes | Shared screen intent | Historical HTML and six PNG assets | Design-prototype only; original capture tool/source identity unknown |

## Deviations and open decisions

- Capture automatically schedules extraction after file readiness. `extraction` and `reviewed` are stored separately on the capture resource; there is no identity decision.
- Independent parse-job endpoints and the richer provenance/warning model in the target architecture are not the current wire API. Use backend transport docs.
- The coordinated [Android finish-screen PR #34](https://github.com/lambdawalker/android.attestra.auth/pull/34) adds server-confirmed Details saved routing. This ledger does not assert that PR is deployed. Manual review support was merged in backend PR #36 and direct capture in Android PR #33.
- Older combined identity mock contracts must not be used as the production capture protocol. Backend transport documentation owns current serialization.
- Cognito `PASSWORD` allowance is a provider constraint despite passwordless client UI. Strong provider-level prohibition needs a separate decision.
- Cross-account index federation and production isolation are not solved by environment naming or scoped publication alone.
- Documentation sites for this central repository and backend are added by this coordinated change, but Pages was disabled at audit time. Hosting must be enabled before advertising them as live.

## Release and documentation policy

Neither target repository had a GitHub release at audit time. This ledger is a source-review record, not a published compatibility matrix. No Android artifact version combination is certified here. Publishing repositories own their `IMPORT.md` and release catalogs; central docs link to those records rather than allocating versions.

The initial archive boundary is current-source documentation only. Historical release records must name immutable code and documentation refs, confirmed installation facts and translation/media provenance before they are advertised. Preserve existing historical design paths as historical material; they are not release-specific SDK manuals.

See the [documentation audit](documentation-audit.md) for the checks actually executed and remaining limits.

## Capture/review update — 2026-10-28 (Ciudad Juárez)

Reviewed the merged source refs above and the coordinated finish-screen change. Capture, extraction and review are distinct outcomes. A failed extraction may still produce a saved manual review; pending extraction and unsafe/unvalidated files may not. `reviewed` confirms data persistence; `id_captured`/`onboarding_complete` do not. The finish screen makes no identity-verification claim. Existing audit evidence for unrelated features remains dated above; no deployment or device validation is implied by this update.
