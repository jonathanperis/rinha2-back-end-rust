# rinha2-back-end-rust

Rust/Actix-web 4 implementation for the Rinha de Backend 2024/Q1 challenge. Manages a fictional bank API with transaction processing and balance statements under strict resource constraints (1.5 CPU, 550MB RAM total across all containers).

## Wiki Pages

| Page | Description |
|------|-------------|
| [Challenge](Challenge) | What is Rinha de Backend 2024/Q1 |
| [Architecture](Architecture) | Stack, services, resource constraints |
| [Getting StartedL(Getting-Started.md) | Prerequisites and how to run |
| [Performance](Performance) | Results, benchmarks, resource usage |
| [CI/CD PipelineL(CI-CD-Pipeline.md) | GitHub Actions workflows |

## Key Features

- Minimal single-file API implementation (~140 lines of Rust)
- Actix-web 4 with Tokio async runtime and SQLx 0.8
- PostgreSQL stored procedures for server-side business logic
- All requests under 800ms at 250MB RAM usage

---

*[GitHubL(https://github.com/jonathanperis/rinha2-back-end-rust.md) · [Jonathan Peris](https://jonathanperis.github.io/)*
