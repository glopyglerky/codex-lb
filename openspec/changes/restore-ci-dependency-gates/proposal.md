## Why

The current native CI run reaches the existing checks but reports dependency-image, contributor-attribution and formatter failures. The formatter command resolves a floating tool instead of the version selected by the project lock.

## What Changes

- Invoke the Ruff version already selected in `uv.lock`.
- Refresh the affected runtime dependency selections and minimum supported versions, and include zlib in the runtime image's explicit OS upgrade list.
- Add verified current contributor logins while preserving historical login entries and contribution records.
- Keep the existing CI tests, vulnerability severity threshold and attribution check enabled.
- Adapt the custom upstream WebSocket handshake to the selected aiohttp parser API while preserving text decoding, uncompressed frames and buffered-message ownership.

## Capabilities

### New Capabilities

- `ci-dependency-selection`: Reproducible formatter selection, maintained runtime dependency floors and traceable contributor identity coverage.

## Impact

Changes are limited to development commands, dependency metadata/lock selections, the container package upgrade list, contributor records and compatibility of the existing upstream WebSocket handshake. Native CI and current-head review remain the acceptance gates. No application routing, database schema, release version or credentials change.
