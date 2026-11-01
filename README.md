# Qumge — find a capability for your agent

[English](README.md) | [简体中文](README.zh-CN.md)

Give your agent a task. Find a capability, inspect its deliverables and price, then choose whether to run it.

## Start here: install, check, search

No Qumge account, API key or top-up is needed to install the skill or search capabilities. Your current agent and model stay in place.

### 1. Install in your project

Have a skill-compatible coding agent, [Node.js LTS](https://nodejs.org/) (includes npm/npx) and [Git](https://git-scm.com/downloads) installed. Check with `node --version`, `npx --version` and `git --version`. Open a terminal in the project you use with your agent.

Choose **one** command for your agent:

**Codex**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent codex
```

**Claude Code**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent claude-code
```

**Cursor**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent cursor
```

For another compatible agent, run the original command and choose your agent if prompted:

```bash
npx skills add Qumge/qumge-skill
```

If npx asks to download a package, check it is the `skills` installer. If npx is missing, install Node.js and reopen the terminal. If asked for installation scope, choose **Project**, not Global. These instructions install into the **current project**. Repeat inside another project when needed.

Only using ChatGPT or Claude in a browser? Use the [MCP connector guide](https://qumge.com/en/docs/connect) instead of running npx in a chat box.

### 2. Check it is installed

The installer should show `Installation complete` and `qumge`. Confirm `.agents/skills/qumge/SKILL.md` or the agent-specific location reported by the installer exists. Return to the **same project** in your agent; reopen the session if it cannot see the new skill. Codex can explicitly select it with `$qumge`.

### 3. Find your first capability for free

Tell your agent:

> Use Qumge to find a meeting-minutes capability. Tell me its required input, deliverables and price. Do not execute it yet.

Expect a suitable capability and its input, complete result and price, or an honest explanation that none fits. Do not sign in or top up just to search. For example, a YouTube overview needs a supported public video link; video generation is not video summarization.

[Browse capabilities](https://qumge.com/en/caps) · [Step-by-step installation guide](https://qumge.com/en/docs/install)

## Do I also need MCP?

The **qumge** skill is the operating guide. **Qumge MCP** is the hosted tool connection. Coding agents with HTTP tools can search through the bundled HTTP reference without extra MCP setup. For native MCP tools or clients without HTTP tools, follow [qumge-mcp](https://github.com/Qumge/qumge-mcp). Installing the skill does not automatically change MCP settings.

Only after choosing a paid task and budget should your agent request sign-in authorization and available balance. Both skills follow your language for explanations and human-readable reports, including English and Simplified Chinese; commands, tool names and protocol fields stay unchanged.

## Developers: publish your own capability

| Skill | For | Purpose |
|---|---|---|
| **qumge** | Capability users | Find and call Caps, install catalog skills, discover models and check balance. |
| **qumge-publish** | Capability suppliers | Inspect a project, prepare the complete-result contract, preflight, adapt/deploy, test and publish within your authorization. |

Install the publisher only when you need it:

```bash
npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish
```

`--full-depth` allows discovery beyond the root SKILL.md. You can also target its directory directly:

```bash
npx skills add https://github.com/Qumge/qumge-skill/tree/main/skills/qumge-publish
```

List both entries without installing: `npx skills add Qumge/qumge-skill --full-depth --list`. To install both, add `--full-depth --skill qumge qumge-publish` to the original command.

Both skills use the same account and hosted endpoint `https://qumge.com/mcp`. The publisher is self-contained and needs Python 3.10+ for its offline checker. It does not install a provider runtime or automatically host a CLI. Models use the compatible model API; `list_models` is discovery, not inference through MCP.

## What publishing includes

1. Inspect the existing API, MCP tools, business functions/CLI and native jobs.
2. Define one explicit input and one complete usable result; compose helper steps privately.
3. Generate/adapt the project's manifest and thin interface only where necessary.
4. Run the bundled **offline readiness checker**, saving an actionable local JSON report.
5. Deploy with the project's existing tools, then register/update the draft through MCP.
6. Run platform checks, distinguish fixture from real delivery, and publish within owner scope.
7. Reconcile actual current/pending state after interruptions; report the version and blockers.

The platform already supplies publish_cap, test_cap and submit_cap. This skill does not create
another account system, wallet, order ledger, MCP service or universal cloud execution host.

### Run local preflight

From the installed **qumge-publish** folder:

```bash
python3 scripts/preflight.py /absolute/project/qumge.json \
  --slug your-cap-slug --report /absolute/project/.qumge/preflight-01.json
```

Python standard library only; no account, key, installation or network access is needed.
It reads the manifest and creates only the requested new report file (or prints JSON).
Exit 0 means the named local checks passed, 1 means blocked, and 2 means usage/report error.
Use a fresh report filename on each run; existing files, including the manifest, are never
overwritten. The raw file fingerprint lets the Agent tell whether local bytes changed.

This is not the complete JSON Schema/server validator, deployment verification, price approval
or real-delivery proof. These remain explicitly not_checked. The template's example.com URLs
are intentional placeholders: replace them before the checker can pass. Its sample price is
not owner approval; native idempotency is never claimed without implemented recovery.

### Existing project types

- Existing complete API/MCP result: reuse the interface and map it to managed execution.
- Partial tools: compose them privately behind the complete-result operation.
- CLI/functions only: add thin HTTPS hooks and select a real server/container for deployment.
- Desktop/GPU dependency: establish that the chosen environment can actually run the task.

Authentication, async job reads, durable request-ID deduplication and private result isolation
must be tested in the provider's native workflow. The maintained Ruby adapter and isolated
fixture contract pack are linked from the publisher's adaptation reference. They are examples,
not automatic hosting or evidence that a real business result was generated.

## Files and maintenance

- SKILL.md: original consumer entry (name qumge).
- references/api-reference.md: complete platform HTTP/tool reference for existing installs.
- skills/qumge-publish/: self-contained developer skill, checker, template and resume guides.
- references/build-a-capability.md: retained compatibility pointer to the publisher.
- references/qumge.example.json: compatible reference path, synchronized to the v2 template.
- marketplace.json: both entries; no new repository or MCP service.

Local checks: `python3 -m unittest discover -s tests -v` and `python3 scripts/check-package.py`.
Live metadata-only check: `bash scripts/check-tools.sh`. It never invokes a paid or publishing tool.

Qumge: https://qumge.com · Agent index: https://qumge.com/llms.txt

## License

MIT
