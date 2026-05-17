# rinha2-back-end-rust

Rust/Actix-web 4 implementation for the Rinha de Backend 2024/Q1 challenge. It manages a fictional bank API with transaction processing and balance statements under strict resource constraints (1.5 CPU, 550MB RAM total across the challenge containers).

## Wiki Pages

| Page | Description |
|------|-------------|
| [Challenge](#challenge) | What Rinha de Backend 2024/Q1 requires |
| [Architecture](#architecture) | Current stack, services, resource constraints, and runtime flow |
| [Getting Started](#getting-started) | Prerequisites, run commands, endpoint smoke tests |
| [Performance](#performance) | How to read benchmark/report artifacts without hard-coding stale numbers |
| [CI/CD Pipeline](#ci-cd-pipeline) | GitHub Actions workflows and release/deploy path |

## Key Features

- Single Rust API entrypoint (`src/WebApi/main.rs`, 173 total lines at this revision)
- Actix-web 4 with Tokio async runtime and SQLx 0.8
- Rust 2024 package; Docker builder currently uses `rust:1.95`
- PostgreSQL stored procedures for balance updates and statement aggregation
- Health endpoint at `/healthz` returns `Healthy`
- Source-backed drift guard: `python3 scripts/check_docs_drift.py`

---

*[GitHub](https://github.com/jonathanperis/rinha2-back-end-rust) · [Jonathan Peris](https://jonathanperis.github.io/)*
