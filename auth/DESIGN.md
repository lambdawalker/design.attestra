# Design System: Auth for Go Onboarding

Use this file as the common visual and interaction brief when generating onboarding and login screens in Google Stitch. Feature prompts: [onboarding](onboarding/stitch.md) and [login](login/stitch.md). The product name, logo, legal copy, and final hostname have not been selected; use neutral sample copy and editable brand text instead of inventing a company identity.

## 1. Visual Theme & Atmosphere

A calm, precise identity flow with the clarity of a well-made document and the restraint of a trusted utility. Density 4/10, variance 5/10, motion 3/10. Distinctive left-aligned headlines and generous negative space, with progress shown by clear language and state rather than celebration effects. In authentication screens, the task itself is the first impression: do not add a decorative marketing hero or imagery that competes with entering an email or approving a passkey.

## 2. Color Palette & Roles

Use one consistent cool zinc neutral scale and one restrained teal accent. Check contrast of actual text, control, and focus color combinations against WCAG AA; adapt state colors if necessary without adding a second brand accent.

| Token | Value | Role |
| --- | --- | --- |
| Paper Canvas | `#F7F8F8` | Full-page background |
| Clear Surface | `#FFFFFF` | Inputs and small raised surfaces |
| Charcoal Ink | `#20282B` | Primary copy, icons, headings |
| Slate Copy | `#4E5B60` | Supporting copy and metadata |
| Mist Border | `#DCE2E3` | Dividers and input outlines |
| Harbor Teal | `#176B64` | Only accent: primary action, active focus, verified status |
| Error Ink | `#9B3435` | Error text and outlines only; never a second brand accent |

Provide dark-mode equivalents using the same zinc/teal family. Preserve readable foreground contrast and visible focus rings in both modes. A code or passkey credential is never printed in a decorative graphic.

## 3. Typography Rules

- **Display:** Geist, weight 600, tracking `-0.025em`; web `clamp(1.8rem, 3vw, 2.6rem)`. Clear task statements rather than all-caps marketing copy.
- **Body and controls:** Geist, `1rem` or larger, line-height 1.5; constrain explanatory text to about `62ch`.
- **Codes and technical detail:** Geist Mono, `0.875rem` minimum. Preserve text selection and platform autofill behavior.
- **Native:** use platform text scaling and equivalent system fonts if Geist is unavailable. Do not lock Android font scale or iOS Dynamic Type.
- Avoid Inter, generic serif typefaces, and all-caps form labels.

## 4. Component Stylings

- **Primary button:** one per step; Harbor Teal fill with high-contrast text, 12px corners, at least 44px height. Press shifts down 1px. Disabled has a separate clearly discernible state. Never use a glowing shadow.
- **Text action:** underlined or otherwise clearly recognizable, e.g. “Use email code instead,” “Resend email,” or “Skip for now”; do not disguise recovery as small decorative text.
- **Input:** visible label above, example/helper below when needed, error below the field. Full email address can be edited. OTP supports paste, one-time-code autofill, and manual entry; segmented visuals must still behave as one accessible input.
- **Surfaces:** prefer spacing and thin dividers. A shallow surface around the active form is acceptable when it improves reading; avoid three equal cards and heavy glass effects.
- **Status:** pair words with icons or color; “Email verified” and “Passkey added” are separate states. Never signal identity/address approval from an auth success state.
- **Loading:** keep the current action label and add a small progress treatment or layout-matched skeleton only when needed. Never run an indefinite animated loop for a stable verified state.
- **Error:** show an inline explanation and a concrete next action. Keep partially completed form data; avoid exposing Cognito exception strings.

## 5. Layout Principles

- Web: `max-width: 72rem` overall; active form column `min(100%, 28rem)`, left-aligned within a two-column shell only where supporting context earns the space. Native: one column with comfortable safe-area insets.
- Use a spacing rhythm of 8, 12, 16, 24, 32, and 48px. Place the primary action immediately after the task form, then recovery actions.
- Below 768px, collapse to one column. No horizontal scrolling or forced viewport-height cards. Support keyboard opening without obscuring the action or OTP entry.
- The `/verify-email` landing view may present the pending email and a confirm action; simply rendering that view never sends the verification request.
- When the installed app claims the HTTPS link, render the same state as the website. If the app does not claim it, the website handles it on the application domain.

## 6. Motion & Interaction

- Use short 120–220ms opacity/transform transitions for transitions between form states. A spring with stiffness 100 and damping 20 is appropriate only for small optional surfaces; auth submit and security feedback should feel steady.
- Animate transform and opacity only. A pending network operation may show a subtle repeating progress cue; stop it on completion, error, or timeout.
- Honor `prefers-reduced-motion` and the native reduced-motion setting by using instant state changes. Do not animate verification codes, secret values, or error text into view character by character.
- Keep keyboard focus predictable: on errors move focus to the error summary or field, on completed steps announce the new status, and preserve the back path without submitting again.

## 7. Anti-Patterns (Banned)

No emojis, neon or purple glows, oversaturated gradients, pure black, custom cursors, spinning success badges, decorative biometrics, three equal feature cards, invented trust statistics, marketing clichés, or generic placeholder identities. No page-load request that confirms email. No raw Cognito error text in the UI. No promise of “identity verified” or “address verified” after only email or passkey completion.
