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

Prefer `result.structuredContent` for state and receipts; content text is display copy, not a stable contract. Check top-level error and result.isError before using a result. The same envelope works for every tool:

| Tool | Key | Arguments |
|---|---|---|
| `search_caps` | – | `query?`, `limit?` (≤10), `max_price_usd?` |
| `get_cap` | optional | `slug` |
| `search_skills` | – | `query?`, `category?`, `offset?`, `limit?` (≤10) |
| `get_skill` | – | `slug`, `include_files?` |
| `list_categories` | – | – |
| `list_models` | – | `query?`, `limit?` (≤60) |
| `call_cap` | **yes** | `slug` + `operation`, `input`, `idempotency_key?`, `accepted_contract_digest?` — or the older `path`, `method?`, `query?`, `body?`, `content_type?`, `accept?` |
| `get_cap_job` | **yes** | `job_id` (the platform id `call_cap` returned); `refresh_result: true` to explicitly renew a supported result URL. Free — ordinary reads don't call the provider |
| `get_balance` | **yes** | – |
| `get_earnings` | **yes** | – |
| `request_payout` | **yes** | `amount_usd`, `confirmed?` |
| `list_wanted` | – | `limit?` (≤50) |
| `become_developer` | **yes** | `display_name`, `country`, `username?` (required if the account has none), `entity_type?`, `social_links?` |
| `list_caps` | **yes** | – |
| `verify_domain` | **yes** | `url`; then `url` + `check: true` after the line is deployed. Not needed to go live; releases frozen earnings |
| `publish_cap` | **yes** | Prefer managed-v2 `manifest_url` + `slug?`; configure private provider credentials separately. Advanced manual HTTP/MCP inputs: inspect current tools/list. Creates/updates a draft; does not deploy the project. |
| `test_cap` | **yes** | `slug`, `price_version?` for exact candidate tests; distinguish connection, fixture and real_delivery |
| `migrate_cap_contract` | **yes** | `slug`, `action`; inspect tools/list for prepare/test/activate/status/repair_review inputs. Owner-scoped existing-contract migration, not an ordinary new draft. |
| `submit_cap` | **yes** | `slug` |
| `cap_status` | **yes** | `slug` |
| `delist_cap` | **yes** | `slug` — take your own Cap down; calls stop at once (404 `cap_delisted`), the public page stays up |
| `relist_cap` | **yes** | `slug` — put it back, no new review; a service address changed while it was down is retested first |

The pre-rename names (`search_apps`, `get_app`, `call_app`, `publish_app`, `test_app`,
`submit_app_review`, `app_status`, `list_apps`) still dispatch; they are not listed.

For a tool that needs a key, send the `Authorization` header, or put
`"qumge_key": "sk_qumge_…"` in `arguments`.

Every tool, which ones need a key, and the output contract: https://qumge.com/en/docs/mcp

Full schemas, always current:

```bash
curl -s -X POST https://qumge.com/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Calling a Cap directly

```
<METHOD> https://qumge.com/v1/caps/<slug>/<route>
Authorization: Bearer sk_qumge_…
```

Operations, prices and error codes for every live Cap, as OpenAPI 3.1:
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
Qumge key. Setup guides per client: https://qumge.com/en/docs/connect

## Getting a key (device login)

```bash
curl -s -X POST https://qumge.com/device/code
curl -s -X POST https://qumge.com/device/token -d device_code=<device_code>
```

Details and the polling rules are in `SKILL.md` → *Spending needs the user's key*.

## Consumer and publisher skills

Use qumge for finding/calling Caps and model access. For adapting or managing your own
service, install qumge-publish from this same repository with
`npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish`.
It includes its own auth/HTTP fallback, offline preflight, managed-v2 example and resume guide.
The platform manifest schema is https://qumge.com/schemas/qumge-manifest/v2.json.

A changed deliverable may require current get_cap contract_state confirmation before passing
accepted_contract_digest. Old spending permission is not acceptance of a different result.
Use one stable idempotency_key for the same managed operation/input; read the returned
platform job ID instead of reissuing a generation. Local file hashes are not platform contract digests.
