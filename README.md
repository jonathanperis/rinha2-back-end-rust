# rinha2-back-end-rust

> Rust/Actix-web 4 implementation for the Rinha de Backend 2024/Q1 challenge with SQLx async driver and PostgreSQL stored procedures

[![Build Check](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check.yml) [![Main Release](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/main-release.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/main-release.yml) [![CodeQL](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/codeql.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/codeql.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Live demo →](https://jonathanperis.github.io/rinha2-back-end-rust/)** | **[Documentation →](https://jonathanperis.github.io/rinha2-back-end-rust/docs)**

---

## About

A Rust implementation of the Brazilian backend challenge Rinha de Backend 2024/Q1, where a fictional bank API must handle concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total). The current API is a single `src/WebApi/main.rs` entrypoint (173 total lines at this revision) using Actix-web 4 with the Tokio runtime and SQLx 0.8 for PostgreSQL access.

## Tech Stack

| Technology | Version / Source | Purpose |
|-----------|------------------|---------|
| Rust | edition 2024; Docker builder `rust:1.95`; CI uses `dtolnay/rust-toolchain@stable` | API implementation |
| Actix-web | 4 | Async HTTP framework |
| SQLx | 0.8 | PostgreSQL driver with offline query metadata (`.sqlx/`) |
| Tokio | 1 (`full`) | Async runtime |
| PostgreSQL | 16.7 Alpine | Database with stored procedures |
| NGINX | 1.27 Alpine | Reverse proxy and load balancer (`least_conn`) |
| Docker | Compose + Buildx | Multi-stage image build and orchestration |
| k6 | `ghcr.io/jonathanperis/rinha2-back-end-k6:latest` | Stress testing |

## Architecture

```
NGINX (:9999, least_conn)
├── webapi1-rust (:8080, 0.4 CPU, 100MB; host :6968 in dev)
├── webapi2-rust (:8080, 0.4 CPU, 100MB; host :6969 in dev)
└── PostgreSQL (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance update + validation
    └── GetSaldoClienteById() — statement with JSONB aggregation
```

| Service | CPU | RAM |
|---------|-----|-----|
| webapi1/2 | 0.4 each | 100MB each |
| PostgreSQL | 0.5 | 330MB |
| NGINX | 0.2 | 20MB |
| **Total** | **1.5** | **550MB** |

## Features

- Single Rust API entrypoint (`src/WebApi/main.rs`, 173 total lines at this revision)
- Actix-web route handlers for transactions, statements, and `/healthz`
- SQLx compile-time query validation with offline cache (`src/WebApi/.sqlx/`)
- PostgreSQL stored procedures for server-side balance updates and statement aggregation
- UNLOGGED `Clientes` and `Transacoes` tables for challenge-oriented write throughput
- Lazy static `HashMap` for the five seeded client limits (no DB round-trip for client existence checks)
- PostgreSQL tuned for benchmark throughput: `synchronous_commit=0`, `fsync=0`, `full_page_writes=0`
- Multi-platform GHCR release flow: `latest` is assembled as a multi-arch manifest from amd64 and arm64 builds; `latest-arm64` is also pushed during the arm64 leg
- Development observability stack with Prometheus, Grafana, InfluxDB, and postgres-exporter
- Committed stress-test report artifacts under `docs/public/reports/`; treat generated reports, not hard-coded README numbers, as the performance source of truth

## Getting Started

### Prerequisites

- Docker with Docker Compose

### Quick Start

```bash
git clone https://github.com/jonathanperis/rinha2-back-end-rust.git
cd rinha2-back-end-rust
docker compose up nginx -d --build
```

API available at `http://localhost:9999`.

The dev compose file also exposes the API instances directly on `localhost:6968` and `localhost:6969`; use the NGINX port (`9999`) for challenge-compatible requests.

### API Endpoints

| Method | Path | Status Codes | Description |
|--------|------|-------------|-------------|
| POST | `/clientes/{id}/transacoes` | 200, 404, 422 | Submit debit or credit transaction for client IDs 1-5 |
| GET | `/clientes/{id}/extrato` | 200, 404 | Get account balance statement with the 10 most recent transactions |
| GET | `/healthz` | 200 | Health check returning `Healthy` |

Transaction payload validation is handled in Rust before the stored procedure call: `tipo` must be `c` or `d`, `descricao` must be non-empty and at most 10 characters, and `valor` must be positive. The JSON input accepts the lowercase fields used by the challenge (`valor`, `tipo`, `descricao`) and PascalCase aliases (`Valor`, `Tipo`, `Descricao`) because the DTO includes Serde aliases.

Current business-limit behavior is source-backed by `InsertTransacao`: if a debit would exceed the client's limit, PostgreSQL leaves the balance unchanged, does not insert a transaction row, and returns the current balance to the API. Therefore `422` is used for invalid payloads or SQL errors, while this over-limit path currently responds with `200` and the unchanged balance payload.

Client limits are seeded in both the Rust `CLIENTS` map and the PostgreSQL dump:

| Client ID | Limit |
|-----------|-------|
| 1 | 100000 |
| 2 | 80000 |
| 3 | 1000000 |
| 4 | 10000000 |
| 5 | 500000 |

### Run Stress Tests

```bash
cp .env.example .env
docker compose up k6 --build --force-recreate
```

The dev compose path runs k6 in `MODE=dev` with InfluxDB/Grafana export, so `.env` must provide `INFLUXDB_PASSWORD` and `INFLUXDB_TOKEN` values for the local observability stack. The production compose file used by the release workflow runs k6 in `MODE=prod` and exports an HTML report artifact.

## Project Structure

```
rinha2-back-end-rust/
├── src/WebApi/
│   ├── main.rs              # Complete API entrypoint (173 total lines at this revision)
│   ├── Cargo.toml           # Rust 2024 package and dependencies
│   ├── Dockerfile           # Multi-stage: rust:1.95 → debian:bookworm-slim
│   └── .sqlx/               # SQLx offline query cache
├── docker-entrypoint-initdb.d/
│   └── rinha.dump.sql       # UNLOGGED schema + stored procedures + seed data
├── docker-compose.yml       # Dev stack: APIs, PostgreSQL, NGINX, observability, k6
├── prod/docker-compose.yml  # Release/load-test stack using GHCR images and prod k6 mode
├── nginx.conf               # Load balancer config
├── docs/                    # Astro/Bun GitHub Pages site and wiki markdown
├── scripts/check_docs_drift.py # Source-backed README/wiki drift guard
└── .github/workflows/       # build-check, main-release, deploy, codeql
```

## CI/CD

| Workflow | Trigger | Description |
|----------|---------|-------------|
| Build Check | Pull requests to `main`; manual dispatch | Rust release build, docs drift guard, and Docker Compose `/healthz` test |
| Main Release | Push to `main`; manual dispatch | Rust release build, amd64 + arm64 GHCR image pushes, multi-arch manifest merge, production compose healthcheck, k6 report artifact upload |
| CodeQL | Push to `main`, pull requests to `main`, Monday weekly schedule | Rust CodeQL analysis with `security-and-quality` queries |
| Deploy to GitHub Pages | Push to `main`; manual dispatch | Reusable shared workflow that builds `docs/` with Bun and deploys GitHub Pages |

**Docker image:** `ghcr.io/jonathanperis/rinha2-back-end-rust:latest`

## Documentation Drift Guard

README and wiki facts that mirror code, Docker, Compose, or workflow state are checked by:

```bash
python3 scripts/check_docs_drift.py
```

The guard verifies high-value source-backed facts such as API line count, Docker builder version, Rust edition, endpoint coverage, workflow triggers, wiki navigation coverage, and known-stale phrases.

## License

MIT — see [LICENSE](LICENSE)
