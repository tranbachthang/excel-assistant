#!/usr/bin/env bash
# Chay pi nhu mot agent rieng chi ve Excel (config dir = thu muc nay).
set -e
export PI_CODING_AGENT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec pi "$@"
