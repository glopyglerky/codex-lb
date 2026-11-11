# CI maintenance context

## Scope and decisions

This change repairs the existing CI gates without changing their acceptance criteria.
`Makefile` currently invokes floating `uvx ruff` while `uv.lock` selects
`0.15.20`; both lint commands will name that selected release explicitly.
For example, a future Ruff release on the index must not change a checkout's
formatting result without a reviewed version update.

The runtime uses frozen dependency installation. Selected direct dependency
minimums are refreshed with the lock, and the existing explicit Debian package
upgrade list includes zlib. Dependency compatibility still requires the native
test suite and a rebuilt-image scan; a successful resolver is not runtime evidence.

## Contributor provenance

The [official upstream contributor record](https://github.com/Soju06/codex-lb/blob/72630bbfeee9e3b0d9acfb95e2b1e706b8b0188e/.all-contributorsrc) supplies the existing entries for
`glopyglerky` (GitHub ID `189872235`) and `felixcake618` (ID `91266981`).
The latter ID matches this repository's historical `Lotfree618` entry.
The current GitHub author on [commit
`464e918c08685532a324a93232b1774b9676bde3`](https://github.com/glopyglerky/codex-lb/commit/464e918c08685532a324a93232b1774b9676bde3) is
`TheFoolThatDoesntBelongToThisEra` (ID `252236154`), matching the historical
`luawl` entry. Current aliases retain the recorded contribution categories;
no new personal profile, biography or contribution claim is inferred.

Historical entries remain because the checker also derives logins from older
commit metadata. Replacing them would merely exchange one coverage failure for
another.

## Verification boundary

Local checks establish resolver consistency, source formatting and focused
dependency compatibility. The image scan, required native CI and current-head
Codex review must succeed before this change is accepted or archived.

Local verification on Python 3.13.5 passed `make lint`, the contributor coverage
check, the frozen lock check and 116 focused HTTP, websocket, authentication,
decompression and file-proxy tests. Those tests ran in a subprocess without
inherited proxy configuration; the first run exposed that configuration in five
tests that expect to control their own proxy settings. Application and test
sources were unchanged.

OpenSpec 1.17.0 validated this change with `--strict`. The repository's documented
`openspec validate --specs` command passed all 31 existing specs. Applying
`--strict` to those existing specs reports pre-existing placeholder-purpose and
long-requirement warnings in 25 specs. Telemetry and update checks were disabled
with the tool's supported environment settings for validation.
