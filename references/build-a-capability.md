# Build a capability from the user's project

**Audience: AI Agent**

Use this when the user wants to sell one thing their project does on Qumge, but the project has
**no public endpoint** Qumge can call. Your job is to add one small endpoint to their project,
publish it, and get it live. The user's job is to deploy it and to say yes before it goes live.

Check the other two paths first. They are much less work:

| The project already has… | Do this instead |
|---|---|
| A remote MCP server (Streamable HTTP, `https://`) | `publish_cap` with `mcp_url` + `mcp_tools`. No code. |
| A public HTTP API that takes an API key | `publish_cap` with `auth_mode: "api_key"` and the user's key as `upstream_token`. No code. See [Existing API](#existing-api-no-code) below. |
| Neither | Continue with this guide. |

## 1. Agree on one thing to sell

Sell **one operation**, not the whole app, for example "make a 15-second product video from a
brief". Ask the user if it is not obvious. Settle three things before you write code:

- **Input and output.** What the caller sends, and what comes back, as JSON.
- **Price per call**, in USD. It must cover what one call costs the user to run (model and API
  bills, compute). The same price every call is the simple case, and this guide assumes it.
  If the cost really varies (per second, per token), read "Meter" at
  https://qumge.com/en/docs/caps before continuing.
- **How long one call takes.** Qumge waits **30 seconds** for a response. Anything slower
  must be asynchronous (see step 4).

## 2. Read the project

Find the function that does the work, and the web framework the project already runs
(Rails, Express, FastAPI, Next.js route handlers…). Add the endpoint **to that server**, in
the project's own style. Don't add a new service, framework or language unless nothing else
can serve HTTP.

If the project has no server at all (a CLI, a library, a script), ask the user where it will
run before writing anything. A small HTTP app on a host they already use is usually enough.

## 3. Put everything under `/qumge/`

Qumge calls `<base_url><path>`. Use the site root as `base_url` and keep every Qumge route
under one prefix:

| Route | Purpose | Billed |
|---|---|---|
| `GET /qumge/ping` | Self-test: proves you verify our signature | no, and it is not in the price book |
| `POST /qumge/<operation>` | The thing you sell, e.g. `/qumge/videos` | yes, per call |
| `GET /qumge/<operation>/{id}` | Only for slow operations: job status | no |

One prefix gives you one place to apply signature verification, and nothing else in the
app is exposed. Never publish a `/**` route.

## 4. Write the endpoint

**Verify the signature on every `/qumge/*` request, before anything else.** Put it in
middleware or a before-filter scoped to the prefix:

```
canonical = "<Qumge-Timestamp>.<METHOD>.<path_with_query>.<sha256_hex(raw body)>"
expected  = "v1=" + hex(HMAC_SHA256(signing_secret, canonical))
```

- Reject when `Qumge-Signature` doesn't match (constant-time compare). During a key
  rotation, also accept `Qumge-Signature-Previous`.
- Reject when `|now − Qumge-Timestamp| > 300` seconds.
- Reject with **401 or 403**. An unsigned request counts as forged.
- `path_with_query` is the path your server receives, query string included exactly as
  sent. The body is the raw bytes, before any JSON parsing.
- Copy-paste verifiers for Node, Python and Ruby are at https://qumge.com/en/docs/caps.

Write a unit test with this vector. If your code agrees with it, it agrees with Qumge:

| Field | Value |
|---|---|
| `signing_secret` | `as_test_vector_do_not_use_in_production` |
| `Qumge-Timestamp` | `1758900000` |
| method, path | `POST /api/videos?page=2` |
| body | `{"credits":52}` |
| `Qumge-Signature` | `v1=0c654aa750f74f49a148bc6746920a184bec1bfc7b83d583724c41e31e043917` |

Then:

- **`GET /qumge/ping`**: after verification, return `200 {"ok":true}`. Our self-test also sends
  a forged request and a 10-minute-old one. Both must get 401/403.
- **`POST /qumge/<operation>`**: validate the input and return **422** with a readable message
  if it's wrong. Do the work and return **2xx** with the result. **Return non-2xx on every
  failure.** Qumge charges each 2xx and nothing else, so an error returned as 200 bills the
  user for a failure.
