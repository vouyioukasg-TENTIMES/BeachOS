# Local Docker environment

`compose.yaml` starts PostgreSQL only. It creates no application tables or seed data.

After Docker and the infrastructure proposal are approved:

1. Copy `.env.example` to `.env` and change the local password.
2. Run `docker compose -f infrastructure/docker/compose.yaml up -d postgres`.
3. Check status with `docker compose -f infrastructure/docker/compose.yaml ps`.
4. Stop with `docker compose -f infrastructure/docker/compose.yaml down`.

Do not add `--volumes` to the stop command unless deleting local database data is explicitly intended.
