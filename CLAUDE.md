# Rinha de Backend 2024/Q1 — Rust Implementation

High-performance banking API built with Rust/Actix-web for the Rinha de Backend challenge. Handles concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM).

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Rust 1.94 | Language |
| Actix-web 4 | Async HTTP framework |
| SQLx 0.8 | Compile-time checked PostgreSQL queries |
| PostgreSQL 16.7 | Database with stored procedures |
| NGINX 1.27 | Load balancer (least_conn) |
| Docker | Multi-stage builds |
| k6 | Load testing (shared suite) |

---

## Build Commands

```sh
cargo build --manifest-path ./src/WebApi/Cargo.toml           # Debug build
cargo build --release --manifest-path ./src/WebApi/Cargo.toml  # Release build
docker compose up nginx -d --build                              # Full dev stack
docker compose up k6 --build --force-recreate                  # Run stress tests
```

---

## Architecture

```
NGINX (:9999, least_conn)
├── webapi1-rust (:8080, 0.4 CPU, 100MB)
├── webapi2-rust (:8080, 0.4 CPU, 100MB)
└── PostgreSQL (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance update + validation
    └── GetSaldoClienteById() — statement with JSONB aggregation
```

**Single-file API** (~140 lines in `src/WebApi/main.rs`). All business logic in PostgreSQL stored procedures.

---

## API Endpoints

| Method | Path | Status Codes |
|--------|------|-------------|
| POST | `/clientes/{id}/transacoes` | 200, 404, 422 |
| GET | `/clientes/{id}/extrato` | 200, 404 |
| GET | `/healthz` | 200 |

---

## Key Patterns

- **Lazy static HashMap** for 5 predefined clients (no DB lookup for validation)
- **SQLx compile-time query validation** with offline cache (`.sqlx/`)
- **UNLOGGED tables** for write performance (no WAL)
- **Stored procedures** handle all transaction logic atomically
- PostgreSQL tuned for throughput: `fsync=0, synchronous_commit=0`

---

## Observability (Dev Stack)

| Service | Port | Purpose |
|---------|------|---------|
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Dashboards (PostgreSQL, k6, performance) |
| InfluxDB | 8086 | k6 time-series metrics |
| postgres-exporter | 9187 | PostgreSQL metrics for Prometheus |

---

## Project Structure

```
rinha2-back-end-rust/
├── src/WebApi/
│   ├── main.rs         # Complete API (~140 lines)
│   ├── Cargo.toml      # Dependencies
│   ├── Dockerfile       # Multi-stage: rust:1.94 → debian:bookworm-slim
│   └── .sqlx/           # SQLx offline query cache
├── docker-entrypoint-initdb.d/
│   └── rinha.dump.sql   # Schema + stored procedures + seed data
├── docker-compose.yml   # Dev stack with observability
├── prod/docker-compose.yml  # Prod stack with GHCR images
├── nginx.conf           # Load balancer config
└── .github/workflows/   # CI/CD (build-check, main-release, codeql)
```

---

## CI/CD

- **PR:** Cargo build (release) + Docker health check
- **Main:** Build + Multi-platform Docker push (amd64/arm64) to GHCR + k6 load test + GitHub Pages report
- **CodeQL:** Security and quality analysis (push/PR + weekly schedule)
- **Deploy Docs:** Generate and deploy documentation to GitHub Pages
- **Image:** `ghcr.io/jonathanperis/rinha2-back-end-rust:latest`

---

## Resource Constraints

| Service | CPU | RAM |
|---------|-----|-----|
| webapi1/2 | 0.4 each | 100MB each |
| PostgreSQL | 0.5 | 330MB |
| NGINX | 0.2 | 20MB |
| **Total** | **1.5** | **550MB** |

---

## Development Workflow

- All changes must go through a **branch + pull request** workflow — never push directly to main
- Always **sync main before creating a branch** (`git checkout main && git fetch origin main && git pull origin main`) and **fetch main again before opening a PR** to avoid conflicts
- PRs use **rebase merge only** (squash and merge commits are disabled)
- Use `gh` CLI for all GitHub operations (PRs, issues, releases, checks)
- Repo-wide community files (CODE_OF_CONDUCT, CONTRIBUTING, FUNDING, etc.) live in the **jonathanperis/.github** repo — do not duplicate them here

## Shared Infrastructure

This repo shares PostgreSQL schema, stored procedures, NGINX config, and resource constraints with sibling implementations (Go, .NET, Python). The k6 test suite is the same across all (`ghcr.io/jonathanperis/rinha2-back-end-k6:latest`).

Changes to `docker-entrypoint-initdb.d/rinha.dump.sql` or `nginx.conf` should be mirrored across all rinha repos.
