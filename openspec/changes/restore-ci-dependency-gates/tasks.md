## 1. Implementation

- [x] Pin both standard Ruff invocations to the release already selected in the lock.
- [x] Add contributor aliases from verified existing metadata without removing history.
- [x] Refresh affected runtime dependency floors and lock selections.
- [x] Add zlib to the runtime image's explicit OS upgrade step.
- [x] Preserve upstream WebSocket parser behavior and lifetime with aiohttp 3.14.4.
- [x] Remove forwarded extension offers from the deliberately uncompressed handshake while preserving unrelated headers.

## 2. Verification

- [x] Validate this change strictly and run the repository's standard main-spec validation.
- [x] Run the actual lint command with the selected formatter.
- [x] Check lock consistency and run focused dependency compatibility tests.
- [x] Exercise the real aiohttp upgrade/parser against a local WebSocket server and pass the exact type-check gate.
- [x] Exercise incoming extension offers with different header casing and rerun the exact type/lint gates.
- [ ] Observe required native CI, rebuilt-image scan and current-head review before merge.
- [ ] Keep this change unarchived until acceptance is complete.
