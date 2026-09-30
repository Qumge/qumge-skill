# Qumge Skill

**Audience: Human (project overview)**

[Qumge](https://qumge.com) is the capability layer for agents. This skill teaches your agent
(Claude Code, Cursor, Codex, OpenClaw, any agent that reads `SKILL.md`) to use it:

- **Capabilities** — find a hosted service that does the job (video, transcription,
  publishing…) and call it, billed per call from your Qumge balance. Same price as calling
  it directly; a failed call (5xx) costs nothing.
- **Skills** — search a curated catalog of popular agent skills and install one into your
  agent without leaving the chat. Free.
- **Models** — one key for many LLMs through an OpenAI- and Anthropic-compatible gateway.
- **Publish** — supply your own HTTPS service to Qumge and get paid per call, straight
  from your agent.

## Quick start

### 1. Install the skill

```bash
npx skills add xnjiang/qumg-skill
```

Or tell your agent: `Install the skill from https://github.com/xnjiang/qumg-skill`

### 2. (Recommended) connect the MCP server too

```bash
claude mcp add --transport http qumge https://qumge.com/mcp
```

The skill works without it — it falls back to plain HTTP — but the MCP tools are
smoother. Other clients: see [qumg-mcp](https://github.com/xnjiang/qumg-mcp).

### 3. Just ask

- "Find me a skill that extracts tables from PDFs"
- "Which models can I use with my Qumge key?"
- "What's my Qumge balance?"
- "Publish my API at https://api.example.com on Qumge"

Searching needs no account. The first time your agent needs to spend, it opens a login
link for you to approve in the browser, and saves the key to
`~/.config/qumge/credentials.json`. Or set `QUMGE_API_KEY` yourself — keys are at
https://qumge.com/en/gateway/api_keys.

Qumge is pay-as-you-go: you top up your balance first, then pay per call.

## Files

| File | For |
|---|---|
| `SKILL.md` | The agent — what Qumge is and how to use it |
| `references/api-reference.md` | The agent — the HTTP API, for agents without MCP |
| `references/build-a-capability.md` | The agent — turning part of the user's project into a capability |
| `marketplace.json` | Skill marketplaces |

## Links

- Website: https://qumge.com
- MCP server: https://github.com/xnjiang/qumg-mcp
- For agents: https://qumge.com/llms.txt

## License

MIT
