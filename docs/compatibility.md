# Compatibility and evidence ledger

Latest source synchronization: **2026-11-15**. The October audit and observations below remain historical; the latest section supersedes their current-flow descriptions.

Historical audit date: 2026-10-11 UTC (2026-10-10 in Ciudad Juárez). Documentation scope is `main`, not a coordinated product release.

| Area | Designed | Implemented evidence | Verification / gap |
| --- | --- | --- | --- |
| Email/passkey/sign-in/session | Onboarding/login specifications | Backend `64f4faea74e71a82795560e4b43e195d820a5242`; Android source `5e017bd2fa74edf5b2a083c72b132c1f5cbffba7` | Unit tests exist; this documentation task does not certify real-device passkeys or SES delivery |
| ID capture | Separate immutable evidence stage | Backend `capture`, `captureapi`, `awscapture`; Android capture guide | Runtime policy controls availability. Real S3/device smoke checks remain required |
| ID parsing | Vision extraction + revisioned review | Gemma extraction and review in card capture `2153d460`; Android early upload and timings in `026e6ec8` | Source reviewed; deployed revision and real-device OCR accuracy and latency need environment evidence |
| ID validation | Separate assurance feature | Deferred | Must not infer success from capture or parsing |
| Environment discovery | Shared public configuration, fenced writes | Backend `registry`, `infra-index`, operator workflows at `64f4fae` | One account/region; Android runtime discovery remains separate |
| Setup and health | Staged prerequisites/readiness and resumable operations | Backend wizard source | User reported dev and QA complete on 2026-10-10; not independently reproduced by this doc audit |
| Teardown | Environment removal distinct from index removal | Backend `teardown` and `teardown-index` at `64f4fae` | Tests/fakes and build evidence; live shared-index destruction was not executed |
| UI prototypes | Shared screen intent | Historical HTML and six PNG assets | Design-prototype only; original capture tool/source identity unknown |

## Deviations and open decisions

- Capture validates and freezes evidence before automatic extraction. The live implementation records extraction on the capture itself, with `image_revision` identifying the finalized pair across worker updates. The parsing design also describes a distinct job lifecycle.
- The application source at `9ee15b1e` selects the capture worker with medium reasoning effort. Source pins and isolated benchmark measurements do not verify an AWS rollout or establish live latency.
- The capture record stores `extraction` and `reviewed` separately.
- Independent parse-job endpoints and the richer provenance/warning model in the target architecture are not the current wire API. Use backend transport docs.
- The coordinated [Android finish-screen PR #34](https://github.com/lambdawalker/android.attestra.auth/pull/34) adds server-confirmed Details saved routing. The PR was merged. Deployment evidence is tracked separately. Manual review support was merged in backend PR #36 and direct capture in Android PR #33.
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

## Source synchronization 2026-11-15

| Area | Merged source evidence | Current contract and verification boundary |
| --- | --- | --- |
| Unified email entry | [Android #78](https://github.com/lambdawalker/android.apexfission.auth/pull/78), [verify-email #6](https://github.com/lambdawalker/go.apexfission.aws.verifyemail/pull/6), [design #15](https://github.com/lambdawalker/design.attestra/pull/15) | One waiting/code surface. A+B is automatic on matching link open; A+C and B+C require explicit code submission. Proof pairs remain transaction-bound and share manual-code budgets. |
| Saved ID review | [Android #79](https://github.com/lambdawalker/android.apexfission.auth/pull/79) | Save and continue returns automatically only after matching server-reviewed data and origin. Account review opens the saved form directly. Legacy saved-state components are not a mandatory success handoff. |
| Camera permission | [Android #80](https://github.com/lambdawalker/android.apexfission.auth/pull/80) | After accepted disclosure and the fresh policy check, request native permission without a duplicate explanation. Preserve denial/Settings/no-camera recovery; standalone camera entry remains explanation-first. Real-device prompt/lifecycle validation remains separate. |
| Composition | [Application #31](https://github.com/lambdawalker/go.attestra.aws/pull/31) | Root, infrastructure and deploy modules pin verify-email `v0.0.0-20261115061044-1963f90999f5`, which supports A+C. The later email-copy-only [#7](https://github.com/lambdawalker/go.apexfission.aws.verifyemail/pull/7) is on feature main but is not included in this application pin. No rollout is certified. |
| Source licensing | [Android #81](https://github.com/lambdawalker/android.apexfission.auth/pull/81) | Project-owned modules declare Apache 2.0; component repositories own license/third-party notices. This is not a package publication. |

The immutable source refs for the nine inspected implementation repositories are recorded in [repositories.json](repositories.json). Source observations were captured on 2026-11-15 at 19:25 UTC. The Android main ref was rechecked during completion and still matched `f356a5b3e168f720ed6b542647b89d89e3e60234`.

The catalog now includes the independent email-verification feature, `go.infra.composer`, and `android.ui.common`. The legacy combined backend remains a separate migration source. Current deployment and feature binding belong to `go.attestra.aws`; changing a repository name or dependency does not migrate live state.

**Documentation drift outside this repository:** some Android consumer-guide sentences still list only A+B/B+C, and some module README links retain older names or task branches. Source validation and the current central contract take precedence; those implementation-owned guide corrections are follow-up work, not evidence that the source lacks A+C.

**Still not implemented by these changes:** automatic submission of the sixth code digit, removing all optional enrollment interruptions, continuous front/back capture, a combined photo/data review screen, richer independent parse-job endpoints, ID validation, and complete web/iOS clients. These remain design or follow-up work, not implicit outcomes of fewer screens.

**Hosting and readiness:** GitHub reports Pages enabled for central design and Android, which supersedes the old disabled-hosting assumption. This audit could not independently retrieve the public HTTP pages. No AWS deployment, real email delivery, live ID upload, state migration, package release, or real-device test was performed.

**Older PR reconciliation:** #14's missing A+C diagram/AWS details and one-time-code semantics are incorporated without restoring its extra Enter verification code button. #11's useful Android raw-guide/catalog links are incorporated with current repository names. Historical screenshots remain byte-identical; their existing provenance is retained. The older branches should not be merged over the newer flow.

### Validation of this synchronization

- `python sites/test_build.py`: four renderer/link-transformation tests passed.
- `python sites/test_current_contracts.py`: six regression tests passed for proof-pair coverage, review routing, permission boundaries, source ownership, translation bindings and temporary-file cleanup. These tests failed against the pre-update content.
- `python sites/catalog.py --check`: generated catalog matches its JSON source.
- `python sites/build.py`: 72 canonical pages rendered as English/Spanish views, with 145 HTML pages validated for local links, anchors and project-base routing.
- `git diff --check`: no whitespace errors. Current external source-file targets were checked against the downloaded implementation snapshots; live external HTTP reachability is not implied.

No historical HTML or PNG asset was changed. No `sites/dist`, transfer payload, temporary workflow, credential or runtime receipt is part of the final change.
