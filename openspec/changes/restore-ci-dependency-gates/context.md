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
tests that expect to control their own proxy settings. That initial dependency-only
qualification left application and test sources unchanged.

OpenSpec 1.17.0 validated this change with `--strict`. The repository's documented
`openspec validate --specs` command passed all 31 existing specs. Applying
`--strict` to those existing specs reports pre-existing placeholder-purpose and
long-requirement warnings in 25 specs. Telemetry and update checks were disabled
with the tool's supported environment settings for validation.

## aiohttp WebSocket compatibility

At commit `e7b492ac0184bbc85943e46f37ca570597804db5`, native
[CI run 43092176479](https://github.com/glopyglerky/codex-lb/actions/runs/43092176479)
passed the rebuilt-image vulnerability scan and the runtime suites, but its type
check found that the custom handshake omitted two required parser arguments in
aiohttp 3.14.4. Existing handshake unit tests substitute a permissive parser stub,
so they cannot detect this constructor failure.

The [upstream client implementation](https://github.com/aio-libs/aiohttp/blob/v3.14.4/aiohttp/client.py)
passes explicit compression and text-decoding choices, then retains the parser on
the WebSocket response. The [upstream reader](https://github.com/aio-libs/aiohttp/blob/v3.14.4/aiohttp/_websocket/reader_py.py)
can retain unparsed input when its queue fills and uses a weak reference from the
queue to resume parsing. Response ownership keeps that input alive after the
protocol drops its parser reference.

This handshake does not implement extension negotiation and already sets its
writer and response to `compress=0`; the reader therefore uses `compress=False`.
Both upstream header builders can preserve an incoming
`Sec-WebSocket-Extensions` offer. The owned handshake removes that header from
its copied headers, regardless of casing, so the server cannot negotiate an
extension that the uncompressed reader does not support. Other headers remain
intact. Text decoding stays enabled because the event stream expects strings for
text frames and decodes binary frames separately. A local server regression
sends Unicode text, binary data and a burst of small frames through the real
aiohttp parser. It adds no remote upstream dependency and leaves the existing
handshake-error body and circuit-breaker behavior intact.

The new local-server test reproduced the constructor `TypeError` before the
repair and passed afterward with 2,050 text/binary messages. Review then exposed
the forwarded extension offer: both standard and lowercase header names caused
the real server to send compressed frames that the client rejected. After
removing the offer, all three local-server cases pass and confirm that an
unrelated trace header reaches the server. Six existing handshake and
event-decoding tests also pass, for nine focused tests in total. The exact
`make typecheck`, `make lint` and strict change validation passed again with the
selected dependencies. Fresh native CI and current-head review remain required
for this follow-up.
