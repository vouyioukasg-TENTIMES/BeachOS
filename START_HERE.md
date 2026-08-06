# Start BeachOS Locally

This guide starts BeachOS on one computer for local development and demonstration.
It is written for someone who does not develop software.

BeachOS currently uses a temporary development identity. Do not expose this local
installation to the internet and do not use real customer or financial information.

## 1. Exact prerequisites

Install these tools before continuing:

1. **Git 2.39 or newer** — obtains the repository.
2. **Node.js 24** — runs the web application. Node 22 or earlier is not supported.
3. **Corepack** — normally included with Node.js and runs the pinned pnpm version
   without requiring administrator access.
4. **pnpm 10.12.4 through Corepack** — installs and runs the web application.
5. **Python 3.13** — runs the backend. Python 3.12 or earlier is not supported.
6. **uv 0.8 or newer** — installs and runs the Python environment.
7. **Docker Desktop with Docker Compose v2** — runs PostgreSQL 17 locally.
8. **curl** — checks that the backend started. It is already included with macOS and
   most Linux systems.

Docker Desktop must be open and show that its engine is running.

From the repository folder, check the tools:

```sh
./scripts/check-environment.sh
corepack pnpm@10.12.4 --version
curl --version
```

Expected major versions are Node `v24`, pnpm `10`, Python `3.13`, PostgreSQL Docker
image `17`, and Docker Compose `v2`.

## 2. First installation

Open **Terminal 1**, move into the repository folder, and run these commands exactly:

```sh
corepack pnpm@10.12.4 install --frozen-lockfile
cd apps/api
uv sync --locked --all-groups
cd ../..
cp .env.example .env
```

Run these commands once after a new checkout. Do not commit `.env`; it contains local
database credentials.

## 3. Start everything with one command

This is the recommended method. Keep Docker Desktop open, then use **one Terminal
window** from the repository root:

```sh
./scripts/start-local.sh
```

The command starts PostgreSQL, applies committed migrations, creates missing local-only
development configuration, starts the Backend, waits for its health check, and starts
the Frontend. It does not erase or replace existing local data.

Successful startup ends with:

```text
BeachOS is ready.
Open: http://127.0.0.1:5173
Press Control+C in this terminal to stop Backend and Frontend.
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173) in Chrome, Safari, Firefox, or
Edge.

## 4. Start each part manually

Use this method when troubleshooting. Open Docker Desktop and **three Terminal
windows**. Every command starts from the repository root.

### Terminal 1 — PostgreSQL and database preparation

```sh
docker compose --env-file .env -f infrastructure/docker/compose.yaml up -d postgres
set -a
. ./.env
set +a
cd apps/api
uv run python ../../scripts/migrate-local-database.py
uv run python ../../scripts/seed-local-development.py
```

Expected messages include:

```text
Container emerald-management-system-postgres-1 Started
BeachOS database is ready: emerald_local on localhost
Local BeachOS configuration is ready for Business Date YYYY-MM-DD.
```

Docker may print `Running` instead of `Started` when PostgreSQL is already running.

### Terminal 2 — Backend

```sh
set -a
. ./.env
set +a
cd apps/api
uv run uvicorn --app-dir src beachos_api.main:app --reload --host 127.0.0.1 --port 8000
```

The Backend is successful when the terminal includes:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

Optional check in another terminal:

```sh
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### Terminal 3 — Frontend

```sh
corepack pnpm@10.12.4 --filter @beachos/web dev --host 127.0.0.1
```

The Frontend is successful when the terminal includes text similar to:

```text
VITE ready
Local: http://127.0.0.1:5173/
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173).

## 5. What to expect in the browser

The BeachOS application shell should appear with its header, acting development user,
role selector, and navigation. On an empty local database, startup creates only the
development configuration needed to open the existing MVP: Emerald Beach Club, the
current Business Date, Kitchen and Bar department ownership, three Service Locations,
and three Menu Items. It creates no readiness declarations, Customer Groups, Orders,
Bills, Payments, or operational history. Running startup again preserves all existing
local facts.

## 6. Common startup problems

### `command not found: node`, `pnpm`, `python3`, `uv`, or `docker`

The named prerequisite is missing or the Terminal has not noticed a recent install.
Install it, close Terminal completely, open it again, and rerun the environment check.

### pnpm reports an unsupported version

Run the repository's exact version through Corepack. This does not require administrator
access to create a global command:

```sh
corepack pnpm@10.12.4 --version
```

### Docker says it cannot connect to the daemon

Open Docker Desktop and wait until it reports that Docker is running. Then retry.

### `.env` is missing

From the repository root run:

```sh
cp .env.example .env
```

### Port `5432`, `8000`, or `5173` is already in use

Another database or BeachOS process is already using the port. Stop the earlier process.
For Docker, inspect the local containers with:

```sh
docker compose --env-file .env -f infrastructure/docker/compose.yaml ps
```

Do not change ports unless the matching connection settings are updated together.

### Backend says `BEACHOS_DATABASE_URL is required`

The `.env` variables were not loaded. Use `./scripts/start-local.sh`, or repeat the three
environment-loading lines shown in the manual Backend instructions.

### Backend reports that a database table does not exist

Stop the Backend, then rerun the migration command from Terminal 1. Migrations preserve
existing local operational history.

### The browser shows an unavailable or uncertain state

First confirm that both Backend and Frontend terminals are still running. Check
`http://127.0.0.1:8000/health`. If it returns `{"status":"ok"}`, the application is
running; an empty database or unavailable operational fact may be the reason. Do not
repeat financial or operational actions while their outcome is uncertain.

### Installation cannot download packages

The first installation requires internet access to the configured package registries.
Check the connection, VPN, proxy, and firewall, then repeat the failed locked install
command. The lockfiles prevent dependency versions from changing.

## 7. Stop BeachOS

When using the automatic command, return to its Terminal and press **Control+C** once.
This stops Backend and Frontend but deliberately keeps PostgreSQL running and preserves
local data.

When using three terminals, press **Control+C** in the Backend and Frontend terminals.
Then stop PostgreSQL from the repository root:

```sh
docker compose --env-file .env -f infrastructure/docker/compose.yaml stop postgres
```

Stopping does not delete data. Never run `docker compose down --volumes` unless local
data deletion has been explicitly approved.

## 8. Clean-checkout verification status

The repository structure, lockfiles, script syntax, and Python migration helper were
verified in an isolated copy with installed dependencies and local configuration
deliberately absent. Frontend checks and the production build were verified in the
working repository using its already installed locked dependencies.

A complete first-run verification—including package downloads, PostgreSQL startup,
migrations against PostgreSQL 17, Backend startup, and the full browser connection—could
not be executed in the current environment because Node, pnpm, uv, Docker, and PostgreSQL
are not installed on its normal command path and no PostgreSQL service is available.
Those steps are therefore documented as **not executed**, not as successful.
