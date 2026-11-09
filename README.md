# codex-lb

glopyglerky's maintained fork of the ChatGPT account load balancer and proxy,
at [glopyglerky/codex-lb](https://github.com/glopyglerky/codex-lb), with default
branch `main`. The verified upstream parent is
[Soju06/codex-lb](https://github.com/Soju06/codex-lb).

This fork keeps the existing account pooling, Responses and Chat Completions
compatibility routes, usage accounting, API keys and dashboard. Its current
implementation is Python/FastAPI with a TypeScript/React dashboard. There is no
Rust replacement in the audited tree. The package manifest declares
`1.21.0-beta.3`, Python 3.13 or newer, and Alpha status; this is not a new
qualified release or an installation receipt.

## Start from this fork's source

```sh
git clone https://github.com/glopyglerky/codex-lb.git
cd codex-lb
uv sync --frozen --dev
cd frontend
bun install --frozen-lockfile
bun run build
cd ..
uv run codex-lb --help
uv run codex-lb --host 127.0.0.1 --port 2455
```

The dashboard is at `http://127.0.0.1:2455`. Add accounts there. Use the
`/v1` compatibility routes or `/backend-api/codex` according to your client.
These are source-derived entry points; this documentation change did not build
or launch the service. The frontend manifest pins Bun 1.3.14. The checked-in
Dockerfile separately selects Python 3.14.

Configuration uses `CODEX_LB_` environment variables; see
[`.env.example`](.env.example). Preserve the database and encryption keys when
changing an existing installation. SQLite is the default and PostgreSQL is an
optional backend. Dashboard authentication and proxy API-key authentication are
separate controls. Consult the [admin authentication context](openspec/specs/admin-auth/context.md)
and [database context](openspec/specs/database-backends/context.md) before
exposing a service or changing storage.

The [archived English guide](UPSTREAM-README.md) and
[archived Chinese guide](UPSTREAM-README.zh-CN.md) retain detailed inherited
client examples. Commands there using `ghcr.io/soju06`, upstream Helm charts or
`uvx codex-lb` select upstream distributions. They do not install this fork's
current source. This README makes no claim that a fork image has been published.

## Source map

| Path | Role |
| --- | --- |
| `app/cli.py` | `codex-lb` command and server launch |
| `app/main.py` | FastAPI application and lifecycle |
| `app/modules/` | Proxy, account, authentication and other application domains |
| `app/db/`, `config/` | Persistence, migrations and packaged configuration |
| `frontend/src/`, `frontend/package.json` | React dashboard and Bun/Vite tasks |
| `frontend/vite.config.ts`, `app/static/` | Dashboard output contract, generated assets bundled with the backend |
| `pyproject.toml`, `uv.lock` | Python dependencies, wheel contents and CLI entry points |
| `tests/`, `Makefile` | Focused checks and CI entry points |
| `openspec/`, `DECISIONS.md` | Behavior contracts, rationale and proxy decomposition decision |
| `Dockerfile`, `docker-compose.yml`, `deploy/helm/codex-lb/` | Retained container and chart build paths |

The [fork design and divergence record](openspec/specs/runtime-portability/fork-design.md)
records ownership, inherited names, path consumers and migration boundaries.
[Development conventions](AGENTS.md) and [contribution guidance](.github/CONTRIBUTING.md)
remain relevant. Behavior changes require the existing OpenSpec workflow.

## Verification and migration direction

For implementation work, choose focused tests in `tests/unit`, `tests/integration`
or `tests/e2e`. `make architecture-check` checks the proxy decomposition;
`make frontend-typecheck` and `make frontend-test-fast` check the dashboard.
See the Makefile for the broader CI gate. This documentation update ran bounded
content/path checks, not application tests or deployment acceptance.

Full native Rust conversion and 100% memory-safe Rust using Lustr/BlueFe are
future goals. Current Python, JavaScript/TypeScript, shell tooling and native
dependencies remain required. No claim is made that Lustr/BlueFe currently
builds those components, or that the complete service is memory-safe Rust.
A future replacement must preserve streaming, retries, cancellation, account
selection, authentication, accounting and data migration behavior before cutover.

## License and origin

The inherited [MIT license](LICENSE), contributor acknowledgements and history
remain intact. Ownership of this fork does not imply authorship of inherited code.


Report vulnerabilities through the [security policy](.github/SECURITY.md).
Inherited contributor history is recorded in [.all-contributorsrc](.all-contributorsrc)
and the [upstream contributor graph](https://github.com/Soju06/codex-lb/graphs/contributors).
