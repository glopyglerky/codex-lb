## Why

Workflow runner selection is currently fixed in each job. Administrators need to select a compatible execution pool without changing job commands, required checks, release permissions, or the original platform fallback.

## What Changes

- Allow standard job selectors to consult the repository variable `CI_RUNNER_ROUTES`, keyed by the original platform label.
- Keep the original GitHub-hosted selector when the variable or platform entry is absent.
- Keep foreign pull requests, including `pull_request_target`, on their original hosted selector.
- Preserve all workflow triggers, checks, dependencies, permissions, and execution steps.

## Capabilities

### New Capabilities

- `ci-runner-routing`: Optional administrator-controlled runner selection with platform-preserving defaults and a foreign-pull-request boundary.

## Impact

Only standard `runs-on` expressions change. Administrators must admit a compatible, available pool before setting a route. This change does not register runners or establish capacity. No credentials or private implementation are stored in workflow files.
