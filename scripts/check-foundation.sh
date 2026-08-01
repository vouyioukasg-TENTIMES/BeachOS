#!/usr/bin/env sh
set -eu

required_directories="apps packages infrastructure scripts tests docs .github"
required_files="README.md BOOTSTRAP.md CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md LICENSE .gitignore .editorconfig .env.example package.json pnpm-workspace.yaml apps/web/package.json apps/web/index.html apps/web/src/main.tsx apps/web/src/App.tsx apps/web/src/App.test.tsx apps/api/pyproject.toml apps/api/src/beachos_api/__init__.py apps/api/src/beachos_api/main.py apps/api/tests/test_health.py infrastructure/docker/compose.yaml docs/DECISIONS.md ENGINEERING_SETUP_REPORT.md"

for directory in $required_directories; do
  if [ ! -d "$directory" ]; then
    echo "Missing required directory: $directory" >&2
    exit 1
  fi
done

for file in $required_files; do
  if [ ! -f "$file" ]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
done

for forbidden in \
  apps/api/alembic.ini \
  apps/api/src/beachos_api/application \
  apps/api/src/beachos_api/infrastructure; do
  if [ -e "$forbidden" ]; then
    echo "Unexpected application implementation found: $forbidden" >&2
    exit 1
  fi
done

echo "BeachOS repository bootstrap is valid."
