# Docs

Astro static site deployed to GitHub Pages.

## Commands

Run from this directory (`docs/`):

This Astro 6 site is built with Bun, uses Sätteri via `@astrojs/markdown-satteri` as the Markdown processor, and should be run with Node 22.12+ available on `PATH` for local npm/preview workflows.

| Command | Action |
|---|---|
| `bun install` | Install dependencies |
| `bun run dev` | Start dev server |
| `bun run build` | Build to `./out/` |
| `bun run preview` | Preview production build locally |

## Environment

Copy `.env.example` to `.env` and fill in local values when needed.

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Optional Google Analytics 4 Measurement ID |
