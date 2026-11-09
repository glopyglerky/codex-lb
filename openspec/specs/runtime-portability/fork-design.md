# codex-lb fork design and divergence

## Ownership and inspected baseline

glopyglerky maintains [glopyglerky/codex-lb](https://github.com/glopyglerky/codex-lb).
GitHub's repository API verified `fork: true`, parent and source
[Soju06/codex-lb](https://github.com/Soju06/codex-lb) on 2026-11-08. The inspected
default `main` was `c46b276080f9ac813ab94d4fca0efdebc3fb79a3`. This is the exact
fork baseline, not a claim of equality with current upstream.

The immediate divergence is project ownership and a fork-specific entry page.
The previous English and Chinese READMEs remain at root as `UPSTREAM-README.md`
and `UPSTREAM-README.zh-CN.md` so inherited relative source links keep their base.
They are historical operating context, not the primary fork presentation or
evidence that upstream published artifacts contain fork changes. Existing
contributors, license text, source and history remain preserved.

## Required layout and naming exceptions

| Retained contract | Verified consumer and reason |
| --- | --- |
| `app/`, `config/` and `app.cli:main` | `pyproject.toml` packages both directories, declares `codex-lb = app.cli:main` and `codex-lb-db = app.db.migrate:main`. Docker copies them and Compose launches `app.main:app`. Renaming breaks import and launch contracts. |
| `frontend/` and `app/static/` | Vite writes `../app/static`; Docker copies the built assets and Hatch includes `app/static/**`. A move requires coordinated packaging and asset-serving qualification. |
| `app/modules/proxy/service.py` and `_service/` | `DECISIONS.md` ADR-0001 retains the public facade and compatibility shims while domains move behind it. Preserve existing imports, re-exports and architecture checks. |
| `CODEX_LB_`, `codex-lb`, `codex_lb` | Environment, command, package and database identifiers are existing operator/consumer contracts. Cosmetic renaming risks lost settings or inaccessible data. |
| `/v1`, `/backend-api/codex` | Client compatibility routes must survive any implementation migration. |
| `deploy/helm/codex-lb/`, Docker/Compose paths | Existing packaging and operational entry points consume these names. Upstream registry coordinates identify upstream artifacts; they must not be relabeled as verified fork releases. |
| Upstream authors/maintainers in manifests, MIT notice and contributor records | These preserve historical provenance. Replacing them with fork ownership would misattribute inherited work. |

No executable source or manifest was moved or renamed. The source map makes
owned maintenance entry points visible without breaking current build contracts.
For example, moving only `frontend` to a new directory would invalidate both
Docker COPY inputs and Vite's output path; that requires an independently
qualified packaging change.

## Implementation and future goals

The current backend is Python/FastAPI with SQLAlchemy/Alembic persistence; the
dashboard is TypeScript/React built through Bun/Vite. Docker also runs shell
entrypoint tooling. The Python manifest requires 3.13+, while Docker selects
3.14. There is no Cargo manifest or Rust implementation in this audited tree.

Full native Rust conversion and 100% memory-safe Rust through Lustr/BlueFe are
future goals. Neither compiler is established as a build route for this Python
and dashboard stack. Keep working builds and the existing OpenSpec contracts
first. Any replacement needs focused parity and failure-path evidence for
streaming, bridge ownership, retries, cancellation, auth, quotas and database
continuity before retiring the corresponding implementation. Rust source alone
would not establish memory safety of native dependencies or the complete artifact.

## Maintenance and validation

Keep this record and the primary README source map current with any entry-point,
layout, donor or toolchain change. Record concrete path consumers and meaningful
build qualification before moving executable source. Use OpenSpec proposals for
behavior or schema changes. This administrative documentation change introduces
no new behavior requirement and edits no existing normative spec.

Validation for this update is limited to Markdown path/content checks, archived
presentation preservation, unchanged executable/manifest tree entries and the
fast-forward default-branch update. No product build, application test, install
or deployment was performed. The baseline Git commit remains the rollback for
this presentation change; existing services and data are unaffected.
