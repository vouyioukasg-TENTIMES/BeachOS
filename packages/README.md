# Shared packages

This directory is reserved for deliberately shared code and configuration.

- `config/` may hold shared engineering configuration when duplication appears.
- `shared/` may hold stable, application-independent contracts or utilities after their ownership is clear.

Nothing should be placed here merely because two files look similar. Shared packages create coupling and require an explicit owner, purpose, tests, and dependency direction.