- **Who is calling**: `Qumge-User` (`au_…`) identifies the caller. It's stable per user and
  different for each capability. Callers never have an account in the user's app. Run the
  work under the app's own service account, and store `Qumge-User` on whatever records you
  create.
- **Slow operations** (over ~25 s): return `202 {"id": "…", "status": "queued"}` as soon as
  the job is accepted, and add a free status route that returns the result once it's done.
  The 202 is the billed response, so accept only jobs you will complete. If jobs often fail
  after they're accepted, per-call pricing is the wrong fit. Use `settle: "on_final"` with
  reported usage instead (see the docs).
- **The self-test caller.** `test_cap` calls your routes once, with `Qumge-User:
  au_qumge_selftest`, **no body**, and `*` in patterns replaced by `qumge-selftest` (so
  `GET /qumge/videos/qumge-selftest`). Both the first free route and the billable route must
  answer **2xx** to that caller. Return a canned sample result when `Qumge-User` is
  `au_qumge_selftest`, after the signature check has passed. Don't skip the check for it.
- **Secrets** go in environment variables (`QUMGE_SIGNING_SECRET`), never in code or logs.

## 5. Publish, deploy, test, go live

Do these in order. Each step needs the one before it.

1. `become_developer(display_name, country)`, once per account, if `publish_cap` asks for it.
2. `publish_cap` creates a **draft**. It doesn't go live and doesn't charge anyone:

   ```json
   {
     "name": "Product video",
     "base_url": "https://app.example.com",
     "summary": "Make a 15-second product video from a one-line brief.",
     "events": [ { "key": "call", "unit_price_usd": 0.5 } ],
     "routes": [
       { "method": "POST", "pattern": "/qumge/videos", "name": "create_video",
         "billable": true, "event": "call", "hold_usd": 0.5,
         "settle": "on_response", "meter": "platform",
         "doc": { "summary": "Start a video from a brief.",
                  "input_schema": { "type": "object", "required": ["brief"],
                                    "properties": { "brief": { "type": "string" } } } } },
       { "method": "GET", "pattern": "/qumge/videos/*", "name": "get_video", "billable": false }
     ]
   }
   ```

   It returns the **signing secret, shown once**. Tell the user to put it in the production
   environment as `QUMGE_SIGNING_SECRET`. Don't write it into files you commit.
3. **Ask the user to deploy, and wait.** Don't deploy for them unless they ask you to.
4. `test_cap(slug)` sends the three pings, then calls the first free route and the billable
   route once each, as the self-test caller described in step 4. Nobody is charged. If it fails, the reply names which probe failed.
   Fix that and redeploy. Don't loosen the verification to make the test pass.
5. Show the user the price and the operation, and ask them to confirm. Then call
   `submit_cap(slug)`. **This takes it live immediately.** No one reviews it first, and agents
   can be charged from that moment.

## Existing API: no code

If the project already has a public API that authenticates with an API key, skip all of the
above. Get the key from the user, then:

```json
{
  "name": "Product video",
  "base_url": "https://api.example.com",
  "auth_mode": "api_key",
  "upstream_token": "<the user's API key>",
  "events": [ { "key": "call", "unit_price_usd": 0.5 } ],
  "routes": [ { "method": "POST", "pattern": "/v1/videos", "name": "create_video",
                "billable": true, "event": "call", "hold_usd": 0.5,
                "settle": "on_response", "meter": "platform" } ]
}
```

Qumge calls that path with `Authorization: Bearer <key>`, and nothing else in their API is
reachable. Two rules:
- Every route must be an **exact path** (no `*` or `{}`).
- Every route must be billed **per call** (`meter: "platform"`).

The key reaches everything the user's account can do, so open only the endpoint being sold.
Then run `test_cap` and `submit_cap` as in step 5. A 400/422 from the probe is fine: it
proves the path exists and the key works.

## Don'ts

- Don't publish a `/**` route or any admin, account or payment endpoint.
- Don't return 200 for errors.
- Don't call `submit_cap` without the user's explicit yes.
- Don't put the signing secret or the user's API key in code, commits or chat logs you share.
