# rinha2-back-end-rust

High-performance backend implementation for the **Rinha de Backend** challenge (2nd Edition, 2024/Q1) — built with **Rust**, **Actix-web**, **PostgreSQL**, and **Nginx**.

**Live results:** [jonathanperis.github.io/rinha2-back-end-rust](https://jonathanperis.github.io/rinha2-back-end-rust/)

---

## About

A Rust implementation of the Brazilian backend programming challenge that pushes API performance to the absolute limit under strict resource constraints. The API manages fictional bank clients with credit/debit transactions and balance statements.

### Endpoints

- `POST /clientes/{id}/transacoes` — Create a transaction (credit or debit)
- `GET /clientes/{id}/extrato` — Get client balance and recent transactions

### Results

All requests completed under 800ms using only **250MB of RAM** — 60% less than the challenge allows.

## Tech Stack

| Technology | Purpose |
|---|---|
| Rust 1.85 | API implementation |
| Actix-web 4 | HTTP framework |
| SQLx 0.7 | Async PostgreSQL driver |
| Tokio | Async runtime |
| PostgreSQL | Database with stored procedures |
| Nginx | Reverse proxy / load balancer |
| Docker | Multi-stage build and orchestration |
| Prometheus + Grafana | Observability |
| k6 | Stress testing |

## Architecture

- **2 Rust API instances** behind Nginx (0.4 CPU, 100MB RAM each)
- **1 PostgreSQL** database (0.5 CPU, 330MB RAM)
- **1 Nginx** load balancer (0.2 CPU, 20MB RAM)
- Business logic pushed into PostgreSQL stored procedures
- Minimal single-file Rust API (~140 lines)

## Getting Started

```bash
docker compose up nginx -d --build
```

The API will be available at `http://localhost:9999`.

## Stress Tests

- [rinha2-back-end-k6](https://github.com/jonathanperis/rinha2-back-end-k6) — Grafana k6 stress test suite used across all implementations

## Other Implementations

- [rinha2-back-end-dotnet](https://github.com/jonathanperis/rinha2-back-end-dotnet) — C# / .NET ![Perfect Score](https://img.shields.io/badge/⭐_Perfect_Score-gold?style=flat-square)
- [rinha2-back-end-go](https://github.com/jonathanperis/rinha2-back-end-go) — Go ![Learning Purposes](https://img.shields.io/badge/📚_Learning_Purposes-blue?style=flat-square)
- [rinha2-back-end-python](https://github.com/jonathanperis/rinha2-back-end-python) — Python ![Learning Purposes](https://img.shields.io/badge/📚_Learning_Purposes-blue?style=flat-square)

## License

Licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
