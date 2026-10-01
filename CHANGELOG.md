# Changelog

## 0.5.0 — 2026-10-01

- Going live no longer waits for `verify_domain`. A cap on an unverified domain is live and
  charges callers, but its earnings stay frozen until the domain is verified; verifying
  releases them (30 days after each call). A domain another developer verified can't be used.
- `get_earnings` shows the frozen amount. DNS TXT verification only counts on the host itself.
- The Publish page takes a pasted service URL and goes live in one click; the GitHub project
  scan is gone (GitHub is only for importing skills).

## 0.4.1 — 2026-10-01

- Publishing rule: every billed operation delivers one complete result for one clear input.
  Helper steps are free; a result that needs several calls is wrapped into one endpoint.

## 0.4.0 — 2026-10-01

- Publishing is one flow the agent runs inside the user's project: it works out what the
  project has (MCP first, then an API with a key, else build an endpoint), proposes a price,
  and asks the user only three things — the price, "it's deployed", "go live".
- New tool `verify_domain`: get the verification line, ship it with the next deploy, then
  `verify_domain(check: true)`.
- `build-a-capability.md`: the default endpoint now checks an API key the agent generates
  (`auth_mode: "api_key"`); the signed variant is for usage-based billing, per-caller records
  or slow jobs.

## 0.3.0 — 2026-09-30

- Publishing starts from what the project already has: a remote MCP server (`mcp_url`), a
  public API with an API key (`auth_mode: "api_key"` — no code to write), or neither.
- New `references/build-a-capability.md`: a step-by-step guide for the agent to add one
  signed endpoint to the user's project and take it live.

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
