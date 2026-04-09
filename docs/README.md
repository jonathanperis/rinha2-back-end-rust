# rinha2-back-end-rust — GitHub Pages

Astro 5 static site for the [rinha2-back-end-rust](https://github.com/jonathanperis/rinha2-back-end-rust) project. Deployed to GitHub Pages at [jonathanperis.github.io/rinha2-back-end-rust](https://jonathanperis.github.io/rinha2-back-end-rust/).

## Stack

| Technology | Purpose |
|---|---|
| Astro 5 | Static site generator |
| React 19 | Interactive islands (docs sidebar, search, scrollspy) |
| Tailwind CSS v4 | Utility-first styling for docs components |
| `@astrojs/sitemap` | Auto-generated sitemap |

## Structure

```
docs/
├── public/
│   ├── images/          # Grafana/Gatling metric screenshots
│   └── reports/         # k6 stress test HTML reports (appended by CI)
└── src/
    ├── components/
    │   ├── home/        # Landing page components (Navbar, Hero, Dashboard, Footer)
    │   └── docs/        # Docs page components (DocPageIsland, Sidebar, sections/)
    ├── hooks/
    │   └── useScrollspy.ts
    ├── layouts/
    │   └── BaseLayout.astro
    ├── pages/
    │   ├── index.astro  # Landing page
    │   └── docs.astro   # Documentation page
    └── styles/
        └── globals.css
```

## Commands

Run from this directory (`docs/`):

| Command | Action |
|---|---|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build to `./out/` |
| `npm run preview` | Preview the production build locally |

## Environment

Copy `.env.example` to `.env` and fill in your values:

```sh
cp .env.example .env
```

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Google Analytics 4 Measurement ID |

## Deployment

Deployed automatically on every push to `main` via `.github/workflows/deploy.yml`. The `PUBLIC_GA_ID` secret must be set in the repository's GitHub Actions secrets.
