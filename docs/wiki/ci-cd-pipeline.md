# CI/CD Pipeline

## Workflows

This repository uses four GitHub Actions workflows plus a source-backed docs drift guard.

### build-check.yml

- **Trigger:** Pull requests to `main` and manual dispatch
- **Rust build:** `cargo build --release --manifest-path ./src/WebApi/Cargo.toml`
- **Docs drift guard:** `python3 scripts/check_docs_drift.py`
- **Container smoke:** `docker compose -f ./docker-compose.yml up nginx --wait`, then `GET http://localhost:9999/healthz`
- **Purpose:** Catch Rust build failures, README/wiki drift, and compose health regressions before merging

### main-release.yml

- **Trigger:** Push to `main` and manual dispatch
- **Build/release path:** build Rust release binary, push amd64 image as `latest`, push arm64 image as `latest-arm64`, merge both digests into the multi-arch `latest` manifest
- **Validation:** start `prod/docker-compose.yml`, poll `/healthz`, then run k6 in `MODE=prod`
- **Artifact:** upload `./prod/conf/stress-test/reports/stress-test-report.html` as `stress-test-report`
- **Purpose:** Publish production-ready container images and preserve the load-test report from the release run

### codeql.yml

- **Trigger:** Push to `main`, pull requests to `main`, and weekly schedule (`0 3 * * 1`)
- **Steps:** Set up stable Rust, initialize CodeQL for Rust with `security-and-quality` queries, build the release binary, perform analysis
- **Purpose:** Continuous security and code quality analysis

### deploy.yml

- **Trigger:** Push to `main` and manual dispatch
- **Steps:** Calls the shared `jonathanperis/.github/.github/workflows/pages-docs-deploy.yml@main` reusable workflow with `package-manager: bun`
- **Purpose:** Build and publish the Astro docs site to GitHub Pages

## Local Documentation Drift Check

```bash
python3 scripts/check_docs_drift.py
```

The guard checks README/wiki claims against the current code and configuration: line count, Rust edition, Docker builder image, endpoints, workflow triggers, image tags, compose resources, and wiki navigation coverage. It also rejects known-stale phrases such as old line-count/version/performance claims.
