# ID parsing UI

Use the [shared onboarding design](../stitch.md) and [processing view](../ui-reference/onboarding_loading/code.html).

| View | Copy/action and boundary |
| --- | --- |
| Queued/running | “Reading your document.” Give a leave/resume option; poll every five seconds initially, then every fifteen seconds after three minutes. Pause in the background. |
| Long-running pending | “Your document is still processing.” Check status or return to account; do not promise a duration. |
| Unreadable | Identify affected side where available; start a new capture. No identity rejection wording. |
| Technical failure | For failed extraction with validated images, open an empty manual-entry form. Transport errors preserve state and offer recovery. |
| Review | Display extracted fields (or empty manual entry), editable values and required country of origin. Current client does not expose the richer planned cross-side warnings. |
| Save conflict | Preserve unsaved local edits, load the current review revision, and ask the user to resolve differences. |
| Confirmed | “Details saved” only after a matching server-stored review. Done returns to the account flow; Review details reopens saved values. No verified badge or identity-success screen. |

The existing [review details](../id-capture/ui-reference/identity_verification_review_details/code.html), [unreadable](../id-capture/ui-reference/identity_verification_document_unreadable/code.html), and [reading](../id-capture/ui-reference/identity_verification_reading_document/code.html) HTML files are layout references retained at historical paths. Their identity-oriented labels are superseded by this page. Android implements loading, review/manual entry and error recovery; the coordinated finish-screen change is tracked in [Android PR #34](https://github.com/lambdawalker/android.attestra.auth/pull/34). Historical HTML/screenshots are not current application captures.

Do not imply the model saw user-supplied values. Preserve raw text where useful for resolving ambiguity, but avoid unnecessary full document-number exposure outside focused review. Error messages, notifications, analytics and background previews contain no document content. Mock runs must show synthetic extraction and never masquerade as a real parsed ID.
