# Cross-application tests

This directory is reserved for tests that cross application boundaries.

- `unit/` is available for repository-level utilities that do not belong to one application.
- `integration/` will hold tests involving multiple components or real infrastructure.
- `e2e/` will hold critical browser-to-backend journeys.

Tests belonging solely to one application should live close to that application. No business tests exist because no business features have been implemented.
