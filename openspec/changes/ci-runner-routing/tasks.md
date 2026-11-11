## 1. Selector implementation

- [x] Add the optional `CI_RUNNER_ROUTES` lookup to the existing standard selectors.
- [x] Preserve each original platform label as the route key and fallback.
- [x] Keep foreign `pull_request` and `pull_request_target` events on the hosted fallback.
- [x] Verify parsed workflow semantics are unchanged outside `runs-on`.

## 2. Acceptance

- [ ] Observe required native workflow results at the published head.
- [ ] Complete the repository's current-head review and CI requirements before merge.
- [ ] Admit a real compatible runner pool and observe an actual routed job before claiming routed execution.
- [ ] Keep this change unarchived until its acceptance evidence is complete.
