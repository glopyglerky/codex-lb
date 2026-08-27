# codex-lb

[English](README.md) | [简体中文](README.zh-CN.md)

A local proxy and load balancer for ChatGPT accounts.

codex-lb pools accounts behind OpenAI-compatible endpoints, keeps a Codex-native endpoint for Codex clients, tracks usage, and provides a browser dashboard for account, key, and routing controls.

[![Fork activity](https://img.shields.io/github/last-commit/glopyglerky/codex-lb?label=fork%20updated)](https://github.com/glopyglerky/codex-lb/commits/main)
[![Upstream release](https://img.shields.io/github/v/release/Soju06/codex-lb?label=upstream%20release)](https://github.com/Soju06/codex-lb/releases/latest)
[![License](https://img.shields.io/github/license/Soju06/codex-lb)](LICENSE)

> This repository is a personal fork of [Soju06/codex-lb](https://github.com/Soju06/codex-lb). It does not publish its own release or container image. The quick start below runs the upstream image. Review this fork's changes before deploying its source.

## What it does

- Balances requests across eligible ChatGPT accounts while preserving sticky conversation routing.
- Exposes `/v1` for OpenAI-compatible clients and `/backend-api/codex` for Codex-native traffic.
- Tracks account usage, request history, costs, quota resets, and routing decisions.
- Issues scoped API keys with model and rate limits.
- Supports SQLite by default and PostgreSQL for shared deployments.
- Provides dashboard password, TOTP, trusted-header, and explicitly disabled authentication modes.
- Runs locally, in Docker, or through the included Helm chart.

No routing strategy can guarantee account safety. Use normal request volumes, follow the applicable terms, and keep sticky routing enabled unless you have a specific reason to change it.

## How it works

```text
client -> authentication -> model and account eligibility -> sticky routing
       -> upstream Codex session -> streamed response -> usage settlement
```

The routing contract, retry rules, and session ownership live in [OpenSpec](openspec/specs/account-routing/spec.md). The dashboard exposes the supported strategies. Capacity weighted and relative availability are the sensible defaults for most pools.

## Current status

The fork's default branch is active development code and currently identifies itself as an alpha package. It has no fork-specific release. Use the live badges above for fork activity and the latest upstream release, and use `GET /v1/models` for the current model catalog. Copied model lists age badly.

The normative behavior lives under [`openspec/specs/`](openspec/specs/). Configuration defaults come from [`.env.example`](.env.example). Those files are better authorities than a dated feature matrix in this README.

## Quick start

```bash
docker volume create codex-lb-data
docker run -d --name codex-lb \
  -p 2455:2455 -p 1455:1455 \
  -v codex-lb-data:/var/lib/codex-lb \
  ghcr.io/soju06/codex-lb:latest
```

Open [localhost:2455](http://localhost:2455), add an account, then check the live model catalog:

```bash
curl http://127.0.0.1:2455/v1/models
```

You can also run the upstream Python package with `uvx codex-lb`.

### First remote login

Local dashboard access bypasses first-run bootstrap. Remote access requires a one-time token when no password exists. The server prints the generated token at startup:

```bash
docker logs codex-lb
```

Set `CODEX_LB_DASHBOARD_BOOTSTRAP_TOKEN` before startup if you need a fixed token. Replicas must share the same encryption key so first-run and session state survive restarts.

## Connect Codex

Pick a model from `/v1/models`, then add a provider to `~/.codex/config.toml`:

```toml
model = "MODEL_ID"
model_provider = "codex-lb"

[model_providers.codex-lb]
name = "openai"
base_url = "http://127.0.0.1:2455/backend-api/codex"
wire_api = "responses"
supports_websockets = true
requires_openai_auth = true
```

If API key authentication is enabled, add `env_key = "CODEX_LB_API_KEY"` to the provider and export the key before starting Codex:

```bash
export CODEX_LB_API_KEY="sk-clb-..."
codex
```

The same proxy also supports OpenCode, OpenClaw, and the OpenAI SDK. Point Responses API clients at `/v1`. Client behavior and edge cases are documented in the [Responses API context](openspec/specs/responses-api-compat/context.md), [chat completions context](openspec/specs/chat-completions-compat/context.md), and [runtime portability context](openspec/specs/runtime-portability/context.md).

## Authentication

Proxy API key authentication is disabled by default. Without it, protected proxy routes accept only local requests. Enable API key authentication in the dashboard before allowing remote clients, then send:

```text
Authorization: Bearer sk-clb-...
```

Dashboard authentication has three explicit modes:

- `standard` uses a password and optional TOTP.
- `trusted_header` accepts an identity header only from configured proxy CIDRs.
- `disabled` removes application-level dashboard authentication and should sit behind a separate access boundary.

See the [admin authentication context](openspec/specs/admin-auth/context.md) and [API key contract](openspec/specs/api-keys/spec.md) before exposing the service beyond localhost.

## Configuration and data

Environment variables use the `CODEX_LB_` prefix. [`.env.example`](.env.example) is the complete configuration reference.

| Runtime | Data path |
| --- | --- |
| Local or `uvx` | `~/.codex-lb/` |
| Docker | `/var/lib/codex-lb/` |

Back up that directory before upgrades. SQLite is the default. PostgreSQL setup and migration rules are in the [database context](openspec/specs/database-backends/context.md).

## Kubernetes

```bash
helm install codex-lb oci://ghcr.io/soju06/charts/codex-lb \
  --set postgresql.auth.password=changeme \
  --set config.databaseMigrateOnStartup=true \
  --set migration.schemaGate.enabled=false
kubectl port-forward svc/codex-lb 2455:2455
```

The [Helm chart README](deploy/helm/codex-lb/README.md) covers external databases, ingress, authentication, observability, and multi-replica routing.

## Development

This project requires Python 3.13 and uses `uv` for the locked environment.

```bash
uv sync --frozen
cd frontend && bun install && cd ..

uv run fastapi run app/main.py --reload
cd frontend && bun run dev
```

Run the focused checks before opening a change:

```bash
uv run --frozen ruff check app tests
uv run --frozen ruff format --check app tests
uv run --frozen ty check app
uv run --frozen pytest tests/unit -q
```

Behavior changes start in [`openspec/`](openspec/). Read [the contribution rules](.github/CONTRIBUTING.md) for the repository's merge gates.

## Repository map

| Path | Contents |
| --- | --- |
| [`app/`](app/) | FastAPI service, routing, persistence, authentication, and proxy runtime |
| [`frontend/`](frontend/) | Dashboard application |
| [`openspec/`](openspec/) | Normative behavior and operating context |
| [`deploy/helm/codex-lb/`](deploy/helm/codex-lb/) | Kubernetes chart and deployment guide |
| [`tests/`](tests/) | Unit, integration, compatibility, and release checks |

## Contributing and security

This fork retains the upstream project's history and contributors. See the [contributor graph](https://github.com/Soju06/codex-lb/graphs/contributors) and [upstream contribution guide](https://github.com/Soju06/codex-lb/blob/main/.github/CONTRIBUTING.md).

Report vulnerabilities through the [security policy](.github/SECURITY.md). Do not post secrets, account exports, access tokens, or production logs in public issues.

## License

codex-lb is licensed under the [MIT License](LICENSE). Copyright and attribution remain with the upstream authors and contributors.
