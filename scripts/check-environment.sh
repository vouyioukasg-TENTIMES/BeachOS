#!/usr/bin/env sh
set -eu

status=0

check_tool() {
  tool="$1"
  version_argument="$2"

  if command -v "$tool" >/dev/null 2>&1; then
    version=$("$tool" "$version_argument" 2>&1 | head -n 1)
    printf '%-12s %s\n' "$tool" "$version"
  else
    printf '%-12s %s\n' "$tool" "not found"
    status=1
  fi
}

check_tool git --version
check_tool node --version
check_tool corepack --version
check_tool python3 --version
check_tool uv --version
check_tool docker --version

if command -v docker >/dev/null 2>&1; then
  if docker compose version >/dev/null 2>&1; then
    printf '%-12s %s\n' "compose" "$(docker compose version)"
  else
    printf '%-12s %s\n' "compose" "not found"
    status=1
  fi
fi

exit "$status"
