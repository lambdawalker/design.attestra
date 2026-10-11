# UI evidence policy

Existing captures are historical design prototypes. The manifest pins current file hashes but does not invent their original capture provenance. Do not label them running-application or regenerate them in ordinary documentation builds. Adjacent `spec.md` files explain current semantics and prototype gaps.

The site copies only manifest-listed PNGs, verifies hashes, and never executes prototype HTML. New capture acceptance requires a synthetic fixture, pinned renderer and assets, viewport/locale/clock configuration, source ref, visual inspection, and an intentionally reviewed manifest update. Browser capture of an HTML prototype is not an Android device test. External Tailwind/fonts are unpinned legacy dependencies; offline reproduction of the historical rendering is not guaranteed.
