#!/usr/bin/env sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
environment_file="$repository_root/.env"
compose_file="$repository_root/infrastructure/docker/compose.yaml"

# Homebrew is not always present on PATH in non-interactive Mac shells.
if [ -d /opt/homebrew/bin ]; then
  PATH="/opt/homebrew/bin:$PATH"
  export PATH
fi

if [ ! -f "$environment_file" ]; then
  echo "Missing .env. Run: cp .env.example .env" >&2
  exit 1
fi

for required_tool in docker node uv curl; do
  if ! command -v "$required_tool" >/dev/null 2>&1; then
    echo "Missing required tool: $required_tool. See START_HERE.md." >&2
    exit 1
  fi
done

if command -v pnpm >/dev/null 2>&1; then
  run_pnpm() { pnpm "$@"; }
elif command -v corepack >/dev/null 2>&1; then
  run_pnpm() { corepack pnpm@10.12.4 "$@"; }
else
  echo "Missing required tool: pnpm or Corepack. See START_HERE.md." >&2
  exit 1
fi

set -a
# This file is local, user-controlled configuration copied from .env.example.
# shellcheck disable=SC1090
. "$environment_file"
set +a

if [ -z "${BEACHOS_DATABASE_URL:-}" ]; then
  echo "BEACHOS_DATABASE_URL is missing from .env." >&2
  exit 1
fi

api_pid=""
web_pid=""

stop_applications() {
  trap - INT TERM EXIT
  if [ -n "$api_pid" ]; then kill "$api_pid" 2>/dev/null || true; fi
  if [ -n "$web_pid" ]; then kill "$web_pid" 2>/dev/null || true; fi
  wait "$api_pid" 2>/dev/null || true
  wait "$web_pid" 2>/dev/null || true
  echo "BeachOS applications stopped. PostgreSQL is still running so local data is preserved."
}

trap stop_applications INT TERM EXIT

echo "Starting local PostgreSQL 17…"
docker compose --env-file "$environment_file" -f "$compose_file" up -d postgres

attempt=0
until docker compose --env-file "$environment_file" -f "$compose_file" exec -T postgres \
  pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "PostgreSQL did not become ready. Open Docker Desktop and retry." >&2
    exit 1
  fi
  sleep 1
done

echo "Applying committed database migrations…"
(
  cd "$repository_root/apps/api"
  uv run python ../../scripts/migrate-local-database.py
  uv run python ../../scripts/seed-local-development.py
)

echo "Starting BeachOS Backend…"
(
  cd "$repository_root/apps/api"
  uv run uvicorn --app-dir src beachos_api.main:app --reload --host 127.0.0.1 --port 8000
) &
api_pid=$!

attempt=0
until curl --silent --fail http://127.0.0.1:8000/health >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "Backend did not become ready. Review the messages above." >&2
    exit 1
  fi
  sleep 1
done

echo "Starting BeachOS Frontend…"
(
  cd "$repository_root"
  run_pnpm --filter @beachos/web dev --host 127.0.0.1
) &
web_pid=$!

echo ""
echo "BeachOS is ready."
echo "Open: http://127.0.0.1:5173"
echo "Press Control+C in this terminal to stop Backend and Frontend."

wait "$api_pid" "$web_pid"
