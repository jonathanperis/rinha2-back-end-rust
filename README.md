# rinha2-back-end-rust

> Rust/Actix-web 4 implementation for the Rinha de Backend 2024/Q1 challenge with SQLx async driver and PostgreSQL stored procedures

[![Build Check](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check.yml) [![Main Release](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/main-release.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/main-release.yml) [![CodeQL](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/codeql.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/codeql.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Live demo →](https://jonathanperis.github.io/rinha2-back-end-rust/)** | **[Documentation →](https://jonathanperis.github.io/rinha2-back-end-rust/docs)**

---

## About

A Rust implementation of the Brazilian backend challenge Rinha de Backend 2024/Q1, where a fictional bank API must handle concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total). Built as a minimal single-file API (~140 lines) using Actix-web 4 with Tokio async runtime and SQLx 0.8 for compile-time checked PostgreSQL queries.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Rust | 1.94 | API implementation |
| Actix-web | 4 | Async HTTP framework |
| SQLx | 0.8 | Compile-time checked PostgreSQL driver |
| Tokio | 1 | Async runtime |
| PostgreSQL | 16.7 | Database with stored procedures |
| NGINX | 1.27 | Reverse proxy and load balancer (least_conn) |
| Docker | - | Multi-stage build and orchestration |
| k6 | - | Stress testing |

## Architecture

```
NGINX (:9999, least_conn)
├── webapi1-rust (:8080, 0.4 CPU, 100MB)
├── webapi2-rust (:8080, 0.4 CPU, 100MB)
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

- Minimal single-file API implementation (~140 lines of Rust)
- Zero-cost async with Tokio runtime and Actix-web
- SQLx compile-time query validation with offline cache (`.sqlx/`)
- PostgreSQL stored procedures for atomic server-side business logic
- UNLOGGED tables for maximum write throughput (no WAL)
- Lazy static HashMap for client validation (no DB round-trip)
- PostgreSQL tuned: `synchronous_commit=0`, `fsync=0`, `full_page_writes=0`
- Multi-platform Docker image (amd64/arm64) published to GHCR
- Observability stack with Prometheus, Grafana, and InfluxDB
- All requests under 800ms at 250MB RAM usage (60% below limit)

## Getting Started

### Prerequisites

- Docker with Docker Compose

### Quick Start

```bash
git clone https://github.com/jonathanperis/rinha2-back-end-rust.git
cd rinha2-back-end-rust
docker compose up nginx -d --build
```

API available at `http://localhost:9999`

### API Endpoints

| Method | Path | Status Codes | Description |
|--------|------|-------------|-------------|
| POST | `/clientes/{id}/transacoes` | 200, 404, 422 | Submit debit or credit transaction |
| GET | `/clientes/{id}/extrato` | 200, 404 | Get account balance statement |
| GET | `/healthz` | 200 | Health check |

### Run Stress Tests

```bash
docker compose up k6 --build --force-recreate
```

## Project Structure

```
rinha2-back-end-rust/
├── src/WebApi/
│   ├── main.rs              # Complete API (~140 lines)
│   ├── Cargo.toml           # Dependencies
│   ├── Dockerfile           # Multi-stage: rust:1.94 → debian:bookworm-slim
│   └── .sqlx/               # SQLx offline query cache
├── docker-entrypoint-initdb.d/
│   └── rinha.dump.sql       # Schema + stored procedures + seed data
├── docker-compose.yml       # Dev stack with observability
├── prod/docker-compose.yml  # Prod stack with GHCR images
├── nginx.conf               # Load balancer config
└── .github/workflows/       # CI/CD (build-check, main-release, codeql)
```

## CI/CD

| Workflow | Trigger | Description |
|----------|---------|-------------|
| Build Check | Pull requests | Cargo build (release) + Docker health check |
| Main Release | Push to main | Build + Multi-platform Docker push (amd64/arm64) to GHCR + k6 load test + GitHub Pages report |
| CodeQL | Push/PR + weekly | Security and quality analysis for Rust |
| Deploy Docs | Push to main | Generate and deploy documentation to GitHub Pages |

**Docker image:** `ghcr.io/jonathanperis/rinha2-back-end-rust:latest`

## License

MIT — see [LICENSE](LICENSE)
