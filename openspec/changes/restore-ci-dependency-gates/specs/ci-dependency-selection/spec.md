## ADDED Requirements

### Requirement: Lint uses the locked formatter release

The standard lint command MUST invoke the Ruff release selected in the project lock and MUST run both lint and formatting checks.

#### Scenario: The package index publishes a newer formatter

- **GIVEN** the project's lock selects a particular Ruff release
- **WHEN** `make lint` runs
- **THEN** both Ruff commands use that exact release
- **AND** a newer available release does not silently change the formatter's behavior

### Requirement: Runtime dependency floors are applied to the frozen image

The package metadata MUST declare the reviewed minimum runtime dependency versions, and the container build MUST use a lock satisfying those minimums. The runtime image MUST include zlib in its existing explicit operating-system package upgrade step. The existing image vulnerability gate MUST remain enabled at its current severity threshold.

#### Scenario: The runtime image is rebuilt after a dependency refresh

- **WHEN** CI rebuilds the image using the committed dependency lock
- **THEN** dependency installation uses the reviewed selected versions without resolving a fresh unpinned Python environment
- **AND** the image is evaluated by the existing vulnerability scan and severity gate

### Requirement: Dependency updates preserve upstream WebSocket parsing

The custom upstream WebSocket handshake MUST remain compatible with the locked aiohttp release. It MUST decode text messages as strings, preserve binary messages as bytes, disable compression, remove forwarded WebSocket extension offers while preserving unrelated headers, and retain the parser while the response can still drain buffered messages.

#### Scenario: A local upstream sends a burst of uncompressed messages

- **WHEN** the custom handshake connects to an upstream that does not negotiate compression
- **AND** the upstream sends Unicode text and binary messages followed by a burst that exceeds the reader queue's high-water mark
- **THEN** the client receives every message in order with its original type and contents
- **AND** the connection closes without dropping buffered messages

#### Scenario: Forwarded headers advertise an unsupported extension

- **GIVEN** caller-supplied headers contain a WebSocket extension offer with any header-name casing
- **WHEN** the custom handshake connects to the upstream
- **THEN** the upstream receives no extension offer
- **AND** unrelated headers and uncompressed message contents remain intact

### Requirement: Contributor renames preserve historical coverage

Contributor records MUST use verified GitHub identities and MUST preserve historical login coverage where the attribution checker consumes historical commit logins.

#### Scenario: A contributor has a current login and a historical login

- **GIVEN** repository history and current GitHub metadata identify both logins as the same numeric account
- **WHEN** contributor coverage is maintained
- **THEN** the existing historical record and contribution categories remain intact
- **AND** the current login is covered using that verified identity
