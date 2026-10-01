# Build a capability from the user's project

**Audience: AI Agent**

Use this when the user wants to sell one thing their project does on Qumge, but the project has
**no public endpoint** Qumge can call — no remote MCP server and no API that takes a key. Your
job is to add one small endpoint to their project, publish it and get it live. The user only
answers three things: the price, "it's deployed", and "go live".

Check the other two paths first (see SKILL.md → Publishing). They need no code:

| The project already has… | Do this instead |
|---|---|
| A remote MCP server (Streamable HTTP, `https://`) | `publish_cap` with `mcp_url` + `mcp_tools`. |
| A public HTTP API that takes an API key | `publish_cap` with `auth_mode: "api_key"` and the user's key as `upstream_token`. See [Existing API](#existing-api-no-code) below. |
| Neither | Continue with this guide. |

## 1. Agree on one thing to sell

Sell **one operation**, not the whole app, for example "make a 15-second product video from a
brief". Pick the obvious one; ask only if there is no obvious one. Settle three things before you write code:

- **Input and output.** What the caller sends, and what comes back, as JSON.
- **Price per call**, in USD. **Propose a number** ("$0.05 per call — OK?"); it must cover what one call
  costs the user to run (model and API bills, compute). The same price every call is the simple case, and this guide assumes it.
  If the cost really varies (per second, per token), read "Meter" at
  https://qumge.com/en/docs/caps before continuing.
- **How long one call takes.** Qumge waits **30 seconds** for a response. Anything slower
  must be asynchronous — that needs the signed variant (see the last section).

## 2. Read the project

Find the function that does the work, and the web framework the project already runs
(Rails, Express, FastAPI, Next.js route handlers…). Add the endpoint **to that server**, in
the project's own style. Don't add a new service, framework or language unless nothing else
can serve HTTP.

If the project has no server at all (a CLI, a library, a script), ask the user where it will
run before writing anything. A small HTTP app on a host they already use is usually enough.

## 3. The endpoint: one route, checked by an API key

This is the default: the simplest code, and the user can read it. Qumge calls your route with
`Authorization: Bearer <key>`, using a key **you generate** for this purpose.

| Route | Purpose | Billed |
|---|---|---|
| `POST /qumge/<operation>` | The thing you sell, e.g. `/qumge/videos` | yes, per call |

- **Check the key first**, in middleware or a before-filter scoped to `/qumge/`:
  compare `Authorization: Bearer <key>` with `QUMGE_API_KEY` from the environment, in
  constant time. Missing or wrong → **401**.
- **Validate the input** and return **422** with a readable message if it's wrong.
- Do the work and return **2xx** with the result as JSON. **Return non-2xx on every failure.**
  Qumge charges each 2xx and nothing else, so an error returned as 200 bills the caller for a
  failure.
- **The self-test call.** `test_cap` calls the route once with the key and **no body**. Answer
  it with 2xx (a canned sample) or 400/422 (it proves the route exists and the key works).
- One exact path, no `*` or `{}` — Qumge forwards only the paths in the price book.

Generate the key yourself (e.g. `openssl rand -hex 32`). It goes in **two** places and
nowhere else — never in code or commits:
1. The production environment, as `QUMGE_API_KEY`. Tell the user the exact name and value to
   set where they deploy (or set it yourself if their host has a CLI they've logged into and
   they say yes).
2. `publish_cap`, as `upstream_token`.

Trade-off you accept with this variant: Qumge calls every request with the same key, so the
endpoint can't tell callers apart, and the price is fixed per call. If the user needs
usage-based billing, per-caller records, or the work takes over ~25 s, use the signed variant
at the end instead.

## 4. Verification file, then one deploy

1. `verify_domain(url: "https://<their host>")` → one line. Serve it at
   `https://<host>/.well-known/qumge-verify.txt` (a static file, or a route returning it as
   text). Skip this if it already says **verified**.
2. **One deploy** for the endpoint, the verification file and the environment variable. If
   pushing to GitHub deploys the project, ask "Shall I commit and push so it deploys?" and do
   it on a yes. Otherwise ask the user to deploy and wait.
3. `verify_domain(url:, check: true)`.

## 5. Publish, test, go live

1. `become_developer(display_name, country)`, once per account, if `publish_cap` asks.
2. `publish_cap` — a **draft**; nobody can call it yet:

   ```json
   {
     "name": "Product video",
     "base_url": "https://app.example.com",
     "summary": "Make a 15-second product video from a one-line brief.",
     "auth_mode": "api_key",
     "upstream_token": "<the key you generated>",
     "events": [ { "key": "call", "unit_price_usd": 0.5 } ],
     "routes": [
       { "method": "POST", "pattern": "/qumge/videos", "name": "create_video",
         "billable": true, "event": "call", "hold_usd": 0.5,
         "settle": "on_response", "meter": "platform",
         "doc": { "summary": "Make a video from a brief.",
                  "input_schema": { "type": "object", "required": ["brief"],
                                    "properties": { "brief": { "type": "string" } } } } }
     ]
   }
   ```
3. `test_cap(slug)`. A 401 means the deployed `QUMGE_API_KEY` doesn't match `upstream_token`
   — usually the variable wasn't set before the deploy.
4. Ask "Go live at $X per call?". On a yes, `submit_cap(slug)` — **live immediately**.

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

## When you need the signed variant

Use this instead of the API-key endpoint when the user needs **usage-based billing**, needs to
know **which caller** made a request (`Qumge-User`), or the work takes **over ~25 s**
(asynchronous jobs with a status route). Qumge signs every request; your endpoint verifies the
signature. Publish without `auth_mode` (signature mode is the default); `publish_cap` returns
the signing secret once — it goes in the production environment as `QUMGE_SIGNING_SECRET`.
Steps 4 and 5 above (verification file, one deploy, publish, test, go live) are the same.

### Routes under `/qumge/`

Qumge calls `<base_url><path>`. Use the site root as `base_url` and keep every Qumge route
under one prefix:

| Route | Purpose | Billed |
|---|---|---|
| `GET /qumge/ping` | Self-test: proves you verify our signature | no, and it is not in the price book |
| `POST /qumge/<operation>` | The thing you sell, e.g. `/qumge/videos` | yes, per call |
| `GET /qumge/<operation>/{id}` | Only for slow operations: job status | no |

One prefix gives you one place to apply signature verification, and nothing else in the
app is exposed. Never publish a `/**` route.

### Write the endpoint

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

### Publish (signed)

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
3. **One deploy**, together with the verification file (see step 4 above). If pushing to GitHub
   deploys the project, offer to commit and push; otherwise ask the user to deploy and wait.
4. `test_cap(slug)` sends the three pings, then calls the first free route and the billable
   route once each, as the self-test caller described above. Nobody is charged. If it fails, the reply names which probe failed.
   Fix that and redeploy. Don't loosen the verification to make the test pass.
5. Show the user the price and the operation, and ask them to confirm. Then call
   `submit_cap(slug)`. **This takes it live immediately.** No one reviews it first, and agents
   can be charged from that moment.

## Don'ts

- Don't publish a `/**` route or any admin, account or payment endpoint.
- Don't return 200 for errors.
- Don't call `submit_cap` without the user's explicit yes.
- Don't put the signing secret, the key you generated, or the user's API key in code, commits or chat logs you share.
