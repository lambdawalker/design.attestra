# UI evidence policy

Existing captures are historical design prototypes. The manifest pins current file hashes but does not invent their original capture provenance. Do not label them running-application or regenerate them in ordinary documentation builds. Adjacent `spec.md` files explain current semantics and prototype gaps.

The site copies only manifest-listed PNGs, verifies hashes, and never executes prototype HTML. New capture acceptance requires a synthetic fixture, pinned renderer and assets, viewport/locale/clock configuration, source ref, visual inspection, and an intentionally reviewed manifest update. Browser capture of an HTML prototype is not an Android device test. External Tailwind/fonts are unpinned legacy dependencies; offline reproduction of the historical rendering is not guaranteed.

On 2026-10-28 the six existing tracked PNGs were visually reviewed against their scenario names after the build detected stale manifest hashes. Their bytes are unchanged from source `a0d5024`; the manifest now records those actual bytes and source ref. They show historical email, card and passkey prototypes, not the current Android capture/review/finish implementation. No new screenshot or renderer provenance is claimed.
