## ADDED Requirements

### Requirement: Optional compatible runner routes

Standard workflow jobs SHALL look up their exact original platform label in the JSON object supplied by the repository variable `CI_RUNNER_ROUTES`. A missing variable or missing entry SHALL retain the original selector. A configured entry SHALL identify a compatible, admitted runner pool.

#### Scenario: No route is configured

- **WHEN** the variable is unset or the original platform key is absent
- **THEN** the job uses its original hosted selector

#### Scenario: A compatible route is configured

- **WHEN** a trusted repository event has a configured entry for the original platform label
- **THEN** the job uses that entry without changing its execution steps or permissions

### Requirement: Foreign pull requests retain hosted execution

A `pull_request` or `pull_request_target` event whose head repository differs from the current repository SHALL retain the original hosted selector regardless of the route map.

#### Scenario: A foreign pull request has a self-hosted route available

- **WHEN** either pull-request event originates from a different repository
- **THEN** its jobs retain their original hosted selectors

### Requirement: Runner selection preserves workflow behavior

Routing changes SHALL preserve workflow triggers, job dependencies, checks, commands, permissions, and platform defaults.

#### Scenario: A route is enabled or removed

- **WHEN** an administrator changes the route map
- **THEN** only runner selection changes and the original job checks still execute
