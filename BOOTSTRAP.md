# BeachOS Repository Bootstrap

## Prerequisites

- Node.js 24
- pnpm 10
- Python 3.13
- uv

Docker is optional for this bootstrap because the backend does not use a database
yet.

## Install

Install the frontend workspace from the repository root:

```sh
pnpm install --frozen-lockfile
```

Install the backend environment:

```sh
cd apps/api
uv sync --locked --all-groups
```

## Run

Start the frontend from the repository root:

```sh
pnpm --filter @beachos/web dev
```

The frontend development server prints its local address. The page contains only:

- BeachOS
- Sprint 1
- Venue Opening

Start the backend in another terminal:

```sh
cd apps/api
uv run uvicorn beachos_api.main:app --reload
```

Verify the health endpoint:

```sh
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Test and verify

Run frontend formatting, linting, type checking, tests, and build:

```sh
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Run backend formatting, linting, type checking, tests, and build:

```sh
cd apps/api
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
uv build
```

Validate the repository skeleton:

```sh
./scripts/check-foundation.sh
```

## Expected project structure

```text
.
├── apps/
│   ├── api/
│   │   ├── src/beachos_api/
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   ├── tests/
│   │   │   └── test_health.py
│   │   ├── pyproject.toml
│   │   └── uv.lock
│   └── web/
│       ├── src/
│       │   ├── App.test.tsx
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── vite.config.ts
│       └── vitest.config.ts
├── docs/
├── framework/
├── infrastructure/
├── packages/
├── scripts/
├── tests/
├── ux/
├── wireframes/
├── .github/workflows/ci.yml
├── BOOTSTRAP.md
├── package.json
├── pnpm-lock.yaml
└── pnpm-workspace.yaml
```

Only the executable foundation exists. There is no authentication, business logic,
database model, migration, business API, or product UI.
