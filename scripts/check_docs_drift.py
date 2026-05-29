#!/usr/bin/env python3
"""Source-backed drift guard for README.md and docs/wiki/*.md.

The project deliberately documents implementation facts (line counts, Docker
builder versions, workflow triggers, endpoint coverage). This script verifies
those claims against the actual source so README/wiki updates do not go stale
silently.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
WIKI_DIR = ROOT / "docs" / "wiki"
SIDEBAR = ROOT / "docs" / "src" / "lib" / "docs-sidebar.config.ts"

DOC_PATHS = [README, *sorted(WIKI_DIR.glob("*.md"))]
DOC_TEXT = "\n".join(path.read_text(encoding="utf-8") for path in DOC_PATHS)


def fail(message: str) -> None:
    print(f"docs drift: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def workflow_text(name: str) -> str:
    return read(f".github/workflows/{name}")


main_rs = read("src/WebApi/main.rs")
cargo_toml = read("src/WebApi/Cargo.toml")
dockerfile = read("src/WebApi/Dockerfile")
dev_compose = read("docker-compose.yml")
prod_compose = read("prod/docker-compose.yml")
nginx_conf = read("nginx.conf")
schema_sql = read("docker-entrypoint-initdb.d/rinha.dump.sql")
sidebar = SIDEBAR.read_text(encoding="utf-8")

# High-value source facts that docs intentionally mirror.
main_rs_lines = len(main_rs.splitlines())
require(f"{main_rs_lines} total lines" in DOC_TEXT, "main.rs line count is not reflected in docs")
require("~140" not in DOC_TEXT and "140 lines" not in DOC_TEXT, "old ~140-line API claim is still present")

rust_builder_match = re.search(r"^FROM\s+rust:([^\s]+)\s+AS\s+builder", dockerfile, re.MULTILINE)
require(rust_builder_match is not None, "Dockerfile builder image was not found")
rust_builder = rust_builder_match.group(1)
require(f"rust:{rust_builder}" in DOC_TEXT, "Docker builder version is not reflected in docs")
require("Rust | 1.94" not in DOC_TEXT and "rust:1.94" not in DOC_TEXT, "old Rust 1.94 claim is still present")

edition_match = re.search(r'^edition\s*=\s*"([^"]+)"', cargo_toml, re.MULTILINE)
require(edition_match is not None, "Cargo edition was not found")
require(f"edition {edition_match.group(1)}" in DOC_TEXT or f"Rust {edition_match.group(1)}" in DOC_TEXT, "Cargo edition is not reflected in docs")

# Endpoint coverage and runtime behavior.
for route in ["/clientes/{id}/transacoes", "/clientes/{id}/extrato", "/healthz"]:
    require(route in DOC_TEXT, f"endpoint {route} is missing from docs")
require('.route("/healthz"' in main_rs and 'body("Healthy")' in main_rs, "health endpoint implementation changed; update docs/checker")
require("Healthy" in DOC_TEXT, "health endpoint body is not documented")
require("max_connections(5)" in main_rs, "SQLx pool size changed; update docs/checker")
require("max_connections(5)" in DOC_TEXT or "pool size is 5" in DOC_TEXT, "SQLx pool size is not documented")

# Payload validation facts mirrored from is_transacao_valid and DTO aliases.
for snippet in ['tipo == "c" || tipo == "d"', 'descricao.len() <= 10', 'valor > 0']:
    require(snippet in main_rs, f"transaction validation changed around {snippet}; update docs/checker")
for phrase in ["tipo", "descricao", "10", "valor"]:
    require(phrase in DOC_TEXT, f"transaction validation docs missing {phrase}")
for alias in ['#[serde(alias = "Valor")]', '#[serde(alias = "Tipo")]', '#[serde(alias = "Descricao")]']:
    require(alias in main_rs, f"transaction DTO alias changed around {alias}; update docs/checker")
require("PascalCase aliases" in DOC_TEXT and "Valor" in DOC_TEXT and "Descricao" in DOC_TEXT, "transaction DTO aliases are not documented")

# Seeded clients and current business-limit behavior.
for client_id, limit in [(1, 100000), (2, 80000), (3, 1000000), (4, 10000000), (5, 500000)]:
    require(f"m.insert({client_id}, {limit})" in main_rs, f"Rust CLIENTS map changed for client {client_id}; update docs/checker")
    require(f"{client_id}\t{limit}\t0" in schema_sql, f"seed SQL changed for client {client_id}; update docs/checker")
    require(str(limit) in DOC_TEXT, f"client limit {limit} is not documented")
require("IF FOUND THEN" in schema_sql and "SELECT \"SaldoInicial\" INTO novo_saldo" in schema_sql, "over-limit stored procedure behavior changed; update docs/checker")
require("unchanged balance" in DOC_TEXT and "200" in DOC_TEXT, "current over-limit response behavior is not documented")

# Compose/runtime source-backed facts.
for resource in ['cpus: "0.4"', 'memory: "100MB"', 'cpus: "0.5"', 'memory: "330MB"', 'cpus: "0.2"', 'memory: "20MB"']:
    require(resource in dev_compose, f"dev compose resource fact changed: {resource}")
for phrase in ["1.5 CPU", "550MB", "100MB", "330MB", "20MB"]:
    require(phrase in DOC_TEXT, f"resource docs missing {phrase}")
require("least_conn" in nginx_conf and "least_conn" in DOC_TEXT, "NGINX least_conn fact drifted")
require("postgres:16.7-alpine" in dev_compose and "PostgreSQL | 16.7" in DOC_TEXT, "PostgreSQL version fact drifted")
for flag in ["synchronous_commit=0", "fsync=0", "full_page_writes=0"]:
    require(flag in dev_compose and flag in prod_compose and flag in DOC_TEXT, f"PostgreSQL tuning flag {flag} drifted")
require("CREATE UNLOGGED TABLE" in schema_sql and "UNLOGGED" in DOC_TEXT, "UNLOGGED table fact drifted")
require("IX_Transacoes_ClienteId_Id_Desc" in schema_sql and "ClienteId, Id DESC" in DOC_TEXT, "transaction index fact drifted")
for env_name in ["INFLUXDB_PASSWORD", "INFLUXDB_TOKEN"]:
    require(env_name in dev_compose, f"dev compose env var changed/missing: {env_name}")
    require(env_name in read(".env.example"), f".env.example missing {env_name}")
    require(env_name in DOC_TEXT, f"local observability env var {env_name} is not documented")

# Workflow facts.
build_check = workflow_text("build-check.yml")
main_release = workflow_text("main-release.yml")
codeql = workflow_text("codeql.yml")
deploy = workflow_text("deploy.yml")
require("pull_request:" in build_check and "workflow_dispatch:" in build_check, "Build Check triggers changed")
require("python3 scripts/check_docs_drift.py" in build_check, "Build Check is not wired to docs drift guard")
require("branches:" in main_release and "- main" in main_release and "workflow_dispatch:" in main_release, "Main Release triggers changed")
require("latest-arm64" in main_release and "buildx imagetools create" in main_release, "Main Release image publishing facts changed")
require("latest-arm64" in DOC_TEXT and "multi-arch" in DOC_TEXT, "image publishing facts are not documented")
require("schedule:" in codeql and "security-and-quality" in codeql, "CodeQL schedule/query facts changed")
require("0 3 * * 1" in DOC_TEXT and "security-and-quality" in DOC_TEXT, "CodeQL trigger/query facts are not documented")
require("pages-docs-deploy.yml@main" in deploy and "package-manager: bun" in deploy, "Deploy workflow reusable/Bun facts changed")
require("package-manager: bun" in DOC_TEXT, "Deploy workflow Bun fact is not documented")

# Wiki coverage through rendered docs sidebar.
ids = re.findall(r'"([a-z0-9-]+)"', sidebar)
for slug in ids:
    require((WIKI_DIR / f"{slug}.md").exists(), f"sidebar references missing wiki page {slug}.md")
for page in WIKI_DIR.glob("*.md"):
    require(page.stem in ids, f"wiki page {page.name} is not included in SECTION_ORDER")

# Known stale performance hard-coding. Generated HTML reports are the source of truth.
for stale in ["All requests under 800ms", "under 800ms", "250MB", "60% below"]:
    require(stale not in DOC_TEXT, f"known stale hard-coded performance phrase remains: {stale!r}")

print("docs drift check passed")
