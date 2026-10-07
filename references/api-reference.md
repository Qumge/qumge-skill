# Qumge HTTP reference

**Audience: AI Agent** — for when the Qumge MCP tools are not connected.

Base: `https://qumge.com`. Auth, where needed: `Authorization: Bearer sk_qumge_…`.

## Search and read (no key)

The MCP endpoint is plain stateless HTTP — no handshake, no session — so any agent can
call its tools with `curl`:

```bash
curl -s -X POST https://qumge.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"search_caps","arguments":{"query":"make a promo video"}}}'
```

The answer is in `result.content[0].text`. The same shape works for every tool:

| Tool | Key | Arguments |
|---|---|---|
| `search_caps` | – | `query?`, `limit?` (≤10), `max_price_usd?` |
| `get_cap` | optional | `slug` |
| `search_skills` | – | `query?`, `category?`, `offset?`, `limit?` (≤10) |
| `get_skill` | – | `slug`, `include_files?` |
| `list_categories` | – | – |
| `list_models` | – | `query?`, `limit?` (≤60) |
| `call_cap` | **yes** | `slug` + `operation`, `input` — or the older `path`, `method?`, `query?`, `body?`, `content_type?`, `accept?` |
| `get_balance` | **yes** | – |
| `get_earnings` | **yes** | – |
| `request_payout` | **yes** | `amount_usd`, `confirmed?` |
| `list_wanted` | – | `limit?` (≤50) |
| `become_developer` | **yes** | `display_name`, `country`, `entity_type?`, `social_links?` |
| `list_caps` | **yes** | – |
| `verify_domain` | **yes** | `url`; then `url` + `check: true` after the line is deployed. Not needed to go live; releases frozen earnings |
| `publish_cap` | **yes** | `name` + `base_url` (HTTP API) or `mcp_url` + `mcp_tools` (remote MCP); price book — see `tools/list`. Or `manifest_url` (the project's qumge.json), plus `slug?` to pick one capability and `upstream_token?` when its auth is `api_key` |
| `test_cap` | **yes** | `slug` |
| `submit_cap` | **yes** | `slug` |
| `cap_status` | **yes** | `slug` |

The pre-rename names (`search_apps`, `get_app`, `call_app`, `publish_app`, `test_app`,
`submit_app_review`, `app_status`, `list_apps`) still dispatch; they are not listed.

For a tool that needs a key, send the `Authorization` header, or put
`"qumge_key": "sk_qumge_…"` in `arguments`.

Full schemas, always current:

```bash
curl -s -X POST https://qumge.com/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Calling a capability directly

```
<METHOD> https://qumge.com/v1/caps/<slug>/<route>
Authorization: Bearer sk_qumge_…
```

Operations, prices and error codes for every live capability, as OpenAPI 3.1:
`GET https://qumge.com/v1/caps/openapi.json` (no key). `/v1/apps/...` still works.

Errors come back as `{"error": {"code": "...", "message": "..."}}` — e.g.
`insufficient_balance`, `app_cap_reached`. See the OpenAPI `QumgeError` schema.

## Balance

```bash
curl -s https://qumge.com/v1/balance -H "Authorization: Bearer $QUMGE_API_KEY"
# → { "email", "balance", "balance_micro_usd", "currency": "USD", "topup_url" }
```

## Models (LLM gateway)

| Style | Endpoint |
|---|---|
| OpenAI | `POST /v1/chat/completions`, `POST /v1/embeddings`, `GET /v1/models` |
| Anthropic | `POST /v1/messages`, `POST /v1/messages/count_tokens` |

Point any OpenAI- or Anthropic-compatible client at `https://qumge.com/v1` with the
Qumge key. Setup guides per client: https://qumge.com/en/docs/quickstart

## Getting a key (device login)

```bash
curl -s -X POST https://qumge.com/device/code
curl -s -X POST https://qumge.com/device/token -d device_code=<device_code>
```

Details and the polling rules are in `SKILL.md` → *Spending needs the user's key*.
