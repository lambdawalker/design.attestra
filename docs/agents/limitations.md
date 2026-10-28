# Status, limitations and decisions

Read [compatibility and deviations](../compatibility.md) before treating design as implementation evidence. Backend source now includes capture, the shared environment index and resumable setup/teardown. Parsing and independent ID validation remain designed/deferred. Android source includes capture and a debug mock; the mock does not validate real S3/device behavior.

The operator reported completed dev and QA setup/health checks on 2026-10-10. This is explicitly operator-reported deployment evidence, not a reproducible test of email delivery, passkeys, document parsing or live capture. Capture remains opt-in by configuration. Keep verified test results separate from these reports.

One index currently serves a single AWS account/region. Production account isolation, cross-account publication, provider choices for parsing/validation and complete web/iOS clients remain open. The API stack does not host the app domain or association files. Cognito permits password authentication at the provider configuration level although the client UI offers passkeys/email OTP.

Documentation is current-source English with Spanish integration guides and same-revision English fallback for untranslated detailed specifications. There are no confirmed system releases or historical release manuals yet. The central site cannot claim a library release merely because a design is approved; publishing owners maintain installation metadata.

The [documentation ownership policy](../../DOCUMENTATION.md) is authoritative. Release automation is audited, not changed into package publication. Other repositories' missing sites or agent entries are recorded as gaps; this task updates only the backend and central design repositories.
