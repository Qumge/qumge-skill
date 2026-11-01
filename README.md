# Qumge Skills

Two skills, one hosted MCP: use existing capabilities, or publish a workflow from your project.

| Skill | For | What the Agent does |
|---|---|---|
| **qumge** | Capability buyers and model users | Find/call paid Caps, install catalog skills, connect a model client and check spending balance. |
| **qumge-publish** | Developers and capability suppliers | Inspect a project, prepare its complete-result contract, run offline preflight, adapt/deploy, test, publish or manage an existing Cap. |

## Install

The original consumer name and command remain compatible:

```bash
npx skills add Qumge/qumge-skill
```

Install the new publisher explicitly:

```bash
npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish
```

`--full-depth` matters: an installer can stop at the root SKILL.md and otherwise only find
qumge. You can also target the publisher folder directly:

```bash
npx skills add https://github.com/Qumge/qumge-skill/tree/main/skills/qumge-publish
```

List both entries without installing: `npx skills add Qumge/qumge-skill --full-depth --list`.
For both, add `--full-depth --skill qumge qumge-publish` to the original install command.
These entries work with SKILL-compatible agents; the publisher requires Python 3.10+ only
for its bundled offline checker. It does not install a provider runtime or host your CLI.

## Use Qumge

Connect the existing MCP when your client supports it:

```bash
claude mcp add --transport http qumge https://qumge.com/mcp
```

Other clients: [qumge-mcp](https://github.com/Qumge/qumge-mcp).
Both skills can use the same endpoint, owner key and account. MCP is preferred; the publisher
includes its own HTTP/auth reference so it does not require installing the consumer skill.

Try the consumer: "Find a capability that summarizes this video and tell me its price."
It reads the actual deliverables, pricing and spending scope before a paid call. Models use
the compatible model API; list_models is discovery, not model inference through MCP.

Try the publisher: "Inspect this project and prepare one complete-result Cap. Do the local
preflight first; use my existing deployment and publication authorization, and ask only for
missing pricing or access."

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
