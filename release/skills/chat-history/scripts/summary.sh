#!/usr/bin/env bash
# Wrapper → chat-history.mjs (giữ tương thích lệnh cũ)
node "$(dirname "$0")/chat-history.mjs" summary "$@"
