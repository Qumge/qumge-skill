# Platform access

Connect to the existing hosted MCP; do not deploy a second MCP server:

```bash
claude mcp add --transport http qumge https://qumge.com/mcp
```

Use available Qumge MCP tools and their `structuredContent`. For an authenticated tool,
reuse `QUMGE_API_KEY` or `~/.config/qumge/credentials.json` (`api_key`) without printing it.
This is the owner's platform credential, not the provider connection credential.

If no key exists, POST https://qumge.com/device/code. Show only its
`verification_uri_complete` for the owner to approve. Poll POST /device/token with the
returned device_code at the advertised interval; respect slow_down and expiry. When
approved, store the access_token as api_key in the credential file with private permissions
(0600), without echoing it or committing it. Reuse it rather than asking again.
The user handles account sign-in and any indispensable browser-owned verification.

Without MCP integration, the same hosted endpoint supports JSON-RPC over HTTP:

```bash
curl -sS https://qumge.com/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Read the current input schema first. Call tools/call with params.name and params.arguments.
For owner tools, add Authorization: Bearer using the stored key without logging it.
Inspect result.isError, protocol error and structuredContent; do not parse prose for state.
Full tool reference: https://qumge.com/en/docs/mcp.md. Searching public Caps/models needs no
key; developer tools require the owner's account. The consumer skill is not required to
install or use this publisher skill.
