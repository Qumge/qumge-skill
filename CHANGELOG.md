# Changelog

## 0.2.1 — 2026-09-28

- Publishing: an existing remote MCP server can be published with `mcp_url` + `mcp_tools`
  (one tool = one operation, billed per successful call).

## 0.2.0 — 2026-09-28

- Renamed apps to capabilities throughout (Qumge is the capability layer for agents).
- Tool names are now `search_caps` / `get_cap` / `call_cap` / `publish_cap` / `test_cap` /
  `submit_cap` / `cap_status` / `list_caps`; the old names still dispatch.
- Publishing now says to write the integration (`GET /qumge/ping`, signature check,
  usage reporting) into the project and deploy it before `test_cap`.
- Added `get_earnings` and `request_payout`; only capability income is withdrawable.
- HTTP paths moved to `/v1/caps/...` (`/v1/apps/...` still works).

## 0.1.0 — 2026-09-27

- First release: apps (search, price book, call, balance), skills (search, install),
  models, publishing an app, device login, and an HTTP fallback for agents without MCP.
