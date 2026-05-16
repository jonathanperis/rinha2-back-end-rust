---
version: alpha
name: Rinha2 Rust Industrial
register: brand
description: Dark Rust-industrial benchmark showcase for a high-performance backend challenge implementation.
colors:
  primary: "#B34100"
  primaryBright: "#F74C00"
  secondary: "#DEA584"
  backgroundDeep: "#0E0B08"
  backgroundSurface: "#141010"
  backgroundMetal: "#1A1411"
  rustDark: "#2D1A00"
  textPrimary: "#F5F0EB"
  textBody: "#E2D8D0"
  textMuted: "#A89888"
  textSubtle: "#8A7A6C"
  borderSubtle: "#332218"
  borderMedium: "#5B3321"
  success: "#9CBF7A"
  warning: "#E6B450"
typography:
  display:
    fontFamily: Inter
    fontSize: 6rem
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "-0.06em"
  h1:
    fontFamily: Inter
    fontSize: 4.5rem
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.05em"
  h2:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  h3:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0em"
  bodyLarge:
    fontFamily: Inter
    fontSize: 1.2rem
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0em"
  label:
    fontFamily: JetBrains Mono
    fontSize: 0.78rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
  code:
    fontFamily: JetBrains Mono
    fontSize: 0.92rem
    fontWeight: 500
    lineHeight: 1.55
    letterSpacing: "-0.01em"
rounded:
  sm: 6px
  md: 10px
  lg: 16px
  xl: 22px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  section: clamp(4rem, 9vw, 8rem)
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.textPrimary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 16px
  button-secondary:
    backgroundColor: "{colors.backgroundDeep}"
    textColor: "{colors.primaryBright}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 16px
  surface-panel:
    backgroundColor: "{colors.backgroundSurface}"
    textColor: "{colors.textBody}"
    rounded: "{rounded.xl}"
    padding: 48px
  metric-tile:
    backgroundColor: "{colors.backgroundMetal}"
    textColor: "{colors.secondary}"
    rounded: "{rounded.lg}"
    padding: 24px
  badge:
    backgroundColor: "{colors.backgroundMetal}"
    textColor: "{colors.primaryBright}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: 10px
---

## Overview

The site should feel like a compact Rust performance rig: warm dark metal, oxidized orange, precise labels, and measured benchmark evidence. The current aesthetic is worth preserving, but future work should make it more intentional and less template-like by replacing generic hero-plus-cards rhythm with engineered artifacts: architecture rails, resource-budget diagrams, run timelines, and proof modules.

## Colors

- **Primary (#B34100):** WCAG-safe Rust orange for high-emphasis actions and identity marks.
- **Primary Bright (#F74C00):** Hot orange for active states and small interactive accents.
- **Secondary (#DEA584):** Warm copper for hero emphasis, numeric proof, and highlight states.
- **Background Deep (#0E0B08):** Page field, never pure black.
- **Background Surface (#141010):** Major panels and section surfaces.
- **Background Metal (#1A1411):** Badges, tiles, and inset controls.
- **Text Primary (#F5F0EB):** Headings and high-priority copy, never pure white.
- **Text Body (#E2D8D0):** Paragraph text.
- **Text Muted/Subtle (#A89888 / #8A7A6C):** Labels and secondary context. Use cautiously and verify contrast.

Use OKLCH equivalents in CSS when revising tokens, but keep this file in hex for DESIGN.md tooling compatibility. Avoid gradient text. If gradients remain, keep them as background atmosphere or hairline separators, not typography fill.

## Typography

Use Inter for display and prose, JetBrains Mono for code, labels, timestamps, badges, and compact metrics. Do not use monospace for long paragraphs. The brand can keep uppercase technical labels, but repeated all-caps section headers should be limited to areas that behave like instrumentation labels.

The hero may stay large, uppercase, and compressed. Body copy should become more readable by using proportional type, max line lengths around 65 to 75 characters, and stronger contrast than the current muted brown text in key explanatory paragraphs.

## Layout

The default page structure is a centered, single-surface brand landing page with dramatic vertical pacing. Future overhaul variants should preserve dark industrial atmosphere but explore stronger composition:

- A constrained max-width for prose and a wider max-width for diagrams and proof modules.
- Asymmetric hero layouts where architecture or benchmark proof appears in the first viewport.
- Section rhythm that alternates dense data modules with breathing room.
- Fewer identical cards. Use system diagrams, timeline strips, resource meters, and linked report rows where those better communicate backend evidence.

## Elevation & Depth

Depth comes from low-chroma borders, warm inner glow, copper hairlines, dark metal panels, and mechanical shadow offsets. Avoid decorative glassmorphism. Blur may be used only for sticky navigation legibility over animated background atmosphere.

## Shapes

Rounded rectangles can stay, but keep radii mechanical and consistent: 6px for chips, 10px for controls, 16px for metric tiles, 22px for large panels. Dashed circular cogs are acceptable as a background motif when subtle; they should not compete with content or create visual noise on mobile.

## Components

- **Primary button:** Rust-orange fill, terse uppercase label, clear focus ring, used for the main documentation path.
- **Secondary button:** Dark fill or outline for GitHub/source links. It should not visually tie the primary CTA.
- **Metric tile:** Copper number, explicit unit/context, optional source link or timestamp for auditability.
- **Report link:** Should read as a data row or compact artifact, not just a date chip. Include date, run type/status when available, and a clear hover/focus affordance.
- **Architecture module:** Prefer a schematic of NGINX, two API instances, and PostgreSQL over prose cards.
- **Stress-test proof module:** Pair headline metrics with provenance: workflow, k6, latest report link, and historical trend.

## Do's and Don'ts

Do:
- Keep the Rust-industrial palette and dark warm mood.
- Expose proof and constraints early.
- Use proportional body text for readability.
- Give benchmark numbers context, source, and units.
- Respect reduced motion and keyboard focus.

Don't:
- Use gradient-filled text.
- Turn every section into the same rounded card grid.
- Use monospace as a blanket style for all copy.
- Add decorative glow without an information role.
- Replace technical credibility with vague speed marketing.
