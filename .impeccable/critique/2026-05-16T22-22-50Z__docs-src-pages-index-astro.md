---
target: docs/src/pages/index.astro
total_score: 27
p0_count: 0
p1_count: 2
timestamp: 2026-05-16T22-22-50Z
slug: docs-src-pages-index-astro
---
# Impeccable Critique: rinha2-back-end-rust homepage

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---:|---:|---|
| 1 | Visibility of System Status | 2 | Benchmark numbers are visible, but latest/best/target provenance is not explicit. |
| 2 | Match System / Real World | 3 | Rust-industrial mood fits the challenge and audience. |
| 3 | User Control and Freedom | 3 | Clear docs/GitHub/report paths; no complex flows. |
| 4 | Consistency and Standards | 3 | Strong palette and component consistency, but repeated card grammar dominates. |
| 5 | Error Prevention | 2 | Not flow-heavy, but users can misread unsupported metric claims because source context is missing. |
| 6 | Recognition Rather Than Recall | 3 | Key stack and metrics are visible; architecture details require reading docs. |
| 7 | Flexibility and Efficiency | 2 | Technical reviewers need faster access to latest run, workflow, source, and architecture proof. |
| 8 | Aesthetic and Minimalist Design | 2 | Attractive, but too much generic hero, badges, card grids, glow, and gradient text. |
| 9 | Error Recovery | 3 | Mostly static navigation, low risk; report links are present. |
| 10 | Help and Documentation | 4 | Docs, GitHub, CI, reports, and archive links are surfaced. |
| **Total** |  | **27/40** | **Good foundation, needs proof-first restructuring.** |

## Anti-patterns Verdict

**LLM assessment:** Not AI slop, but it is close to the common dark developer landing template: centered hero, gradient-filled headline, pill badges, paired CTAs, rounded metric cards, glow/cog decoration, and repeated card grids. The content itself is credible and specific, which saves it from generic AI-site territory.

**Deterministic scan:** `npx impeccable detect --json src/pages/index.astro src/components/home src/layouts/BaseLayout.astro` returned one warning: `single-font` in `BaseLayout.astro`, reporting only Fira Code from linked font detection. Source inspection shows the broader issue is not literally one font, but mono-heavy body styling in `globals.css`.

**Technical audit:** Build succeeds with Bun/Astro. DESIGN.md lint passes with 0 errors and 7 non-blocking warnings for intentionally defined but currently unreferenced auxiliary tokens.

## Audit Health Score

| Dimension | Score | Key Finding |
|---|---:|---|
| Accessibility | 2/4 | Reduced-motion support exists, but muted text, orange-on-dark edge cases, gradient text, and focus-state visibility need a dedicated pass. |
| Performance | 3/4 | Static Astro build is lean; ambient particles, cogs, glow, and backdrop blur should remain bounded. |
| Responsive Design | 3/4 | Mobile breakpoints exist for core grids and CTAs; overhaul should test historical reports and nav density on narrow screens. |
| Theming | 2/4 | CSS variables exist, but palette is hex/RGBA mixed and not yet aligned to the new DESIGN.md token contract. |
| Anti-patterns | 2/4 | Gradient text, generic card grids, glow-heavy dark dev aesthetic, and mono-heavy copy are the main tells. |
| **Total** | **12/20** | **Acceptable, but the redesign should harden the design system.** |

## Overall Impression

The page has a strong Rust-industrial mood and useful proof artifacts, but it currently presents them through a familiar landing-page shell. The biggest opportunity is to turn it from an attractive dark developer landing page into a compact benchmark evidence machine.

## What's Working

1. **Distinct palette:** deep brown-black, oxidized orange, copper metrics, and warm muted text are coherent and worth preserving.
2. **Memorable hero:** “Blazingly Fast. Eventually Compiled.” has Rust-native personality without becoming pure meme copy.
3. **Real artifacts:** docs, GitHub, CI workflow, and historical stress reports make the page more credible than a generic speed-claim page.

## Priority Issues

### [P1] Benchmark proof lacks provenance

**Why it matters:** Technical reviewers need to know whether `46k+`, `<50ms`, and `99.9%` are latest, best, target, or representative values. Without source context, the page asks users to trust marketing-like claims.

**Fix:** Convert the stress metrics into a “latest verified run” module with timestamp, workflow source, report link, environment note, and constraint confirmation.

**Suggested command:** `impeccable layout`, then `impeccable clarify`.

### [P1] Architecture is too small for its importance

**Why it matters:** The implementation strategy is the differentiator: NGINX, two Actix instances, PostgreSQL stored procedures, strict CPU/RAM. Current prose cards undersell this.

**Fix:** Replace architecture cards with a compact system schematic and resource allocation rail.

**Suggested command:** `impeccable layout`.

### [P2] Repeated card grids make the page feel templated

**Why it matters:** The aesthetic is good, but generic cards flatten the story and trigger the “AI/devtool template” reflex.

**Fix:** Vary component grammar: resource meters, architecture rails, report rows, terminal/source plaques, and latest-run strips.

