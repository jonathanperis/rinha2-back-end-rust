# Getting Started

## Prerequisites

- Docker with Docker Compose

## Clone and Run

```bash
git clone https://github.com/jonathanperis/rinha2-back-end-rust.git
cd rinha2-back-end-rust
docker compose up nginx -d --build
```

## Access

The challenge-facing API is available at `http://localhost:9999` through NGINX.

The dev compose file also maps the two API containers directly:

- `http://localhost:6968` → `webapi1-rust:8080`
- `http://localhost:6969` → `webapi2-rust:8080`

Use port `9999` for normal validation and load-test requests.

## Endpoints

| Endpoint | Method | Status Codes | Description |
|----------|--------|--------------|-------------|
| `/clientes/{id}/transacoes` | POST | 200, 404, 422 | Submit a debit or credit transaction for client IDs 1-5 |
| `/clientes/{id}/extrato` | GET | 200, 404 | Get current balance, credit limit, timestamp, and up to 10 recent transactions |
| `/healthz` | GET | 200 | Health check returning `Healthy` |

Transaction payloads must have `tipo` equal to `c` or `d`, a non-empty `descricao` of at most 10 characters, and a positive integer `valor`. The DTO also accepts PascalCase aliases (`Valor`, `Tipo`, `Descricao`) in addition to the lowercase challenge field names (`valor`, `tipo`, `descricao`).

### Current Response Contract

`POST /clientes/{id}/transacoes` returns:

```json
{
  "id": 1,
  "limite": 100000,
  "saldo": 1000
}
```

`GET /clientes/{id}/extrato` returns a `saldo` object with `total`, `limite`, and `data_extrato`, plus `ultimas_transacoes` entries serialized as `valor`, `tipo`, and `descricao`.

The current stored procedure handles a debit that would exceed the client limit by leaving the balance unchanged and skipping the transaction insert, then returning the current balance to the API. That path currently responds with `200`; `422` is reserved for invalid payloads or database errors.

Seeded client limits:

| ID | Limit |
|----|-------|
| 1 | 100000 |
| 2 | 80000 |
| 3 | 1000000 |
| 4 | 10000000 |
| 5 | 500000 |

## Example Requests

### Health Check

```bash
curl http://localhost:9999/healthz
```

### Create Transaction

```bash
curl -X POST http://localhost:9999/clientes/1/transacoes   -H "Content-Type: application/json"   -d '{"valor": 1000, "tipo": "c", "descricao": "deposito"}'
```

### Get Statement

```bash
curl http://localhost:9999/clientes/1/extrato
```

## Stress Tests

```bash
cp .env.example .env
docker compose up k6 --build --force-recreate
```

In `docker-compose.yml`, k6 runs in `MODE=dev` and exports time-series data to InfluxDB/Grafana. Copy `.env.example` first so `INFLUXDB_PASSWORD` and `INFLUXDB_TOKEN` are defined for InfluxDB, Grafana, and xk6 output. The release workflow uses `prod/docker-compose.yml`, where k6 runs in `MODE=prod` and writes an HTML stress-test report artifact.
