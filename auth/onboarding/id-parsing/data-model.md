# ID parsing data model

This is the shared semantic contract, not a deployed API schema. Exact serialization/OpenAPI schemas and schema validators belong in the [Go backend](https://github.com/lambdawalker/go.attestra.aws.auth). [Parsing architecture](architecture.md) owns behavior.

## Records

| Record | Required conceptual content |
| --- | --- |
| Parse job | Account binding, job ID, capture ID/evidence version, parser configuration version, operation key, state, attempt/lease generation, timestamps, safe error code |
| Extraction | Extraction ID, immutable capture/manifest reference, schema version, fields, warnings, model/prompt/preprocessing provenance, created time |
| Review revision | Extraction ID, revision, corrections, confirmation state/time, authenticated actor; expected revision on write |
| Current document pointer | Account, selected capture, selected extraction and confirmed review revision, conditional revision |

Provider details and internal diagnostics stay server-side. The client receives only the identifiers, safe field evidence, warnings and status necessary for review. Raw provider responses, if retained at all for debugging, are private with an explicit short retention policy and are never general-purpose logs.

## Extraction fields

Use a field envelope with `raw`, `normalized`, `status`, and source references. Both values are nullable. Status distinguishes `extracted`, `not_present`, `unreadable`, and `ambiguous`. A normalized value requires deterministic, unambiguous conversion; missing normalization never licenses guessing. A raw value may still be preserved for ambiguous text. Sources name the evidence slot and optionally a validated bounding region; unsupported regions are omitted, never invented. Coordinates must declare the derivative image and normalized coordinate system.

Initial semantic fields: full name; optional components only when printed and distinguishable; date of birth; address; document number; issuing country/authority; document type; issue date; expiration date. Required review fields depend on document policy: a passport without a printed residential address must not acquire a fake extracted address. Additional user-supplied profile information is explicitly labeled and kept outside the claimed extraction.

- Document numbers are strings. Preserve leading zeros, separators and script.
- Preserve full printed names, accents and multiple surnames. Do not force every culture into first/middle/last fields.
- Preserve printed dates; normalize to ISO date only when interpretation is supported. An ambiguous `03/04/1990` remains unresolved without document-specific evidence.
- Model-inferred country/type remains an extraction claim; match it against selected policy and flag contradictions.
- Do not collect extra machine-readable/barcode data merely because it is visible. Define any future decoder/cross-check as an explicit data-minimization decision.

Illustrative field envelope, not an actual person's data:

```json
{
  "document_number": {
    "raw": "00012345",
    "normalized": "00012345",
    "status": "extracted",
    "sources": [{ "slot": "front" }]
  },
  "address": {
    "raw": null,
    "normalized": null,
    "status": "not_present",
    "sources": []
  }
}
```

The server attaches provenance (`schema_version`, `model_id`, `prompt_version`, `preprocessing_version`, `capture_id`, `evidence_version`) from its job configuration. The model must not choose these values. Enforce bounded strings/arrays, known fields/enums and permitted schema versions; unknown or invalid results fail closed as parsing errors rather than application exceptions.

## Corrections and confirmation

A review request references extraction ID plus expected review revision and carries only user corrections/confirmation intent. The backend reads its immutable extraction, validates allowed editable fields, and saves a new attributed review revision. A field may be supplied by a user even when absent from the image, but that fact must remain visible to future consumers. Date/field validation errors stay on the review screen without losing edits.

Lost responses reconcile by operation key. Conflicting writes from another device return the current revision and require explicit resolution; no silent last-writer-wins. Editing a confirmed review creates a new unconfirmed revision. Any later validation record must bind to the exact confirmed revision it used, not a mutable “latest details” object.
