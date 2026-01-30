#!/usr/bin/env bash
set -euo pipefail

# Quick setup validation for Week 6 pilot workflows.
required_tools=(python jq gh)

missing=()
for tool in "${required_tools[@]}"; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    missing+=("$tool")
  fi
done

if [ ${#missing[@]} -gt 0 ]; then
  echo "Missing required tools: ${missing[*]}" >&2
  exit 1
fi

echo "Environment looks ready for Week 6 setup."
