# Architecture

## Overview

The system follows the Rinha de Backend topology used by this repository: two Rust/Actix-web API containers behind NGINX, one PostgreSQL database, and optional observability/load-test services in the development compose file.

## Services

| Service | Role | CPU | RAM |
|---------|------|-----|-----|
| `webapi1-rust` | Actix-web 4 API instance using SQLx 0.8 + Tokio | 0.4 | 100MB |
| `webapi2-rust` | Actix-web 4 API instance using SQLx 0.8 + Tokio | 0.4 | 100MB |
| `nginx` | Reverse proxy / load balancer on port 9999 (`least_conn`) | 0.2 | 20MB |
| `db` | PostgreSQL 16.7 Alpine with stored procedures | 0.5 | 330MB |
| `k6` | Shared load-test runner (`MODE=dev` in dev compose, `MODE=prod` in prod compose) | not counted | not counted |
| `prometheus`, `grafana`, `influxdb`, `postgres-exporter` | Development observability stack | not counted | not counted |

The compose CPU/RAM limits for the challenge services total 1.5 CPU and 550MB.

## Load Balancing

NGINX listens on `:9999` and proxies all routes to an upstream named `api` with `least_conn` across `webapi1-rust:8080` and `webapi2-rust:8080`. The dev compose file also maps the two API containers to host ports `6968` and `6969`, but challenge-compatible traffic should go through NGINX.

## API Runtime

The API is a single Rust entrypoint (`src/WebApi/main.rs`, 173 total lines at this revision):

- `GET /clientes/{id}/extrato` validates the client ID against a lazy static `HashMap`, then calls `GetSaldoClienteById($1)`.
- `POST /clientes/{id}/transacoes` validates the client ID and payload (`tipo`, `descricao`, `valor`), then calls `InsertTransacao($1, $2, $3, $4)`.
- `GET /healthz` returns `Healthy` for compose and CI smoke checks.
- The SQLx pool is created from `DATABASE_URL` with `max_connections(5)` per API instance.

## Database

Business logic is implemented in PostgreSQL stored procedures over UNLOGGED tables:

- `Clientes` stores the five seeded clients and their current balance (`SaldoInicial`).
- `Transacoes` stores accepted transactions and has an index on `(ClienteId, Id DESC)` for recent-statement reads.
- `InsertTransacao` applies credit/debit balance updates and inserts the transaction only when the update succeeds.
- `GetSaldoClienteById` returns the current balance, limit, timestamp, and up to 10 latest transactions as JSONB.

The database command is tuned for benchmark throughput, not durability:

- `synchronous_commit=0` — no wait for WAL flush
- `fsync=0` — skip fsync on writes
- `full_page_writes=0` — skip full page writes

## Container Images

The API Dockerfile builds with `rust:1.95` and runs on `debian:bookworm-slim` as a non-root `app` user. The release workflow publishes `ghcr.io/jonathanperis/rinha2-back-end-rust:latest` as the multi-arch image used by `prod/docker-compose.yml`.
