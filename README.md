# rinha2-back-end-rust

> Rust/Actix-web 4 implementation for the Rinha de Backend 2024/Q1 challenge with SQLx async driver and PostgreSQL stored procedures

[![CI](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check-webapi.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-rust/actions/workflows/build-check-webapi.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## About

A Rust implementation of the Brazilian backend challenge Rinha de Backend 2024/Q1, where a fictional bank API must handle concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total). Built as a minimal single-file API (~140 lines) using Actix-web 4 with Tokio async runtime and SQLx 0.7 for compile-time checked PostgreSQL queries. Built for learning purposes.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Rust | 1.85 | API implementation |
| Actix-web | 4 | HTTP framework |
| SQLx | 0.7 | Async PostgreSQL driver |
| Tokio | - | Async runtime |
| PostgreSQL | - | Database with stored procedures |
| Nginx | 1.27 | Reverse proxy and load balancer (least-conn) |
| Docker | - | Multi-stage build and orchestration |
| k6 | - | Stress testing |

## Features

- Minimal single-file API implementation (~140 lines of Rust)
- Zero-cost async with Tokio runtime and Actix-web
- SQLx 0.7 async PostgreSQL driver
- PostgreSQL stored procedures for server-side business logic
- PostgreSQL tuned with synchronous_commit=0, fsync=0, full_page_writes=0
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

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/clientes/{id}/transacoes` | POST | Submit debit or credit transaction |
| `/clientes/{id}/extrato` | GET | Get account balance statement |

## Project Structure

```
rinha2-back-end-rust/
├── src/WebApi/         — API implementation
├── docker-compose.yml  — Full stack: API x2, Nginx, PostgreSQL, k6, observability
└── .github/workflows/  — CI/CD pipelines
```

## CI/CD

Two GitHub Actions workflows: `build-check-webapi.yml` runs on pull requests to build and health-check the API, and `main-release-webapi.yml` runs on the main branch to build a multi-platform Docker image and push it to GHCR.

## License

MIT — see [LICENSE](LICENSE)
