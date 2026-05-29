# Performance

## Resource Constraints

The challenge allows a total of 1.5 CPU and 550MB RAM across the core API, database, and load-balancer containers.

| Service | CPU | RAM |
|---------|-----|-----|
| `webapi1-rust` | 0.4 | 100MB |
| `webapi2-rust` | 0.4 | 100MB |
| `db` | 0.5 | 330MB |
| `nginx` | 0.2 | 20MB |
| **Total** | **1.5** | **550MB** |

Observability (`prometheus`, `grafana`, `influxdb`, `postgres-exporter`) and k6 are part of the development/test harness and are not part of the challenge resource total.

## Source of Truth for Results

Avoid treating fixed numbers in Markdown as the performance source of truth. This repository stores generated stress-test report artifacts under `docs/public/reports/`, and the `main-release.yml` workflow uploads the newest k6 HTML report from `prod/conf/stress-test/reports/stress-test-report.html`.

Use those generated reports and workflow artifacts for exact latency, throughput, and error-rate figures. This wiki page documents where the results come from and what runtime shape produced them.

## Performance-Relevant Runtime Choices

- Two API instances behind NGINX `least_conn`.
- SQLx pool size is 5 connections per API instance.
- Client existence and limits are validated from a lazy static Rust `HashMap` for the five seeded clients.
- Balance mutation and statement aggregation are handled in PostgreSQL stored procedures.
- `Clientes` and `Transacoes` are UNLOGGED tables for challenge throughput.
- Debits that would exceed a client's limit do not insert a transaction row; the stored procedure returns the unchanged balance.
- PostgreSQL durability flags are disabled for benchmarking: `synchronous_commit=0`, `fsync=0`, and `full_page_writes=0`.

## Stress Testing

Load tests are run using the shared [rinha2-back-end-k6](https://github.com/jonathanperis/rinha2-back-end-k6) suite, which simulates concurrent users performing debits, credits, validations, and statement queries.

Development mode:

```bash
docker compose up k6 --build --force-recreate
```

Release mode is executed by GitHub Actions with `prod/docker-compose.yml`, `MODE=prod`, and HTML report artifact upload.