**Suggested command:** `impeccable bolder` or `impeccable overdrive` with same-aesthetic constraint.

### [P2] Typography overuses monospace and uppercase

**Why it matters:** Monospace everywhere reduces readability and makes the page feel more like costume terminal UI than serious technical communication.

**Fix:** Inter for body/prose, JetBrains Mono for instrumentation labels, code, metrics, timestamps, and badges.

**Suggested command:** `impeccable typeset`.

### [P2] Gradient text and decorative glow conflict with the new design contract

**Why it matters:** The headline looks polished, but gradient-filled text is banned in the Impeccable system and is a common AI landing-page tell.

**Fix:** Use solid copper/tinted text, typographic scale, tracking, and maybe a physical shadow/engraving treatment instead of gradient fill.

**Suggested command:** `impeccable polish`.

## Persona Red Flags

**Backend engineer comparing implementations:** Needs architecture, stored procedure strategy, and bottleneck tradeoffs faster than the current page provides.

**Rinha participant or reviewer:** Needs proof that numbers are under challenge constraints and a clearer latest/best/report archive model.

**Rust developer from GitHub/search:** Needs quick reasons to inspect the repo: ~140-line API, SQLx compile checks, stored procedures, unlogged tables, GHCR image.

**Accessibility-conscious technical user:** May struggle with muted text, all-caps density, mono-heavy paragraphs, and decorative motion if not carefully constrained.

## Same-aesthetic Overhaul Plan

### North Star

Preserve the dark Rust-industrial brand, but shift the page from `hero + cards` into `benchmark rig + evidence trail`.

### Proposed IA

1. **Hero + latest verified run:** split first viewport, headline on the left, current run evidence panel on the right.
2. **Constraint ledger:** CPU and RAM budget as segmented bars for NGINX, API 1, API 2, PostgreSQL.
3. **Architecture schematic:** NGINX to Actix instances to PostgreSQL stored procedures, with ports and resource caps.
4. **Implementation proof strip:** ~140 lines, SQLx offline cache, stored procedures, unlogged tables, least_conn, GHCR image.
5. **Stress-test archive:** convert date chips into compact audit rows with run date, status, headline metric, and report link.
6. **Docs/GitHub footer CTA:** quieter, with explicit “read architecture,” “inspect source,” and “open latest report.”

## A/B Testing Plan

### Test 1: Hero proof density

- **Hypothesis:** Putting verified benchmark proof in the first viewport increases trust and report engagement.
- **A/control:** Current centered hero, badges, CTAs, metrics below.
- **B:** Split hero with latest verified run panel above the fold.
- **C:** Constraint-first hero: `Rust banking API under 1.5 CPU / 550MB RAM`, with proof strip below.
- **Primary metric:** report link clicks and docs clicks.
- **Recommendation:** Try B first. It preserves the current hero while adding proof.

### Test 2: Architecture presentation

- **Hypothesis:** A schematic improves comprehension and increases GitHub/docs clicks.
- **A/control:** Current two prose architecture cards.
- **B:** NGINX → API/API → PostgreSQL diagram with ports and CPU/RAM.
- **C:** Resource-budget rail first, diagram second.
- **Primary metric:** docs architecture clicks, scroll depth, GitHub clicks.
- **Recommendation:** Try B first. It is clearer without changing narrative order too much.

### Test 3: Metric provenance

- **Hypothesis:** Metrics with timestamp/source outperform standalone metric cards.
- **A/control:** Current `46k+`, `<50ms`, `99.9%` cards.
- **B:** Each metric includes source label and links to latest report.
- **C:** One “latest run” module plus historical trend sparkline/list.
- **Primary metric:** latest report clicks, CI workflow clicks.
- **Recommendation:** Try C if implementation budget allows; otherwise B.

### Test 4: Typography readability

- **Hypothesis:** Proportional body copy improves reading and scroll depth without weakening the technical mood.
- **A/control:** Current mono-heavy body and uppercase labels.
- **B:** Inter body, JetBrains Mono only for instrumentation.
- **C:** Same as B plus fewer repeated all-caps labels and stronger contrast.
- **Primary metric:** scroll depth and docs click-through.
- **Recommendation:** Try B first because it matches DESIGN.md.

### Test 5: Report archive format

- **Hypothesis:** Audit rows make reports feel more credible than date chips.
- **A/control:** Current date/time grid.
- **B:** Compact table rows: date, time, status, headline metric, open report.
- **C:** Timeline rail grouped by day with latest/best badges.
- **Primary metric:** report clicks and “view all reports” clicks.
- **Recommendation:** Try B first for clarity and mobile resilience.

## Recommended Actions

1. `impeccable layout`: Rework homepage IA around latest verified run, constraint ledger, and architecture schematic.
2. `impeccable typeset`: Move body copy to Inter and reserve JetBrains Mono for instrumentation.
3. `impeccable clarify`: Tighten claims and label metrics with source/provenance.
4. `impeccable adapt`: Verify mobile layout for report archive and architecture schematic.
5. `impeccable polish`: Remove gradient text, improve focus/contrast, and refine motion.
