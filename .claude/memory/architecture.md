---
name: Rust Rinha Architecture
description: Single-file Actix-web API design, SQLx compile-time queries, lazy static client map, stored procedure delegation
type: project
---

## Design Decisions

**Single-file API (~140 lines in main.rs):**
- All routes, DTOs, validation, and DB calls in one file
- Intentionally minimal — the challenge rewards simplicity and performance, not abstractions

**Why:** Challenge constraints (1.5 CPU, 550MB RAM) favor the smallest possible footprint. Rust's type system provides safety without architectural overhead.

**How to apply:** Keep it single-file. Resist the urge to split into modules unless the file grows past ~300 lines.

## Key Technical Choices

- **Lazy static HashMap**: 5 client IDs → credit limits. Avoids DB round-trip for client validation.
- **SQLx compile-time queries**: Validated against schema at build time. Offline cache in `.sqlx/` enables builds without a running database.
- **SQLX_OFFLINE=1**: Set in Dockerfile so Docker builds don't need a database connection.
- **Actix-web handler macros**: `#[get(...)]` and `#[post(...)]` for declarative routing.

## Shared Infrastructure

This repo shares PostgreSQL schema, stored procedures, NGINX config, and resource constraints with the Go, .NET, and Python implementations. The k6 test suite (`ghcr.io/jonathanperis/rinha2-back-end-k6:latest`) is the same across all.

Changes to `docker-entrypoint-initdb.d/rinha.dump.sql` or `nginx.conf` should be mirrored across all 4 rinha repos.
