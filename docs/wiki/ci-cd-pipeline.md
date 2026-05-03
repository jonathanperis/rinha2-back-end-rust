# CI/CD Pipeline

## Workflows

This repository uses four GitHub Actions workflows:

### build-check.yml

- **Trigger:** Pull requests to main
- **Steps:** Builds the Rust release binary, then runs Docker Compose and validates the healthcheck endpoint
- **Purpose:** Catch build failures and regressions before merging

### main-release.yml

- **Trigger:** Push to main branch
- **Steps:** Builds the release binary, builds and pushes a multi-platform Docker image (amd64/arm64) to GHCR, runs container healthcheck, then runs k6 load tests and uploads the stress test report as an artifact
- **Purpose:** Automated release of production-ready container images with load test validation

### codeql.yml

- **Trigger:** Push to main, pull requests to main, weekly schedule (Mondays)
- **Steps:** Runs CodeQL static analysis for Rust with security-and-quality queries
- **Purpose:** Continuous security and code quality analysis

### deploy.yml

- **Trigger:** Push to main branch
- **Steps:** Deploys the `docs/` directory to GitHub Pages using the actions/deploy-pages workflow
- **Purpose:** Publish project documentation and stress test reports to GitHub Pages
