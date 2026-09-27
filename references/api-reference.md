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
       "params":{"name":"search_apps","arguments":{"query":"make a promo video"}}}'
```

The answer is in `result.content[0].text`. The same shape works for every tool:

| Tool | Key | Arguments |
|---|---|---|
| `search_apps` | – | `query?`, `limit?` (≤10) |
| `get_app` | optional | `slug` |
| `search_skills` | – | `query?`, `category?`, `offset?`, `limit?` (≤10) |
| `get_skill` | – | `slug`, `include_files?` |
| `list_categories` | – | – |
| `list_models` | – | `query?`, `limit?` (≤60) |
| `call_app` | **yes** | `slug`, `path`, `method?`, `query?`, `body?`, `content_type?`, `accept?` |
| `get_balance` | **yes** | – |
| `become_developer` | **yes** | `display_name`, `country`, `entity_type?`, `social_links?` |
| `list_apps` | **yes** | – |
| `publish_app` | **yes** | `name`, `base_url`, and the price book — see `tools/list` |
| `test_app` | **yes** | `slug` |
| `submit_app_review` | **yes** | `slug` |
| `app_status` | **yes** | `slug` |

For a tool that needs a key, send the `Authorization` header, or put
`"qumge_key": "sk_qumge_…"` in `arguments`.

Full schemas, always current:

```bash
curl -s -X POST https://qumge.com/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Calling an app directly

```
<METHOD> https://qumge.com/v1/apps/<slug>/<route>
Authorization: Bearer sk_qumge_…
```

Routes, prices and error codes for every live app, as OpenAPI 3.1:
`GET https://qumge.com/v1/apps/openapi.json` (no key).

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
