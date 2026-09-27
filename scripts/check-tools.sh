#!/usr/bin/env bash
# The docs in this repo are what an agent acts on. If qumge.com adds, renames or drops an
# MCP tool, the docs go stale silently — the agent doesn't error, it just does the wrong
# thing. This compares the live tool list against references/api-reference.md and fails
# on any difference, in either direction.
set -euo pipefail

endpoint="${QUMGE_MCP_URL:-https://qumge.com/mcp}"
doc="$(dirname "$0")/../references/api-reference.md"

live="$(curl -sf -X POST "$endpoint" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | jq -r '.result.tools[].name' | sort)"

if [ -z "$live" ]; then
  echo "Could not read tools/list from $endpoint" >&2
  exit 1
fi

documented="$(grep -oE '^\| `[a-z_]+` \|' "$doc" | tr -d '|` ' | sort)"

if [ "$live" != "$documented" ]; then
  echo "Tool list drifted from references/api-reference.md" >&2
  diff <(echo "$documented") <(echo "$live") --label documented --label live >&2 || true
  exit 1
fi

echo "OK: $(echo "$live" | wc -l | tr -d ' ') tools documented, matching $endpoint"
